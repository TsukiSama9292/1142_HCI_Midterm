"""
SNA 分析執行器 - 執行所有 15 個分析主題
"""

from typing import Dict, Any
from pathlib import Path
import json
import pandas as pd

from src.data.data_loader import DataLoader
from src.analysis.centrality import CentralityAnalyzer
from src.analysis.core_efficiency import CoreEfficiencyAnalyzer
from src.analysis.tag_cooccurrence import TagCooccurrenceAnalyzer
from src.analysis.connected_components import ConnectedComponentAnalyzer
from src.analysis.content_features import ContentFeatureAnalyzer
from src.analysis.account_age import AccountAgeAnalyzer
from src.analysis.voting_behavior import VotingBehaviorAnalyzer
from src.analysis.comment_network import CommentNetworkAnalyzer
from src.analysis.badge_network import BadgeNetworkAnalyzer
from src.analysis.edit_collaboration import EditCollaborationAnalyzer
from src.analysis.post_link import PostLinkAnalyzer
from src.analysis.review_task import ReviewTaskAnalyzer
from src.analysis.bounty_network import BountyNetworkAnalyzer
from src.analysis.user_location import UserLocationAnalyzer
from src.analysis.time_series import TimeSeriesAnalyzer
from src.visualization.plots import SNAPlotter, generate_summary_report
from src.utils.helpers import save_json


