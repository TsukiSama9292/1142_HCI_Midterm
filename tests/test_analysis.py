"""
分析模組測試

測試所有 6 個社會網路分析模組
"""

import pytest
from unittest.mock import MagicMock, patch
import pandas as pd
import numpy as np


class TestCentralityAnalyzer:
    """測試分析主題 1: 使用者聲望與網路中心度"""
    
    def test_analyzer_initialization(self):
        """測試分析器初始化"""
        print("\n測試中心度分析器初始化")
        print("輸入值: CentralityAnalyzer()")
        
        with patch('src.analysis.centrality.DataLoader'):
            from src.analysis.centrality import CentralityAnalyzer
            
            analyzer = CentralityAnalyzer()
            
            assert analyzer is not None
            assert analyzer.builder is not None
            print(f"中間過程: builder = {type(analyzer.builder).__name__}")
            print("最終輸出值: 初始化成功")
    
    def test_metrics_dataclass(self):
        """測試中心度指標資料類別"""
        print("\n測試中心度指標資料類別")
        print("輸入值: betweenness=[0.1, 0.2, 0.3]")
        
        from src.analysis.centrality import CentralityMetrics
        
        metrics = CentralityMetrics(
            betweenness=[0.1, 0.2, 0.3],
            degree=[5, 10, 15],
            closeness=[0.5, 0.6, 0.7],
            pagerank=[0.2, 0.3, 0.5],
        )
        
        print("中間過程: 轉換為DataFrame")
        df = metrics.to_dataframe()
        
        assert len(df) == 3
        assert 'betweenness' in df.columns
        assert 'degree' in df.columns
        assert 'closeness' in df.columns
        assert 'pagerank' in df.columns
        print(f"最終輸出值: columns={list(df.columns)}")


class TestCoreEfficiencyAnalyzer:
    """測試分析主題 2: 網路核心結構與解答效率"""
    
    def test_analyzer_initialization(self):
        """測試分析器初始化"""
        print("\n測試核心效率分析器初始化")
        print("輸入值: CoreEfficiencyAnalyzer()")
        
        with patch('src.analysis.core_efficiency.DataLoader'):
            from src.analysis.core_efficiency import CoreEfficiencyAnalyzer
            
            analyzer = CoreEfficiencyAnalyzer()
            
            assert analyzer is not None
            assert analyzer.builder is not None
            print("最終輸出值: 初始化成功")
    
    def test_metrics_dataclass(self):
        """測試核心指標資料類別"""
        print("\n測試核心-邊緣指標資料類別")
        print("輸入值: core_scores=[3, 5, 2]")
        
        from src.analysis.core_efficiency import CorePeripheryMetrics
        
        metrics = CorePeripheryMetrics(
            core_scores=[3, 5, 2],
            k_core=[1, 2, 1],
            is_core=[False, True, False],
        )
        
        print("中間過程: 轉換為DataFrame")
        df = metrics.to_dataframe()
        
        assert len(df) == 3
        assert 'core_score' in df.columns
        assert 'k_core' in df.columns
        assert 'is_core' in df.columns
        print(f"最終輸出值: columns={list(df.columns)}")


class TestTagCooccurrenceAnalyzer:
    """測試分析主題 3: 技術標籤共現與領域地圖"""
    
    def test_analyzer_initialization(self):
        """測試分析器初始化"""
        print("\n測試標籤共現分析器初始化")
        print("輸入值: TagCooccurrenceAnalyzer()")
        
        with patch('src.analysis.tag_cooccurrence.DataLoader'):
            from src.analysis.tag_cooccurrence import TagCooccurrenceAnalyzer
            
            analyzer = TagCooccurrenceAnalyzer()
            
            assert analyzer is not None
            assert len(analyzer.DOMAIN_KEYWORDS) > 0
            print(f"中間過程: DOMAIN_KEYWORDS={list(analyzer.DOMAIN_KEYWORDS.keys())}")
            print("最終輸出值: 初始化成功")
    
    def test_cluster_dataclass(self):
        """測試群聚資料類別"""
        print("\n測試標籤群聚資料類別")
        print("輸入值: name='Web', tags=['javascript', 'html', 'css']")
        
        from src.analysis.tag_cooccurrence import TagCluster
        
        cluster = TagCluster(
            name='Web',
            tags=['javascript', 'html', 'css'],
            avg_popularity=1000000,
            total_connections=50,
        )
        
        assert cluster.name == 'Web'
        assert len(cluster.tags) == 3
        assert cluster.avg_popularity == 1000000
        print(f"最終輸出值: avg_popularity={cluster.avg_popularity}")


