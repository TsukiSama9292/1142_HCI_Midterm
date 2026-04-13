"""
分析主題 4: 知識孤島與連通分量分析
===================================
識別社群中的「技術孤島」：利用連通分量分析，找出僅有少數人互動的孤立組件
"""

from typing import Dict, Any, List
from dataclasses import dataclass

import pandas as pd
import igraph as ig

from ..data.data_loader import DataLoader
from ..models.graph_builder import UserNetworkBuilder


@dataclass
class ComponentInfo:
    """連通分量資訊"""
    component_id: int
    size: int
    user_ids: List[int]
    avg_reputation: float
    avg_interactions: float
    is_main_component: bool


class ConnectedComponentAnalyzer:
    """知識孤島與連通分量分析器"""
    
    def __init__(self, data_loader: DataLoader = None):
        self.data_loader = data_loader or DataLoader()
        self.builder = UserNetworkBuilder(self.data_loader)
        self.graph: ig.Graph = None
        self.connectivity_df: pd.DataFrame = None
        self.components: List[ComponentInfo] = []
    
    def run(self, limit: int = 100) -> Dict[str, Any]:
        """
        執行完整分析
        
        Returns:
            Dict containing analysis results
        """
        print("\n" + "=" * 60)
        print("分析主題 4: 知識孤島與連通分量分析")
        print("=" * 60)
        
        self.graph, self.connectivity_df = self.builder.build_connectivity_network(limit=limit)
        
        print("\n測試知識孤島與連通分量功能")
        print(f"輸入值: limit={limit}")
        print(f"中間過程: 分析 {len(self.graph.vs)} 個用戶節點的連通分量...")
        
        self.components = self._analyze_connected_components()
        
        islands = self._identify_knowledge_islands()
        
        result = self._generate_summary(islands)
        
        print("最終輸出值:")
        print(f"  - 總連通分量數: {len(self.components)}")
        print(f"  - 主連通分量大小: {result['main_component_size']}")
        print(f"  - 識別出的知識孤島數: {result['island_count']}")
        print(f"  - 孤島用戶總數: {result['island_user_count']}")
        
        return {
            'graph': self.graph,
            'connectivity_df': self.connectivity_df,
            'components': self.components,
            'islands': islands,
            'summary': result,
        }
    
    def _analyze_connected_components(self) -> List[ComponentInfo]:
        """分析連通分量"""
        print("\n中間過程: 計算連通分量...")
        
        undirected = self.graph.as_undirected()
        components = undirected.components()
        
        component_info_list = []
        
        main_component_size = max(len(c) for c in components)
        
        for i, component in enumerate(components):
            user_ids = [self.graph.vs[idx]['user_id'] for idx in component]
            
            reputations = [self.graph.vs[idx]['reputation'] for idx in component]
            interactions = [self.graph.vs[idx]['total_interactions'] for idx in component]
            
            component_info_list.append(ComponentInfo(
                component_id=i,
                size=len(component),
                user_ids=user_ids,
                avg_reputation=sum(reputations) / len(reputations) if reputations else 0,
                avg_interactions=sum(interactions) / len(interactions) if interactions else 0,
                is_main_component=(len(component) == main_component_size),
            ))
        
        return sorted(component_info_list, key=lambda x: x.size, reverse=True)
    
    def _identify_knowledge_islands(self) -> List[ComponentInfo]:
        """識別知識孤島"""
        print("\n中間過程: 識別知識孤島...")
        
        islands = []
        for comp in self.components:
            if comp.size <= 5 or not comp.is_main_component:
                islands.append(comp)
        
        return islands
    
    def _generate_summary(self, islands: List[ComponentInfo]) -> Dict[str, Any]:
        """生成分析摘要"""
        print("\n中間過程: 生成分析摘要...")
        
        main_component = next((c for c in self.components if c.is_main_component), None)
        
        summary = {
            'total_components': len(self.components),
            'main_component_size': main_component.size if main_component else 0,
            'main_component_avg_reputation': main_component.avg_reputation if main_component else 0,
            'main_component_avg_interactions': main_component.avg_interactions if main_component else 0,
            'island_count': len(islands),
            'island_user_count': sum(c.size for c in islands),
            'island_components': [
                {
                    'component_id': c.component_id,
                    'size': c.size,
                    'avg_reputation': c.avg_reputation,
                    'avg_interactions': c.avg_interactions,
                }
                for c in islands[:10]
            ],
            'isolation_ratio': sum(c.size for c in islands) / sum(c.size for c in self.components) 
                              if self.components else 0,
        }
        
        return summary
    
    def get_component_distribution(self) -> pd.DataFrame:
        """取得連通分量分佈"""
        if not self.components:
            return pd.DataFrame()
        
        return pd.DataFrame([{
            'component_id': c.component_id,
            'size': c.size,
            'avg_reputation': c.avg_reputation,
            'avg_interactions': c.avg_interactions,
            'is_main_component': c.is_main_component,
            'is_island': c.size <= 5 and not c.is_main_component,
        } for c in self.components])
    
    def get_island_users(self) -> pd.DataFrame:
        """取得知識孤島用戶列表"""
        if not self.components:
            return pd.DataFrame()
        
        island_user_ids = []
        for comp in self.components:
            if comp.size <= 5:
                for uid in comp.user_ids:
                    island_user_ids.append({
                        'user_id': uid,
                        'component_id': comp.component_id,
                        'component_size': comp.size,
                    })
        
        return pd.DataFrame(island_user_ids)
