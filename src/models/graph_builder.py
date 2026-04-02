"""
圖形建構器 - 使用 igraph 建構社會網路圖
"""

from typing import List, Optional, Tuple, Dict, Any

import pandas as pd
import numpy as np
from igraph import Graph, Vertex

from ..data.data_loader import DataLoader


class GraphBuilder:
    """基礎圖形建構器"""
    
    def __init__(self, data_loader: Optional[DataLoader] = None):
        self.data_loader = data_loader or DataLoader()
        self.graph: Optional[Graph] = None
    
    def get_vertex_attributes(self) -> List[str]:
        """取得頂點屬性列表"""
        return []
    
    def get_edge_attributes(self) -> List[str]:
        """取得邊屬性列表"""
        return ["weight"]
    
    def build(self, **kwargs) -> Graph:
        """建構圖形（子類別需實作）"""
        raise NotImplementedError


class UserNetworkBuilder(GraphBuilder):
    """使用者網路建構器 - 分析主題 1, 2, 4, 6"""
    
    def build_answer_network(self, limit: int = 100) -> Graph:
        """
        建構回答者→發問者網路
        用於分析主題 1: 使用者聲望與網路中心度
        """
        posts_df = self.data_loader.load_posts_with_answers(limit=limit)
        
        edges = []
        edge_weights = []
        
        for _, row in posts_df.iterrows():
            if pd.notna(row['answerer_id']) and pd.notna(row['questioner_id']):
                edges.append((row['answerer_id'], row['questioner_id']))
                edge_weights.append(1)
        
        self.graph = Graph(directed=True)
        self.graph.add_vertices(range(limit * 2))
        self.graph.add_edges(edges)
        
        unique_users = list(set([e[0] for e in edges] + [e[1] for e in edges]))
        self.graph = Graph(directed=True)
        self.graph.add_vertices(len(unique_users))
        
        name_to_idx = {name: idx for idx, name in enumerate(unique_users)}
        
        weighted_edges = []
        edge_weight_list = []
        for e in edges:
            if e[0] in name_to_idx and e[1] in name_to_idx:
                weighted_edges.append((name_to_idx[e[0]], name_to_idx[e[1]]))
                edge_weight_list.append(1)
        
        self.graph.add_edges(weighted_edges)
        self.graph.es['weight'] = edge_weight_list
        
        self.graph.vs['user_id'] = [unique_users[i] if i < len(unique_users) else None 
                                    for i in range(len(self.graph.vs))]
        self.graph.vs['name'] = [f"User_{unique_users[i]}" if i < len(unique_users) else f"V{i}" 
                                 for i in range(len(self.graph.vs))]
        
        return self.graph
    
    def build_answer_network_with_reputation(self, limit: int = 100) -> Tuple[Graph, pd.DataFrame]:
        """建構含聲望資訊的回答網路（研究方法1: 使用者聲望與網路中心度）"""
        posts_df = self.data_loader.load_posts_with_answers(limit=limit)
        
        edge_counts = {}
        for _, row in posts_df.iterrows():
            if pd.notna(row['answerer_id']) and pd.notna(row['questioner_id']):
                key = (row['answerer_id'], row['questioner_id'])
                edge_counts[key] = edge_counts.get(key, 0) + 1
        
        unique_users = list(set([e[0] for e in edge_counts.keys()] + [e[1] for e in edge_counts.keys()]))
        
        users_df = self.data_loader.load_users(user_ids=unique_users)
        
        user_reputation = dict(zip(users_df['id'], users_df['reputation']))
        user_reputation_level = dict(zip(users_df['id'], users_df['reputation_level']))
        
        self.graph = Graph(directed=True)
        self.graph.add_vertices(len(unique_users))
        
        name_to_idx = {name: idx for idx, name in enumerate(unique_users)}
        
        weighted_edges = []
        weights = []
        for (src, dst), count in edge_counts.items():
            if src in name_to_idx and dst in name_to_idx:
                weighted_edges.append((name_to_idx[src], name_to_idx[dst]))
                weights.append(count)
        
        self.graph.add_edges(weighted_edges)
        self.graph.es['weight'] = weights
        
        self.graph.vs['user_id'] = unique_users
        self.graph.vs['reputation'] = [user_reputation.get(uid, 0) for uid in unique_users]
        self.graph.vs['reputation_level'] = [user_reputation_level.get(uid, '0_None') for uid in unique_users]
        self.graph.vs['name'] = [f"U{uid}" for uid in unique_users]
        
        betweenness = self.graph.betweenness(directed=True)
        median_bt = np.median(betweenness) if betweenness else 0
        self.graph.vs['betweenness'] = betweenness
        self.graph.vs['centrality_level'] = ['high' if b >= median_bt else 'low' for b in betweenness]
        
        return self.graph, users_df[users_df['id'].isin(unique_users)]
    
    def build_connectivity_network(self, limit: int = 100) -> Tuple[Graph, pd.DataFrame]:
        """
        建構用戶連通性網路
        用於分析主題 4: 知識孤島與連通分量分析
        基於問答關係建立網路
        """
        posts_df = self.data_loader.load_posts_with_answers(limit=limit)
        
        edge_counts = {}
        for _, row in posts_df.iterrows():
            if pd.notna(row['answerer_id']) and pd.notna(row['questioner_id']):
                key = (row['answerer_id'], row['questioner_id'])
                edge_counts[key] = edge_counts.get(key, 0) + 1
        
        unique_users = list(set([e[0] for e in edge_counts.keys()] + [e[1] for e in edge_counts.keys()]))
        
        connectivity_df = self.data_loader.load_user_connectivity(limit=limit * 2, user_ids=unique_users)
        connectivity_df_filtered = connectivity_df[connectivity_df['user_id'].isin(unique_users)]
        
        user_data = {}
        for _, row in connectivity_df_filtered.iterrows():
            user_data[row['user_id']] = {
                'reputation': row['reputation'],
                'total_interactions': row['total_interactions'],
                'connectivity_level': row['connectivity_level'],
            }
        
        self.graph = Graph(directed=False)
        self.graph.add_vertices(len(unique_users))
        
        name_to_idx = {uid: idx for idx, uid in enumerate(unique_users)}
        
        weighted_edges = []
        weights = []
        for (src, dst), count in edge_counts.items():
            if src in name_to_idx and dst in name_to_idx:
                weighted_edges.append((name_to_idx[src], name_to_idx[dst]))
                weights.append(count)
        
        self.graph.add_edges(weighted_edges)
        self.graph.es['weight'] = weights
        
        undirected = self.graph.as_undirected()
        components = undirected.components()
        largest_component = max(components, key=len)
        main_component_indices = set(largest_component)
        
        self.graph.vs['user_id'] = unique_users
        self.graph.vs['name'] = [f"U{uid}" for uid in unique_users]
        self.graph.vs['reputation'] = [user_data.get(uid, {}).get('reputation', 0) for uid in unique_users]
        self.graph.vs['total_interactions'] = [user_data.get(uid, {}).get('total_interactions', 0) for uid in unique_users]
        self.graph.vs['connectivity_level'] = [user_data.get(uid, {}).get('connectivity_level', '0_None') for uid in unique_users]
        
        self.graph.vs['connectivity_type'] = ['main_component' if idx in main_component_indices else 'isolated' 
                                              for idx in range(len(unique_users))]
        self.graph.vs['interaction_type'] = ['continuous' if user_data.get(uid, {}).get('total_interactions', 0) > 1 else 'single'
                                            for uid in unique_users]
        
        return self.graph, connectivity_df
    
    def build_account_age_network(self, limit: int = 100) -> Tuple[Graph, pd.DataFrame]:
        """
        建構帳號年資網路
        用於分析主題 6: 帳號年資與社群貢獻
        基於問答關係建立網路
        """
        posts_df = self.data_loader.load_posts_with_answers(limit=limit)
        
        edge_counts = {}
        for _, row in posts_df.iterrows():
            if pd.notna(row['answerer_id']) and pd.notna(row['questioner_id']):
                key = (row['answerer_id'], row['questioner_id'])
                edge_counts[key] = edge_counts.get(key, 0) + 1
        
        unique_users = list(set([e[0] for e in edge_counts.keys()] + [e[1] for e in edge_counts.keys()]))
        
        age_df = self.data_loader.load_account_age(limit=limit * 2, user_ids=unique_users)
        age_df_filtered = age_df[age_df['user_id'].isin(unique_users)]
        
        user_data = {}
        for _, row in age_df_filtered.iterrows():
            user_data[row['user_id']] = {
                'reputation': row['reputation'],
                'account_age_days': row['account_age_days'],
                'account_age_level': row['account_age_level'],
                'post_type': row['post_type'],
                'question_count': row['question_count'],
                'answer_count': row['answer_count'],
            }
        
        self.graph = Graph(directed=False)
        self.graph.add_vertices(len(unique_users))
        
        name_to_idx = {uid: idx for idx, uid in enumerate(unique_users)}
        
        weighted_edges = []
        weights = []
        for (src, dst), count in edge_counts.items():
            if src in name_to_idx and dst in name_to_idx:
                weighted_edges.append((name_to_idx[src], name_to_idx[dst]))
                weights.append(count)
        
        self.graph.add_edges(weighted_edges)
        self.graph.es['weight'] = weights
        
        self.graph.vs['user_id'] = unique_users
        self.graph.vs['name'] = [f"U{uid}" for uid in unique_users]
        self.graph.vs['reputation'] = [user_data.get(uid, {}).get('reputation', 0) for uid in unique_users]
        self.graph.vs['account_age_days'] = [user_data.get(uid, {}).get('account_age_days', 0) for uid in unique_users]
        self.graph.vs['account_age_level'] = [user_data.get(uid, {}).get('account_age_level', '0_None') for uid in unique_users]
        self.graph.vs['post_type'] = [user_data.get(uid, {}).get('post_type', '4_Neither') for uid in unique_users]
        self.graph.vs['question_count'] = [int(user_data.get(uid, {}).get('question_count', 0)) for uid in unique_users]
        self.graph.vs['answer_count'] = [int(user_data.get(uid, {}).get('answer_count', 0)) for uid in unique_users]
        
        return self.graph, age_df


