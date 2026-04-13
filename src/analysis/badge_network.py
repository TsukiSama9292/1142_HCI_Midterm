"""
分析主題 9: 徽章成就網路分析
==============================
分析徽章獲得者的網路結構，了解哪些使用者獲得較多成就
"""

from typing import Dict, Any, Tuple

import pandas as pd
import igraph as ig

from ..data.data_loader import DataLoader
from ..models.graph_builder import GraphBuilder


class BadgeNetworkBuilder(GraphBuilder):
    """徽章網路建構器"""
    
    BADGE_COLORS = {
        1: '#FFD700',  # Gold
        2: '#C0C0C0',  # Silver
        3: '#CD7F32',  # Bronze
    }
    
    def build_badge_network(self, limit: int = 100) -> Tuple[ig.Graph, pd.DataFrame]:
        sql = f"""
        SELECT
            b.id AS badge_id,
            b.user_id,
            b.name AS badge_name,
            b.class AS badge_class,
            b.tag_based,
            b.date,
            u.reputation,
            u.display_name
        FROM `bigquery-public-data.stackoverflow.badges` b
        LEFT JOIN `bigquery-public-data.stackoverflow.users` u
            ON b.user_id = u.id
        WHERE EXTRACT(YEAR FROM b.date) = 2021
        ORDER BY b.date DESC
        LIMIT {limit}
        """
        
        df = self.data_loader.client.query(sql)
        
        unique_users = df['user_id'].dropna().unique().tolist()
        
        self.graph = ig.Graph(directed=False)
        self.graph.add_vertices(len(unique_users))
        
        name_to_idx = {uid: idx for idx, uid in enumerate(unique_users)}
        
        badge_by_user = df.groupby(['user_id', 'badge_class']).size().unstack(fill_value=0)
        
        edges = []
        edge_weights = {}
        
        posts_by_badge = df.groupby('badge_name')['user_id'].apply(list).to_dict()
        
        for badge_name, users in posts_by_badge.items():
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
        
        gold_dict = dict(zip(badge_by_user.index, badge_by_user.get(1, pd.Series(0, index=badge_by_user.index))))
        silver_dict = dict(zip(badge_by_user.index, badge_by_user.get(2, pd.Series(0, index=badge_by_user.index))))
        bronze_dict = dict(zip(badge_by_user.index, badge_by_user.get(3, pd.Series(0, index=badge_by_user.index))))
        
        user_rep = df.groupby('user_id')['reputation'].first().to_dict()
        
        self.graph.vs['user_id'] = unique_users
        self.graph.vs['name'] = [f"U{uid}" for uid in unique_users]
        self.graph.vs['gold_badges'] = [int(gold_dict.get(uid, 0)) for uid in unique_users]
        self.graph.vs['silver_badges'] = [int(silver_dict.get(uid, 0)) for uid in unique_users]
        self.graph.vs['bronze_badges'] = [int(bronze_dict.get(uid, 0)) for uid in unique_users]
        self.graph.vs['reputation'] = [user_rep.get(uid, 0) for uid in unique_users]
        
        def badge_level(g, s, b):
            if g > 0: return '1_Gold'
            if s > 0: return '2_Silver'
            if b > 0: return '3_Bronze'
            return '0_None'
        
        self.graph.vs['badge_level'] = [
            badge_level(
                int(gold_dict.get(uid, 0)),
                int(silver_dict.get(uid, 0)),
                int(bronze_dict.get(uid, 0))
            ) for uid in unique_users
        ]
        
        return self.graph, df


class BadgeNetworkAnalyzer:
    """徽章成就網路分析器"""
    
    def __init__(self, data_loader: DataLoader = None):
        self.data_loader = data_loader or DataLoader()
        self.builder = BadgeNetworkBuilder(self.data_loader)
        self.graph: ig.Graph = None
        self.badges_df: pd.DataFrame = None
    
    def run(self, limit: int = 100) -> Dict[str, Any]:
        print("\n" + "=" * 60)
        print("分析主題 9: 徽章成就網路分析")
        print("=" * 60)
        
        self.graph, self.badges_df = self.builder.build_badge_network(limit=limit)
        
        print("\n測試徽章成就網路功能")
        print(f"輸入值: limit={limit}")
        print(f"中間過程: 建立 {len(self.graph.vs)} 個節點, {len(self.graph.es)} 條邊的網路")
        
        summary = self._generate_summary()
        
        print("最終輸出值:")
        print(f"  - 總徽章數: {summary['total_badges']}")
        print(f"  - 平均每人徽章數: {summary['avg_badges_per_user']:.2f}")
        
        return {
            'graph': self.graph,
            'badges_df': self.badges_df,
            'summary': summary,
        }
    
    def _generate_summary(self) -> Dict[str, Any]:
        badge_dist = self.badges_df['badge_class'].value_counts().to_dict() if 'badge_class' in self.badges_df.columns else {}
        
        return {
            'total_badges': len(self.badges_df),
            'unique_users': len(self.graph.vs),
            'avg_badges_per_user': len(self.badges_df) / len(self.graph.vs) if len(self.graph.vs) > 0 else 0,
            'badge_distribution': badge_dist,
        }