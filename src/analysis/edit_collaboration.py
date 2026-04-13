"""
分析主題 10: 編輯協作網路分析
==============================
建構多人共同編輯同一貼文的協作網路，識別熱心的編輯者
"""

from typing import Dict, Any, Tuple

import pandas as pd
import igraph as ig

from ..data.data_loader import DataLoader
from ..models.graph_builder import GraphBuilder


class EditCollaborationNetworkBuilder(GraphBuilder):
    """編輯協作網路建構器"""

    def build_edit_network(self, limit: int = 100) -> Tuple[ig.Graph, pd.DataFrame]:
        query_limit = limit
        sql = f"""
        SELECT
        ph.id AS history_id,
        ph.post_id,
        ph.user_id AS editor_id,
        ph.post_history_type_id,
        ph.creation_date,
        ph.comment AS edit_comment,
        u.reputation,
        u.display_name
        FROM `bigquery-public-data.stackoverflow.post_history` ph
        LEFT JOIN `bigquery-public-data.stackoverflow.users` u
        ON ph.user_id = u.id
        WHERE ph.post_history_type_id IN (4, 5, 6)
          AND EXTRACT(YEAR FROM ph.creation_date) = 2021
        LIMIT {query_limit}
        """
        
        df = self.data_loader.client.query(sql)
        
        if df.empty:
            self.graph = ig.Graph(directed=False)
            self.graph.add_vertices(0)
            return self.graph, df
        
        unique_users = df['editor_id'].dropna().unique().tolist()
        
        if not unique_users:
            self.graph = ig.Graph(directed=False)
            self.graph.add_vertices(0)
            return self.graph, df
        
        self.graph = ig.Graph(directed=False)
        self.graph.add_vertices(len(unique_users))
        
        name_to_idx = {uid: idx for idx, uid in enumerate(unique_users)}
        
        post_editors = df.groupby('post_id')['editor_id'].apply(list).to_dict()
        
        edges = []
        edge_weights = {}
        
        for post_id, editors in post_editors.items():
            editors = [int(e) for e in editors if pd.notna(e)]
            if len(editors) >= 2:
                for i in range(len(editors)):
                    for j in range(i+1, len(editors)):
                        u1, u2 = editors[i], editors[j]
                        if u1 in name_to_idx and u2 in name_to_idx:
                            key = (name_to_idx[u1], name_to_idx[u2])
                            edge_weights[key] = edge_weights.get(key, 0) + 1
        
        for (src, dst), weight in edge_weights.items():
            edges.append((src, dst))
        
        if edges:
            self.graph.add_edges(edges)
            self.graph.es['weight'] = [edge_weights[(e[0], e[1])] for e in edges]
        
        edit_counts = df.groupby('editor_id').size().to_dict()
        user_rep = df.groupby('editor_id')['reputation'].first().to_dict()
        
        self.graph.vs['user_id'] = unique_users
        self.graph.vs['name'] = [f"U{uid}" for uid in unique_users]
        self.graph.vs['edit_count'] = [edit_counts.get(uid, 0) for uid in unique_users]
        self.graph.vs['reputation'] = [user_rep.get(uid, 0) for uid in unique_users]
        
        def editor_level(count):
            if count == 0: return '0_None'
            if count <= 2: return '1_Casual'
            if count <= 5: return '2_Active'
            return '3_Power'
        
        self.graph.vs['editor_level'] = [editor_level(edit_counts.get(uid, 0)) for uid in unique_users]
        
        return self.graph, df


class EditCollaborationAnalyzer:
    """編輯協作網路分析器"""
    
    def __init__(self, data_loader: DataLoader = None):
        self.data_loader = data_loader or DataLoader()
        self.builder = EditCollaborationNetworkBuilder(self.data_loader)
        self.graph: ig.Graph = None
        self.edits_df: pd.DataFrame = None
    
    def run(self, limit: int = 100) -> Dict[str, Any]:
        print("\n" + "=" * 60)
        print("分析主題 10: 編輯協作網路分析")
        print("=" * 60)
        
        self.graph, self.edits_df = self.builder.build_edit_network(limit=limit)
        
        print("\n測試編輯協作網路功能")
        print(f"輸入值: limit={limit}")
        print(f"中間過程: 建立 {len(self.graph.vs)} 個節點, {len(self.graph.es)} 條邊的網路")
        
        summary = self._generate_summary()
        
        print("最終輸出值:")
        print(f"  - 總編輯數: {summary['total_edits']}")
        print(f"  - 活躍編輯者: {summary['active_editors']}")
        
        return {
            'graph': self.graph,
            'edits_df': self.edits_df,
            'summary': summary,
        }
    
    def _generate_summary(self) -> Dict[str, Any]:
        edit_counts = self.edits_df.groupby('editor_id').size()
        
        return {
            'total_edits': len(self.edits_df),
            'unique_editors': len(self.graph.vs),
            'active_editors': len([c for c in edit_counts if c >= 2]),
            'avg_edits_per_editor': edit_counts.mean() if len(edit_counts) > 0 else 0,
        }
