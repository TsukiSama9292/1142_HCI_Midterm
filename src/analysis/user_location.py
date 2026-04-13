"""
分析主題 14: 使用者地理分布網路分析
====================================
根據使用者 location 欄位建構地理分布網路
"""

from typing import Dict, Any, Tuple

import pandas as pd
import igraph as ig

from ..data.data_loader import DataLoader
from ..models.graph_builder import GraphBuilder


class UserLocationNetworkBuilder(GraphBuilder):
    """使用者地理分布網路建構器"""
    
    REGION_MAP = {
        'North America': ['usa', 'united states', 'canada', 'mexico', 'new york', 'california', 'toronto', 'san francisco', 'seattle', 'boston', 'texas', 'chicago', 'los angeles', 'washington', 'dc', 'montreal', 'vancouver', 'ontario'],
        'Europe': ['uk', 'united kingdom', 'germany', 'france', 'netherlands', 'spain', 'italy', 'sweden', 'poland', 'london', 'berlin', 'paris', 'amsterdam', 'madrid', 'rome', 'stockholm', 'warsaw', 'dublin', 'vienna', 'zurich', 'belgium', 'austria', 'switzerland', 'norway', 'denmark', 'finland', 'portugal', 'greece', 'czech', 'russia', 'ukraine', 'romania', 'hungary', 'ireland', 'scotland', 'manchester', 'milan', 'munich', 'barcelona'],
        'Asia': ['india', 'china', 'japan', 'taiwan', 'korea', 'singapore', 'hong kong', 'indonesia', 'thailand', 'vietnam', 'beijing', 'tokyo', 'bangalore', 'mumbai', 'seoul', 'taipei', 'shanghai', 'shenzhen', 'osaka', 'manila', 'jakarta', 'bangkok', 'hanoi', 'kuala lumpur', 'malaysia', 'philippines', 'pakistan', 'bangladesh', 'sri lanka', 'nepal'],
        'Oceania': ['australia', 'new zealand', 'sydney', 'melbourne', 'auckland', 'brisbane', 'perth', 'wellington'],
        'South America': ['brazil', 'argentina', 'chile', 'colombia', 'venezuela', 'sao paulo', 'buenos aires', 'santiago', 'bogota', 'lima', 'peru', 'ecuador', 'uruguay'],
        'Africa': ['south africa', 'nigeria', 'egypt', 'kenya', 'morocco', 'tunisia', 'ghana', 'ethiopia', 'cairo', 'lagos', 'nairobi', 'cape town'],
        'Middle East': ['israel', 'uae', 'turkey', 'iran', 'saudi arabia', 'dubai', 'tel aviv', 'istanbul', 'tehran', 'riyadh', 'lebanon', 'jordan', 'qatar'],
    }
    
    REGION_COLORS = {
        'North America': '#2196F3',
        'Europe': '#4CAF50',
        'Asia': '#FFC107',
        'Oceania': '#9E9E9E',
        'South America': '#FF5722',
        'Africa': '#795548',
        'Middle East': '#607D8B',
        'Other': '#BDBDBD',
    }
    
    def _classify_region(self, location: str) -> str:
        if pd.isna(location) or location == '':
            return 'Other'
        location_lower = location.lower()
        for region, keywords in self.REGION_MAP.items():
            if any(kw in location_lower for kw in keywords):
                return region
        return 'Other'
    
    def build_location_network(self, limit: int = 100) -> Tuple[ig.Graph, pd.DataFrame]:
        sql = f"""
        SELECT
            id,
            display_name,
            reputation,
            location,
            up_votes,
            down_votes
        FROM `bigquery-public-data.stackoverflow.users`
        WHERE location IS NOT NULL AND location != ''
        LIMIT {limit}
        """
        
        df = self.data_loader.client.query(sql)
        
        df['region'] = df['location'].apply(self._classify_region)
        
        region_counts = df.groupby('region').size().to_dict()
        
        self.graph = ig.Graph(directed=False)
        regions = list(region_counts.keys())
        self.graph.add_vertices(len(regions))
        
        name_to_idx = {r: idx for idx, r in enumerate(regions)}
        
        edges = []
        weights = []
        
        for i in range(len(regions)):
            for j in range(i+1, len(regions)):
                edges.append((i, j))
                weights.append(region_counts[regions[i]] * region_counts[regions[j]])
        
        if edges:
            self.graph.add_edges(edges)
            self.graph.es['weight'] = weights
        
        self.graph.vs['region'] = regions
        self.graph.vs['name'] = regions
        self.graph.vs['user_count'] = [region_counts[r] for r in regions]
        self.graph.vs['color'] = [self.REGION_COLORS.get(r, '#BDBDBD') for r in regions]
        
        return self.graph, df


class UserLocationAnalyzer:
    """使用者地理分布網路分析器"""
    
    def __init__(self, data_loader: DataLoader = None):
        self.data_loader = data_loader or DataLoader()
        self.builder = UserLocationNetworkBuilder(self.data_loader)
        self.graph: ig.Graph = None
        self.users_df: pd.DataFrame = None
    
    def run(self, limit: int = 100) -> Dict[str, Any]:
        print("\n" + "=" * 60)
        print("分析主題 14: 使用者地理分布網路分析")
        print("=" * 60)
        
        self.graph, self.users_df = self.builder.build_location_network(limit=limit)
        
        print("\n測試地理分布網路功能")
        print(f"輸入值: limit={limit}")
        print(f"中間過程: 建立 {len(self.graph.vs)} 個節點, {len(self.graph.es)} 條邊的網路")
        
        summary = self._generate_summary()
        
        print("最終輸出值:")
        print(f"  - 總使用者數: {summary['total_users']}")
        print(f"  - 主要區域: {summary['top_region']}")
        
        return {
            'graph': self.graph,
            'users_df': self.users_df,
            'summary': summary,
        }
    
    def _generate_summary(self) -> Dict[str, Any]:
        region_dist = self.users_df['region'].value_counts().to_dict()
        top_region = max(region_dist, key=region_dist.get) if region_dist else 'N/A'
        
        return {
            'total_users': len(self.users_df),
            'unique_regions': len(self.graph.vs),
            'region_distribution': region_dist,
            'top_region': top_region,
        }