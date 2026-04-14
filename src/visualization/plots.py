"""
社會網路分析視覺化工具
===============================
根據研究方法規格設計：
- 不同聲望/特徵使用不同顏色
- 不同類別使用不同形狀
"""

from pathlib import Path
from typing import Dict, Any, List, Optional

import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("Agg")
import matplotlib.patches as mpatches

import igraph as ig

from ..config import OUTPUT_DIR


COLOR_MAPS = {
    "reputation": {
        "0_None": "#90CAF9",
        "1_Low": "#4CAF50",  # 綠色 - 新手 (<1,000)
        "2_Medium-Low": "#FFD700",  # 黃色 - 中階 (1,000~10,000)
        "3_Medium-High": "#FF9800",  # 橘色 - 資深 (10,000~50,000)
        "4_High": "#F44336",  # 紅色 - 大神 (>50,000)
    },
    "answer_time": {
        "1_VeryFast": "#4CAF50",  # 綠色 - <1小時
        "2_Fast": "#FFD700",  # 黃色 - 1~12小時
        "3_Slow": "#FFCDD2",  # 淺紅色 - 12~24小時
        "4_VerySlow": "#F44336",  # 紅色 - >24小時
        "0_Unresolved": "#9E9E9E",  # 灰色 - 未解決
    },
    "tech_domain": {
        "Web": "#42A5F5",  # Web技術
        "AI_ML": "#FB8C00",  # AI/ML
        "Mobile": "#A5D6A7",  # 行動開發
        "DataScience": "#5E35B1",  # 資料科學
        "Backend": "#8E24AA",  # 後端
        "Database": "#FFB300",  # 資料庫
        "DevOps": "#43A047",  # DevOps
        "Other": "#9E9E9E",  # 其他
    },
    "connectivity": {
        "main_component": "#1565C0",  # 深藍色 - 主連通分量
        "isolated": "#9E9E9E",  # 灰色 - 孤立組件
    },
    "code_presence": {
        "has_code": "#42A5F5",  # 藍色 - 有程式碼
        "no_code": "#FFA726",  # 橙色 - 純文字
    },
    "score_level": {
        "1_VeryNegative": "#9E9E9E",
        "2_Negative": "#B0BEC5",
        "3_Neutral": "#BDBDBD",
        "4_Positive": "#66BB6A",  # 綠色
        "5_VeryPositive": "#FFD54F",  # 黃色
        "6_ExtremelyPositive": "#FF7043",  # 橘色/紅色
    },
    "account_age": {
        "1_New": "#4CAF50",  # 綠色 - 1年內
        "2_Young": "#FFD700",  # 黃色 - 1~3年
        "3_Mature": "#FF9800",  # 橘色 - 3~6年
        "4_Established": "#F44336",  # 紅色 - 6~10年
        "5_Senior": "#9C27B0",  # 紫色 - 10年以上
    },
}

SHAPE_MAP = {
    "centrality": {
        "high": "o",  # 圓形 - 高中心度
        "low": "^",  # 三角形 - 低中心度
    },
    "core_periphery": {
        "core": "s",  # 正方形 - 核心
        "periphery": "o",  # 圓形 - 邊緣
    },
    "interaction": {
        "continuous": "o",  # 圓形 - 持續互動
        "single": "^",  # 三角形 - 單次
    },
    "post_type": {
        "questions": "o",  # 圓形 - 發問者
        "answers": "^",  # 三角形 - 回答者
        "both": "s",  # 正方形 - 兩者皆有
    },
    "code_presence": {
        "has_code": "o",  # 圓形 - 有程式碼
        "no_code": "s",  # 正方形 - 純文字
    },
}


