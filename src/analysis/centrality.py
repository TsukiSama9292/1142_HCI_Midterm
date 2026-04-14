"""
分析主題 1: 使用者聲望與網路中心度
===================================
驗證高聲望使用者的核心作用：分析高聲望使用者是否在網路結構中具有更高的介性中心度
"""

from typing import Dict, Any, List
from dataclasses import dataclass

import pandas as pd
import igraph as ig

from ..data.data_loader import DataLoader
from ..models.graph_builder import (
    UserNetworkBuilder,
    MultiInteractionNetworkBuilder,
)


@dataclass
class CentralityMetrics:
    """中心度指標"""

    betweenness: List[float]
    degree: List[int]
    closeness: List[float]
    pagerank: List[float]

    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(
            {
                "betweenness": self.betweenness,
                "degree": self.degree,
                "closeness": self.closeness,
                "pagerank": self.pagerank,
            }
        )


class CentralityAnalyzer:
    """使用者聲望與網路中心度分析器"""

    def __init__(self, data_loader: DataLoader = None):
        self.data_loader = data_loader or DataLoader()
        self.builder = UserNetworkBuilder(self.data_loader)
        self.multi_builder = MultiInteractionNetworkBuilder(self.data_loader)
        self.graph: ig.Graph = None
        self.users_df: pd.DataFrame = None
        self.centrality_metrics: CentralityMetrics = None

    def run(self, limit: int = 100, network_type: str = "answer") -> Dict[str, Any]:
        """
        執行完整分析

        Args:
            limit: Number of records to analyze
            network_type: Type of network to build:
                - "answer": Only answer relationships (answerer -> questioner)
                - "combined": Combined network (answers + comments + votes + edits)

        Returns:
            Dict containing:
            - graph: igraph Graph object
            - users_df: User data with reputation levels
            - centrality_metrics: Centrality metrics dataframe
            - reputation_centrality_correlation: Correlation between reputation and betweenness
            - summary: Analysis summary statistics
        """
        print("\n" + "=" * 60)
        print("分析主題 1: 使用者聲望與網路中心度分析")
        print("=" * 60)

        if network_type == "combined":
            print("\n使用綜合網路類型（回答+評論+投票+編輯）")
            self.graph, self.users_df = self.multi_builder.build_combined_network(
                limit=limit
            )
        else:
            self.graph, self.users_df = (
                self.builder.build_answer_network_with_reputation(limit=limit)
            )

        print("\n測試使用者聲望與網路中心度功能")
        print(f"輸入值: limit={limit}")
        print(
            f"中間過程: 建立 {len(self.graph.vs)} 個節點, {len(self.graph.es)} 條邊的網路"
        )

        self.centrality_metrics = self._calculate_centrality()

        analysis_df = self._combine_with_reputation()

        correlation = self._calculate_correlation(analysis_df)

        result = self._generate_summary(analysis_df, correlation)

        print("最終輸出值:")
        print(f"  - 聲望與介性中心度相關係數: {correlation:.4f}")
        print(f"  - 高聲望用戶平均介性中心度: {result['high_rep_avg_betweenness']:.4f}")
        print(f"  - 低聲望用戶平均介性中心度: {result['low_rep_avg_betweenness']:.4f}")
        print(f"  - 未知聲望用戶數: {result['unknown_rep_users']}")

        return {
            "graph": self.graph,
            "users_df": self.users_df,
            "centrality_metrics": self.centrality_metrics.to_dataframe(),
            "reputation_centrality_correlation": correlation,
            "summary": result,
            "analysis_df": analysis_df,
        }

    def _calculate_centrality(self) -> CentralityMetrics:
        """計算各種中心度指標"""
        print("\n中間過程: 計算網路中心度指標...")

        betweenness = self.graph.betweenness()
        degree = self.graph.degree()

        try:
            closeness = self.graph.closeness()
        except:
            closeness = [0.0] * len(self.graph.vs)

        try:
            pagerank = self.graph.pagerank()
        except:
            pagerank = [0.0] * len(self.graph.vs)

        return CentralityMetrics(
            betweenness=betweenness,
            degree=degree,
            closeness=closeness,
            pagerank=pagerank,
        )

    def _combine_with_reputation(self) -> pd.DataFrame:
        """結合聲望資料與中心度指標"""
        print("\n中間過程: 結合聲望資料與中心度指標...")

        metrics_df = self.centrality_metrics.to_dataframe()

        result_df = pd.DataFrame(
            {
                "user_id": self.graph.vs["user_id"],
                "reputation": self.graph.vs["reputation"],
                "reputation_level": self.graph.vs["reputation_level"],
                "betweenness": metrics_df["betweenness"].values,
                "degree": metrics_df["degree"].values,
                "closeness": metrics_df["closeness"].values,
                "pagerank": metrics_df["pagerank"].values,
            }
        )

        return result_df

    def _calculate_correlation(self, df: pd.DataFrame) -> float:
        """計算聲望與介性中心度的相關係數"""
        print("\n中間過程: 計算聲望與介性中心度相關係數...")

        if df["reputation"].sum() == 0:
            return 0.0

        correlation = df["reputation"].corr(df["betweenness"])

        if pd.isna(correlation):
            return 0.0

        return correlation

    def _generate_summary(self, df: pd.DataFrame, correlation: float) -> Dict[str, Any]:
        """生成分析摘要"""
        print("\n中間過程: 生成分析摘要...")

        high_rep = df[df["reputation_level"] == "4_Expert"]
        low_rep = df[df["reputation_level"] == "1_Low"]

        unknown_rep = df[df["reputation_level"] == "0_None"]
        summary = {
            "total_users": len(df),
            "high_rep_users": len(high_rep),
            "low_rep_users": len(low_rep),
            "unknown_rep_users": len(unknown_rep),
            "high_rep_avg_betweenness": high_rep["betweenness"].mean()
            if len(high_rep) > 0
            else 0,
            "low_rep_avg_betweenness": low_rep["betweenness"].mean()
            if len(low_rep) > 0
            else 0,
            "reputation_centrality_correlation": correlation,
            "hypothesis_verified": correlation > 0.3,
        }

        return summary

    def get_top_users(self, n: int = 10, metric: str = "betweenness") -> pd.DataFrame:
        """取得排名最高的用戶"""
        if self.centrality_metrics is None:
            return pd.DataFrame()

        metrics_df = self.centrality_metrics.to_dataframe()
        metrics_df["user_id"] = self.graph.vs["user_id"]
        metrics_df["reputation"] = self.graph.vs["reputation"]
        metrics_df["reputation_level"] = self.graph.vs["reputation_level"]

        return metrics_df.nlargest(n, metric)
