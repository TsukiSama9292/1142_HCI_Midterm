"""
分析主題 13: 賞金懸賞網路分析
==============================
分析懸賞者與回答者之間的賞金分配關係
"""

from typing import Dict, Any, Tuple

import pandas as pd
import igraph as ig

from ..data.data_loader import DataLoader
from ..models.graph_builder import GraphBuilder


class BountyNetworkBuilder(GraphBuilder):
    """賞金懸賞網路建構器"""

    def build_bounty_network(self, limit: int = 100) -> Tuple[ig.Graph, pd.DataFrame]:
        sample_size = limit * 50
        sql = f"""
        SELECT
            v.id AS vote_id,
            v.post_id,
            v.vote_type_id,
            v.creation_date,
            p.owner_user_id AS post_owner_id,
            p.title,
            p.score AS post_score,
            p.tags,
            u.reputation,
            u.display_name,
            CASE
                WHEN v.vote_type_id = 8 THEN 'BountyStart'
                WHEN v.vote_type_id = 9 THEN 'BountyClose'
                ELSE 'Other'
            END AS bounty_type
        FROM `bigquery-public-data.stackoverflow.votes` v
        INNER JOIN `bigquery-public-data.stackoverflow.posts_questions` p
        ON v.post_id = p.id
        LEFT JOIN `bigquery-public-data.stackoverflow.users` u
        ON p.owner_user_id = u.id
        WHERE v.vote_type_id IN (8, 9)
        AND MOD(ABS(FARM_FINGERPRINT(CAST(v.post_id AS STRING))), 100000) < {sample_size}
        """

        df = self.data_loader.client.query(sql)

        if df.empty:
            self.graph = ig.Graph(directed=False)
            self.graph.add_vertices(0)
            return self.graph, df

        unique_users = df['post_owner_id'].dropna().unique().tolist()

        if not unique_users:
            self.graph = ig.Graph(directed=False)
            self.graph.add_vertices(0)
            return self.graph, df

        max_users = 500
        if len(unique_users) > max_users:
            user_counts = df.groupby('post_owner_id').size()
            top_users = user_counts.nlargest(max_users).index.tolist()
            unique_users = [u for u in unique_users if u in top_users]

        self.graph = ig.Graph(directed=False)
        self.graph.add_vertices(len(unique_users))

        name_to_idx = {uid: idx for idx, uid in enumerate(unique_users)}

        user_tags = {}
        for _, row in df.iterrows():
            uid = row['post_owner_id']
            if pd.notna(uid) and uid in name_to_idx and pd.notna(row.get('tags')):
                uid = int(uid)
                tags = set(row['tags'].split('|'))
                if uid not in user_tags:
                    user_tags[uid] = set()
                user_tags[uid].update(tags)

        edges = []
        edge_weights = {}
        users_list = sorted(user_tags.keys())
        for i in range(len(users_list)):
            for j in range(i + 1, len(users_list)):
                u1, u2 = users_list[i], users_list[j]
                common = len(user_tags[u1] & user_tags[u2])
                if common > 0:
                    key = (name_to_idx[u1], name_to_idx[u2])
                    edge_weights[key] = common
                    edges.append((name_to_idx[u1], name_to_idx[u2]))

        if edges:
            self.graph.add_edges(edges)
            self.graph.es['weight'] = [edge_weights[(e[0], e[1])] for e in edges]

        bounty_counts = df.groupby('post_owner_id').size().to_dict()
        user_rep = df.groupby('post_owner_id')['reputation'].first().to_dict()

        self.graph.vs['user_id'] = unique_users
        self.graph.vs['name'] = [f"U{uid}" for uid in unique_users]
        self.graph.vs['bounty_count'] = [bounty_counts.get(uid, 0) for uid in unique_users]
        self.graph.vs['reputation'] = [user_rep.get(uid, 0) for uid in unique_users]

        def bounty_level(count):
            if count == 0:
                return '0_None'
            if count < 2:
                return '1_Meager'
            if count <= 5:
                return '2_Normal'
            if count <= 10:
                return '3_Generous'
            return '4_Extravagant'

        self.graph.vs['bounty_level'] = [bounty_level(bounty_counts.get(uid, 0)) for uid in unique_users]

        return self.graph, df


class BountyNetworkAnalyzer:
    """賞金懸賞網路分析器"""

    def __init__(self, data_loader: DataLoader = None):
        self.data_loader = data_loader or DataLoader()
        self.builder = BountyNetworkBuilder(self.data_loader)
        self.graph: ig.Graph = None
        self.bounties_df: pd.DataFrame = None

    def run(self, limit: int = 100) -> Dict[str, Any]:
        print("\n" + "=" * 60)
        print("分析主題 13: 賞金懸賞網路分析")
        print("=" * 60)

        self.graph, self.bounties_df = self.builder.build_bounty_network(limit=limit)

        print(f"\n測試賞金懸賞網路功能")
        print(f"輸入值: limit={limit}")
        print(f"中間過程: 建立 {len(self.graph.vs)} 個節點, {len(self.graph.es)} 條邊的網路")

        summary = self._generate_summary()

        print(f"最終輸出值:")
        print(f" - 總賞金數: {summary['total_bounties']}")
        print(f" - 活躍用戶: {summary['active_users']}")

        return {
            'graph': self.graph,
            'bounties_df': self.bounties_df,
            'summary': summary,
        }

    def _generate_summary(self) -> Dict[str, Any]:
        if self.bounties_df.empty:
            return {
                'total_bounties': 0,
                'unique_users': 0,
                'active_users': 0,
                'bounty_type_distribution': {},
            }

        bounty_counts = self.bounties_df.groupby('post_owner_id').size()

        return {
            'total_bounties': len(self.bounties_df),
            'unique_users': len(self.graph.vs),
            'active_users': len([c for c in bounty_counts if c >= 2]),
            'avg_bounties_per_user': bounty_counts.mean() if len(bounty_counts) > 0 else 0,
            'bounty_type_distribution': self.bounties_df['bounty_type'].value_counts().to_dict(),
        }