class TagNetworkBuilder(GraphBuilder):
    """標籤網路建構器 - 分析主題 3"""
    
    TAG_DOMAINS = {
        'Web': ['javascript', 'html', 'css', 'react', 'angular', 'vue', 'jquery', 'ajax', 
                'node.js', 'nodejs', 'webpack', 'sass', 'bootstrap', 'typescript', 'html5'],
        'AI_ML': ['python', 'tensorflow', 'pytorch', 'keras', 'machine-learning', 'deep-learning', 
                  'nlp', 'neural-network', 'scikit-learn', 'pandas', 'numpy', 'data-science', 'ai'],
        'Mobile': ['android', 'ios', 'swift', 'kotlin', 'flutter', 'react-native', 'xamarin', 'objective-c', 'mobile'],
        'DataScience': ['pandas', 'numpy', 'matplotlib', 'jupyter', 'r', 'statistics', 'data-analysis', 
                       'visualization', 'data-science', 'bigdata', 'spark'],
        'Backend': ['java', 'c#', 'ruby', 'php', 'go', 'rust', 'scala', 'spring', 'django', 'flask', 
                   'rails', 'laravel', 'express', '.net', 'asp.net', 'spring-boot', 'python-3.x'],
        'Database': ['sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'oracle', 
                    'sqlite', 'nosql', 'database', 'postgresql', 'mariadb', 'firebase'],
        'DevOps': ['docker', 'kubernetes', 'aws', 'azure', 'gcp', 'jenkins', 'ci-cd', 'linux', 
                  'bash', 'terraform', 'ansible', 'nginx', 'apache', 'git', 'github', 'devops'],
    }
    
    def _get_tag_domain(self, tag: str) -> str:
        """根據標籤名稱判斷技術領域"""
        tag_lower = tag.lower()
        for domain, keywords in self.TAG_DOMAINS.items():
            if any(kw in tag_lower for kw in keywords):
                return domain
        return 'Other'
    
    def build_tag_cooccurrence_network(self, limit: int = 100) -> Tuple[Graph, pd.DataFrame]:
        """
        建構標籤共現網路
        用於研究方法3: 技術標籤共現與領域地圖
        """
        tag_df = self.data_loader.load_tag_cooccurrence(limit=limit)
        popularity_df = self.data_loader.load_tags_popularity(limit=limit)
        
        unique_tags = list(set(tag_df['tag1'].tolist() + tag_df['tag2'].tolist()))
        tag_popularity = dict(zip(popularity_df['tag_name'], popularity_df['usage_count']))
        
        self.graph = Graph(directed=False)
        self.graph.add_vertices(len(unique_tags))
        
        name_to_idx = {name: idx for idx, name in enumerate(unique_tags)}
        
        edges = []
        weights = []
        for _, row in tag_df.iterrows():
            if row['tag1'] in name_to_idx and row['tag2'] in name_to_idx:
                edges.append((name_to_idx[row['tag1']], name_to_idx[row['tag2']]))
                weights.append(int(row['co_occurrence_count']))
        
        self.graph.add_edges(edges)
        self.graph.es['weight'] = weights
        
        self.graph.vs['tag_name'] = unique_tags
        self.graph.vs['popularity'] = [tag_popularity.get(tag, 0) for tag in unique_tags]
        self.graph.vs['tech_domain'] = [self._get_tag_domain(tag) for tag in unique_tags]
        self.graph.vs['name'] = unique_tags
        
        return self.graph, tag_df


