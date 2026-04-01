#!/usr/bin/env python3
"""
直接執行社會網路分析的腳本
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.sna_runner import SNARunner


def main():
    """主函數"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Stack Overflow Social Network Analysis')
    parser.add_argument('--limit', type=int, default=100, help='Number of records to analyze')
    parser.add_argument('--output', type=str, default='output', help='Output directory')
    parser.add_argument('--analysis', type=str, default='all', 
                       choices=['all', '1', '2', '3', '4', '5', '6'],
                       help='Which analysis to run')
    
    args = parser.parse_args()
    
    if args.analysis == 'all':
        runner = SNARunner(output_dir=args.output, data_limit=args.limit)
        runner.run_all()
    else:
        from src.analysis import (
            CentralityAnalyzer,
            CoreEfficiencyAnalyzer,
            TagCooccurrenceAnalyzer,
            ConnectedComponentAnalyzer,
            ContentFeatureAnalyzer,
            AccountAgeAnalyzer,
        )
        
        analyzers = {
            '1': CentralityAnalyzer,
            '2': CoreEfficiencyAnalyzer,
            '3': TagCooccurrenceAnalyzer,
            '4': ConnectedComponentAnalyzer,
            '5': ContentFeatureAnalyzer,
            '6': AccountAgeAnalyzer,
        }
        
        analyzer_class = analyzers[args.analysis]
        analyzer = analyzer_class()
        result = analyzer.run(limit=args.limit)
        
        print("\n" + "=" * 60)
        print(f"Analysis {args.analysis} completed successfully!")
        print("=" * 60)
        print("\nSummary:")
        for key, value in result.get('summary', {}).items():
            print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
