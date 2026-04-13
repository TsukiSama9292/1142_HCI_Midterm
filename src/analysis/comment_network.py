"""
分析主題 8: 評論互動網路分析
==============================
驗證評論者之間是否存在緊密的社交網路
"""

from typing import Dict, Any, Tuple

import pandas as pd
import igraph as ig

from ..data.data_loader import DataLoader
from ..models.graph_builder import GraphBuilder


class CommentNetworkBuilder(GraphBuilder):
    """評論網路建構器"""

    def build_comment_network(self, limit: int = 100) -> Tuple[ig.Graph, pd.DataFrame]:
        sql = f"""
        SELECT
            c.id AS comment_id,
            c.post_id,
            c.user_id AS commenter_id,
            c.score AS comment_score,
            c.creation_date,
            p.owner_user_id AS post_owner_id,
            p.post_type_id,
            u.reputation AS commenter_reputation,
            u.display_name AS commenter_name
        FROM `bigquery-public-data.stackoverflow.comments` c
        INNER JOIN `bigquery-public-data.stackoverflow.posts_questions` p
        ON c.post_id = p.id
        LEFT JOIN `bigquery-public-data.stackoverflow.users` u
        ON c.user_id = u.id
        LIMIT {limit * 20}
        """
        
        df = self.data_loader.client.query(sql)
        
        if df.empty:
            self.graph = ig.Graph(directed=False)
            self.graph.add_vertices(0)
            return self.graph, df
        
        unique_users = df['commenter_id'].dropna().unique().tolist()
        
        if not unique_users:
            self.graph = ig.Graph(directed=False)
            self.graph.add_vertices(0)
            return self.graph, df
        
        self.graph = ig.Graph(directed=False)
        self.graph.add_vertices(len(unique_users))
        
        name_to_idx = {uid: idx for idx, uid in enumerate(unique_users)}
        
        post_commenters = df.groupby('post_id')['commenter_id'].apply(list).to_dict()
        
        edges = []
        edge_weights = {}
        
        for post_id, commenters in post_commenters.items():
            commenters = [int(c) for c in commenters if pd.notna(c)]
            if len(commenters) >= 2:
                for i in range(len(commenters)):
                    for j in range(i+1, len(commenters)):
                        u1, u2 = commenters[i], commenters[j]
                        if u1 in name_to_idx and u2 in name_to_idx:
                            key = (name_to_idx[u1], name_to_idx[u2])
                            edge_weights[key] = edge_weights.get(key, 0) + 1
        
        for (src, dst), weight in edge_weights.items():
            edges.append((src, dst))
        
        if edges:
            self.graph.add_edges(edges)
            self.graph.es['weight'] = [edge_weights[(e[0], e[1])] for e in edges]
        
        user_data = df.groupby('commenter_id').agg({
            'comment_score': 'sum',
            'post_id': 'count',
            'commenter_reputation': 'first',
            'commenter_name': 'first',
        }).reset_index()
        
        user_dict = dict(zip(user_data['commenter_id'], user_data['comment_score']))
        rep_dict = dict(zip(user_data['commenter_id'], user_data['commenter_reputation']))
        name_dict = dict(zip(user_data['commenter_id'], user_data['commenter_name']))
        
        self.graph.vs['user_id'] = unique_users
        self.graph.vs['name'] = [str(name_dict.get(uid, f"U{uid}")) for uid in unique_users]
        self.graph.vs['comment_count'] = [user_dict.get(uid, 0) for uid in unique_users]
        self.graph.vs['reputation'] = [rep_dict.get(uid, 0) for uid in unique_users]
        
        return self.graph, df


class CommentNetworkAnalyzer:
    """評論互動網路分析器"""
    
    def __init__(self, data_loader: DataLoader = None):
        self.data_loader = data_loader or DataLoader()
        self.builder = CommentNetworkBuilder(self.data_loader)
        self.graph: ig.Graph = None
        self.comments_df: pd.DataFrame = None
    
    def run(self, limit: int = 100) -> Dict[str, Any]:
        print("\n" + "=" * 60)
        print("分析主題 8: 評論互動網路分析")
        print("=" * 60)
        
        self.graph, self.comments_df = self.builder.build_comment_network(limit=limit)
        
        print("\n測試評論互動網路功能")
        print(f"輸入值: limit={limit}")
        print(f"中間過程: 建立 {len(self.graph.vs)} 個節點, {len(self.graph.es)} 條邊的網路")
        
        summary = self._generate_summary()
        
        print("最終輸出值:")
        print(f"  - 總評論數: {summary['total_comments']}")
        print(f"  - 網路密度: {summary['network_density']:.4f}")
        
        return {
            'graph': self.graph,
            'comments_df': self.comments_df,
            'summary': summary,
        }
    
    def _generate_summary(self) -> Dict[str, Any]:
        n = len(self.graph.vs)
        m = len(self.graph.es)
        density = 2 * m / (n * (n - 1)) if n > 1 else 0
        
        return {
            'total_comments': len(self.comments_df),
            'unique_commenters': len(self.graph.vs),
            'network_density': density,
            'avg_comments_per_user': len(self.comments_df) / len(self.graph.vs) if len(self.graph.vs) > 0 else 0,
        }