class TestConnectedComponentAnalyzer:
    """測試分析主題 4: 知識孤島與連通分量分析"""
    
    def test_analyzer_initialization(self):
        """測試分析器初始化"""
        print("\n測試連通分量分析器初始化")
        print("輸入值: ConnectedComponentAnalyzer()")
        
        with patch('src.analysis.connected_components.DataLoader'):
            from src.analysis.connected_components import ConnectedComponentAnalyzer
            
            analyzer = ConnectedComponentAnalyzer()
            
            assert analyzer is not None
            assert analyzer.builder is not None
            print("最終輸出值: 初始化成功")
    
    def test_component_dataclass(self):
        """測試連通分量資料類別"""
        print("\n測試連通分量資料類別")
        print("輸入值: size=10, is_main=True")
        
        from src.analysis.connected_components import ComponentInfo
        
        component = ComponentInfo(
            component_id=0,
            size=10,
            user_ids=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            avg_reputation=500.0,
            avg_interactions=5.0,
            is_main_component=True,
        )
        
        assert component.size == 10
        assert component.is_main_component == True
        assert len(component.user_ids) == 10
        print(f"最終輸出值: avg_reputation={component.avg_reputation}")


class TestContentFeatureAnalyzer:
    """測試分析主題 5: 內容特徵與互動反響"""
    
    def test_analyzer_initialization(self):
        """測試分析器初始化"""
        print("\n測試內容特徵分析器初始化")
        print("輸入值: ContentFeatureAnalyzer()")
        
        with patch('src.analysis.content_features.DataLoader'):
            from src.analysis.content_features import ContentFeatureAnalyzer
            
            analyzer = ContentFeatureAnalyzer()
            
            assert analyzer is not None
            print("最終輸出值: 初始化成功")
    
    def test_impact_analysis_dataclass(self):
        """測試程式碼影響分析資料類別"""
        print("\n測試程式碼影響分析資料類別")
        print("輸入值: has_code_avg=15.5, no_code_avg=8.2")
        
        from src.analysis.content_features import CodeImpactAnalysis
        
        impact = CodeImpactAnalysis(
            has_code_avg_score=15.5,
            no_code_avg_score=8.2,
            t_statistic=2.5,
            p_value=0.01,
            is_significant=True,
        )
        
        assert impact.has_code_avg_score == 15.5
        assert impact.no_code_avg_score == 8.2
        assert impact.is_significant == True
        print(f"中間過程: 分數差異={impact.has_code_avg_score - impact.no_code_avg_score}")
        print(f"最終輸出值: is_significant={impact.is_significant}")


class TestAccountAgeAnalyzer:
    """測試分析主題 6: 帳號年資與社群貢獻"""
    
    def test_analyzer_initialization(self):
        """測試分析器初始化"""
        print("\n測試帳號年資分析器初始化")
        print("輸入值: AccountAgeAnalyzer()")
        
        with patch('src.analysis.account_age.DataLoader'):
            from src.analysis.account_age import AccountAgeAnalyzer
            
            analyzer = AccountAgeAnalyzer()
            
            assert analyzer is not None
            assert analyzer.builder is not None
            print("最終輸出值: 初始化成功")
    
    def test_pattern_dataclass(self):
        """測試年資貢獻模式資料類別"""
        print("\n測試年資貢獻模式資料類別")
        print("輸入值: age_level='3_Mature', avg_rep=5000.0")
        
        from src.analysis.account_age import AgeContributionPattern
        
        pattern = AgeContributionPattern(
            age_level='3_Mature',
            avg_reputation=5000.0,
            avg_questions=3.5,
            avg_answers=10.2,
            both_ratio=0.6,
            questions_only_ratio=0.2,
            answers_only_ratio=0.2,
        )
        
        assert pattern.age_level == '3_Mature'
        assert pattern.avg_reputation == 5000.0
        assert pattern.both_ratio == 0.6
        print(f"中間過程: 全能比例={pattern.both_ratio}")
        print(f"最終輸出值: avg_questions={pattern.avg_questions}, avg_answers={pattern.avg_answers}")


