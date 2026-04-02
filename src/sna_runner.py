"""
SNA 分析執行器 - 執行所有 15 個分析主題
"""

from typing import Dict, Any, Optional
from pathlib import Path
import json
import numpy as np
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
    
    def __init__(self, output_dir: str = "output", data_limit: int = 100):
        self.data_loader = DataLoader()
        self.plotter = SNAPlotter(output_dir=Path(output_dir))
        self.data_limit = data_limit
        self.results: Dict[str, Dict[str, Any]] = {}
        self.analysis_limits = {
            1: data_limit,
            2: data_limit,
            3: data_limit,
            4: data_limit,
            5: data_limit,
            6: data_limit,
            7: max(data_limit, 500),
            8: max(data_limit, 500),
            9: max(data_limit, 500),
            10: max(data_limit, 500),
            11: max(data_limit, 500),
            12: max(data_limit, 500),
            13: max(data_limit, 500),
            14: max(data_limit, 500),
            15: max(data_limit, 1000),
        }
    
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
        self.results['analysis_1_centrality'] = analyzer.run(limit=self.data_limit)
    
    def _run_analysis_2(self):
        """執行分析 2: 網路核心結構與解答效率"""
        print("\n" + "#" * 60)
        print("# 分析主題 2: 網路核心結構與解答效率")
        print("#" * 60)
        
        analyzer = CoreEfficiencyAnalyzer(self.data_loader)
        self.results['analysis_2_core_efficiency'] = analyzer.run(limit=self.data_limit)
    
    def _run_analysis_3(self):
        """執行分析 3: 技術標籤共現與領域地圖"""
        print("\n" + "#" * 60)
        print("# 分析主題 3: 技術標籤共現與領域地圖")
        print("#" * 60)
        
        analyzer = TagCooccurrenceAnalyzer(self.data_loader)
        self.results['analysis_3_tag_cooccurrence'] = analyzer.run(limit=self.data_limit)
    
    def _run_analysis_4(self):
        """執行分析 4: 知識孤島與連通分量分析"""
        print("\n" + "#" * 60)
        print("# 分析主題 4: 知識孤島與連通分量分析")
        print("#" * 60)
        
        analyzer = ConnectedComponentAnalyzer(self.data_loader)
        self.results['analysis_4_connected_components'] = analyzer.run(limit=self.data_limit)
    
    def _run_analysis_5(self):
        """執行分析 5: 內容特徵與互動反響"""
        print("\n" + "#" * 60)
        print("# 分析主題 5: 內容特徵與互動反響")
        print("#" * 60)
        
        analyzer = ContentFeatureAnalyzer(self.data_loader)
        self.results['analysis_5_content_features'] = analyzer.run(limit=self.data_limit)
    
    def _run_analysis_6(self):
        """執行分析 6: 帳號年資與社群貢獻"""
        print("\n" + "#" * 60)
        print("# 分析主題 6: 帳號年資與社群貢獻")
        print("#" * 60)
        
        analyzer = AccountAgeAnalyzer(self.data_loader)
        self.results['analysis_6_account_age'] = analyzer.run(limit=self.data_limit)
    
    def _run_analysis_7(self):
        """執行分析 7: 投票行為網路"""
        print("\n" + "#" * 60)
        print("# 分析主題 7: 投票行為網路")
        print("#" * 60)
        
        analyzer = VotingBehaviorAnalyzer(self.data_loader)
        self.results['analysis_7_voting_behavior'] = analyzer.run(limit=self.analysis_limits[7])
    
    def _run_analysis_8(self):
        """執行分析 8: 評論互動網路"""
        print("\n" + "#" * 60)
        print("# 分析主題 8: 評論互動網路")
        print("#" * 60)
        
        analyzer = CommentNetworkAnalyzer(self.data_loader)
        self.results['analysis_8_comment_network'] = analyzer.run(limit=self.analysis_limits[8])
    
    def _run_analysis_9(self):
        """執行分析 9: 徽章成就網路"""
        print("\n" + "#" * 60)
        print("# 分析主題 9: 徽章成就網路")
        print("#" * 60)
        
        analyzer = BadgeNetworkAnalyzer(self.data_loader)
        self.results['analysis_9_badge_network'] = analyzer.run(limit=self.analysis_limits[9])
    
    def _run_analysis_10(self):
        """執行分析 10: 編輯協作網路"""
        print("\n" + "#" * 60)
        print("# 分析主題 10: 編輯協作網路")
        print("#" * 60)
        
        analyzer = EditCollaborationAnalyzer(self.data_loader)
        self.results['analysis_10_edit_collaboration'] = analyzer.run(limit=self.analysis_limits[10])
    
    def _run_analysis_11(self):
        """執行分析 11: 引用與重複問題網路"""
        print("\n" + "#" * 60)
        print("# 分析主題 11: 引用與重複問題網路")
        print("#" * 60)
        
        analyzer = PostLinkAnalyzer(self.data_loader)
        self.results['analysis_11_post_link'] = analyzer.run(limit=self.analysis_limits[11])
    
    def _run_analysis_12(self):
        """執行分析 12: 審核任務網路"""
        print("\n" + "#" * 60)
        print("# 分析主題 12: 審核任務網路")
        print("#" * 60)
        
        analyzer = ReviewTaskAnalyzer(self.data_loader)
        self.results['analysis_12_review_task'] = analyzer.run(limit=self.analysis_limits[12])
    
    def _run_analysis_13(self):
        """執行分析 13: 賞金懸賞網路"""
        print("\n" + "#" * 60)
        print("# 分析主題 13: 賞金懸賞網路")
        print("#" * 60)
        
        analyzer = BountyNetworkAnalyzer(self.data_loader)
        self.results['analysis_13_bounty_network'] = analyzer.run(limit=self.analysis_limits[13])
    
    def _run_analysis_14(self):
        """執行分析 14: 使用者地理分布網路"""
        print("\n" + "#" * 60)
        print("# 分析主題 14: 使用者地理分布網路")
        print("#" * 60)
        
        analyzer = UserLocationAnalyzer(self.data_loader)
        self.results['analysis_14_user_location'] = analyzer.run(limit=self.analysis_limits[14])
    
    def _run_analysis_15(self):
        """執行分析 15: 時間序列活躍度網路"""
        print("\n" + "#" * 60)
        print("# 分析主題 15: 時間序列活躍度網路")
        print("#" * 60)
        
        analyzer = TimeSeriesAnalyzer(self.data_loader)
        self.results['analysis_15_time_series'] = analyzer.run(limit=self.analysis_limits[15])
    
    def _generate_visualizations(self):
        """產生視覺化圖表"""
        print("\n" + "=" * 60)
        print("產生視覺化圖表 (使用 igraph)")
        print("=" * 60)
        
        LEGEND_INFO = {
            'analysis_1': {
                'colors': {
                    'Green-Newcomer (<1K)': '#4CAF50',
                    'Yellow-Mid (1K~10K)': '#FFD700',
                    'Orange-Senior (10K~50K)': '#FF9800',
                    'Red-Expert (>50K)': '#F44336',
                },
                'shapes': {
                    'Circle-High Centrality': 'o',
                    'Triangle-Low Centrality': '^',
                },
                'edge_weights': {
                    'Thick-Strong Tie': 3.0,
                    'Thin-Weak Tie': 0.5,
                },
            },
            'analysis_2': {
                'colors': {
                    'Green-<1h': '#4CAF50',
                    'Yellow-1~12h': '#FFD700',
                    'LightRed-12~24h': '#FFCDD2',
                    'Red->24h': '#F44336',
                    'Gray-Unresolved': '#9E9E9E',
                },
                'shapes': {
                    'Square-Core': 's',
                    'Circle-Periphery': 'o',
                },
                'edge_weights': {
                    'Thick-Strong Tie': 3.0,
                    'Thin-Weak Tie': 0.5,
                },
            },
            'analysis_3': {
                'colors': {
                    'LightBlue-Web': '#81D4FA',
                    'Pink-AI/Data': '#F8BBD9',
                    'Green-Mobile': '#A5D6A7',
                    'Yellow-Backend': '#FFE082',
                    'Purple-Database': '#CE93D8',
                    'Gray-Other': '#E0E0E0',
                },
                'edge_weights': {
                    'Thick-High Co-occurrence': 3.0,
                    'Thin-Low Co-occurrence': 0.5,
                },
            },
            'analysis_4': {
                'colors': {
                    'DarkBlue-Main Component': '#1565C0',
                    'Gray-Isolated': '#9E9E9E',
                },
                'shapes': {
                    'Circle-Continuous': 'o',
                    'Triangle-Single': '^',
                },
                'edge_weights': {
                    'Thick-Strong Tie': 3.0,
                    'Thin-Weak Tie': 0.5,
                },
            },
            'analysis_5': {
                'colors': {
                    'Gray-0 votes': '#BDBDBD',
                    'Green-1~10 votes': '#66BB6A',
                    'Yellow-11~50 votes': '#FFD54F',
                    'Orange-51~100 votes': '#FF7043',
                    'Red->100 votes': '#F44336',
                },
                'shapes': {
                    'Circle-Has Code': 'o',
                    'Square-Text Only': 's',
                },
                'edge_weights': {
                    'Thick-Similar Tags': 3.0,
                    'Thin-Different Tags': 0.5,
                },
            },
            'analysis_6': {
                'colors': {
                    'Green-<1 year': '#4CAF50',
                    'Yellow-1~3 years': '#FFD700',
                    'Orange-3~6 years': '#FF9800',
                    'Red-6~10 years': '#F44336',
                    'Purple->10 years': '#9C27B0',
                },
                'shapes': {
                    'Circle-Asker': 'o',
                    'Triangle-Answerer': '^',
                    'Square-Both': 's',
                },
                'edge_weights': {
                    'Thick-Strong Tie': 3.0,
                    'Thin-Weak Tie': 0.5,
                },
            },
            'analysis_7': {
                'colors': {
                    'Gold-Accepted': '#FFD700',
                    'Green-Upvote': '#4CAF50',
                    'Red-Downvote': '#F44336',
                    'Black-Spam': '#212121',
                    'Blue-Favorite': '#2196F3',
                },
                'shapes': {
                    'Circle-High Votes': 'o',
                    'Triangle-Low Votes': '^',
                },
                'edge_weights': {
                    'Thick-Strong Tie': 3.0,
                    'Thin-Weak Tie': 0.5,
                },
            },
            'analysis_8': {
                'colors': {
                    'Blue-Active': '#2196F3',
                    'Green-Moderate': '#4CAF50',
                    'Gray-Low': '#9E9E9E',
                },
                'shapes': {
                    'Circle-Commenter': 'o',
                },
                'edge_weights': {
                    'Thick-Strong Tie': 3.0,
                    'Thin-Weak Tie': 0.5,
                },
            },
            'analysis_9': {
                'colors': {
                    'Gold-Gold Badge': '#FFD700',
                    'Silver-Silver Badge': '#C0C0C0',
                    'Bronze-Bronze Badge': '#CD7F32',
                },
                'shapes': {
                    'Circle-Top Earner': 'o',
                    'Triangle-Regular': '^',
                },
                'edge_weights': {
                    'Thick-Strong Tie': 3.0,
                    'Thin-Weak Tie': 0.5,
                },
            },
            'analysis_10': {
                'colors': {
                    'Green-Active': '#4CAF50',
                    'Yellow-Moderate': '#FFC107',
                    'Gray-Casual': '#9E9E9E',
                },
                'shapes': {
                    'Circle-Editor': 'o',
                },
                'edge_weights': {
                    'Thick-Strong Tie': 3.0,
                    'Thin-Weak Tie': 0.5,
                },
            },
            'analysis_11': {
                'colors': {
                    'Blue-Linked': '#2196F3',
                    'Red-Duplicate': '#F44336',
                },
                'shapes': {
                    'Circle-Question': 'o',
                },
                'edge_weights': {
                    'Thick-Strong Tie': 3.0,
                    'Thin-Weak Tie': 0.5,
                },
            },
            'analysis_12': {
                'colors': {
                    'Green-Active': '#4CAF50',
                    'Yellow-Moderate': '#FFC107',
                    'Gray-Casual': '#9E9E9E',
                },
                'shapes': {
                    'Circle-Reviewer': 'o',
                },
                'edge_weights': {
                    'Thick-Strong Tie': 3.0,
                    'Thin-Weak Tie': 0.5,
                },
            },
            'analysis_13': {
                'colors': {
                    'Gray-Meager': '#9E9E9E',
                    'Green-Normal': '#4CAF50',
                    'Yellow-Generous': '#FFC107',
                    'Red-Extravagant': '#F44336',
                },
                'shapes': {
                    'Circle-Bounty User': 'o',
                },
                'edge_weights': {
                    'Thick-Strong Tie': 3.0,
                    'Thin-Weak Tie': 0.5,
                },
            },
            'analysis_14': {
                'colors': {
                    'Blue-North America': '#2196F3',
                    'Green-Europe': '#4CAF50',
                    'Yellow-Asia': '#FFC107',
                    'Gray-Other': '#9E9E9E',
                },
                'shapes': {
                    'Circle-Region': 'o',
                },
                'edge_weights': {
                    'Thick-Strong Tie': 3.0,
                    'Thin-Weak Tie': 0.5,
                },
            },
            'analysis_15': {
                'colors': {
                    'Blue-High Activity': '#2196F3',
                    'Green-Medium': '#4CAF50',
                    'Gray-Low': '#9E9E9E',
                },
                'shapes': {
                    'Circle-Month': 'o',
                },
                'edge_weights': {
                    'Thick-Strong Tie': 3.0,
                    'Thin-Weak Tie': 0.5,
                },
            },
        }
        
        if 'analysis_1_centrality' in self.results:
            result = self.results['analysis_1_centrality']
            if 'graph' in result and result['graph'] is not None:
                self.plotter.plot_network_graph(
                    result['graph'],
                    'Method 1: Reputation vs Network Centrality\nNodes=Users, Edges=Answer (Answerer->Asker) | Color: Reputation Level | Shape: Centrality',
                    color_by='reputation_level',
                    shape_by='centrality_level',
                    filename='analysis_1_network.png',
                    legend_info=LEGEND_INFO['analysis_1']
                )
        
        if 'analysis_2_core_efficiency' in self.results:
            result = self.results['analysis_2_core_efficiency']
            if 'graph' in result and result['graph'] is not None:
                self.plotter.plot_network_graph(
                    result['graph'],
                    'Method 2: Core-Periphery vs Answer Efficiency\nNodes=Users, Edges=Interaction | Color: Answer Time | Shape: Core/Periphery',
                    color_by='answer_time_level',
                    shape_by='is_core',
                    filename='analysis_2_network.png',
                    legend_info=LEGEND_INFO['analysis_2']
                )
        
        if 'analysis_3_tag_cooccurrence' in self.results:
            result = self.results['analysis_3_tag_cooccurrence']
            if 'graph' in result and result['graph'] is not None:
                self.plotter.plot_network_graph(
                    result['graph'],
                    'Method 3: Tag Co-occurrence & Technology Map\nNodes=Tags, Edges=Co-occurrence | Color: Tech Domain | Size: Popularity',
                    color_by='tech_domain',
                    filename='analysis_3_tag_network.png',
                    legend_info=LEGEND_INFO['analysis_3']
                )
        
        if 'analysis_4_connected_components' in self.results:
            result = self.results['analysis_4_connected_components']
            if 'graph' in result and result['graph'] is not None:
                self.plotter.plot_network_graph(
                    result['graph'],
                    'Method 4: Knowledge Islands & Connected Components\nNodes=Users, Edges=Interaction | Color: Connectivity | Shape: Type',
                    color_by='connectivity_type',
                    shape_by='interaction_type',
                    filename='analysis_4_network.png',
                    legend_info=LEGEND_INFO['analysis_4']
                )
        
        if 'analysis_5_content_features' in self.results:
            result = self.results['analysis_5_content_features']
            if 'graph' in result and result['graph'] is not None:
                self.plotter.plot_network_graph(
                    result['graph'],
                    'Method 5: Content Features vs Upvotes\nNodes=Posts, Edges=Similar Tags | Color: Score | Shape: Code Presence',
                    color_by='score_level',
                    shape_by='has_code',
                    filename='analysis_5_network.png',
                    legend_info=LEGEND_INFO['analysis_5']
                )
        
        if 'analysis_6_account_age' in self.results:
            result = self.results['analysis_6_account_age']
            if 'graph' in result and result['graph'] is not None:
                self.plotter.plot_network_graph(
                    result['graph'],
                    'Method 6: Account Age vs Community Contribution\nColor: Age Level | Shape: Post Type',
                    color_by='account_age_level',
                    shape_by='post_type',
                    filename='analysis_6_network.png',
                    legend_info=LEGEND_INFO['analysis_6']
                )
        
        if 'analysis_7_voting_behavior' in self.results:
            result = self.results['analysis_7_voting_behavior']
            if 'graph' in result and result['graph'] is not None:
                self.plotter.plot_network_graph(
                    result['graph'],
                    'Method 7: Voting Behavior Network\nNodes=Users, Edges=Co-voted Posts | Color: Vote Type',
                    color_by='vote_type',
                    filename='analysis_7_network.png',
                    legend_info=LEGEND_INFO['analysis_7']
                )
        
        if 'analysis_8_comment_network' in self.results:
            result = self.results['analysis_8_comment_network']
            if 'graph' in result and result['graph'] is not None:
                self.plotter.plot_network_graph(
                    result['graph'],
                    'Method 8: Comment Interaction Network\nNodes=Users, Edges=Comment Co-occurrence | Color: Comment Count',
                    color_by='comment_count',
                    filename='analysis_8_network.png',
                    legend_info=LEGEND_INFO['analysis_8']
                )
        
        if 'analysis_9_badge_network' in self.results:
            result = self.results['analysis_9_badge_network']
            if 'graph' in result and result['graph'] is not None:
                self.plotter.plot_network_graph(
                    result['graph'],
                    'Method 9: Badge Achievement Network\nNodes=Users, Edges=Shared Badges | Color: Badge Level',
                    color_by='badge_level',
                    filename='analysis_9_network.png',
                    legend_info=LEGEND_INFO['analysis_9']
                )
        
        if 'analysis_10_edit_collaboration' in self.results:
            result = self.results['analysis_10_edit_collaboration']
            if 'graph' in result and result['graph'] is not None:
                self.plotter.plot_network_graph(
                    result['graph'],
                    'Method 10: Edit Collaboration Network\nNodes=Users, Edges=Co-edit | Color: Editor Level',
                    color_by='editor_level',
                    filename='analysis_10_network.png',
                    legend_info=LEGEND_INFO['analysis_10']
                )
        
        if 'analysis_11_post_link' in self.results:
            result = self.results['analysis_11_post_link']
            if 'graph' in result and result['graph'] is not None:
                self.plotter.plot_network_graph(
                    result['graph'],
                    'Method 11: Post Link & Duplicate Network\nNodes=Posts, Edges=Link | Color: Link Type',
                    color_by='link_type',
                    filename='analysis_11_network.png',
                    legend_info=LEGEND_INFO['analysis_11']
                )
        
        if 'analysis_12_review_task' in self.results:
            result = self.results['analysis_12_review_task']
            if 'graph' in result and result['graph'] is not None:
                self.plotter.plot_network_graph(
                    result['graph'],
                    'Method 12: Review Task Network\nNodes=Users, Edges=Co-review | Color: Reviewer Level',
                    color_by='reviewer_level',
                    filename='analysis_12_network.png',
                    legend_info=LEGEND_INFO['analysis_12']
                )
        
        if 'analysis_13_bounty_network' in self.results:
            result = self.results['analysis_13_bounty_network']
            if 'graph' in result and result['graph'] is not None:
                self.plotter.plot_network_graph(
                    result['graph'],
                    'Method 13: Bounty Network\nNodes=Users, Edges=Bounty | Color: Bounty Level',
                    color_by='bounty_level',
                    filename='analysis_13_network.png',
                    legend_info=LEGEND_INFO['analysis_13']
                )
        
        if 'analysis_14_user_location' in self.results:
            result = self.results['analysis_14_user_location']
            if 'graph' in result and result['graph'] is not None:
                g = result['graph']
                labels = g.vs['region'] if 'region' in g.vs.attribute_names() else None
                self.plotter.plot_network_graph(
                    g,
                    'Method 14: User Location Network\nNodes=Regions, Edges=Connection | Color: Region | Label: Region Name',
                    color_by='region',
                    vertex_labels=labels,
                    filename='analysis_14_network.png',
                    legend_info=LEGEND_INFO['analysis_14']
                )
        
        if 'analysis_15_time_series' in self.results:
            result = self.results['analysis_15_time_series']
            if 'graph' in result and result['graph'] is not None:
                self.plotter.plot_network_graph(
                    result['graph'],
                    'Method 15: Time Series Activity Network\nNodes=Months, Edges=Activity | Color: Activity Level',
                    color_by='activity_level',
                    filename='analysis_15_network.png',
                    legend_info=LEGEND_INFO['analysis_15']
                )
    
    def _make_serializable(self, obj):
        """Recursively convert numpy types to Python native types"""
        if isinstance(obj, dict):
            return {str(k): self._make_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [self._make_serializable(item) for item in obj]
        elif hasattr(obj, 'item'):
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
                if key == 'graph':
                    serializable_results[name][key] = {
                        'nodes': len(value.vs) if value else 0,
                        'edges': len(value.es) if value else 0,
                    }
                elif key == 'summary':
                    serializable_results[name][key] = self._make_serializable(value)
                elif key == 'posts_df':
                    if hasattr(value, 'to_dict'):
                        df = value.copy()
                        for col in df.columns:
                            if df[col].dtype.name == 'datetime64[ns, UTC]':
                                df[col] = df[col].astype(str)
                        serializable_results[name][key] = df.to_dict(orient='records')[:10]
                    else:
                        serializable_results[name][key] = {}
                elif key == 'analysis_df':
                    if hasattr(value, 'to_dict'):
                        df = value.copy()
                        for col in df.columns:
                            if df[col].dtype.name == 'datetime64[ns, UTC]':
                                df[col] = df[col].astype(str)
                        serializable_results[name][key] = df.to_dict(orient='records')[:10]
                    else:
                        serializable_results[name][key] = {}
                elif key == 'age_df':
                    if hasattr(value, 'to_dict'):
                        df = value.copy()
                        for col in df.columns:
                            if df[col].dtype.name == 'datetime64[ns, UTC]':
                                df[col] = df[col].astype(str)
                        serializable_results[name][key] = df.to_dict(orient='records')[:10]
                    else:
                        serializable_results[name][key] = {}
                elif key == 'connectivity_df':
                    if hasattr(value, 'to_dict'):
                        df = value.copy()
                        for col in df.columns:
                            if df[col].dtype.name == 'datetime64[ns, UTC]':
                                df[col] = df[col].astype(str)
                        serializable_results[name][key] = df.to_dict(orient='records')[:10]
                    else:
                        serializable_results[name][key] = {}
                elif key == 'tag_df':
                    if hasattr(value, 'to_dict'):
                        df = value.copy()
                        for col in df.columns:
                            if df[col].dtype.name == 'datetime64[ns, UTC]':
                                df[col] = df[col].astype(str)
                        serializable_results[name][key] = df.to_dict(orient='records')[:10]
                    else:
                        serializable_results[name][key] = {}
                elif key in ('votes_df', 'comments_df', 'badges_df', 'edits_df', 'links_df',
                             'reviews_df', 'bounties_df', 'users_df'):
                    if hasattr(value, 'to_dict'):
                        df = value.copy()
                        for col in df.columns:
                            if df[col].dtype.name == 'datetime64[ns, UTC]':
                                df[col] = df[col].astype(str)
                        serializable_results[name][key] = df.to_dict(orient='records')[:10]
                    else:
                        serializable_results[name][key] = {}
                elif key == 'centrality_metrics':
                    serializable_results[name][key] = value.to_dict() if hasattr(value, 'to_dict') else {}
                elif key == 'metrics':
                    serializable_results[name][key] = value.to_dict() if hasattr(value, 'to_dict') else {}
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
    
    parser = argparse.ArgumentParser(description='Stack Overflow Social Network Analysis')
    parser.add_argument('--limit', type=int, default=100, help='Number of records to analyze')
    parser.add_argument('--output', type=str, default='output', help='Output directory')
    
    args = parser.parse_args()
    
    runner = SNARunner(output_dir=args.output, data_limit=args.limit)
    runner.run_all()


if __name__ == "__main__":
    main()