"""
分析主題 15: 時間序列活躍度網路分析
====================================
分析使用者上線模式的時間規律
"""

from typing import Dict, Any, Tuple

import pandas as pd
import igraph as ig

from ..data.data_loader import DataLoader
from ..models.graph_builder import GraphBuilder


class TimeSeriesNetworkBuilder(GraphBuilder):
    """時間序列活躍度網路建構器"""

    def build_time_series_network(self, limit: int = 100) -> Tuple[ig.Graph, pd.DataFrame]:
        sample_size = limit * 5
        sql = f"""
        SELECT
            p.id AS post_id,
            p.owner_user_id AS user_id,
            p.creation_date,
            p.post_type_id,
            p.score,
            EXTRACT(MONTH FROM p.creation_date) AS month,
            EXTRACT(YEAR FROM p.creation_date) AS year,
            EXTRACT(DAYOFWEEK FROM p.creation_date) AS day_of_week,
            EXTRACT(HOUR FROM p.creation_date) AS hour,
            u.reputation,
            u.display_name
        FROM `bigquery-public-data.stackoverflow.posts_questions` p
        LEFT JOIN `bigquery-public-data.stackoverflow.users` u
        ON p.owner_user_id = u.id
        WHERE MOD(ABS(FARM_FINGERPRINT(CAST(p.id AS STRING))), 10000) < {sample_size}
        LIMIT {limit * 100}
        """
        
        df = self.data_loader.client.query(sql)
        
        if df.empty:
            self.graph = ig.Graph(directed=False)
            self.graph.add_vertices(0)
            return self.graph, df
        
        df['year_month'] = df['year'].astype(str) + '-' + df['month'].astype(str).str.zfill(2)
        
        month_stats = df.groupby('year_month').agg({
            'post_id': 'count',
            'score': 'mean',
            'user_id': 'nunique',
        }).reset_index()
        month_stats.columns = ['year_month', 'post_count', 'avg_score', 'unique_users']
        
        unique_months = month_stats['year_month'].tolist()
        
        if len(unique_months) < 2:
            self.graph = ig.Graph(directed=False)
            self.graph.add_vertices(1)
            self.graph.vs['year_month'] = unique_months
            self.graph.vs['name'] = unique_months
            self.graph.vs['post_count'] = [month_stats.iloc[0]['post_count']]
            self.graph.vs['activity_level'] = ['high']
            return self.graph, df
        
        self.graph = ig.Graph(directed=False)
        self.graph.add_vertices(len(unique_months))
        
        name_to_idx = {m: idx for idx, m in enumerate(unique_months)}
        
        month_counts = dict(zip(month_stats['year_month'], month_stats['post_count']))
        
        edges = []
        weights = []
        
        for i in range(len(unique_months)):
            for j in range(i+1, len(unique_months)):
                edges.append((i, j))
                weights.append(month_counts[unique_months[i]] * month_counts[unique_months[j]])
        
        if edges:
            self.graph.add_edges(edges)
            self.graph.es['weight'] = weights
        
        post_counts = month_stats['post_count'].values
        median_count = pd.Series(post_counts).median()
        
        def activity_level(count):
            if count >= median_count * 1.5: return 'high'
            if count >= median_count * 0.5: return 'medium'
            return 'low'
        
        self.graph.vs['year_month'] = unique_months
        self.graph.vs['name'] = unique_months
        self.graph.vs['post_count'] = [month_counts.get(m, 0) for m in unique_months]
        self.graph.vs['activity_level'] = [activity_level(month_counts.get(m, 0)) for m in unique_months]
        
        return self.graph, df


class TimeSeriesAnalyzer:
    """時間序列活躍度網路分析器"""
    
    def __init__(self, data_loader: DataLoader = None):
        self.data_loader = data_loader or DataLoader()
        self.builder = TimeSeriesNetworkBuilder(self.data_loader)
        self.graph: ig.Graph = None
        self.posts_df: pd.DataFrame = None
    
    def run(self, limit: int = 100) -> Dict[str, Any]:
        print("\n" + "=" * 60)
        print("分析主題 15: 時間序列活躍度網路分析")
        print("=" * 60)
        
        self.graph, self.posts_df = self.builder.build_time_series_network(limit=limit)
        
        print(f"\n測試時間序列活躍度網路功能")
        print(f"輸入值: limit={limit}")
        print(f"中間過程: 建立 {len(self.graph.vs)} 個節點, {len(self.graph.es)} 條邊的網路")
        
        summary = self._generate_summary()
        
        print(f"最終輸出值:")
        print(f"  - 總貼文數: {summary['total_posts']}")
        print(f"  - 最活躍月份: {summary['peak_month']}")
        
        return {
            'graph': self.graph,
            'posts_df': self.posts_df,
            'summary': summary,
        }
    
    def _generate_summary(self) -> Dict[str, Any]:
        if self.posts_df.empty:
            return {
                'total_posts': 0,
                'unique_months': 0,
                'peak_month': 'N/A',
                'avg_posts_per_month': 0,
                'hour_distribution': {},
                'day_of_week_distribution': {},
            }
        
        month_counts = self.posts_df.groupby('year_month').size()
        peak_month = month_counts.idxmax() if len(month_counts) > 0 else 'N/A'
        
        hour_dist = self.posts_df.groupby('hour').size().to_dict()
        day_dist = self.posts_df.groupby('day_of_week').size().to_dict()
        
        return {
            'total_posts': len(self.posts_df),
            'unique_months': len(self.graph.vs),
            'peak_month': peak_month,
            'avg_posts_per_month': month_counts.mean() if len(month_counts) > 0 else 0,
            'hour_distribution': hour_dist,
            'day_of_week_distribution': day_dist,
        }
