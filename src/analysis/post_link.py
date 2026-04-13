"""
分析主題 11: 引用與重複問題網路分析
====================================
分析問題之間的引用關係與重複問題網路，理解知識傳播路徑
"""

from typing import Dict, Any, Tuple

import pandas as pd
import igraph as ig

from ..data.data_loader import DataLoader
from ..models.graph_builder import GraphBuilder


class PostLinkNetworkBuilder(GraphBuilder):
    """引用與重複問題網路建構器"""
    
    LINK_TYPES = {
        1: 'Linked',
        3: 'Duplicate',
    }
    
    def build_post_link_network(self, limit: int = 100) -> Tuple[ig.Graph, pd.DataFrame]:
        sql = f"""
        SELECT
            pl.id AS link_id,
            pl.post_id AS source_post_id,
            pl.related_post_id AS target_post_id,
            pl.link_type_id,
            pl.creation_date,
            CASE
                WHEN pl.link_type_id = 1 THEN 'Linked'
                WHEN pl.link_type_id = 3 THEN 'Duplicate'
                ELSE 'Other'
            END AS link_type,
            sp.owner_user_id AS source_user_id,
            tp.owner_user_id AS target_user_id,
            sp.score AS source_score,
            tp.score AS target_score
        FROM `bigquery-public-data.stackoverflow.post_links` pl
        LEFT JOIN `bigquery-public-data.stackoverflow.posts_questions` sp
            ON pl.post_id = sp.id
        LEFT JOIN `bigquery-public-data.stackoverflow.posts_questions` tp
            ON pl.related_post_id = tp.id
        WHERE pl.link_type_id IN (1, 3)
          AND EXTRACT(YEAR FROM pl.creation_date) = 2021
        LIMIT {limit}
        """
        
        df = self.data_loader.client.query(sql)
        
        unique_posts = pd.concat([df['source_post_id'], df['target_post_id']]).dropna().unique().tolist()
        
        self.graph = ig.Graph(directed=True)
        self.graph.add_vertices(len(unique_posts))
        
        name_to_idx = {pid: idx for idx, pid in enumerate(unique_posts)}
        
        edges = []
        link_types = []
        weights = []
        
        for _, row in df.iterrows():
            if pd.notna(row['source_post_id']) and pd.notna(row['target_post_id']):
                src = name_to_idx.get(row['source_post_id'])
                dst = name_to_idx.get(row['target_post_id'])
                if src is not None and dst is not None:
                    edges.append((src, dst))
                    link_types.append(row['link_type'])
                    weights.append(1)
        
        if edges:
            self.graph.add_edges(edges)
            self.graph.es['link_type'] = link_types
            self.graph.es['weight'] = weights
        
        post_scores = {}
        for _, row in df.iterrows():
            if pd.notna(row['source_post_id']):
                post_scores[row['source_post_id']] = row.get('source_score', 0)
            if pd.notna(row['target_post_id']):
                post_scores[row['target_post_id']] = row.get('target_score', 0)
        
        self.graph.vs['post_id'] = unique_posts
        self.graph.vs['name'] = [f"P{pid}" for pid in unique_posts]
        self.graph.vs['score'] = [post_scores.get(pid, 0) for pid in unique_posts]
        
        return self.graph, df


class PostLinkAnalyzer:
    """引用與重複問題網路分析器"""
    
    def __init__(self, data_loader: DataLoader = None):
        self.data_loader = data_loader or DataLoader()
        self.builder = PostLinkNetworkBuilder(self.data_loader)
        self.graph: ig.Graph = None
        self.links_df: pd.DataFrame = None
    
    def run(self, limit: int = 100) -> Dict[str, Any]:
        print("\n" + "=" * 60)
        print("分析主題 11: 引用與重複問題網路分析")
        print("=" * 60)
        
        self.graph, self.links_df = self.builder.build_post_link_network(limit=limit)
        
        print("\n測試引用與重複問題網路功能")
        print(f"輸入值: limit={limit}")
        print(f"中間過程: 建立 {len(self.graph.vs)} 個節點, {len(self.graph.es)} 條邊的網路")
        
        summary = self._generate_summary()
        
        print("最終輸出值:")
        print(f"  - 總連結數: {summary['total_links']}")
        print(f"  - 重複問題比例: {summary['duplicate_ratio']:.2%}")
        
        return {
            'graph': self.graph,
            'links_df': self.links_df,
            'summary': summary,
        }
    
    def _generate_summary(self) -> Dict[str, Any]:
        link_dist = self.links_df['link_type'].value_counts().to_dict()
        total = len(self.links_df)
        duplicates = link_dist.get('Duplicate', 0)
        
        return {
            'total_links': total,
            'unique_posts': len(self.graph.vs),
            'link_type_distribution': link_dist,
            'duplicate_ratio': duplicates / total if total > 0 else 0,
        }