"""
分析主題 12: 審核任務網路分析
==============================
分析參與審核任務的使用者之間的協作網路
使用 PostHistory 中的關閉/重新開啟/刪除行為作為審核任務代理
"""

from typing import Dict, Any, Tuple

import pandas as pd
import igraph as ig

from ..data.data_loader import DataLoader
from ..models.graph_builder import GraphBuilder


class ReviewTaskNetworkBuilder(GraphBuilder):
    """審核任務網路建構器"""
    
    REVIEW_TYPES = {
        10: 'Close',
        11: 'Reopen',
        12: 'Delete',
        13: 'Undelete',
        24: 'SuggestedEdit',
    }
    
    def build_review_network(self, limit: int = 100) -> Tuple[ig.Graph, pd.DataFrame]:
        sql = f"""
        SELECT
            ph.id AS history_id,
            ph.post_id,
            ph.user_id AS reviewer_id,
            ph.post_history_type_id,
            ph.creation_date,
            ph.comment,
            CASE
                WHEN ph.post_history_type_id = 10 THEN 'Close'
                WHEN ph.post_history_type_id = 11 THEN 'Reopen'
                WHEN ph.post_history_type_id = 12 THEN 'Delete'
                WHEN ph.post_history_type_id = 13 THEN 'Undelete'
                WHEN ph.post_history_type_id = 24 THEN 'SuggestedEdit'
                ELSE 'Other'
            END AS review_type,
            p.owner_user_id AS post_owner_id,
            u.reputation,
            u.display_name
        FROM `bigquery-public-data.stackoverflow.post_history` ph
        LEFT JOIN `bigquery-public-data.stackoverflow.posts_questions` p
            ON ph.post_id = p.id
        LEFT JOIN `bigquery-public-data.stackoverflow.users` u
            ON ph.user_id = u.id
        WHERE ph.post_history_type_id IN (10, 11, 12, 13, 24)
          AND EXTRACT(YEAR FROM ph.creation_date) = 2021
        ORDER BY ph.creation_date DESC
        LIMIT {limit}
        """
        
        df = self.data_loader.client.query(sql)
        
        if df.empty:
            self.graph = ig.Graph(directed=False)
            self.graph.add_vertices(0)
            return self.graph, df
        
        unique_users = df['reviewer_id'].dropna().unique().tolist()
        
        if not unique_users:
            self.graph = ig.Graph(directed=False)
            self.graph.add_vertices(0)
            return self.graph, df
        
        self.graph = ig.Graph(directed=False)
        self.graph.add_vertices(len(unique_users))
        
        name_to_idx = {uid: idx for idx, uid in enumerate(unique_users)}
        
        posts_by_review = df.groupby('post_id')['reviewer_id'].apply(list).to_dict()
        
        edges = []
        edge_weights = {}
        
        for post_id, users in posts_by_review.items():
            users = [u for u in users if pd.notna(u)]
            for i in range(len(users)):
                for j in range(i+1, len(users)):
                    u1, u2 = int(users[i]), int(users[j])
                    if u1 in name_to_idx and u2 in name_to_idx:
                        key = (name_to_idx[u1], name_to_idx[u2])
                        edge_weights[key] = edge_weights.get(key, 0) + 1
        
        for (src, dst), weight in edge_weights.items():
            edges.append((src, dst))
        
        if edges:
            self.graph.add_edges(edges)
            self.graph.es['weight'] = [edge_weights[(e[0], e[1])] for e in edges]
        
        review_counts = df.groupby('reviewer_id').size().to_dict()
        user_rep = df.groupby('reviewer_id')['reputation'].first().to_dict()
        
        self.graph.vs['user_id'] = unique_users
        self.graph.vs['name'] = [f"U{uid}" for uid in unique_users]
        self.graph.vs['review_count'] = [review_counts.get(uid, 0) for uid in unique_users]
        self.graph.vs['reputation'] = [user_rep.get(uid, 0) for uid in unique_users]
        
        def reviewer_level(count):
            if count == 0: return '0_None'
            if count <= 3: return '1_Casual'
            if count <= 10: return '2_Active'
            return '3_Power'
        
        self.graph.vs['reviewer_level'] = [reviewer_level(review_counts.get(uid, 0)) for uid in unique_users]
        
        return self.graph, df


class ReviewTaskAnalyzer:
    """審核任務網路分析器"""
    
    def __init__(self, data_loader: DataLoader = None):
        self.data_loader = data_loader or DataLoader()
        self.builder = ReviewTaskNetworkBuilder(self.data_loader)
        self.graph: ig.Graph = None
        self.reviews_df: pd.DataFrame = None
    
    def run(self, limit: int = 100) -> Dict[str, Any]:
        print("\n" + "=" * 60)
        print("分析主題 12: 審核任務網路分析")
        print("=" * 60)
        
        self.graph, self.reviews_df = self.builder.build_review_network(limit=limit)
        
        print("\n測試審核任務網路功能")
        print(f"輸入值: limit={limit}")
        print(f"中間過程: 建立 {len(self.graph.vs)} 個節點, {len(self.graph.es)} 條邊的網路")
        
        summary = self._generate_summary()
        
        print("最終輸出值:")
        print(f"  - 總審核任務數: {summary['total_reviews']}")
        print(f"  - 活躍審核者: {summary['active_reviewers']}")
        
        return {
            'graph': self.graph,
            'reviews_df': self.reviews_df,
            'summary': summary,
        }
    
    def _generate_summary(self) -> Dict[str, Any]:
        if self.reviews_df.empty:
            return {
                'total_reviews': 0,
                'unique_reviewers': 0,
                'active_reviewers': 0,
                'avg_reviews_per_reviewer': 0,
                'review_type_distribution': {},
            }
        
        review_counts = self.reviews_df.groupby('reviewer_id').size()
        
        return {
            'total_reviews': len(self.reviews_df),
            'unique_reviewers': len(self.graph.vs),
            'active_reviewers': len([c for c in review_counts if c >= 3]),
            'avg_reviews_per_reviewer': review_counts.mean() if len(review_counts) > 0 else 0,
            'review_type_distribution': self.reviews_df['review_type'].value_counts().to_dict(),
        }