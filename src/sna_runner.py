"""
SNA 分析執行器 - 執行所有 6 個分析主題
"""

from typing import Dict, Any, Optional
from pathlib import Path
import json

from src.data.data_loader import DataLoader
from src.analysis.centrality import CentralityAnalyzer
from src.analysis.core_efficiency import CoreEfficiencyAnalyzer
from src.analysis.tag_cooccurrence import TagCooccurrenceAnalyzer
from src.analysis.connected_components import ConnectedComponentAnalyzer
from src.analysis.content_features import ContentFeatureAnalyzer
from src.analysis.account_age import AccountAgeAnalyzer
from src.visualization.plots import SNAPlotter, generate_summary_report
from src.utils.helpers import save_json


class SNARunner:
    """社會網路分析執行器"""
    
    def __init__(self, output_dir: str = "output", data_limit: int = 100):
        self.data_loader = DataLoader()
        self.plotter = SNAPlotter(output_dir=Path(output_dir))
        self.data_limit = data_limit
        self.results: Dict[str, Dict[str, Any]] = {}
    
    def run_all(self) -> Dict[str, Dict[str, Any]]:
        """執行所有分析"""
        print("\n" + "=" * 70)
        print("Stack Overflow 社會網路分析 - 執行所有分析")
        print("=" * 70)
        
        print(f"\n設定參數: data_limit={self.data_limit}")
        
        self._run_analysis_1()
        self._run_analysis_2()
        self._run_analysis_3()
        self._run_analysis_4()
        self._run_analysis_5()
        self._run_analysis_6()
        
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
                }
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
                }
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
            },
            'analysis_4': {
                'colors': {
                    'DarkBlue-Main Component': '#1565C0',
                    'Gray-Isolated': '#9E9E9E',
                },
                'shapes': {
                    'Circle-Continuous': 'o',
                    'Triangle-Single': '^',
                }
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
                }
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
                }
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
                    serializable_results[name][key] = value
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