class TestSNARunner:
    """測試 SNA 執行器"""
    
    def test_runner_initialization(self):
        """測試執行器初始化"""
        print("\n測試SNA執行器初始化")
        print("輸入值: output_dir='output', data_limit=50")
        
        with patch('src.sna_runner.DataLoader'):
            with patch('src.sna_runner.SNAPlotter'):
                from src.sna_runner import SNARunner
                
                runner = SNARunner(output_dir='output', data_limit=50)
                
                assert runner is not None
                assert runner.data_limit == 50
                print(f"中間過程: results={runner.results}")
                print("最終輸出值: 初始化成功")


class TestVisualization:
    """測試視覺化工具"""
    
    def test_plotter_initialization(self):
        """測試繪圖工具初始化"""
        print("\n測試視覺化工具初始化")
        print("輸入值: output_dir='output'")
        
        from src.visualization.plots import SNAPlotter
        from pathlib import Path
        
        plotter = SNAPlotter(output_dir=Path('output'))
        
        assert plotter is not None
        assert 'reputation' in plotter.color_maps
        assert 'score_level' in plotter.color_maps
        assert 'account_age' in plotter.color_maps
        print(f"中間過程: color_maps keys={list(plotter.color_maps.keys())}")
        print("最終輸出值: 初始化成功")


class TestDataLoader:
    """測試資料載入器"""
    
    def test_loader_initialization(self):
        """測試資料載入器初始化"""
        print("\n測試資料載入器初始化")
        print("輸入值: DataLoader()")
        
        with patch('src.data.data_loader.BigQueryClient'):
            from src.data.data_loader import DataLoader
            
            loader = DataLoader()
            
            assert loader is not None
            assert loader._cache == {}
            print("最終輸出值: 初始化成功")
    
    def test_cache_functionality(self):
        """測試快取功能"""
        print("\n測試快取功能")
        
        mock_df = pd.DataFrame({'id': [1, 2, 3]})
        
        with patch('src.data.data_loader.BigQueryClient'):
            from src.data.data_loader import DataLoader
            
            loader = DataLoader()
            
            loader._cache['test_key'] = mock_df
            
            result = loader._cache.get('test_key')
            assert result is not None
            assert len(result) == 3
            
            loader.clear_cache()
            assert loader._cache == {}
            print("最終輸出值: 快取功能正常")


class TestGraphBuilder:
    """測試圖形建構器"""
    
    def test_user_network_builder(self):
        """測試用戶網路建構器"""
        print("\n測試用戶網路建構器")
        print("輸入值: UserNetworkBuilder()")
        
        with patch('src.models.graph_builder.DataLoader'):
            from src.models.graph_builder import UserNetworkBuilder
            
            builder = UserNetworkBuilder()
            
            assert builder is not None
            assert builder.graph is None
            print("最終輸出值: 初始化成功")
    
    def test_tag_network_builder(self):
        """測試標籤網路建構器"""
        print("\n測試標籤網路建構器")
        print("輸入值: TagNetworkBuilder()")
        
        with patch('src.models.graph_builder.DataLoader'):
            from src.models.graph_builder import TagNetworkBuilder
            
            builder = TagNetworkBuilder()
            
            assert builder is not None
            print("最終輸出值: 初始化成功")


class TestCLI:
    """測試命令列介面"""
    
    def test_cli_help(self):
        """測試 CLI 幫助訊息"""
        print("\n測試 CLI 幫助訊息")
        
        import subprocess
        import sys
        result = subprocess.run(
            [sys.executable, 'main.py', '--help'],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert 'Stack Overflow' in result.stdout
        assert '--run' in result.stdout
        print("最終輸出值: 幫助訊息正確顯示")
    
    def test_cli_list(self):
        """測試 CLI 列表功能"""
        print("\n測試 CLI 列表功能")
        
        import subprocess
        import sys
        result = subprocess.run(
            [sys.executable, 'main.py', '--list'],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert '使用者聲望與網路中心度' in result.stdout
        assert '技術標籤共現' in result.stdout
        print("最終輸出值: 分析主題列表正確顯示")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
