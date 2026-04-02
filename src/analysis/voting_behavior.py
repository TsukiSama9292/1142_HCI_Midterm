from typing import Dict, Any, Tuple

import pandas as pd
import igraph as ig

from ..data.data_loader import DataLoader
from ..models.graph_builder import GraphBuilder


class VoteNetworkBuilder(GraphBuilder):
    """投票網路建構器"""

    VOTE_COLORS = {
        'accepted': '#FFD700',
        'upvote': '#4CAF50',
        'downvote': '#F44336',
    }

    def build_vote_network(self, limit: int = 100) -> Tuple[ig.Graph, pd.DataFrame]:
        sql = f"""
        SELECT v.id AS vote_id, v.post_id, v.vote_type_id, v.creation_date,
               p.owner_user_id AS post_owner_id
        FROM `bigquery-public-data.stackoverflow.votes` v
        INNER JOIN `bigquery-public-data.stackoverflow.posts_questions` p
        ON v.post_id = p.id
        WHERE v.vote_type_id IN (1, 2, 3)
        AND p.owner_user_id IS NOT NULL
        LIMIT {limit * 20}
        """

        df = self.data_loader.client.query(sql)

        if df.empty:
            self.graph = ig.Graph(directed=False)
            self.graph.add_vertices(0)
            return self.graph, df

        df['vote_type'] = df['vote_type_id'].map({1: 'accepted', 2: 'upvote', 3: 'downvote'})

        user_votes = df.groupby('post_owner_id')['vote_type'].apply(list).to_dict()
        unique_users = list(user_votes.keys())[:200]

        if not unique_users:
            self.graph = ig.Graph(directed=False)
            self.graph.add_vertices(0)
            return self.graph, df

        self.graph = ig.Graph(directed=False)
        self.graph.add_vertices(len(unique_users))

        name_to_idx = {uid: idx for idx, uid in enumerate(unique_users)}

        edges = []
        edge_weights = {}
        for i, u1 in enumerate(unique_users):
            for j, u2 in enumerate(unique_users):
                if i >= j:
                    continue
                votes1 = set(user_votes[u1])
                votes2 = set(user_votes[u2])
                common = len(votes1 & votes2)
                if common > 0:
                    idx1, idx2 = name_to_idx[u1], name_to_idx[u2]
                    key = (min(idx1, idx2), max(idx1, idx2))
                    edge_weights[key] = common
                    edges.append((idx1, idx2))

        if edges:
            self.graph.add_edges(edges)
            self.graph.es['weight'] = [edge_weights[(min(e[0], e[1]), max(e[0], e[1]))] for e in edges]

        vote_counts = df.groupby('post_owner_id')['vote_type'].value_counts().unstack(fill_value=0)

        self.graph.vs['user_id'] = unique_users
        self.graph.vs['name'] = [f"U{int(uid)}" for uid in unique_users]

        def get_vote_level(uid):
            votes = user_votes.get(uid, [])
            total = len(votes)
            if total == 0:
                return '1_NoVotes'
            if total <= 3:
                return '2_Low'
            if total <= 10:
                return '3_Medium'
            return '4_High'

        self.graph.vs['vote_level'] = [get_vote_level(uid) for uid in unique_users]

        return self.graph, df


class VotingBehaviorAnalyzer:
    """投票行為分析器"""

    def __init__(self, data_loader: DataLoader = None):
        self.data_loader = data_loader or DataLoader()
        self.builder = VoteNetworkBuilder(self.data_loader)
        self.graph: ig.Graph = None
        self.votes_df: pd.DataFrame = None

    def run(self, limit: int = 100) -> Dict[str, Any]:
        print("\n" + "=" * 60)
        print("分析主題 7: 投票行為網路分析")
        print("=" * 60)

        self.graph, self.votes_df = self.builder.build_vote_network(limit=limit)

        print(f"\n測試投票行為網路功能")
        print(f"輸入值: limit={limit}")
        print(f"中間過程: 建立 {len(self.graph.vs)} 個節點, {len(self.graph.es)} 條邊的網路")

        summary = self._generate_summary()

        print(f"最終輸出值:")
        print(f" - 總投票數: {summary['total_votes']}")
        print(f" - 平均每人投票數: {summary['avg_votes_per_user']:.2f}")

        return {
            'graph': self.graph,
            'votes_df': self.votes_df,
            'summary': summary,
        }

    def _generate_summary(self) -> Dict[str, Any]:
        if self.votes_df.empty:
            return {
                'total_votes': 0,
                'unique_voters': 0,
                'avg_votes_per_user': 0,
                'vote_type_distribution': {},
            }

        vote_counts = self.votes_df.groupby('post_owner_id').size()

        return {
            'total_votes': len(self.votes_df),
            'unique_voters': len(vote_counts),
            'avg_votes_per_user': vote_counts.mean() if len(vote_counts) > 0 else 0,
            'vote_type_distribution': self.votes_df['vote_type'].value_counts().to_dict(),
        }