"""
分析主題 6: 帳號年資與社群貢獻 (補充)
=====================================
分析老手與新手的行為差異：分析不同帳號年資的使用者在社群中的發文類型差異
"""

from typing import Dict, Any, List
from dataclasses import dataclass

import pandas as pd
import numpy as np
import igraph as ig

from ..data.data_loader import DataLoader
from ..models.graph_builder import UserNetworkBuilder


@dataclass
class AgeContributionPattern:
    """年資貢獻模式"""
    age_level: str
    avg_reputation: float
    avg_questions: float
    avg_answers: float
    both_ratio: float
    questions_only_ratio: float
    answers_only_ratio: float


class AccountAgeAnalyzer:
    """帳號年資與社群貢獻分析器"""
    
    def __init__(self, data_loader: DataLoader = None):
        self.data_loader = data_loader or DataLoader()
        self.builder = UserNetworkBuilder(self.data_loader)
        self.graph: ig.Graph = None
        self.age_df: pd.DataFrame = None
    
    def run(self, limit: int = 100) -> Dict[str, Any]:
        """
        執行完整分析
        
        Returns:
            Dict containing analysis results
        """
        print("\n" + "=" * 60)
        print("分析主題 6: 帳號年資與社群貢獻分析")
        print("=" * 60)
        
        self.graph, self.age_df = self.builder.build_account_age_network(limit=limit)
        
        print(f"\n測試帳號年資與社群貢獻功能")
        print(f"輸入值: limit={limit}")
        print(f"中間過程: 分析 {len(self.age_df)} 個用戶的帳號年資與發文類型...")
        
        patterns = self._analyze_age_contribution_patterns()
        
        behavior_evolution = self._analyze_behavior_evolution(patterns)
        
        result = self._generate_summary(patterns, behavior_evolution)
        
        print(f"最終輸出值:")
        print(f"  - 新手(問題為主)比例: {result['newcomer_questions_only_ratio']:.1%}")
        print(f"  - 老手(回答為主)比例: {result['senior_answers_only_ratio']:.1%}")
        print(f"  - 全能型用戶比例: {result['veteran_both_ratio']:.1%}")
        
        return {
            'graph': self.graph,
            'age_df': self.age_df,
            'patterns': patterns,
            'behavior_evolution': behavior_evolution,
            'summary': result,
        }
    
    def _analyze_age_contribution_patterns(self) -> List[AgeContributionPattern]:
        """分析年資貢獻模式"""
        print(f"\n中間過程: 分析不同年資層級的貢獻模式...")
        
        patterns = []
        
        age_levels = sorted(self.age_df['account_age_level'].unique())
        
        for level in age_levels:
            level_df = self.age_df[self.age_df['account_age_level'] == level]
            
            avg_rep = level_df['reputation'].mean()
            avg_q = level_df['question_count'].mean()
            avg_a = level_df['answer_count'].mean()
            
            total = len(level_df)
            both = len(level_df[level_df['post_type'] == '1_Both'])
            q_only = len(level_df[level_df['post_type'] == '2_QuestionsOnly'])
            a_only = len(level_df[level_df['post_type'] == '3_AnswersOnly'])
            
            patterns.append(AgeContributionPattern(
                age_level=level,
                avg_reputation=avg_rep,
                avg_questions=avg_q,
                avg_answers=avg_a,
                both_ratio=both / total if total > 0 else 0,
                questions_only_ratio=q_only / total if total > 0 else 0,
                answers_only_ratio=a_only / total if total > 0 else 0,
            ))
        
        return patterns
    
    def _analyze_behavior_evolution(self, patterns: List[AgeContributionPattern]) -> Dict[str, Any]:
        """分析行為演變"""
        print(f"\n中間過程: 分析新手到老手的行為演變...")
        
        if not patterns:
            return {}
        
        evolution = {
            'reputation_growth': {},
            'question_trend': {},
            'answer_trend': {},
        }
        
        for p in patterns:
            level_short = p.age_level.split('_')[1] if '_' in p.age_level else p.age_level
            evolution['reputation_growth'][level_short] = p.avg_reputation
            evolution['question_trend'][level_short] = p.avg_questions
            evolution['answer_trend'][level_short] = p.avg_answers
        
        new_users = next((p for p in patterns if 'New' in p.age_level), None)
        seniors = next((p for p in patterns if 'Senior' in p.age_level), None)
        
        if new_users and seniors:
            evolution['reputation_gap'] = seniors.avg_reputation - new_users.avg_reputation
            evolution['question_trend_direction'] = 'decreasing' if seniors.avg_questions < new_users.avg_questions else 'increasing'
            evolution['answer_trend_direction'] = 'increasing' if seniors.avg_answers > new_users.avg_answers else 'decreasing'
        
        return evolution
    
    def _generate_summary(self, patterns: List[AgeContributionPattern],
                         evolution: Dict[str, Any]) -> Dict[str, Any]:
        """生成分析摘要"""
        print(f"\n中間過程: 生成分析摘要...")
        
        newcomer = next((p for p in patterns if 'New' in p.age_level), None)
        senior = next((p for p in patterns if 'Senior' in p.age_level), None)
        veteran = next((p for p in patterns if p.answers_only_ratio > 0.5), None)
        
        summary = {
            'total_users': len(self.age_df),
            'age_level_distribution': {
                p.age_level: {
                    'count': len(self.age_df[self.age_df['account_age_level'] == p.age_level]),
                    'avg_reputation': p.avg_reputation,
                }
                for p in patterns
            },
            'newcomer_questions_only_ratio': newcomer.questions_only_ratio if newcomer else 0,
            'senior_answers_only_ratio': senior.answers_only_ratio if senior else 0,
            'veteran_both_ratio': veteran.both_ratio if veteran else 0,
            'avg_account_age_days': self.age_df['account_age_days'].mean(),
            'behavior_evolution': evolution,
            'hypothesis_newbie_asks_more': newcomer.avg_questions > senior.avg_questions if newcomer and senior else False,
            'hypothesis_veteran_answers_more': senior.avg_answers > newcomer.avg_answers if senior and newcomer else False,
        }
        
        return summary
    
    def get_post_type_by_age(self) -> pd.DataFrame:
        """取得不同年資的發文類型分佈"""
        if self.age_df is None:
            return pd.DataFrame()
        
        return self.age_df.groupby(['account_age_level', 'post_type']).size().unstack(fill_value=0)
    
    def get_activity_correlation(self) -> Dict[str, float]:
        """取得年資與活動的相關性"""
        if self.age_df is None:
            return {}
        
        return {
            'age_vs_reputation': self.age_df['account_age_days'].corr(self.age_df['reputation']),
            'age_vs_questions': self.age_df['account_age_days'].corr(self.age_df['question_count']),
            'age_vs_answers': self.age_df['account_age_days'].corr(self.age_df['answer_count']),
            'age_vs_total_posts': self.age_df['account_age_days'].corr(
                self.age_df['question_count'] + self.age_df['answer_count']
            ),
        }
