"""
分析主題 5: 內容特徵與互動反響 (補充)
=====================================
量化程式碼區塊對 Upvotes 的影響：探討貼文內容特徵（是否包含程式碼區塊）對社群回饋分數的影響
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass

import pandas as pd
import numpy as np
from scipy import stats
import igraph as ig

from ..data.data_loader import DataLoader


@dataclass
class CodeImpactAnalysis:
    """程式碼影響分析結果"""
    has_code_avg_score: float
    no_code_avg_score: float
    t_statistic: float
    p_value: float
    is_significant: bool


class ContentFeatureAnalyzer:
    """內容特徵與互動反響分析器"""
    
    def __init__(self, data_loader: DataLoader = None):
        self.data_loader = data_loader or DataLoader()
        self.posts_df: pd.DataFrame = None
        self.graph: Optional[ig.Graph] = None
    
    def run(self, limit: int = 100) -> Dict[str, Any]:
        """
        執行完整分析
        
        Returns:
            Dict containing analysis results
        """
        print("\n" + "=" * 60)
        print("分析主題 5: 內容特徵與互動反響分析")
        print("=" * 60)
        
        self.posts_df = self.data_loader.load_posts_with_code(limit=limit)
        
        print(f"\n測試內容特徵與互動反響功能")
        print(f"輸入值: limit={limit}")
        print(f"中間過程: 分析 {len(self.posts_df)} 篇貼文的內容特徵...")
        
        impact_analysis = self._analyze_code_impact()
        
        score_distribution = self._analyze_score_distribution()
        
        self.graph = self._build_content_network()
        
        result = self._generate_summary(impact_analysis, score_distribution)
        
        print(f"最終輸出值:")
        print(f"  - 含程式碼平均分數: {impact_analysis.has_code_avg_score:.2f}")
        print(f"  - 不含程式碼平均分數: {impact_analysis.no_code_avg_score:.2f}")
        print(f"  - 統計顯著性: {'是' if impact_analysis.is_significant else '否'}")
        print(f"  - 含程式碼貼文數: {result['has_code_count']}")
        print(f"  - 不含程式碼貼文數: {result['no_code_count']}")
        
        return {
            'posts_df': self.posts_df,
            'graph': self.graph,
            'impact_analysis': {
                'has_code_avg_score': impact_analysis.has_code_avg_score,
                'no_code_avg_score': impact_analysis.no_code_avg_score,
                't_statistic': impact_analysis.t_statistic,
                'p_value': impact_analysis.p_value,
                'is_significant': impact_analysis.is_significant,
            },
            'score_distribution': score_distribution,
            'summary': result,
        }
    
    def _analyze_code_impact(self) -> CodeImpactAnalysis:
        """分析程式碼區塊對分數的影響"""
        print(f"\n中間過程: 分析程式碼區塊對分數的影響...")
        
        has_code = self.posts_df[self.posts_df['has_code_block'] == 1]['score']
        no_code = self.posts_df[self.posts_df['has_code_block'] == 0]['score']
        
        has_code_avg = has_code.mean() if len(has_code) > 0 else 0
        no_code_avg = no_code.mean() if len(no_code) > 0 else 0
        
        if len(has_code) > 1 and len(no_code) > 1:
            t_stat, p_value = stats.ttest_ind(has_code, no_code)
            is_significant = p_value < 0.05
        else:
            t_stat, p_value = 0, 1
            is_significant = False
        
        return CodeImpactAnalysis(
            has_code_avg_score=has_code_avg,
            no_code_avg_score=no_code_avg,
            t_statistic=t_stat,
            p_value=p_value,
            is_significant=is_significant,
        )
    
    def _analyze_score_distribution(self) -> Dict[str, Any]:
        """分析分數分佈"""
        print(f"\n中間過程: 分析分數分佈...")
        
        distribution = {}
        
        for level in self.posts_df['score_level'].unique():
            count = len(self.posts_df[self.posts_df['score_level'] == level])
            has_code = len(self.posts_df[(self.posts_df['score_level'] == level) & 
                                          (self.posts_df['has_code_block'] == 1)])
            no_code = len(self.posts_df[(self.posts_df['score_level'] == level) & 
                                        (self.posts_df['has_code_block'] == 0)])
            distribution[level] = {
                'total': count,
                'has_code': has_code,
                'no_code': no_code,
                'has_code_ratio': has_code / count if count > 0 else 0,
            }
        
        return distribution
    
    def _generate_summary(self, impact: CodeImpactAnalysis, 
                         distribution: Dict[str, Any]) -> Dict[str, Any]:
        """生成分析摘要"""
        print(f"\n中間過程: 生成分析摘要...")
        
        has_code_df = self.posts_df[self.posts_df['has_code_block'] == 1]
        no_code_df = self.posts_df[self.posts_df['has_code_block'] == 0]
        
        summary = {
            'total_posts': len(self.posts_df),
            'has_code_count': len(has_code_df),
            'no_code_count': len(no_code_df),
            'has_code_ratio': len(has_code_df) / len(self.posts_df) if len(self.posts_df) > 0 else 0,
            'has_code_avg_score': impact.has_code_avg_score,
            'no_code_avg_score': impact.no_code_avg_score,
            'score_difference': impact.has_code_avg_score - impact.no_code_avg_score,
            'code_helps_upvotes': impact.has_code_avg_score > impact.no_code_avg_score,
            'is_statistically_significant': impact.is_significant,
            'p_value': impact.p_value,
            'score_distribution': distribution,
        }
        
        return summary
    
    def _build_content_network(self) -> ig.Graph:
        """
        建構內容特徵網路圖
        研究方法5: 節點為貼文，邊為相似標籤關係
        """
        print(f"\n中間過程: 建構內容特徵網路圖...")
        
        df = self.posts_df.copy()
        df = df[df['score'].notna() & df['has_code_block'].notna()]
        
        if len(df) == 0:
            return ig.Graph(directed=False)
        
        n_posts = len(df)
        graph = ig.Graph(directed=False)
        graph.add_vertices(n_posts)
        
        edges = []
        for i in range(n_posts):
            for j in range(i + 1, n_posts):
                tags_i = str(df.iloc[i].get('tags', ''))
                tags_j = str(df.iloc[j].get('tags', ''))
                if tags_i and tags_j and len(set(tags_i.split('|')) & set(tags_j.split('|'))) > 0:
                    edges.append((i, j))
        
        graph.add_edges(edges)
        
        graph.vs['name'] = [f"P{row['id']}" for _, row in df.iterrows()]
        graph.vs['post_id'] = df['id'].tolist()
        graph.vs['score'] = df['score'].tolist()
        graph.vs['has_code'] = ['yes' if hc == 1 else 'no' for hc in df['has_code_block'].tolist()]
        graph.vs['score_level'] = df['score_level'].tolist()
        graph.vs['score_level'] = [str(sl) if pd.notna(sl) else '3_Neutral' for sl in graph.vs['score_level']]
        
        return graph
    
    def get_posts_comparison(self) -> pd.DataFrame:
        """取得含/不含程式碼貼文比較"""
        if self.posts_df is None:
            return pd.DataFrame()
        
        return self.posts_df.groupby('has_code_block').agg({
            'score': ['mean', 'median', 'std', 'min', 'max'],
            'view_count': ['mean', 'median'],
            'answer_count': ['mean', 'median'],
            'comment_count': ['mean', 'median'],
        }).round(2)