class SNARunner:
    """社會網路分析執行器"""

    def __init__(
        self,
        output_dir: str = "output",
        data_limit: int = 100,
        analysis_limit_map: dict | None = None,
    ):
        self.data_loader = DataLoader()
        self.plotter = SNAPlotter(output_dir=Path(output_dir))
        self.data_limit = data_limit
        self.analysis_limit_map = analysis_limit_map or {}
        self.results: Dict[str, Dict[str, Any]] = {}
        self.analysis_limits = self._build_analysis_limits()

    def _build_analysis_limits(self) -> Dict[int, int]:
        default_limit = self.analysis_limit_map.get("default", self.data_limit)
        limits: Dict[int, int] = {}

        for analysis_id in range(1, 16):
            if analysis_id in self.analysis_limit_map:
                limits[analysis_id] = self.analysis_limit_map[analysis_id]
                continue

            if analysis_id in [7, 8, 9, 10, 11, 12, 13, 14]:
                limits[analysis_id] = max(default_limit, 500)
            elif analysis_id == 15:
                limits[analysis_id] = max(default_limit, 1000)
            else:
                limits[analysis_id] = default_limit

        return limits

    def run_all(self) -> Dict[str, Dict[str, Any]]:
        """執行所有分析"""
        print("\n" + "=" * 70)
        print("Stack Overflow 社會網路分析 - 執行所有 15 個分析")
        print("=" * 70)

        print(f"\n設定參數: data_limit={self.data_limit}")

        self._run_analysis_1()
        self._run_analysis_2()
        self._run_analysis_3()
        self._run_analysis_4()
        self._run_analysis_5()
        self._run_analysis_6()
        self._run_analysis_7()
        self._run_analysis_8()
        self._run_analysis_9()
        self._run_analysis_10()
        self._run_analysis_11()
        self._run_analysis_12()
        self._run_analysis_13()
        self._run_analysis_14()
        self._run_analysis_15()

        self._generate_visualizations()

        self._save_results()

        return self.results

    def _run_analysis_1(self):
        """執行分析 1: 使用者聲望與網路中心度"""
        print("\n" + "#" * 60)
        print("# 分析主題 1: 使用者聲望與網路中心度")
        print("#" * 60)

        analyzer = CentralityAnalyzer(self.data_loader)
        self.results["analysis_1_centrality"] = analyzer.run(limit=self.data_limit)

    def _run_analysis_2(self):
        """執行分析 2: 網路核心結構與解答效率"""
        print("\n" + "#" * 60)
        print("# 分析主題 2: 網路核心結構與解答效率")
        print("#" * 60)

        analyzer = CoreEfficiencyAnalyzer(self.data_loader)
        self.results["analysis_2_core_efficiency"] = analyzer.run(limit=self.data_limit)

    def _run_analysis_3(self):
        """執行分析 3: 技術標籤共現與領域地圖"""
        print("\n" + "#" * 60)
        print("# 分析主題 3: 技術標籤共現與領域地圖")
        print("#" * 60)

        analyzer = TagCooccurrenceAnalyzer(self.data_loader)
        self.results["analysis_3_tag_cooccurrence"] = analyzer.run(
            limit=self.data_limit
        )

    def _run_analysis_4(self):
        """執行分析 4: 知識孤島與連通分量分析"""
        print("\n" + "#" * 60)
        print("# 分析主題 4: 知識孤島與連通分量分析")
        print("#" * 60)

        analyzer = ConnectedComponentAnalyzer(self.data_loader)
        self.results["analysis_4_connected_components"] = analyzer.run(
            limit=self.data_limit
        )

    def _run_analysis_5(self):
        """執行分析 5: 內容特徵與互動反響"""
        print("\n" + "#" * 60)
        print("# 分析主題 5: 內容特徵與互動反響")
        print("#" * 60)

        analyzer = ContentFeatureAnalyzer(self.data_loader)
        self.results["analysis_5_content_features"] = analyzer.run(
            limit=self.data_limit
        )

    def _run_analysis_6(self):
        """執行分析 6: 帳號年資與社群貢獻"""
        print("\n" + "#" * 60)
        print("# 分析主題 6: 帳號年資與社群貢獻")
        print("#" * 60)

        analyzer = AccountAgeAnalyzer(self.data_loader)
        self.results["analysis_6_account_age"] = analyzer.run(limit=self.data_limit)

    def _run_analysis_7(self):
        """執行分析 7: 投票行為網路"""
        print("\n" + "#" * 60)
        print("# 分析主題 7: 投票行為網路")
        print("#" * 60)

        analyzer = VotingBehaviorAnalyzer(self.data_loader)
        self.results["analysis_7_voting_behavior"] = analyzer.run(
            limit=self.analysis_limits[7]
        )

    def _run_analysis_8(self):
        """執行分析 8: 評論互動網路"""
        print("\n" + "#" * 60)
        print("# 分析主題 8: 評論互動網路")
        print("#" * 60)

        analyzer = CommentNetworkAnalyzer(self.data_loader)
        self.results["analysis_8_comment_network"] = analyzer.run(
            limit=self.analysis_limits[8]
        )

    def _run_analysis_9(self):
        """執行分析 9: 徽章成就網路"""
        print("\n" + "#" * 60)
        print("# 分析主題 9: 徽章成就網路")
        print("#" * 60)

        analyzer = BadgeNetworkAnalyzer(self.data_loader)
        self.results["analysis_9_badge_network"] = analyzer.run(
            limit=self.analysis_limits[9]
        )

    def _run_analysis_10(self):
        """執行分析 10: 編輯協作網路"""
        print("\n" + "#" * 60)
        print("# 分析主題 10: 編輯協作網路")
        print("#" * 60)

        analyzer = EditCollaborationAnalyzer(self.data_loader)
        self.results["analysis_10_edit_collaboration"] = analyzer.run(
            limit=self.analysis_limits[10]
        )

    def _run_analysis_11(self):
        """執行分析 11: 引用與重複問題網路"""
        print("\n" + "#" * 60)
        print("# 分析主題 11: 引用與重複問題網路")
        print("#" * 60)

        analyzer = PostLinkAnalyzer(self.data_loader)
        self.results["analysis_11_post_link"] = analyzer.run(
            limit=self.analysis_limits[11]
        )

    def _run_analysis_12(self):
        """執行分析 12: 審核任務網路"""
        print("\n" + "#" * 60)
        print("# 分析主題 12: 審核任務網路")
        print("#" * 60)

        analyzer = ReviewTaskAnalyzer(self.data_loader)
        self.results["analysis_12_review_task"] = analyzer.run(
            limit=self.analysis_limits[12]
        )

    def _run_analysis_13(self):
        """執行分析 13: 賞金懸賞網路"""
        print("\n" + "#" * 60)
        print("# 分析主題 13: 賞金懸賞網路")
        print("#" * 60)

        analyzer = BountyNetworkAnalyzer(self.data_loader)
        self.results["analysis_13_bounty_network"] = analyzer.run(
            limit=self.analysis_limits[13]
        )

    def _run_analysis_14(self):
        """執行分析 14: 使用者地理分布網路"""
        print("\n" + "#" * 60)
        print("# 分析主題 14: 使用者地理分布網路")
        print("#" * 60)

        analyzer = UserLocationAnalyzer(self.data_loader)
        self.results["analysis_14_user_location"] = analyzer.run(
            limit=self.analysis_limits[14]
        )

    def _run_analysis_15(self):
        """執行分析 15: 時間序列活躍度網路"""
        print("\n" + "#" * 60)
        print("# 分析主題 15: 時間序列活躍度網路")
        print("#" * 60)

        analyzer = TimeSeriesAnalyzer(self.data_loader)
        self.results["analysis_15_time_series"] = analyzer.run(
            limit=self.analysis_limits[15]
        )

    def _generate_visualizations(self):
        """產生視覺化圖表"""
        print("\n" + "=" * 60)
        print("產生視覺化圖表 (使用 igraph)")
        print("=" * 60)

        LEGEND_INFO = {
            "analysis_1": {
                "colors": {
                    "Green-Newcomer (<1K)": "#4CAF50",
                    "Yellow-Mid (1K~10K)": "#FFD700",
                    "Orange-Senior (10K~50K)": "#FF9800",
                    "Red-Expert (>50K)": "#F44336",
                },
                "shapes": {
                    "Circle-High Centrality": "o",
                    "Triangle-Low Centrality": "^",
                },
                "edge_weights": {
                    "Thick-Strong Tie": 3.0,
                    "Thin-Weak Tie": 0.5,
                },
            },
            "analysis_2": {
                "colors": {
                    "Green-<1h": "#4CAF50",
                    "Yellow-1~12h": "#FFD700",
                    "LightRed-12~24h": "#FFCDD2",
                    "Red->24h": "#F44336",
                    "Gray-Unresolved": "#9E9E9E",
                },
                "shapes": {
                    "Square-Core": "s",
                    "Circle-Periphery": "o",
                },
                "edge_weights": {
                    "Thick-Strong Tie": 3.0,
                    "Thin-Weak Tie": 0.5,
                },
            },
            "analysis_3": {
                "colors": {
                    "LightBlue-Web": "#81D4FA",
                    "Pink-AI/Data": "#F8BBD9",
                    "Green-Mobile": "#A5D6A7",
                    "Yellow-Backend": "#FFE082",
                    "Purple-Database": "#CE93D8",
                    "Gray-Other": "#E0E0E0",
                },
                "edge_weights": {
                    "Thick-High Co-occurrence": 3.0,
                    "Thin-Low Co-occurrence": 0.5,
                },
            },
            "analysis_4": {
                "colors": {
                    "DarkBlue-Main Component": "#1565C0",
                    "Gray-Isolated": "#9E9E9E",
                },
                "shapes": {
                    "Circle-Continuous": "o",
                    "Triangle-Single": "^",
                },
                "edge_weights": {
                    "Thick-Strong Tie": 3.0,
                    "Thin-Weak Tie": 0.5,
                },
            },
            "analysis_5": {
                "colors": {
                    "Gray-0 votes": "#BDBDBD",
                    "Green-1~10 votes": "#66BB6A",
                    "Yellow-11~50 votes": "#FFD54F",
                    "Orange-51~100 votes": "#FF7043",
                    "Red->100 votes": "#F44336",
                },
                "shapes": {
                    "Circle-Has Code": "o",
                    "Square-Text Only": "s",
                },
                "edge_weights": {
                    "Thick-Similar Tags": 3.0,
                    "Thin-Different Tags": 0.5,
                },
            },
            "analysis_6": {
                "colors": {
                    "Green-<1 year": "#4CAF50",
                    "Yellow-1~3 years": "#FFD700",
                    "Orange-3~6 years": "#FF9800",
                    "Red-6~10 years": "#F44336",
                    "Purple->10 years": "#9C27B0",
                },
                "shapes": {
                    "Circle-Asker": "o",
                    "Triangle-Answerer": "^",
                    "Square-Both": "s",
                },
                "edge_weights": {
                    "Thick-Strong Tie": 3.0,
                    "Thin-Weak Tie": 0.5,
                },
            },
            "analysis_7": {
                "colors": {
                    "Gold-Accepted": "#FFD700",
                    "Green-Upvote": "#4CAF50",
                    "Red-Downvote": "#F44336",
                    "Black-Spam": "#212121",
                    "Blue-Favorite": "#2196F3",
                },
                "shapes": {
                    "Circle-High Votes": "o",
                    "Triangle-Low Votes": "^",
                },
                "edge_weights": {
                    "Thick-Strong Tie": 3.0,
                    "Thin-Weak Tie": 0.5,
                },
            },
            "analysis_8": {
                "colors": {
                    "Blue-Active": "#2196F3",
                    "Green-Moderate": "#4CAF50",
                    "Gray-Low": "#9E9E9E",
                },
                "shapes": {
                    "Circle-Commenter": "o",
                },
                "edge_weights": {
                    "Thick-Strong Tie": 3.0,
                    "Thin-Weak Tie": 0.5,
                },
            },
            "analysis_9": {
                "colors": {
                    "Gold-Gold Badge": "#FFD700",
                    "Silver-Silver Badge": "#C0C0C0",
                    "Bronze-Bronze Badge": "#CD7F32",
                },
                "shapes": {
                    "Circle-Top Earner": "o",
                    "Triangle-Regular": "^",
                },
                "edge_weights": {
                    "Thick-Strong Tie": 3.0,
                    "Thin-Weak Tie": 0.5,
                },
            },
            "analysis_10": {
                "colors": {
                    "Green-Active": "#4CAF50",
                    "Yellow-Moderate": "#FFC107",
                    "Gray-Casual": "#9E9E9E",
                },
                "shapes": {
                    "Circle-Editor": "o",
                },
                "edge_weights": {
                    "Thick-Strong Tie": 3.0,
                    "Thin-Weak Tie": 0.5,
                },
            },
            "analysis_11": {
                "colors": {
                    "Blue-Linked": "#2196F3",
                    "Red-Duplicate": "#F44336",
                },
                "shapes": {
                    "Circle-Question": "o",
                },
                "edge_weights": {
                    "Thick-Strong Tie": 3.0,
                    "Thin-Weak Tie": 0.5,
                },
            },
            "analysis_12": {
                "colors": {
                    "Green-Active": "#4CAF50",
                    "Yellow-Moderate": "#FFC107",
                    "Gray-Casual": "#9E9E9E",
                },
                "shapes": {
                    "Circle-Reviewer": "o",
                },
                "edge_weights": {
                    "Thick-Strong Tie": 3.0,
                    "Thin-Weak Tie": 0.5,
                },
            },
            "analysis_13": {
                "colors": {
                    "Gray-Meager": "#9E9E9E",
                    "Green-Normal": "#4CAF50",
                    "Yellow-Generous": "#FFC107",
                    "Red-Extravagant": "#F44336",
                },
                "shapes": {
                    "Circle-Bounty User": "o",
                },
                "edge_weights": {
                    "Thick-Strong Tie": 3.0,
                    "Thin-Weak Tie": 0.5,
                },
            },
            "analysis_14": {
                "colors": {
                    "Blue-North America": "#2196F3",
                    "Green-Europe": "#4CAF50",
                    "Yellow-Asia": "#FFC107",
                    "Gray-Other": "#9E9E9E",
                },
                "shapes": {
                    "Circle-Region": "o",
                },
                "edge_weights": {
                    "Thick-Strong Tie": 3.0,
                    "Thin-Weak Tie": 0.5,
                },
            },
            "analysis_15": {
                "colors": {
                    "Blue-High Activity": "#2196F3",
                    "Green-Medium": "#4CAF50",
                    "Gray-Low": "#9E9E9E",
                },
                "shapes": {
                    "Circle-Month": "o",
                },
                "edge_weights": {
                    "Thick-Strong Tie": 3.0,
                    "Thin-Weak Tie": 0.5,
                },
            },
        }

        if "analysis_1_centrality" in self.results:
            result = self.results["analysis_1_centrality"]
            if "graph" in result and result["graph"] is not None:
                self.plotter.plot_network_graph(
                    result["graph"],
                    "Method 1: Reputation vs Network Centrality (Raw User Graph)",
                    color_by="reputation_level",
                    filename="analysis_1_network_raw.png",
                    legend_info=LEGEND_INFO["analysis_1"],
                )
                self._plot_reputation_network_aggregated(result["graph"])

        if "analysis_2_core_efficiency" in self.results:
            result = self.results["analysis_2_core_efficiency"]
            if "graph" in result and result["graph"] is not None:
                self.plotter.plot_network_graph(
                    result["graph"],
                    "Method 2: Core-Periphery vs Answer Efficiency (Raw User Graph)",
                    color_by="answer_time_level",
                    filename="analysis_2_network_raw.png",
                    legend_info=LEGEND_INFO["analysis_2"],
                )
                self._plot_core_efficiency_network_aggregated(result["graph"], result)

        if "analysis_3_tag_cooccurrence" in self.results:
            result = self.results["analysis_3_tag_cooccurrence"]
            if "graph" in result and result["graph"] is not None:
                self.plotter.plot_network_graph(
                    result["graph"],
                    "Method 3: Tag Co-occurrence & Technology Map\nNodes=Tags, Edges=Co-occurrence | Color: Tech Domain | Size: Popularity",
                    color_by="tech_domain",
                    filename="analysis_3_network_raw.png",
                    legend_info=LEGEND_INFO["analysis_3"],
                )
                self._plot_tag_cooccurrence_network_aggregated(result["graph"], result)

        if "analysis_4_connected_components" in self.results:
            result = self.results["analysis_4_connected_components"]
            if "graph" in result and result["graph"] is not None:
                self.plotter.plot_network_graph(
                    result["graph"],
                    "Method 4: Knowledge Islands & Connected Components (Raw User Graph)",
                    color_by="connectivity_level",
                    filename="analysis_4_network_raw.png",
                    legend_info=LEGEND_INFO["analysis_4"],
                )
                self._plot_connected_components_network_aggregated(
                    result["graph"], result
                )

        if "analysis_5_content_features" in self.results:
            result = self.results["analysis_5_content_features"]
            if "graph" in result and result["graph"] is not None:
                self.plotter.plot_network_graph(
                    result["graph"],
                    "Method 5: Content Features vs Upvotes\nNodes=Posts, Edges=Similar Tags | Color: Score | Shape: Code Presence",
                    color_by="score_level",
                    shape_by="has_code",
                    filename="analysis_5_network_raw.png",
                    legend_info=LEGEND_INFO["analysis_5"],
                )
                self._plot_content_features_network_aggregated(result["graph"], result)

        if "analysis_6_account_age" in self.results:
            result = self.results["analysis_6_account_age"]
            if "graph" in result and result["graph"] is not None:
                self.plotter.plot_network_graph(
                    result["graph"],
                    "Method 6: Account Age vs Community Contribution (Raw User Graph)",
                    color_by="account_age_level",
                    filename="analysis_6_network_raw.png",
                    legend_info=LEGEND_INFO["analysis_6"],
                )
                self._plot_account_age_network_aggregated(result["graph"], result)

        if "analysis_7_voting_behavior" in self.results:
            result = self.results["analysis_7_voting_behavior"]
            if "graph" in result and result["graph"] is not None:
                self.plotter.plot_network_graph(
                    result["graph"],
                    "Method 7: Voting Behavior Network (Raw User Graph)",
                    color_by="vote_type",
                    filename="analysis_7_network_raw.png",
                    legend_info=LEGEND_INFO["analysis_7"],
                )
                self._plot_voting_behavior_network_aggregated(result["graph"], result)

        if "analysis_8_comment_network" in self.results:
            result = self.results["analysis_8_comment_network"]
            if "graph" in result and result["graph"] is not None:
                self.plotter.plot_network_graph(
                    result["graph"],
                    "Method 8: Comment Interaction Network (Raw User Graph)",
                    color_by="activity_level",
                    filename="analysis_8_network_raw.png",
                    legend_info=LEGEND_INFO["analysis_8"],
                )
                self._plot_comment_network_aggregated(result["graph"], result)

        if "analysis_9_badge_network" in self.results:
            result = self.results["analysis_9_badge_network"]
            if "graph" in result and result["graph"] is not None:
                self.plotter.plot_network_graph(
                    result["graph"],
                    "Method 9: Badge Achievement Network\nNodes=Users, Edges=Shared Badges | Color: Badge Level",
                    color_by="badge_level",
                    filename="analysis_9_network_raw.png",
                    legend_info=LEGEND_INFO["analysis_9"],
                )
                self._plot_badge_network_aggregated(result["graph"], result)

        if "analysis_10_edit_collaboration" in self.results:
            result = self.results["analysis_10_edit_collaboration"]
            if "graph" in result and result["graph"] is not None:
                self._plot_edit_collaboration_network_aggregated(
                    result["graph"], result
                )

        if "analysis_11_post_link" in self.results:
            result = self.results["analysis_11_post_link"]
            if "graph" in result and result["graph"] is not None:
                self.plotter.plot_network_graph(
                    result["graph"],
                    "Method 11: Post Link & Duplicate Network\nNodes=Posts, Edges=Link | Color: Link Type",
                    color_by="link_type",
                    filename="analysis_11_network_raw.png",
                    legend_info=LEGEND_INFO["analysis_11"],
                )
                self._plot_post_link_network_aggregated(result["graph"], result)

        if "analysis_12_review_task" in self.results:
            result = self.results["analysis_12_review_task"]
            if "graph" in result and result["graph"] is not None:
                self.plotter.plot_network_graph(
                    result["graph"],
                    "Method 12: Review Task Network (Raw User Graph)",
                    color_by="reviewer_level",
                    filename="analysis_12_network_raw.png",
                    legend_info=LEGEND_INFO["analysis_12"],
                )
                self._plot_review_task_network_aggregated(result["graph"], result)

        if "analysis_13_bounty_network" in self.results:
            result = self.results["analysis_13_bounty_network"]
            if "graph" in result and result["graph"] is not None:
                self.plotter.plot_network_graph(
                    result["graph"],
                    "Method 13: Bounty Network\nNodes=Users, Edges=Bounty | Color: Bounty Level",
                    color_by="bounty_level",
                    filename="analysis_13_network_raw.png",
                    legend_info=LEGEND_INFO["analysis_13"],
                )
                self._plot_bounty_network_aggregated(result["graph"], result)

        if "analysis_14_user_location" in self.results:
            result = self.results["analysis_14_user_location"]
            if "graph" in result and result["graph"] is not None:
                g = result["graph"]
                labels = g.vs["region"] if "region" in g.vs.attribute_names() else None
                self.plotter.plot_network_graph(
                    g,
                    "Method 14: User Location Network\nNodes=Regions, Edges=Connection | Color: Region | Label: Region Name",
                    color_by="region",
                    vertex_labels=labels,
                    filename="analysis_14_network_raw.png",
                    legend_info=LEGEND_INFO["analysis_14"],
                )
                self._plot_user_location_network_aggregated(result["graph"], result)

        if "analysis_15_time_series" in self.results:
            result = self.results["analysis_15_time_series"]
            if "graph" in result and result["graph"] is not None:
                self.plotter.plot_network_graph(
                    result["graph"],
                    "Method 15: Time Series Activity Network (Raw Node Graph)",
                    color_by="activity_level",
                    filename="analysis_15_network_raw.png",
                    legend_info=LEGEND_INFO["analysis_15"],
                )
                self._plot_time_series_network_aggregated(result["graph"], result)

    def _plot_reputation_network_aggregated(self, graph):
        """Plot aggregated 4-node reputation network visualization."""
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches

        node_positions = {
            "1_Low": (0.5, 0.9),
            "2_Medium": (0.85, 0.6),
            "3_Senior": (0.15, 0.6),
            "4_Expert": (0.5, 0.15),
        }
        node_colors = {
            "1_Low": "#4CAF50",
            "2_Medium": "#FFD700",
            "3_Senior": "#FF9800",
            "4_Expert": "#F44336",
        }
        node_labels = {
            "1_Low": "Low",
            "2_Medium": "Mid",
            "3_Senior": "Senior",
            "4_Expert": "Expert",
        }

        rep_counts = {"1_Low": 0, "2_Medium": 0, "3_Senior": 0, "4_Expert": 0}
        node_rep_map = {}
        for i, v in enumerate(graph.vs):
            rep_level = (
                v["reputation_level"]
                if "reputation_level" in v.attributes()
                else "1_Low"
            )
            if rep_level not in rep_counts:
                rep_level = "1_Low"
            rep_counts[rep_level] += 1
            node_rep_map[i] = rep_level

        edge_pair_counts = {}
        for e in graph.es:
            src_rep = node_rep_map[e.source]
            tgt_rep = node_rep_map[e.target]
            pair = tuple(sorted([src_rep, tgt_rep]))
            edge_pair_counts[pair] = edge_pair_counts.get(pair, 0) + 1

        fig, ax = plt.subplots(figsize=(10, 8))
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")

        for rep_level, count in rep_counts.items():
            x, y = node_positions[rep_level]
            size = max(500, count * 3)
            ax.scatter(
                x,
                y,
                s=size,
                c=node_colors[rep_level],
                zorder=3,
                edgecolors="black",
                linewidths=1.5,
            )
            ax.text(
                x,
                y,
                f"{node_labels[rep_level]}\n({count})",
                ha="center",
                va="center",
                fontsize=11,
                fontweight="bold",
                zorder=4,
            )

        pair_color_map = {
            ("1_Low", "1_Low"): "#4CAF50",
            ("1_Low", "2_Medium"): "#8BC34A",
            ("1_Low", "3_Senior"): "#FFC107",
            ("1_Low", "4_Expert"): "#FF9800",
            ("2_Medium", "2_Medium"): "#FFD700",
            ("2_Medium", "3_Senior"): "#FFB300",
            ("2_Medium", "4_Expert"): "#FF7043",
            ("3_Senior", "3_Senior"): "#FF9800",
            ("3_Senior", "4_Expert"): "#F44336",
            ("4_Expert", "4_Expert"): "#D32F2F",
        }

        pair_label_map = {
            ("1_Low", "1_Low"): "Low↔Low",
            ("1_Low", "2_Medium"): "Mid↔Low",
            ("1_Low", "3_Senior"): "Senior↔Low",
            ("1_Low", "4_Expert"): "Expert↔Low",
            ("2_Medium", "2_Medium"): "Mid↔Mid",
            ("2_Medium", "3_Senior"): "Senior↔Mid",
            ("2_Medium", "4_Expert"): "Expert↔Mid",
            ("3_Senior", "3_Senior"): "Senior↔Senior",
            ("3_Senior", "4_Expert"): "Expert↔Senior",
            ("4_Expert", "4_Expert"): "Expert↔Expert",
        }

        max_count = max(edge_pair_counts.values()) if edge_pair_counts else 1

        for pair, cnt in edge_pair_counts.items():
            n1, n2 = pair
            x1, y1 = node_positions[n1]
            x2, y2 = node_positions[n2]
            thickness = max(2, cnt / max_count * 12)
            color = pair_color_map.get(pair, "#9E9E9E")
            ax.annotate(
                "",
                xy=(x2, y2),
                xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-", color=color, lw=thickness, alpha=0.7),
                zorder=2,
            )
            if n1 == n2:
                mx, my = x1, y1 + 0.08
            else:
                mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(
                mx,
                my,
                str(cnt),
                ha="center",
                va="center",
                fontsize=9,
                fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.8),
                zorder=5,
            )

        legend_patches = []
        for pair, color in pair_color_map.items():
            if pair in edge_pair_counts:
                label = pair_label_map.get(pair, f"{pair[0]}-{pair[1]}")
                patch = mpatches.Patch(color=color, label=label)
                legend_patches.append(patch)

        ax.legend(
            handles=legend_patches,
            loc="lower right",
            fontsize=7,
            title="Interaction Types",
        )

        ax.set_title(
            "Method 1: Reputation vs Network Centrality\nNodes=Users, Edges=Answer | Color: Reputation Level",
            fontsize=13,
            fontweight="bold",
            pad=15,
        )

        output_path = self.plotter.output_dir / "analysis_1_network.png"
        plt.tight_layout()
        output_path.unlink(missing_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches="tight")
        plt.close()
        print(f"  Saved aggregated reputation network: {output_path}")

    def _plot_time_series_network_aggregated(self, graph, result):
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches

        activity_levels = {
            "high": (0.5, 0.8),
            "medium": (0.8, 0.4),
            "low": (0.2, 0.4),
        }
        level_colors = {
            "high": "#2196F3",
            "medium": "#4CAF50",
            "low": "#9E9E9E",
        }

        level_counts = {lv: 0 for lv in activity_levels}
        node_level_map = {}
        for i, v in enumerate(graph.vs):
            level = v["activity_level"] if "activity_level" in v.attributes() else "low"
            if level not in level_counts:
                level = "low"
            level_counts[level] += 1
            node_level_map[i] = level

        edge_pair_counts = {}
        for e in graph.es:
            src_lv = node_level_map[e.source]
            tgt_lv = node_level_map[e.target]
            pair = tuple(sorted([src_lv, tgt_lv]))
            edge_pair_counts[pair] = edge_pair_counts.get(pair, 0) + 1

        fig, ax = plt.subplots(figsize=(10, 8))
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")

        for level, count in level_counts.items():
            if count == 0:
                continue
            x, y = activity_levels[level]
            size = max(500, count * 3)
            ax.scatter(
                x,
                y,
                s=size,
                c=level_colors[level],
                zorder=3,
                edgecolors="black",
                linewidths=1.5,
            )
            ax.text(
                x,
                y,
                f"{level.capitalize()}\n({count})",
                ha="center",
                va="center",
                fontsize=10,
                fontweight="bold",
                zorder=4,
            )

        max_count = max(edge_pair_counts.values()) if edge_pair_counts else 1

        for pair, cnt in edge_pair_counts.items():
            n1, n2 = pair
            if n1 not in activity_levels or n2 not in activity_levels:
                continue
            x1, y1 = activity_levels[n1]
            x2, y2 = activity_levels[n2]
            thickness = max(2, cnt / max_count * 12)
            color = level_colors.get(n1, "#9E9E9E")
            ax.annotate(
                "",
                xy=(x2, y2),
                xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-", color=color, lw=thickness, alpha=0.7),
                zorder=2,
            )
            if n1 == n2:
                mx, my = x1, y1 + 0.08
            else:
                mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(
                mx,
                my,
                str(cnt),
                ha="center",
                va="center",
                fontsize=9,
                fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.8),
                zorder=5,
            )

        legend_patches = []
        for level, color in level_colors.items():
            if level_counts.get(level, 0) > 0:
                legend_patches.append(
                    mpatches.Patch(color=color, label=level.capitalize())
                )

        ax.legend(
            handles=legend_patches,
            loc="lower right",
            fontsize=7,
            title="Activity Level",
        )
        ax.set_title(
            "Method 15: Time Series Activity Network\nNodes=Months (grouped by activity), Edges=Activity Flow | Color: Activity Level",
            fontsize=13,
            fontweight="bold",
            pad=15,
        )

        output_path = self.plotter.output_dir / "analysis_15_network.png"
        plt.tight_layout()
        output_path.unlink(missing_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches="tight")
        plt.close()
        print(f"  Saved aggregated time series network: {output_path}")

    def _plot_core_efficiency_network_aggregated(self, graph, result):
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches

        node_positions = {
            "1_VeryFast": (0.5, 0.88),
            "2_Fast": (0.82, 0.55),
            "3_Slow": (0.18, 0.55),
            "4_VerySlow": (0.5, 0.22),
            "0_Unresolved": (0.2, 0.22),
        }
        node_colors = {
            "1_VeryFast": "#4CAF50",
            "2_Fast": "#FFD700",
            "3_Slow": "#FFCDD2",
            "4_VerySlow": "#F44336",
            "0_Unresolved": "#9E9E9E",
        }
        node_labels_map = {
            "1_VeryFast": "VeryFast\n(<1h)",
            "2_Fast": "Fast\n(1~12h)",
            "3_Slow": "Slow\n(12~24h)",
            "4_VerySlow": "VerySlow\n(>24h)",
            "0_Unresolved": "Unresolved",
        }

        answer_time_levels = list(node_positions.keys())
        level_counts = {lv: 0 for lv in answer_time_levels}
        node_level_map = {}
        for i, v in enumerate(graph.vs):
            level = (
                v["answer_time_level"]
                if "answer_time_level" in v.attributes()
                else "0_Unresolved"
            )
            if level not in level_counts:
                level = "0_Unresolved"
            level_counts[level] += 1
            node_level_map[i] = level

        edge_pair_counts = {}
        for e in graph.es:
            src_lv = node_level_map[e.source]
            tgt_lv = node_level_map[e.target]
            pair = tuple(sorted([src_lv, tgt_lv]))
            edge_pair_counts[pair] = edge_pair_counts.get(pair, 0) + 1

        fig, ax = plt.subplots(figsize=(10, 8))
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")

        for level, count in level_counts.items():
            if count == 0:
                continue
            x, y = node_positions[level]
            size = max(500, count * 3)
            ax.scatter(
                x,
                y,
                s=size,
                c=node_colors[level],
                zorder=3,
                edgecolors="black",
                linewidths=1.5,
            )
            ax.text(
                x,
                y,
                f"{node_labels_map[level]}\n({count})",
                ha="center",
                va="center",
                fontsize=10,
                fontweight="bold",
                zorder=4,
            )

        pair_color_map = {}
        for i, lv1 in enumerate(answer_time_levels):
            for j, lv2 in enumerate(answer_time_levels):
                if j >= i:
                    pair_color_map[tuple(sorted([lv1, lv2]))] = node_colors.get(
                        lv1, "#9E9E9E"
                    )

        max_count = max(edge_pair_counts.values()) if edge_pair_counts else 1

        for pair, cnt in edge_pair_counts.items():
            n1, n2 = pair
            if n1 not in node_positions or n2 not in node_positions:
                continue
            x1, y1 = node_positions[n1]
            x2, y2 = node_positions[n2]
            thickness = max(2, cnt / max_count * 12)
            color = pair_color_map.get(pair, "#9E9E9E")
            ax.annotate(
                "",
                xy=(x2, y2),
                xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-", color=color, lw=thickness, alpha=0.7),
                zorder=2,
            )
            if n1 == n2:
                mx, my = x1, y1 + 0.08
            else:
                mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(
                mx,
                my,
                str(cnt),
                ha="center",
                va="center",
                fontsize=9,
                fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.8),
                zorder=5,
            )

        legend_patches = []
        for level, color in node_colors.items():
            if level_counts.get(level, 0) > 0:
                legend_patches.append(
                    mpatches.Patch(color=color, label=node_labels_map.get(level, level))
                )

        ax.legend(
            handles=legend_patches,
            loc="lower right",
            fontsize=7,
            title="Answer Time Levels",
        )
        ax.set_title(
            "Method 2: Core-Periphery vs Answer Efficiency\nNodes=Users (grouped by answer time), Edges=Interaction | Color: Answer Time",
            fontsize=13,
            fontweight="bold",
            pad=15,
        )

        output_path = self.plotter.output_dir / "analysis_2_network.png"
        plt.tight_layout()
        output_path.unlink(missing_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches="tight")
        plt.close()
        print(f"  Saved aggregated core-efficiency network: {output_path}")

    def _plot_connected_components_network_aggregated(self, graph, result):
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches

        components = result.get("components", [])
        summary = result.get("summary", {})

        main_size = summary.get("main_component_size", 0)
        island_count = summary.get("island_count", 0)
        island_user_count = summary.get("island_user_count", 0)
        total_components = summary.get("total_components", 0)

        node_positions = {
            "Main\nComponent": (0.5, 0.7),
            "Small\nIslands\n(2-5 users)": (0.2, 0.35),
            "Tiny\nIslands\n(1 user)": (0.8, 0.35),
        }
        node_colors = {
            "Main\nComponent": "#1565C0",
            "Small\nIslands\n(2-5 users)": "#FF9800",
            "Tiny\nIslands\n(1 user)": "#9E9E9E",
        }

        main_count = main_size
        small_islands = sum(
            1 for c in components if 2 <= c.size <= 5 and not c.is_main_component
        )
        tiny_islands = sum(1 for c in components if c.size == 1)

        counts = {
            "Main\nComponent": main_count,
            "Small\nIslands\n(2-5 users)": small_islands,
            "Tiny\nIslands\n(1 user)": tiny_islands,
        }

        edge_pair_counts = {}
        node_component_map = {}
        idx = 0
        for c in components:
            if c.is_main_component:
                comp_label = "Main\nComponent"
            elif c.size == 1:
                comp_label = "Tiny\nIslands\n(1 user)"
            else:
                comp_label = "Small\nIslands\n(2-5 users)"
            for uid in c.user_ids:
                node_component_map[idx] = comp_label
                idx += 1

        for e in graph.es:
            src_comp = node_component_map.get(e.source, "Main\nComponent")
            tgt_comp = node_component_map.get(e.target, "Main\nComponent")
            pair = tuple(sorted([src_comp, tgt_comp]))
            edge_pair_counts[pair] = edge_pair_counts.get(pair, 0) + 1

        fig, ax = plt.subplots(figsize=(10, 8))
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")

        for comp_label, count in counts.items():
            if count == 0:
                continue
            x, y = node_positions[comp_label]
            size = max(500, count * 2)
            ax.scatter(
                x,
                y,
                s=size,
                c=node_colors[comp_label],
                zorder=3,
                edgecolors="black",
                linewidths=1.5,
            )
            ax.text(
                x,
                y,
                f"{comp_label}\n({count})",
                ha="center",
                va="center",
                fontsize=10,
                fontweight="bold",
                zorder=4,
            )

        max_count = max(edge_pair_counts.values()) if edge_pair_counts else 1

        for pair, cnt in edge_pair_counts.items():
            n1, n2 = pair
            if n1 not in node_positions or n2 not in node_positions:
                continue
            x1, y1 = node_positions[n1]
            x2, y2 = node_positions[n2]
            thickness = max(2, cnt / max_count * 12)
            color = node_colors.get(n1, "#9E9E9E")
            ax.annotate(
                "",
                xy=(x2, y2),
                xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-", color=color, lw=thickness, alpha=0.7),
                zorder=2,
            )
            if n1 == n2:
                mx, my = x1, y1 + 0.08
            else:
                mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(
                mx,
                my,
                str(cnt),
                ha="center",
                va="center",
                fontsize=9,
                fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.8),
                zorder=5,
            )

        legend_patches = []
        for comp_label, color in node_colors.items():
            if counts.get(comp_label, 0) > 0:
                legend_patches.append(
                    mpatches.Patch(color=color, label=comp_label.replace("\n", " "))
                )

        ax.legend(
            handles=legend_patches,
            loc="lower right",
            fontsize=7,
            title="Component Types",
        )
        ax.set_title(
            f"Method 4: Knowledge Islands & Connected Components\nTotal: {total_components} components, {island_count} islands ({island_user_count} users)",
            fontsize=13,
            fontweight="bold",
            pad=15,
        )

        output_path = self.plotter.output_dir / "analysis_4_network.png"
        plt.tight_layout()
        output_path.unlink(missing_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches="tight")
        plt.close()
        print(f"  Saved aggregated connected components network: {output_path}")

    def _plot_account_age_network_aggregated(self, graph, result):
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches

        node_positions = {
            "1_New": (0.5, 0.88),
            "2_Young": (0.82, 0.65),
            "3_Mature": (0.18, 0.65),
            "4_Established": (0.82, 0.35),
            "5_Senior": (0.18, 0.35),
        }
        node_colors = {
            "1_New": "#4CAF50",
            "2_Young": "#FFD700",
            "3_Mature": "#FF9800",
            "4_Established": "#F44336",
            "5_Senior": "#9C27B0",
        }
        node_labels_map = {
            "1_New": "New\n(<1yr)",
            "2_Young": "Young\n(1~3yr)",
            "3_Mature": "Mature\n(3~6yr)",
            "4_Established": "Estab.\n(6~10yr)",
            "5_Senior": "Senior\n(>10yr)",
        }

        age_levels = list(node_positions.keys())
        level_counts = {lv: 0 for lv in age_levels}
        node_level_map = {}
        for i, v in enumerate(graph.vs):
            level = (
                v["account_age_level"]
                if "account_age_level" in v.attributes()
                else "1_New"
            )
            if level not in level_counts:
                level = "1_New"
            level_counts[level] += 1
            node_level_map[i] = level

        post_type_counts = {"1_Both": 0, "2_QuestionsOnly": 0, "3_AnswersOnly": 0}
        if "post_type" in graph.vs.attribute_names():
            for v in graph.vs:
                pt = v["post_type"]
                if pt in post_type_counts:
                    post_type_counts[pt] += 1

        edge_pair_counts = {}
        for e in graph.es:
            src_lv = node_level_map[e.source]
            tgt_lv = node_level_map[e.target]
            pair = tuple(sorted([src_lv, tgt_lv]))
            edge_pair_counts[pair] = edge_pair_counts.get(pair, 0) + 1

        fig, ax = plt.subplots(figsize=(10, 8))
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")

        for level, count in level_counts.items():
            if count == 0:
                continue
            x, y = node_positions[level]
            size = max(500, count * 3)
            ax.scatter(
                x,
                y,
                s=size,
                c=node_colors[level],
                zorder=3,
                edgecolors="black",
                linewidths=1.5,
            )
            ax.text(
                x,
                y,
                f"{node_labels_map[level]}\n({count})",
                ha="center",
                va="center",
                fontsize=10,
                fontweight="bold",
                zorder=4,
            )

        max_count = max(edge_pair_counts.values()) if edge_pair_counts else 1

        for pair, cnt in edge_pair_counts.items():
            n1, n2 = pair
            if n1 not in node_positions or n2 not in node_positions:
                continue
            x1, y1 = node_positions[n1]
            x2, y2 = node_positions[n2]
            thickness = max(2, cnt / max_count * 12)
            color = node_colors.get(n1, "#9E9E9E")
            ax.annotate(
                "",
                xy=(x2, y2),
                xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-", color=color, lw=thickness, alpha=0.7),
                zorder=2,
            )
            if n1 == n2:
                mx, my = x1, y1 + 0.08
            else:
                mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(
                mx,
                my,
                str(cnt),
                ha="center",
                va="center",
                fontsize=9,
                fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.8),
                zorder=5,
            )

        legend_patches = []
        for level, color in node_colors.items():
            if level_counts.get(level, 0) > 0:
                legend_patches.append(
                    mpatches.Patch(color=color, label=node_labels_map.get(level, level))
                )

        ax.legend(
            handles=legend_patches,
            loc="lower right",
            fontsize=7,
            title="Account Age Levels",
        )
        ax.set_title(
            "Method 6: Account Age vs Community Contribution\nNodes=Users (grouped by age), Edges=Interaction | Color: Age Level",
            fontsize=13,
            fontweight="bold",
            pad=15,
        )

        output_path = self.plotter.output_dir / "analysis_6_network.png"
        plt.tight_layout()
        output_path.unlink(missing_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches="tight")
        plt.close()
        print(f"  Saved aggregated account age network: {output_path}")

    def _plot_tag_cooccurrence_network_aggregated(self, graph, result):
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches

        domain_positions = {
            "Web": (0.5, 0.9),
            "Backend": (0.85, 0.55),
            "Database": (0.15, 0.55),
            "AI_ML": (0.2, 0.2),
            "DevOps": (0.8, 0.2),
            "DataScience": (0.5, 0.5),
            "Other": (0.5, 0.1),
        }
        domain_colors = {
            "Web": "#42A5F5",
            "Backend": "#8E24AA",
            "Database": "#FFB300",
            "AI_ML": "#FB8C00",
            "DevOps": "#43A047",
            "DataScience": "#5E35B1",
            "Other": "#9E9E9E",
        }

        domain_counts = {domain: 0 for domain in domain_positions}
        node_domain_map = {}
        attrs = graph.vs.attribute_names()
        for i, v in enumerate(graph.vs):
            domain = v["tech_domain"] if "tech_domain" in attrs else "Other"
            if domain not in domain_counts:
                domain = "Other"
            domain_counts[domain] += 1
            node_domain_map[i] = domain

        edge_pair_counts = {}
        for e in graph.es:
            src_domain = node_domain_map[e.source]
            tgt_domain = node_domain_map[e.target]
            pair = tuple(sorted([src_domain, tgt_domain]))
            edge_pair_counts[pair] = edge_pair_counts.get(pair, 0) + 1

        fig, ax = plt.subplots(figsize=(10, 8))
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")

        for domain, count in domain_counts.items():
            if count == 0:
                continue
            x, y = domain_positions[domain]
            size = max(500, count * 3)
            ax.scatter(
                x,
                y,
                s=size,
                c=domain_colors[domain],
                zorder=3,
                edgecolors="black",
                linewidths=1.5,
            )
            ax.text(
                x,
                y,
                f"{domain}\n({count})",
                ha="center",
                va="center",
                fontsize=10,
                fontweight="bold",
                zorder=4,
            )

        max_count = max(edge_pair_counts.values()) if edge_pair_counts else 1
        for pair, cnt in edge_pair_counts.items():
            n1, n2 = pair
            if n1 not in domain_positions or n2 not in domain_positions:
                continue
            x1, y1 = domain_positions[n1]
            x2, y2 = domain_positions[n2]
            thickness = max(2, cnt / max_count * 12)
            color = domain_colors.get(n1, "#9E9E9E")
            ax.annotate(
                "",
                xy=(x2, y2),
                xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-", color=color, lw=thickness, alpha=0.7),
                zorder=2,
            )
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(
                mx,
                my,
                str(cnt),
                ha="center",
                va="center",
                fontsize=9,
                fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.8),
                zorder=5,
            )

        legend_patches = []
        for domain, color in domain_colors.items():
            if domain_counts.get(domain, 0) > 0:
                legend_patches.append(mpatches.Patch(color=color, label=domain))

        ax.legend(
            handles=legend_patches,
            loc="lower right",
            fontsize=8,
            title="Technology Domains",
        )
        ax.set_title(
            "Method 3: Tag Co-occurrence Technology Map\nNodes=Tags (grouped by domain), Edges=Co-occurrence",
            fontsize=13,
            fontweight="bold",
            pad=15,
        )

        output_path = self.plotter.output_dir / "analysis_3_network.png"
        plt.tight_layout()
        output_path.unlink(missing_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches="tight")
        plt.close()
        print(f"  Saved aggregated tag co-occurrence network: {output_path}")

    def _plot_content_features_network_aggregated(self, graph, result):
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches

        positions = {
            "HasCode": (0.25, 0.55),
            "NoCode": (0.75, 0.55),
        }
        colors = {
            "HasCode": "#42A5F5",
            "NoCode": "#FFB300",
        }

        counts = {"HasCode": 0, "NoCode": 0}
        node_map = {}
        attrs = graph.vs.attribute_names()
        for i, v in enumerate(graph.vs):
            has_code = v["has_code"] if "has_code" in attrs else "no"
            group = "HasCode" if str(has_code).lower() in ("yes", "true", "1") else "NoCode"
            counts[group] += 1
            node_map[i] = group

        edge_pair_counts = {}
        for e in graph.es:
            src = node_map[e.source]
            tgt = node_map[e.target]
            pair = tuple(sorted([src, tgt]))
            edge_pair_counts[pair] = edge_pair_counts.get(pair, 0) + 1

        fig, ax = plt.subplots(figsize=(10, 8))
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")

        for group, count in counts.items():
            if count == 0:
                continue
            x, y = positions[group]
            size = max(500, count * 4)
            ax.scatter(
                x,
                y,
                s=size,
                c=colors[group],
                zorder=3,
                edgecolors="black",
                linewidths=1.5,
            )
            ax.text(
                x,
                y,
                f"{group}\n({count})",
                ha="center",
                va="center",
                fontsize=11,
                fontweight="bold",
                zorder=4,
            )

        max_count = max(edge_pair_counts.values()) if edge_pair_counts else 1
        for pair, cnt in edge_pair_counts.items():
            n1, n2 = pair
            x1, y1 = positions[n1]
            x2, y2 = positions[n2]
            thickness = max(2, cnt / max_count * 12)
            color = colors.get(n1, "#9E9E9E")
            ax.annotate(
                "",
                xy=(x2, y2),
                xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-", color=color, lw=thickness, alpha=0.7),
                zorder=2,
            )
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(
                mx,
                my,
                str(cnt),
                ha="center",
                va="center",
                fontsize=9,
                fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.8),
                zorder=5,
            )

        legend_patches = [mpatches.Patch(color=colors[g], label=g) for g in counts if counts[g] > 0]
        ax.legend(
            handles=legend_patches,
            loc="lower right",
            fontsize=8,
            title="Code Presence",
        )
        ax.set_title(
            "Method 5: Content Features & Code Presence\nNodes=Posts, Edges=Tag Similarity | Color: Code Present",
            fontsize=13,
            fontweight="bold",
            pad=15,
        )

        output_path = self.plotter.output_dir / "analysis_5_network.png"
        plt.tight_layout()
        output_path.unlink(missing_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches="tight")
        plt.close()
        print(f"  Saved aggregated content features network: {output_path}")

    def _plot_badge_network_aggregated(self, graph, result):
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches

        positions = {
            "0_None": (0.5, 0.15),
            "1_Gold": (0.5, 0.85),
            "2_Silver": (0.2, 0.45),
            "3_Bronze": (0.8, 0.45),
        }
        colors = {
            "0_None": "#9E9E9E",
            "1_Gold": "#FFD700",
            "2_Silver": "#C0C0C0",
            "3_Bronze": "#CD7F32",
        }

        counts = {level: 0 for level in positions}
        node_map = {}
        attrs = graph.vs.attribute_names()
        for i, v in enumerate(graph.vs):
            level = v["badge_level"] if "badge_level" in attrs else "0_None"
            if level not in counts:
                level = "0_None"
            counts[level] += 1
            node_map[i] = level

        edge_pair_counts = {}
        for e in graph.es:
            src = node_map[e.source]
            tgt = node_map[e.target]
            pair = tuple(sorted([src, tgt]))
            edge_pair_counts[pair] = edge_pair_counts.get(pair, 0) + 1

        fig, ax = plt.subplots(figsize=(10, 8))
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")

        for level, count in counts.items():
            if count == 0:
                continue
            x, y = positions[level]
            size = max(500, count * 3)
            ax.scatter(
                x,
                y,
                s=size,
                c=colors[level],
                zorder=3,
                edgecolors="black",
                linewidths=1.5,
            )
            ax.text(
                x,
                y,
                f"{level.replace('_', ' ')}\n({count})",
                ha="center",
                va="center",
                fontsize=10,
                fontweight="bold",
                zorder=4,
            )

        max_count = max(edge_pair_counts.values()) if edge_pair_counts else 1
        for pair, cnt in edge_pair_counts.items():
            n1, n2 = pair
            if n1 not in positions or n2 not in positions:
                continue
            x1, y1 = positions[n1]
            x2, y2 = positions[n2]
            thickness = max(2, cnt / max_count * 12)
            color = colors.get(n1, "#9E9E9E")
            ax.annotate(
                "",
                xy=(x2, y2),
                xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-", color=color, lw=thickness, alpha=0.7),
                zorder=2,
            )
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(
                mx,
                my,
                str(cnt),
                ha="center",
                va="center",
                fontsize=9,
                fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.8),
                zorder=5,
            )

        legend_patches = []
        for level, color in colors.items():
            if counts.get(level, 0) > 0:
                legend_patches.append(mpatches.Patch(color=color, label=level.replace('_', ' ')))

        ax.legend(
            handles=legend_patches,
            loc="lower right",
            fontsize=8,
            title="Badge Level",
        )
        ax.set_title(
            "Method 9: Badge Achievement Network\nNodes=Users (grouped by badge level), Edges=Shared Badges",
            fontsize=13,
            fontweight="bold",
            pad=15,
        )

        output_path = self.plotter.output_dir / "analysis_9_network.png"
        plt.tight_layout()
        output_path.unlink(missing_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches="tight")
        plt.close()
        print(f"  Saved aggregated badge network: {output_path}")

    def _plot_post_link_network_aggregated(self, graph, result):
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches

        link_positions = {
            "Linked": (0.3, 0.75),
            "Duplicate": (0.7, 0.75),
            "Other": (0.5, 0.25),
        }
        link_colors = {
            "Linked": "#2196F3",
            "Duplicate": "#F44336",
            "Other": "#9E9E9E",
        }

        type_counts = {t: 0 for t in link_positions}
        edge_types = graph.es["link_type"] if "link_type" in graph.es.attribute_names() else []
        for t in edge_types:
            typ = t if t in type_counts else "Other"
            type_counts[typ] += 1

        fig, ax = plt.subplots(figsize=(10, 8))
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")

        for typ, count in type_counts.items():
            if count == 0:
                continue
            x, y = link_positions[typ]
            size = max(500, count * 6)
            ax.scatter(
                x,
                y,
                s=size,
                c=link_colors[typ],
                zorder=3,
                edgecolors="black",
                linewidths=1.5,
            )
            ax.text(
                x,
                y,
                f"{typ}\n({count})",
                ha="center",
                va="center",
                fontsize=11,
                fontweight="bold",
                zorder=4,
            )

        legend_patches = [mpatches.Patch(color=link_colors[k], label=k) for k, v in type_counts.items() if v > 0]
        ax.legend(
            handles=legend_patches,
            loc="lower right",
            fontsize=8,
            title="Link Type",
        )
        ax.set_title(
            "Method 11: Post Link & Duplicate Network\nNodes=Posts, Edges=Linked/Duplicate Relationships",
            fontsize=13,
            fontweight="bold",
            pad=15,
        )

        output_path = self.plotter.output_dir / "analysis_11_network.png"
        plt.tight_layout()
        output_path.unlink(missing_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches="tight")
        plt.close()
        print(f"  Saved aggregated post link network: {output_path}")

    def _plot_bounty_network_aggregated(self, graph, result):
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches

        positions = {
            "0_None": (0.5, 0.1),
            "1_Meager": (0.2, 0.55),
            "2_Normal": (0.5, 0.85),
            "3_Generous": (0.8, 0.55),
            "4_Extravagant": (0.5, 0.35),
        }
        colors = {
            "0_None": "#9E9E9E",
            "1_Meager": "#42A5F5",
            "2_Normal": "#4CAF50",
            "3_Generous": "#FFC107",
            "4_Extravagant": "#F44336",
        }

        counts = {lvl: 0 for lvl in positions}
        node_map = {}
        attrs = graph.vs.attribute_names()
        for i, v in enumerate(graph.vs):
            lvl = v["bounty_level"] if "bounty_level" in attrs else "0_None"
            if lvl not in counts:
                lvl = "0_None"
            counts[lvl] += 1
            node_map[i] = lvl

        edge_pair_counts = {}
        for e in graph.es:
            src = node_map.get(e.source, "0_None")
            tgt = node_map.get(e.target, "0_None")
            pair = tuple(sorted([src, tgt]))
            edge_pair_counts[pair] = edge_pair_counts.get(pair, 0) + 1

        fig, ax = plt.subplots(figsize=(10, 8))
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")

        for lvl, count in counts.items():
            if count == 0:
                continue
            x, y = positions[lvl]
            size = max(500, count * 3)
            ax.scatter(
                x,
                y,
                s=size,
                c=colors[lvl],
                zorder=3,
                edgecolors="black",
                linewidths=1.5,
            )
            ax.text(
                x,
                y,
                f"{lvl.replace('_', ' ')}\n({count})",
                ha="center",
                va="center",
                fontsize=10,
                fontweight="bold",
                zorder=4,
            )

        max_count = max(edge_pair_counts.values()) if edge_pair_counts else 1
        for pair, cnt in edge_pair_counts.items():
            n1, n2 = pair
            if n1 not in positions or n2 not in positions:
                continue
            x1, y1 = positions[n1]
            x2, y2 = positions[n2]
            thickness = max(2, cnt / max_count * 12)
            color = colors.get(n1, "#9E9E9E")
            ax.annotate(
                "",
                xy=(x2, y2),
                xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-", color=color, lw=thickness, alpha=0.7),
                zorder=2,
            )
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(
                mx,
                my,
                str(cnt),
                ha="center",
                va="center",
                fontsize=9,
                fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.8),
                zorder=5,
            )

        legend_patches = []
        for lvl, color in colors.items():
            if counts.get(lvl, 0) > 0:
                legend_patches.append(mpatches.Patch(color=color, label=lvl.replace('_', ' ')))

        ax.legend(
            handles=legend_patches,
            loc="lower right",
            fontsize=8,
            title="Bounty Level",
        )
        ax.set_title(
            "Method 13: Bounty Network\nNodes=Users (grouped by bounty activity), Edges=Shared Tags",
            fontsize=13,
            fontweight="bold",
            pad=15,
        )

        output_path = self.plotter.output_dir / "analysis_13_network.png"
        plt.tight_layout()
        output_path.unlink(missing_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches="tight")
        plt.close()
        print(f"  Saved aggregated bounty network: {output_path}")

    def _plot_user_location_network_aggregated(self, graph, result):
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches

        region_positions = {
            "North America": (0.5, 0.85),
            "Europe": (0.2, 0.6),
            "Asia": (0.8, 0.6),
            "Oceania": (0.85, 0.25),
            "South America": (0.35, 0.25),
            "Africa": (0.65, 0.25),
            "Middle East": (0.5, 0.45),
            "Other": (0.5, 0.1),
        }
        region_colors = {
            "North America": "#2196F3",
            "Europe": "#4CAF50",
            "Asia": "#FFC107",
            "Oceania": "#9E9E9E",
            "South America": "#FF5722",
            "Africa": "#795548",
            "Middle East": "#607D8B",
            "Other": "#BDBDBD",
        }

        region_counts = {region: 0 for region in region_positions}
        attrs = graph.vs.attribute_names()
        for v in graph.vs:
            region = v["region"] if "region" in attrs else "Other"
            if region not in region_counts:
                region = "Other"
            region_counts[region] += 1

        fig, ax = plt.subplots(figsize=(10, 8))
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")

        for region, count in region_counts.items():
            if count == 0:
                continue
            x, y = region_positions[region]
            size = max(500, count * 3)
            ax.scatter(
                x,
                y,
                s=size,
                c=region_colors[region],
                zorder=3,
                edgecolors="black",
                linewidths=1.5,
            )
            ax.text(
                x,
                y,
                f"{region}\n({count})",
                ha="center",
                va="center",
                fontsize=9,
                fontweight="bold",
                zorder=4,
            )

        legend_patches = [mpatches.Patch(color=region_colors[r], label=r) for r, c in region_counts.items() if c > 0]
        ax.legend(
            handles=legend_patches,
            loc="lower right",
            fontsize=8,
            title="Region",
        )
        ax.set_title(
            "Method 14: User Location Network\nNodes=Regions, Edges=Regional Connections",
            fontsize=13,
            fontweight="bold",
            pad=15,
        )

        output_path = self.plotter.output_dir / "analysis_14_network.png"
        plt.tight_layout()
        output_path.unlink(missing_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches="tight")
        plt.close()
        print(f"  Saved aggregated user location network: {output_path}")

    def _plot_comment_network_aggregated(self, graph, result):
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches

        activity_levels = {
            "High\n(>50 comments)": (0.5, 0.8),
            "Medium\n(10~50)": (0.8, 0.45),
            "Low\n(2~9)": (0.2, 0.45),
            "Minimal\n(1)": (0.5, 0.15),
        }
        level_colors = {
            "High\n(>50 comments)": "#2196F3",
            "Medium\n(10~50)": "#4CAF50",
            "Low\n(2~9)": "#FF9800",
            "Minimal\n(1)": "#9E9E9E",
        }

        level_counts = {lv: 0 for lv in activity_levels}
        node_level_map = {}
        for i, v in enumerate(graph.vs):
            cc = v["comment_count"] if "comment_count" in v.attributes() else 0
            if cc > 50:
                lv = "High\n(>50 comments)"
            elif cc >= 10:
                lv = "Medium\n(10~50)"
            elif cc >= 2:
                lv = "Low\n(2~9)"
            else:
                lv = "Minimal\n(1)"
            level_counts[lv] += 1
            node_level_map[i] = lv

        edge_pair_counts = {}
        for e in graph.es:
            src_lv = node_level_map[e.source]
            tgt_lv = node_level_map[e.target]
            pair = tuple(sorted([src_lv, tgt_lv]))
            edge_pair_counts[pair] = edge_pair_counts.get(pair, 0) + 1

        fig, ax = plt.subplots(figsize=(10, 8))
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")

        for level, count in level_counts.items():
            if count == 0:
                continue
            x, y = activity_levels[level]
            size = max(500, count * 3)
            ax.scatter(
                x,
                y,
                s=size,
                c=level_colors[level],
                zorder=3,
                edgecolors="black",
                linewidths=1.5,
            )
            ax.text(
                x,
                y,
                f"{level}\n({count})",
                ha="center",
                va="center",
                fontsize=10,
                fontweight="bold",
                zorder=4,
            )

        max_count = max(edge_pair_counts.values()) if edge_pair_counts else 1

        for pair, cnt in edge_pair_counts.items():
            n1, n2 = pair
            if n1 not in activity_levels or n2 not in activity_levels:
                continue
            x1, y1 = activity_levels[n1]
            x2, y2 = activity_levels[n2]
            thickness = max(2, cnt / max_count * 12)
            color = level_colors.get(n1, "#9E9E9E")
            ax.annotate(
                "",
                xy=(x2, y2),
                xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-", color=color, lw=thickness, alpha=0.7),
                zorder=2,
            )
            if n1 == n2:
                mx, my = x1, y1 + 0.08
            else:
                mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(
                mx,
                my,
                str(cnt),
                ha="center",
                va="center",
                fontsize=9,
                fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.8),
                zorder=5,
            )

        legend_patches = []
        for level, color in level_colors.items():
            if level_counts.get(level, 0) > 0:
                legend_patches.append(
                    mpatches.Patch(color=color, label=level.replace("\n", " "))
                )

        ax.legend(
            handles=legend_patches,
            loc="lower right",
            fontsize=7,
            title="Comment Activity",
        )
        ax.set_title(
            "Method 8: Comment Interaction Network\nNodes=Users (grouped by activity), Edges=Comment Co-occurrence | Color: Activity Level",
            fontsize=13,
            fontweight="bold",
            pad=15,
        )

        output_path = self.plotter.output_dir / "analysis_8_network.png"
        plt.tight_layout()
        output_path.unlink(missing_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches="tight")
        plt.close()
        print(f"  Saved aggregated comment network: {output_path}")

    def _plot_voting_behavior_network_aggregated(self, graph, result):
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches

        node_positions = {
            "1_NoVotes": (0.5, 0.88),
            "2_Low": (0.82, 0.6),
            "3_Medium": (0.18, 0.6),
            "4_High": (0.5, 0.2),
        }
        node_colors = {
            "1_NoVotes": "#9E9E9E",
            "2_Low": "#4CAF50",
            "3_Medium": "#FFD700",
            "4_High": "#F44336",
        }
        node_labels_map = {
            "1_NoVotes": "NoVotes",
            "2_Low": "Low\n(1~3)",
            "3_Medium": "Medium\n(4~10)",
            "4_High": "High\n(>10)",
        }

        level_counts = {lv: 0 for lv in node_positions}
        node_level_map = {}
        attrs = graph.vs.attribute_names()
        for i, v in enumerate(graph.vs):
            level = v["vote_level"] if "vote_level" in attrs else "1_NoVotes"
            if level not in level_counts:
                level = "1_NoVotes"
            level_counts[level] += 1
            node_level_map[i] = level

        edge_pair_counts = {}
        for e in graph.es:
            src_lv = node_level_map[e.source]
            tgt_lv = node_level_map[e.target]
            pair = tuple(sorted([src_lv, tgt_lv]))
            edge_pair_counts[pair] = edge_pair_counts.get(pair, 0) + 1

        fig, ax = plt.subplots(figsize=(10, 8))
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")

        for level, count in level_counts.items():
            if count == 0:
                continue
            x, y = node_positions[level]
            size = max(500, count * 3)
            ax.scatter(
                x,
                y,
                s=size,
                c=node_colors[level],
                zorder=3,
                edgecolors="black",
                linewidths=1.5,
            )
            ax.text(
                x,
                y,
                f"{node_labels_map[level]}\n({count})",
                ha="center",
                va="center",
                fontsize=10,
                fontweight="bold",
                zorder=4,
            )

        max_count = max(edge_pair_counts.values()) if edge_pair_counts else 1

        for pair, cnt in edge_pair_counts.items():
            n1, n2 = pair
            if n1 not in node_positions or n2 not in node_positions:
                continue
            x1, y1 = node_positions[n1]
            x2, y2 = node_positions[n2]
            thickness = max(2, cnt / max_count * 12)
            color = node_colors.get(n1, "#9E9E9E")
            ax.annotate(
                "",
                xy=(x2, y2),
                xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-", color=color, lw=thickness, alpha=0.7),
                zorder=2,
            )
            if n1 == n2:
                mx, my = x1, y1 + 0.08
            else:
                mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(
                mx,
                my,
                str(cnt),
                ha="center",
                va="center",
                fontsize=9,
                fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.8),
                zorder=5,
            )

        legend_patches = []
        for level, color in node_colors.items():
            if level_counts.get(level, 0) > 0:
                legend_patches.append(
                    mpatches.Patch(color=color, label=node_labels_map.get(level, level))
                )

        ax.legend(
            handles=legend_patches,
            loc="lower right",
            fontsize=7,
            title="Vote Level",
        )
        ax.set_title(
            "Method 7: Voting Behavior Network\nNodes=Users (grouped by vote count), Edges=Co-vote | Color: Vote Level",
            fontsize=13,
            fontweight="bold",
            pad=15,
        )

        output_path = self.plotter.output_dir / "analysis_7_network.png"
        plt.tight_layout()
        output_path.unlink(missing_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches="tight")
        plt.close()
        print(f"  Saved aggregated voting behavior network: {output_path}")

    def _plot_edit_collaboration_network_aggregated(self, graph, result):
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches

        node_positions = {
            "3_Power": (0.5, 0.8),
            "2_Active": (0.8, 0.45),
            "1_Casual": (0.2, 0.45),
            "0_None": (0.5, 0.15),
        }
        node_colors = {
            "3_Power": "#F44336",
            "2_Active": "#FF9800",
            "1_Casual": "#4CAF50",
            "0_None": "#BDBDBD",
        }
        node_labels_map = {
            "3_Power": "Power\n(>5 edits)",
            "2_Active": "Active\n(3~5)",
            "1_Casual": "Casual\n(1~2)",
            "0_None": "None",
        }

        level_counts = {lv: 0 for lv in node_positions}
        node_level_map = {}
        for i, v in enumerate(graph.vs):
            level = v["editor_level"] if "editor_level" in v.attributes() else "0_None"
            if level not in level_counts:
                level = "0_None"
            level_counts[level] += 1
            node_level_map[i] = level

        edge_pair_counts = {}
        for e in graph.es:
            src_lv = node_level_map[e.source]
            tgt_lv = node_level_map[e.target]
            pair = tuple(sorted([src_lv, tgt_lv]))
            edge_pair_counts[pair] = edge_pair_counts.get(pair, 0) + 1

        fig, ax = plt.subplots(figsize=(10, 8))
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")

        for level, count in level_counts.items():
            if count == 0:
                continue
            x, y = node_positions[level]
            size = max(500, count * 3)
            ax.scatter(
                x,
                y,
                s=size,
                c=node_colors[level],
                zorder=3,
                edgecolors="black",
                linewidths=1.5,
            )
            ax.text(
                x,
                y,
                f"{node_labels_map[level]}\n({count})",
                ha="center",
                va="center",
                fontsize=10,
                fontweight="bold",
                zorder=4,
            )

        max_count = max(edge_pair_counts.values()) if edge_pair_counts else 1

        for pair, cnt in edge_pair_counts.items():
            n1, n2 = pair
            if n1 not in node_positions or n2 not in node_positions:
                continue
            x1, y1 = node_positions[n1]
            x2, y2 = node_positions[n2]
            thickness = max(2, cnt / max_count * 12)
            color = node_colors.get(n1, "#9E9E9E")

            if n1 == n2:
                # do not draw self-loop lines for same-level aggregation
                mx, my = x1, y1 - 0.12
                ax.text(
                    mx,
                    my,
                    str(cnt),
                    ha="center",
                    va="center",
                    fontsize=9,
                    fontweight="bold",
                    bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.8),
                    zorder=5,
                )
                continue

            ax.annotate(
                "",
                xy=(x2, y2),
                xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-", color=color, lw=thickness, alpha=0.7),
                zorder=2,
            )
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(
                mx,
                my,
                str(cnt),
                ha="center",
                va="center",
                fontsize=9,
                fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.8),
                zorder=5,
            )

        legend_patches = []
        for level, color in node_colors.items():
            if level_counts.get(level, 0) > 0:
                legend_patches.append(
                    mpatches.Patch(color=color, label=node_labels_map.get(level, level))
                )

        ax.legend(
            handles=legend_patches, loc="lower right", fontsize=7, title="Editor Level"
        )
        ax.set_title(
            "Method 10: Edit Collaboration Network\nNodes=Users (grouped by edits), Edges=Co-edit | Color: Editor Level",
            fontsize=13,
            fontweight="bold",
            pad=15,
        )

        output_path = self.plotter.output_dir / "analysis_10_network.png"
        plt.tight_layout()
        output_path.unlink(missing_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches="tight")
        plt.close()
        print(f"  Saved aggregated edit collaboration network: {output_path}")

    def _plot_review_task_network_aggregated(self, graph, result):
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches

        node_positions = {
            "3_Power": (0.5, 0.8),
            "2_Active": (0.8, 0.45),
            "1_Casual": (0.2, 0.45),
            "0_None": (0.5, 0.15),
        }
        node_colors = {
            "3_Power": "#F44336",
            "2_Active": "#FF9800",
            "1_Casual": "#4CAF50",
            "0_None": "#BDBDBD",
        }
        node_labels_map = {
            "3_Power": "Power\n(>10)",
            "2_Active": "Active\n(3~10)",
            "1_Casual": "Casual\n(1~2)",
            "0_None": "None",
        }

        level_counts = {lv: 0 for lv in node_positions}
        node_level_map = {}
        for i, v in enumerate(graph.vs):
            level = (
                v["reviewer_level"] if "reviewer_level" in v.attributes() else "0_None"
            )
            if level not in level_counts:
                level = "0_None"
            level_counts[level] += 1
            node_level_map[i] = level

        edge_pair_counts = {}
        for e in graph.es:
            src_lv = node_level_map[e.source]
            tgt_lv = node_level_map[e.target]
            pair = tuple(sorted([src_lv, tgt_lv]))
            edge_pair_counts[pair] = edge_pair_counts.get(pair, 0) + 1

        fig, ax = plt.subplots(figsize=(10, 8))
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")

        for level, count in level_counts.items():
            if count == 0:
                continue
            x, y = node_positions[level]
            size = max(500, count * 3)
            ax.scatter(
                x,
                y,
                s=size,
                c=node_colors[level],
                zorder=3,
                edgecolors="black",
                linewidths=1.5,
            )
            ax.text(
                x,
                y,
                f"{node_labels_map[level]}\n({count})",
                ha="center",
                va="center",
                fontsize=10,
                fontweight="bold",
                zorder=4,
            )

        max_count = max(edge_pair_counts.values()) if edge_pair_counts else 1

        for pair, cnt in edge_pair_counts.items():
            n1, n2 = pair
            if n1 not in node_positions or n2 not in node_positions:
                continue
            x1, y1 = node_positions[n1]
            x2, y2 = node_positions[n2]
            thickness = max(2, cnt / max_count * 12)
            color = node_colors.get(n1, "#9E9E9E")
            ax.annotate(
                "",
                xy=(x2, y2),
                xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-", color=color, lw=thickness, alpha=0.7),
                zorder=2,
            )
            if n1 == n2:
                mx, my = x1, y1 + 0.08
            else:
                mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(
                mx,
                my,
                str(cnt),
                ha="center",
                va="center",
                fontsize=9,
                fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.8),
                zorder=5,
            )

        legend_patches = []
        for level, color in node_colors.items():
            if level_counts.get(level, 0) > 0:
                legend_patches.append(
                    mpatches.Patch(color=color, label=node_labels_map.get(level, level))
                )

        ax.legend(
            handles=legend_patches,
            loc="lower right",
            fontsize=7,
            title="Reviewer Level",
        )
        ax.set_title(
            "Method 12: Review Task Network\nNodes=Users (grouped by reviews), Edges=Co-review | Color: Reviewer Level",
            fontsize=13,
            fontweight="bold",
            pad=15,
        )

        output_path = self.plotter.output_dir / "analysis_12_network.png"
        plt.tight_layout()
        output_path.unlink(missing_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches="tight")
        plt.close()
        print(f"  Saved aggregated review task network: {output_path}")

    def _make_serializable(self, obj):
        """Recursively convert numpy types to Python native types"""
        if isinstance(obj, dict):
            return {str(k): self._make_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [self._make_serializable(item) for item in obj]
        elif hasattr(obj, "item"):
            return obj.item()
        elif isinstance(obj, (pd.Timestamp, pd.Timedelta)):
            return str(obj)
        else:
            return obj

    def _save_results(self):
        """儲存分析結果"""
        print("\n" + "=" * 60)
        print("儲存分析結果")
        print("=" * 60)

        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)

        serializable_results = {}
        for name, result in self.results.items():
            serializable_results[name] = {}
            for key, value in result.items():
                if key == "graph":
                    serializable_results[name][key] = {
                        "nodes": len(value.vs) if value else 0,
                        "edges": len(value.es) if value else 0,
                    }
                elif key == "summary":
                    serializable_results[name][key] = self._make_serializable(value)
                elif key == "posts_df":
                    if hasattr(value, "to_dict"):
                        df = value.copy()
                        for col in df.columns:
                            if df[col].dtype.name == "datetime64[ns, UTC]":
                                df[col] = df[col].astype(str)
                        serializable_results[name][key] = df.to_dict(orient="records")[
                            :10
                        ]
                    else:
                        serializable_results[name][key] = {}
                elif key == "analysis_df":
                    if hasattr(value, "to_dict"):
                        df = value.copy()
                        for col in df.columns:
                            if df[col].dtype.name == "datetime64[ns, UTC]":
                                df[col] = df[col].astype(str)
                        serializable_results[name][key] = df.to_dict(orient="records")[
                            :10
                        ]
                    else:
                        serializable_results[name][key] = {}
                elif key == "age_df":
                    if hasattr(value, "to_dict"):
                        df = value.copy()
                        for col in df.columns:
                            if df[col].dtype.name == "datetime64[ns, UTC]":
                                df[col] = df[col].astype(str)
                        serializable_results[name][key] = df.to_dict(orient="records")[
                            :10
                        ]
                    else:
                        serializable_results[name][key] = {}
                elif key == "connectivity_df":
                    if hasattr(value, "to_dict"):
                        df = value.copy()
                        for col in df.columns:
                            if df[col].dtype.name == "datetime64[ns, UTC]":
                                df[col] = df[col].astype(str)
                        serializable_results[name][key] = df.to_dict(orient="records")[
                            :10
                        ]
                    else:
                        serializable_results[name][key] = {}
                elif key == "tag_df":
                    if hasattr(value, "to_dict"):
                        df = value.copy()
                        for col in df.columns:
                            if df[col].dtype.name == "datetime64[ns, UTC]":
                                df[col] = df[col].astype(str)
                        serializable_results[name][key] = df.to_dict(orient="records")[
                            :10
                        ]
                    else:
                        serializable_results[name][key] = {}
                elif key in (
                    "votes_df",
                    "comments_df",
                    "badges_df",
                    "edits_df",
                    "links_df",
                    "reviews_df",
                    "bounties_df",
                    "users_df",
                ):
                    if hasattr(value, "to_dict"):
                        df = value.copy()
                        for col in df.columns:
                            if df[col].dtype.name == "datetime64[ns, UTC]":
                                df[col] = df[col].astype(str)
                        serializable_results[name][key] = df.to_dict(orient="records")[
                            :10
                        ]
                    else:
                        serializable_results[name][key] = {}
                elif key == "centrality_metrics":
                    serializable_results[name][key] = (
                        value.to_dict() if hasattr(value, "to_dict") else {}
                    )
                elif key == "metrics":
                    serializable_results[name][key] = (
                        value.to_dict() if hasattr(value, "to_dict") else {}
                    )
                else:
                    try:
                        json.dumps(value)
                        serializable_results[name][key] = value
                    except:
                        serializable_results[name][key] = str(value)

        save_json(serializable_results, output_dir / "analysis_results.json")

        print("\n" + "=" * 60)
        print("分析完成！")
        print("=" * 60)

        generate_summary_report(self.results)


def main():
    """主函數"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Stack Overflow Social Network Analysis"
    )
    parser.add_argument(
        "--limit", type=int, default=100, help="Number of records to analyze"
    )
    parser.add_argument("--output", type=str, default="output", help="Output directory")

    args = parser.parse_args()

    runner = SNARunner(output_dir=args.output, data_limit=args.limit)
    runner.run_all()


if __name__ == "__main__":
    main()