class SNAPlotter:
    """社會網路分析視覺化工具"""

    def __init__(self, output_dir: Path = OUTPUT_DIR):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.color_maps = COLOR_MAPS
        self.shape_maps = SHAPE_MAP

    def plot_network_graph(
        self,
        graph: ig.Graph,
        title: str,
        color_by: Optional[str] = None,
        shape_by: Optional[str] = None,
        edge_color_by: Optional[str] = None,
        default_vertex_color: str = "#87CEEB",
        vertex_labels: Optional[List[str]] = None,
        filename: str = "network.png",
        legend_info: Optional[Dict] = None,
        edge_weight_attribute: str = "weight",
        show_edge_weights: bool = True,
    ) -> str:
        """
        繪製網路圖

        Args:
            graph: igraph 圖形物件
            title: 圖表標題
            color_by: 節點顏色依據的屬性
            shape_by: 節點形狀依據的屬性
            edge_color_by: 邊顏色依據的屬性
            vertex_labels: 節點標籤列表
            filename: 輸出檔案名
            legend_info: 圖例資訊
            edge_weight_attribute: 邊權重屬性名稱 (default: "weight")
            show_edge_weights: 是否根據權重調整連線粗細 (default: True)
        """
        print(f"\n中間過程: 繪製網路圖 ({title})...")

        fig, ax = plt.subplots(1, 1, figsize=(16, 12))

        try:
            layout = graph.layout_fruchterman_reingold()
        except:
            try:
                layout = graph.layout_kamada_kawai()
            except:
                layout = graph.layout_circle()

        n_vertices = len(graph.vs)
        if n_vertices == 0:
            ax.text(
                0.5,
                0.5,
                "No data to display",
                ha="center",
                va="center",
                transform=ax.transAxes,
            )
            ax.axis("off")
            output_path = self.output_dir / filename
            output_path.unlink(missing_ok=True)
            plt.savefig(output_path, dpi=150, bbox_inches="tight", facecolor="white")
            plt.close()
            return str(output_path)

        colors = self._get_colors(graph, color_by, default_vertex_color)
        sizes = self._get_sizes(graph, color_by)

        if shape_by:
            shapes_data = self._get_shapes(graph, shape_by)
            for shape_name, vertex_indices in shapes_data.items():
                if not vertex_indices:
                    continue

                x = [layout[vid][0] for vid in vertex_indices]
                y = [layout[vid][1] for vid in vertex_indices]
                c = [colors[vid] for vid in vertex_indices]
                s = [sizes[vid] for vid in vertex_indices]

                ax.scatter(
                    x,
                    y,
                    c=c,
                    s=s,
                    marker=shape_name,
                    edgecolors="white",
                    linewidths=0.5,
                    alpha=0.8,
                    zorder=2,
                )
        else:
            ax.scatter(
                [layout[vid][0] for vid in range(n_vertices)],
                [layout[vid][1] for vid in range(n_vertices)],
                c=colors,
                s=sizes,
                edgecolors="white",
                linewidths=0.5,
                alpha=0.8,
                zorder=2,
            )

        edge_colors = self._get_edge_colors(graph, edge_color_by)

        if show_edge_weights and edge_weight_attribute in graph.es.attribute_names():
            weights = graph.es[edge_weight_attribute]
            if weights and len(weights) > 0:
                weights = np.array(weights, dtype=float)
                max_w = weights.max() if weights.max() > 0 else 1
                min_w = weights.min()
                if max_w > min_w:
                    norm_weights = (weights - min_w) / (max_w - min_w)
                    line_widths = 1.0 + norm_weights * 5
                else:
                    line_widths = [2.0] * len(weights)

                for i, edge in enumerate(graph.es):
                    source, target = edge.tuple
                    x_coords = [layout[source][0], layout[target][0]]
                    y_coords = [layout[source][1], layout[target][1]]
                    alpha = 0.5 + norm_weights[i] * 0.3 if max_w > min_w else 0.7
                    ax.plot(
                        x_coords,
                        y_coords,
                        color=edge_colors[i] if edge_colors else "#666666",
                        alpha=alpha,
                        linewidth=line_widths[i],
                        zorder=1,
                    )
        else:
            for i, edge in enumerate(graph.es):
                source, target = edge.tuple
                x_coords = [layout[source][0], layout[target][0]]
                y_coords = [layout[source][1], layout[target][1]]
                ax.plot(
                    x_coords,
                    y_coords,
                    color=edge_colors[i] if edge_colors else "#444444",
                    alpha=0.78,
                    linewidth=1.8,
                    zorder=1,
                )

        if vertex_labels and len(vertex_labels) == n_vertices:
            for i, (x, y) in enumerate(layout):
                if i < len(vertex_labels) and vertex_labels[i]:
                    ax.annotate(
                        str(vertex_labels[i])[:15],
                        (x, y),
                        fontsize=6,
                        ha="center",
                        va="bottom",
                        alpha=0.7,
                    )

        if legend_info:
            self._add_legend(ax, legend_info, graph)

        ax.set_title(title, fontsize=14, fontweight="bold", pad=20)
        ax.axis("off")

        output_path = self.output_dir / filename
        output_path.unlink(missing_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches="tight", facecolor="white")
        plt.close()

        print(f"最終輸出值: 圖片已儲存至 {output_path}")
        return str(output_path)

    def _get_colors(
        self,
        graph: ig.Graph,
        color_by: Optional[str],
        default_vertex_color: str = "#87CEEB",
    ) -> List[str]:
        """根據屬性獲取顏色"""
        default_color = default_vertex_color

        if not color_by or color_by not in graph.vs.attribute_names():
            return [default_color] * len(graph.vs)

        values = graph.vs[color_by]

        if color_by == "reputation":
            color_map = self.color_maps["reputation"]
            return [color_map.get(v, default_color) for v in values]

        elif color_by == "reputation_level":
            color_map = self.color_maps["reputation"]
            return [color_map.get(v, default_color) for v in values]

        elif color_by == "answer_time_level":
            color_map = self.color_maps["answer_time"]
            return [color_map.get(v, default_color) for v in values]

        elif color_by == "tech_domain":
            color_map = self.color_maps["tech_domain"]
            return [color_map.get(v, default_color) for v in values]

        elif color_by == "connectivity_type":
            color_map = self.color_maps["connectivity"]
            return [color_map.get(v, default_color) for v in values]

        elif color_by == "has_code":
            color_map = {"yes": "#42A5F5", "no": "#FFA726"}
            return [color_map.get(str(v), default_color) for v in values]

        elif color_by == "post_type":
            color_map = {
                "1_Both": "#9C27B0",
                "2_QuestionsOnly": "#42A5F5",
                "3_AnswersOnly": "#4CAF50",
                "4_Neither": "#9E9E9E",
            }
            return [color_map.get(v, default_color) for v in values]

        elif color_by == "account_age_level":
            color_map = self.color_maps["account_age"]
            return [color_map.get(v, default_color) for v in values]

        elif color_by == "score_level":
            color_map = self.color_maps["score_level"]
            return [color_map.get(v, default_color) for v in values]

        elif color_by == "is_core":
            color_map = {"True": "#F44336", "False": "#2196F3"}
            return [color_map.get(str(v), default_color) for v in values]

        elif color_by == "vote_type":
            color_map = {
                "accepted": "#FFD700",
                "upvote": "#4CAF50",
                "downvote": "#F44336",
                "spam": "#212121",
                "favorite": "#2196F3",
                "none": "#BDBDBD",
                "other": "#9E9E9E",
            }
            return [color_map.get(str(v), default_color) for v in values]

        elif color_by == "badge_level":
            color_map = {
                "1_Gold": "#FFD700",
                "2_Silver": "#C0C0C0",
                "3_Bronze": "#CD7F32",
                "0_None": "#4CAF50",
            }
            return [color_map.get(str(v), default_color) for v in values]

        elif color_by == "editor_level":
            color_map = {
                "3_Power": "#F44336",
                "2_Active": "#FF9800",
                "1_Casual": "#4CAF50",
                "0_None": "#BDBDBD",
            }
            return [color_map.get(str(v), default_color) for v in values]

        elif color_by == "link_type":
            color_map = {
                "Linked": "#2196F3",
                "Duplicate": "#F44336",
                "Other": "#9E9E9E",
            }
            return [color_map.get(str(v), default_color) for v in values]

        elif color_by == "reviewer_level":
            color_map = {
                "3_Power": "#F44336",
                "2_Active": "#FF9800",
                "1_Casual": "#4CAF50",
                "0_None": "#BDBDBD",
            }
            return [color_map.get(str(v), default_color) for v in values]

        elif color_by == "bounty_level":
            color_map = {
                "4_Extravagant": "#F44336",
                "3_Generous": "#FF9800",
                "2_Normal": "#4CAF50",
                "1_Meager": "#9E9E9E",
                "0_None": "#BDBDBD",
            }
            return [color_map.get(str(v), default_color) for v in values]

        elif color_by == "region":
            color_map = {
                "North America": "#2196F3",
                "Europe": "#4CAF50",
                "Asia": "#FFC107",
                "Oceania": "#9E9E9E",
                "South America": "#FF5722",
                "Africa": "#795548",
                "Middle East": "#607D8B",
                "Other": "#BDBDBD",
            }
            return [color_map.get(str(v), default_color) for v in values]

        elif color_by == "activity_level":
            color_map = {
                "high": "#F44336",
                "medium": "#FF9800",
                "low": "#4CAF50",
            }
            return [color_map.get(str(v), default_color) for v in values]

        elif isinstance(values[0], (int, float)):
            norm_values = np.array(values, dtype=float)
            max_v, min_v = norm_values.max(), norm_values.min()
            if max_v > min_v:
                norm_values = (norm_values - min_v) / (max_v - min_v)
            else:
                norm_values = np.zeros_like(norm_values)
            return [plt.cm.RdYlGn_r(v) for v in norm_values]

        return [default_color] * len(graph.vs)

    def _get_edge_colors(self, graph: ig.Graph, color_by: Optional[str]) -> List[str]:
        default_color = "#9E9E9E"
        if not color_by or color_by not in graph.es.attribute_names():
            return [default_color] * len(graph.es)

        values = graph.es[color_by]
        if color_by == "link_type":
            color_map = {
                "Linked": "#2196F3",
                "Duplicate": "#F44336",
                "Other": "#9E9E9E",
            }
            return [color_map.get(str(v), default_color) for v in values]

        return [default_color] * len(graph.es)

    def _get_sizes(self, graph: ig.Graph, color_by: Optional[str]) -> List[int]:
        """根據屬性獲取節點大小"""
        n = len(graph.vs)
        base_size = 100
        max_size = 500
        min_size = 50

        if color_by in ["reputation", "popularity", "degree", "score"]:
            values = (
                graph.vs[color_by] if color_by in graph.vs.attribute_names() else None
            )
            if values:
                values = np.array(values, dtype=float)
                max_v, min_v = values.max(), values.min()
                if max_v > min_v:
                    norm_values = (values - min_v) / (max_v - min_v)
                    return [
                        int(min_size + norm_values[i] * (max_size - min_size))
                        for i in range(n)
                    ]

        return [base_size] * n

    def _get_shapes(self, graph: ig.Graph, shape_by: str) -> Dict[str, List[int]]:
        """根據屬性獲取形狀分組"""
        result = {}

        if shape_by == "centrality_level":
            if "betweenness" in graph.vs.attribute_names():
                values = graph.vs["betweenness"]
                median = np.median(values)
                result["o"] = [i for i, v in enumerate(values) if v >= median]
                result["^"] = [i for i, v in enumerate(values) if v < median]

        elif shape_by == "is_core":
            is_core = graph.vs["is_core"]
            result["s"] = [i for i, v in enumerate(is_core) if v]
            result["o"] = [i for i, v in enumerate(is_core) if not v]

        elif shape_by == "post_type":
            post_types = (
                list(graph.vs["post_type"])
                if "post_type" in graph.vs.attribute_names()
                else []
            )
            result["s"] = [i for i, v in enumerate(post_types) if v == "1_Both"]
            result["o"] = [
                i for i, v in enumerate(post_types) if v == "2_QuestionsOnly"
            ]
            result["^"] = [i for i, v in enumerate(post_types) if v == "3_AnswersOnly"]

        elif shape_by == "interaction_type":
            interaction_types = (
                list(graph.vs["interaction_type"])
                if "interaction_type" in graph.vs.attribute_names()
                else []
            )
            result["o"] = [
                i for i, v in enumerate(interaction_types) if v == "continuous"
            ]
            result["^"] = [i for i, v in enumerate(interaction_types) if v == "single"]

        elif shape_by == "has_code":
            has_code = (
                list(graph.vs["has_code"])
                if "has_code" in graph.vs.attribute_names()
                else []
            )
            result["o"] = [i for i, v in enumerate(has_code) if v == 1 or v == "yes"]
            result["s"] = [i for i, v in enumerate(has_code) if v == 0 or v == "no"]

        elif shape_by == "badge_level":
            badge_levels = (
                list(graph.vs["badge_level"])
                if "badge_level" in graph.vs.attribute_names()
                else []
            )
            result["o"] = [i for i, v in enumerate(badge_levels) if v == "1_Gold"]
            result["s"] = [i for i, v in enumerate(badge_levels) if v == "2_Silver"]
            result["^"] = [i for i, v in enumerate(badge_levels) if v == "3_Bronze"]
            result["d"] = [i for i, v in enumerate(badge_levels) if v == "0_None"]

        return result

    def _add_legend(self, ax, legend_info: Dict, graph: Optional[ig.Graph] = None):
        """添加图例"""
        patches = []

        if "colors" in legend_info:
            for label, color in legend_info["colors"].items():
                patches.append(mpatches.Patch(color=color, label=label))

        if "shapes" in legend_info:
            for label, marker in legend_info["shapes"].items():
                patches.append(
                    plt.Line2D(
                        [0],
                        [0],
                        marker=marker,
                        color="w",
                        markerfacecolor="gray",
                        markersize=10,
                        label=label,
                    )
                )

        if "edge_weights" in legend_info and graph is not None:
            weights = (
                graph.es["weight"] if "weight" in graph.es.attribute_names() else []
            )
            if weights and len(weights) > 0:
                try:
                    max_w = max(weights)
                    min_w = min(weights)
                except (TypeError, ValueError):
                    max_w = None
                    min_w = None
                if max_w is not None and min_w is not None:
                    for label, width in legend_info["edge_weights"].items():
                        patches.append(
                            plt.Line2D(
                                [0],
                                [0],
                                color="#666666",
                                linewidth=width,
                                alpha=0.7,
                                label=label,
                            )
                        )

        if patches:
            ax.legend(
                handles=patches,
                loc="upper left",
                fontsize=8,
                framealpha=0.9,
                fancybox=True,
            )


def save_analysis_results(results: Dict[str, Any], output_path: str):
    """儲存分析結果到 CSV"""
    from ..utils.helpers import save_json

    print("\n中間過程: 儲存分析結果...")

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    save_json(results, output_path / "analysis_results.json")

    print(f"最終輸出值: 結果已儲存至 {output_path}")


def generate_summary_report(analysis_results: Dict[str, Dict[str, Any]]) -> str:
    """生成分析摘要報告"""
    report_lines = []
    report_lines.append("=" * 60)
    report_lines.append("Stack Overflow 社會網路分析摘要報告")
    report_lines.append("=" * 60)
    report_lines.append("")

    for name, result in analysis_results.items():
        report_lines.append(f"\n## {name}")
        report_lines.append("-" * 40)

        if "summary" in result:
            for key, value in result["summary"].items():
                if not isinstance(value, (dict, list)):
                    report_lines.append(f"  {key}: {value}")

        if "graph" in result and result["graph"] is not None:
            g = result["graph"]
            report_lines.append(f"  nodes: {len(g.vs)}")
            report_lines.append(f"  edges: {len(g.es)}")

    report_lines.append("")
    report_lines.append("=" * 60)

    report = "\n".join(report_lines)
    print(report)

    return report