class CorePeripheryBuilder(GraphBuilder):
    """核心-邊緣網路建構器 - 分析主題 2"""
    
    def build_core_periphery_network(self, limit: int = 100) -> Tuple[Graph, pd.DataFrame]:
        """
        建構核心-邊緣結構網路
        用於研究方法2: 網路核心結構與解答效率
        """
        posts_df = self.data_loader.load_posts_with_answers(limit=limit)
        
        edge_counts = {}
        answer_time_levels = {}
        for _, row in posts_df.iterrows():
            if pd.notna(row['answerer_id']) and pd.notna(row['questioner_id']):
                key = (row['answerer_id'], row['questioner_id'])
                edge_counts[key] = edge_counts.get(key, 0) + 1
                answer_time_levels[row['questioner_id']] = row.get('answer_time_level', '0_Unresolved')
        
        unique_users = list(set([e[0] for e in edge_counts.keys()] + [e[1] for e in edge_counts.keys()]))
        
        self.graph = Graph(directed=False)
        self.graph.add_vertices(len(unique_users))
        
        name_to_idx = {uid: idx for idx, uid in enumerate(unique_users)}
        
        weighted_edges = []
        weights = []
        for (src, dst), count in edge_counts.items():
            if src in name_to_idx and dst in name_to_idx:
                weighted_edges.append((name_to_idx[src], name_to_idx[dst]))
                weights.append(count)
        
        self.graph.add_edges(weighted_edges)
        self.graph.es['weight'] = weights
        
        undirected = self.graph.as_undirected()
        degrees = undirected.degree()
        median_deg = np.median(degrees) if degrees else 0
        
        self.graph.vs['user_id'] = unique_users
        self.graph.vs['name'] = [f"U{uid}" for uid in unique_users]
        self.graph.vs['degree'] = degrees
        self.graph.vs['is_core'] = [d >= median_deg for d in degrees]
        self.graph.vs['answer_time_level'] = [answer_time_levels.get(uid, '0_Unresolved') for uid in unique_users]
        
        return self.graph, posts_df
