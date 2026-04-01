"""
Stack Overflow Social Network Analysis (SNA)
命令列工具 - 執行社會網路分析
"""

import argparse
import sys
import warnings

warnings.filterwarnings('ignore')

from src.sna_runner import SNARunner
from src.analysis import (
    CentralityAnalyzer,
    CoreEfficiencyAnalyzer,
    TagCooccurrenceAnalyzer,
    ConnectedComponentAnalyzer,
    ContentFeatureAnalyzer,
    AccountAgeAnalyzer,
)


ANALYSIS_MODULES = {
    '1': ('CentralityAnalyzer', '使用者聲望與網路中心度'),
    '2': ('CoreEfficiencyAnalyzer', '網路核心結構與解答效率'),
    '3': ('TagCooccurrenceAnalyzer', '技術標籤共現與領域地圖'),
    '4': ('ConnectedComponentAnalyzer', '知識孤島與連通分量分析'),
    '5': ('ContentFeatureAnalyzer', '內容特徵與互動反響'),
    '6': ('AccountAgeAnalyzer', '帳號年資與社群貢獻'),
}


def print_banner():
    print("=" * 70)
    print("Stack Overflow 社會網路分析 (Social Network Analysis)")
    print("=" * 70)
    print()


def run_analysis(analysis_id: str, limit: int, output_dir: str):
    """執行單一分析"""
    if analysis_id not in ANALYSIS_MODULES:
        print(f"錯誤: 無效的分析 ID '{analysis_id}'")
        print(f"可用選項: {', '.join(ANALYSIS_MODULES.keys())}")
        return 1
    
    analyzer_class_name, analysis_name = ANALYSIS_MODULES[analysis_id]
    
    print(f"\n{'=' * 70}")
    print(f"執行分析 {analysis_id}: {analysis_name}")
    print(f"{'=' * 70}")
    
    analyzer_map = {
        'CentralityAnalyzer': CentralityAnalyzer,
        'CoreEfficiencyAnalyzer': CoreEfficiencyAnalyzer,
        'TagCooccurrenceAnalyzer': TagCooccurrenceAnalyzer,
        'ConnectedComponentAnalyzer': ConnectedComponentAnalyzer,
        'ContentFeatureAnalyzer': ContentFeatureAnalyzer,
        'AccountAgeAnalyzer': AccountAgeAnalyzer,
    }
    
    analyzer_class = analyzer_map[analyzer_class_name]
    analyzer = analyzer_class()
    result = analyzer.run(limit=limit)
    
    print(f"\n{'=' * 70}")
    print(f"分析 {analysis_id} 完成!")
    print(f"{'=' * 70}")
    
    print("\n摘要:")
    for key, value in result.get('summary', {}).items():
        if not isinstance(value, (dict, list)):
            print(f"  {key}: {value}")
    
    return 0


def run_all_analyses(limit: int, output_dir: str):
    """執行所有分析"""
    print("\n" + "=" * 70)
    print("執行所有 6 個分析主題")
    print("=" * 70)
    
    runner = SNARunner(output_dir=output_dir, data_limit=limit)
    runner.run_all()
    
    print("\n" + "=" * 70)
    print("所有分析完成!")
    print("=" * 70)
    
    return 0


def main():
    """主函數"""
    parser = argparse.ArgumentParser(
        description='Stack Overflow Social Network Analysis (SNA)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
範例:
  python main.py                          # 顯示此幫助
  python main.py --list                   # 列出所有分析主題
  python main.py --run 1                  # 執行分析 1
  python main.py --run all                # 執行所有分析
  python main.py --run 3 --limit 200      # 執行分析 3，取 200 筆記錄
  python main.py --run 1 -o output/       # 指定輸出目錄

分析主題:
  1. 使用者聲望與網路中心度
  2. 網路核心結構與解答效率
  3. 技術標籤共現與領域地圖
  4. 知識孤島與連通分量分析
  5. 內容特徵與互動反響
  6. 帳號年資與社群貢獻
"""
    )
    
    parser.add_argument(
        '--list', '-l',
        action='store_true',
        help='列出所有可用的分析主題'
    )
    
    parser.add_argument(
        '--run', '-r',
        type=str,
        default='all',
        help='執行指定分析 (1-6 或 all，預設: all)'
    )
    
    parser.add_argument(
        '--limit',
        type=int,
        default=100,
        help='查詢的資料筆數 (預設: 100)'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        default='output',
        help='輸出目錄 (預設: output)'
    )
    
    parser.add_argument(
        '--version', '-v',
        action='version',
        version='%(prog)s 1.0.0'
    )
    
    args = parser.parse_args()
    
    print_banner()
    
    if args.list:
        print("可用的分析主題:")
        print("-" * 50)
        for aid, (name, desc) in ANALYSIS_MODULES.items():
            print(f"  {aid}. {desc}")
        print("-" * 50)
        print("  all. 執行所有分析")
        print()
        return 0
    
    run_id = str(args.run).lower()
    
    if run_id == 'all':
        return run_all_analyses(args.limit, args.output)
    elif run_id in ANALYSIS_MODULES:
        return run_analysis(run_id, args.limit, args.output)
    else:
        print(f"錯誤: 無效的選擇 '{args.run}'")
        print(f"可用選項: {', '.join(ANALYSIS_MODULES.keys())} 或 all")
        return 1


if __name__ == "__main__":
    sys.exit(main())
