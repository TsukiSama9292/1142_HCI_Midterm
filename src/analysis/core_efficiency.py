"""
分析主題 2: 網路核心結構與解答效率
===================================
評估核心發問者的問題解決速度：判斷位於網路核心區域的發問者，其問題是否能更快獲得獲納解答
"""

from typing import Dict, Any, List
from dataclasses import dataclass

import pandas as pd
import numpy as np
import igraph as ig

from ..data.data_loader import DataLoader
from ..models.graph_builder import CorePeripheryBuilder


@dataclass
class CorePeripheryMetrics:
    """核心-邊緣結構指標"""
    core_scores: List[float]
    k_core: List[int]
    is_core: List[bool]
    
    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame({
            'core_score': self.core_scores,
            'k_core': self.k_core,
            'is_core': self.is_core,
        })


class CoreEfficiencyAnalyzer:
    """網路核心結構與解答效率分析器"""
    
    def __init__(self, data_loader: DataLoader = None):
        self.data_loader = data_loader or DataLoader()
        self.builder = CorePeripheryBuilder(self.data_loader)
        self.graph: ig.Graph = None
        self.posts_df: pd.DataFrame = None
        self.metrics: CorePeripheryMetrics = None
    
    def run(self, limit: int = 100) -> Dict[str, Any]:
        """
        執行完整分析
        
        Returns:
            Dict containing analysis results
        """
        print("\n" + "=" * 60)
        print("分析主題 2: 網路核心結構與解答效率分析")
        print("=" * 60)
        
        self.graph, self.posts_df = self.builder.build_core_periphery_network(limit=limit)
        
        print(f"\n測試網路核心結構與解答效率功能")
        print(f"輸入值: limit={limit}")
        print(f"中間過程: 建立 {len(self.graph.vs)} 個節點, {len(self.graph.es)} 條邊的網路")
        
        self.metrics = self._calculate_core_metrics()
        
        analysis_df = self._combine_with_efficiency()
        
        efficiency_comparison = self._compare_core_periphery_efficiency(analysis_df)
        
        result = self._generate_summary(analysis_df, efficiency_comparison)
        
        print(f"最終輸出值:")
        print(f"  - 核心用戶平均解答時間: {result['core_avg_hours']:.2f} 小時")
        print(f"  - 邊緣用戶平均解答時間: {result['periphery_avg_hours']:.2f} 小時")
        print(f"  - 核心用戶數量: {result['core_user_count']}")
        
        return {
            'graph': self.graph,
            'posts_df': self.posts_df,
            'metrics': self.metrics.to_dataframe(),
            'analysis_df': analysis_df,
            'efficiency_comparison': efficiency_comparison,
            'summary': result,
        }
    
    def _calculate_core_metrics(self) -> CorePeripheryMetrics:
        """計算核心-邊緣結構指標"""
        print(f"\n中間過程: 計算網路核心-邊緣結構指標...")
        
        undirected = self.graph.as_undirected()
        
        core_scores = []
        for v in undirected.vs:
            neighbors = undirected.neighbors(v)
            core_scores.append(len(neighbors))
        
        try:
            k_core = undirected.coreness()
        except:
            k_core = [0] * len(undirected.vs)
        
        max_k = max(k_core) if k_core and len(k_core) > 0 else 0
        is_core = [k >= max_k * 0.5 if max_k > 0 else False for k in k_core]
        
        return CorePeripheryMetrics(
            core_scores=core_scores,
            k_core=k_core,
            is_core=is_core,
        )
    
    def _combine_with_efficiency(self) -> pd.DataFrame:
        """結合核心結構與解答效率"""
        print(f"\n中間過程: 結合核心結構與解答效率資料...")
        
        posts_with_efficiency = self.posts_df.copy()
        posts_with_efficiency = posts_with_efficiency[
            posts_with_efficiency['hours_to_accept'].notna() & 
            (posts_with_efficiency['hours_to_accept'] >= 0)
        ]
        
        metrics_df = self.metrics.to_dataframe()
        
        user_ids = [uid for uid in self.graph.vs['user_id'] if uid is not None and not pd.isna(uid)]
        
        user_positions = []
        for uid in posts_with_efficiency['questioner_id'].values:
            if pd.notna(uid) and uid in user_ids:
                try:
                    idx = self.graph.vs['user_id'].index(uid)
                    user_positions.append(idx)
                except ValueError:
                    user_positions.append(-1)
            else:
                user_positions.append(-1)
        
        posts_with_efficiency['node_idx'] = user_positions
        
        result_dfs = []
        for idx, row in posts_with_efficiency.iterrows():
            node_idx = row['node_idx']
            if 0 <= node_idx < len(metrics_df):
                temp_df = pd.DataFrame({
                    'question_id': [row['question_id']],
                    'questioner_id': [row['questioner_id']],
                    'answerer_id': [row['answerer_id']],
                    'hours_to_accept': [row['hours_to_accept']],
                    'core_score': [metrics_df.iloc[node_idx]['core_score']],
                    'k_core': [metrics_df.iloc[node_idx]['k_core']],
                    'is_core': [metrics_df.iloc[node_idx]['is_core']],
                })
                result_dfs.append(temp_df)
        
        if result_dfs:
            return pd.concat(result_dfs, ignore_index=True)
        else:
            return pd.DataFrame(columns=[
                'question_id', 'questioner_id', 'answerer_id', 
                'hours_to_accept', 'core_score', 'k_core', 'is_core'
            ])
    
    def _compare_core_periphery_efficiency(self, df: pd.DataFrame) -> Dict[str, Any]:
        """比較核心與邊緣用戶的解答效率"""
        print(f"\n中間過程: 比較核心與邊緣用戶的解答效率...")
        
        if len(df) == 0:
            return {
                'core_avg_hours': 0,
                'periphery_avg_hours': 0,
                'core_median_hours': 0,
                'periphery_median_hours': 0,
            }
        
        core_df = df[df['is_core'] == True]
        periphery_df = df[df['is_core'] == False]
        
        comparison = {
            'core_avg_hours': core_df['hours_to_accept'].mean() if len(core_df) > 0 else 0,
            'periphery_avg_hours': periphery_df['hours_to_accept'].mean() if len(periphery_df) > 0 else 0,
            'core_median_hours': core_df['hours_to_accept'].median() if len(core_df) > 0 else 0,
            'periphery_median_hours': periphery_df['hours_to_accept'].median() if len(periphery_df) > 0 else 0,
            'core_count': len(core_df),
            'periphery_count': len(periphery_df),
        }
        
        return comparison
    
    def _generate_summary(self, df: pd.DataFrame, comparison: Dict[str, Any]) -> Dict[str, Any]:
        """生成分析摘要"""
        print(f"\n中間過程: 生成分析摘要...")
        
        efficiency_level = pd.cut(
            df['hours_to_accept'],
            bins=[0, 1, 24, 168, float('inf')],
            labels=['1_VeryFast', '2_Fast', '3_Slow', '4_VerySlow']
        )
        df['efficiency_level'] = efficiency_level
        
        summary = {
            'total_questions': len(df),
            'core_user_count': int(df['is_core'].sum()),
            'periphery_user_count': int((~df['is_core']).sum()),
            'core_avg_hours': comparison['core_avg_hours'],
            'periphery_avg_hours': comparison['periphery_avg_hours'],
            'core_faster': comparison['core_avg_hours'] < comparison['periphery_avg_hours'],
            'efficiency_by_level': df['efficiency_level'].value_counts().to_dict(),
        }
        
        return summary
    
    def get_efficiency_distribution(self) -> pd.DataFrame:
        """取得效率分佈"""
        if self.metrics is None:
            return pd.DataFrame()
        
        return self.metrics.to_dataframe()
