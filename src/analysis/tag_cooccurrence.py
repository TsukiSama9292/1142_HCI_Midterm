"""
分析主題 3: 技術標籤共現與領域地圖
===================================
建構技術領域發展地圖：透過技術標籤的共現分析，描繪出不同程式語言或框架之間的群聚效應和技術關聯性
"""

from typing import Dict, Any, List
from dataclasses import dataclass

import pandas as pd
import igraph as ig

from ..data.data_loader import DataLoader
from ..models.graph_builder import TagNetworkBuilder


@dataclass
class TagCluster:
    """標籤群聚"""
    name: str
    tags: List[str]
    avg_popularity: float
    total_connections: int


class TagCooccurrenceAnalyzer:
    """技術標籤共現與領域地圖分析器"""
    
    DOMAIN_KEYWORDS = {
        'Web': ['javascript', 'html', 'css', 'react', 'angular', 'vue', 'jquery', 'ajax', 'node.js', 'nodejs', 'webpack', 'sass', 'bootstrap'],
        'Backend': ['python', 'java', 'c#', 'ruby', 'php', 'go', 'rust', 'scala', 'spring', 'django', 'flask', 'rails', 'laravel'],
        'Database': ['sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'oracle', 'sqlite', 'nosql', 'database'],
        'Mobile': ['android', 'ios', 'swift', 'kotlin', 'flutter', 'react-native', 'xamarin', 'objective-c'],
        'AI_ML': ['python', 'tensorflow', 'pytorch', 'keras', 'machine-learning', 'deep-learning', 'nlp', 'neural-network', 'scikit-learn'],
        'DevOps': ['docker', 'kubernetes', 'aws', 'azure', 'gcp', 'jenkins', 'ci/cd', 'terraform', 'linux', 'bash'],
        'DataScience': ['pandas', 'numpy', 'matplotlib', 'jupyter', 'r', 'statistics', 'data-analysis', 'visualization'],
    }
    
    def __init__(self, data_loader: DataLoader = None):
        self.data_loader = data_loader or DataLoader()
        self.builder = TagNetworkBuilder(self.data_loader)
        self.graph: ig.Graph = None
        self.tag_df: pd.DataFrame = None
        self.popularity_df: pd.DataFrame = None
    
    def run(self, limit: int = 100) -> Dict[str, Any]:
        """
        執行完整分析
        
        Returns:
            Dict containing analysis results
        """
        print("\n" + "=" * 60)
        print("分析主題 3: 技術標籤共現與領域地圖分析")
        print("=" * 60)
        
        self.graph, self.tag_df = self.builder.build_tag_cooccurrence_network(limit=limit)
        
        print("\n測試技術標籤共現與領域地圖功能")
        print(f"輸入值: limit={limit}")
        print(f"中間過程: 建立 {len(self.graph.vs)} 個標籤節點, {len(self.graph.es)} 條共現關係邊")
        
        clusters = self._identify_technology_domains()
        
        community_structure = self._analyze_community_structure()
        
        result = self._generate_summary(clusters, community_structure)
        
        print("最終輸出值:")
        print(f"  - 識別出 {len(clusters)} 個技術領域")
        for cluster in clusters[:5]:
            print(f"    * {cluster.name}: {len(cluster.tags)} 個標籤")
        
        return {
            'graph': self.graph,
            'tag_df': self.tag_df,
            'clusters': clusters,
            'community_structure': community_structure,
            'summary': result,
        }
    
    def _identify_technology_domains(self) -> List[TagCluster]:
        """識別技術領域群聚"""
        print("\n中間過程: 識別技術領域群聚...")
        
        clusters = []
        tag_to_domain = {}
        
        for tag in self.graph.vs['tag_name']:
            tag_lower = tag.lower()
            assigned = False
            for domain, keywords in self.DOMAIN_KEYWORDS.items():
                if any(kw in tag_lower for kw in keywords):
                    if domain not in [c.name for c in clusters]:
                        clusters.append(TagCluster(
                            name=domain,
                            tags=[],
                            avg_popularity=0,
                            total_connections=0
                        ))
                    idx = [c.name for c in clusters].index(domain)
                    clusters[idx].tags.append(tag)
                    tag_to_domain[tag] = domain
                    assigned = True
                    break
            if not assigned:
                if 'Other' not in [c.name for c in clusters]:
                    clusters.append(TagCluster(
                        name='Other',
                        tags=[],
                        avg_popularity=0,
                        total_connections=0
                    ))
                idx = [c.name for c in clusters].index('Other')
                clusters[idx].tags.append(tag)
                tag_to_domain[tag] = 'Other'
        
        for cluster in clusters:
            if cluster.tags:
                popularities = [self.graph.vs['popularity'][self.graph.vs['tag_name'].index(t)] 
                              for t in cluster.tags if t in self.graph.vs['tag_name']]
                cluster.avg_popularity = sum(popularities) / len(popularities) if popularities else 0
                
                conn_count = 0
                for t in cluster.tags:
                    if t in self.graph.vs['tag_name']:
                        idx = self.graph.vs['tag_name'].index(t)
                        conn_count += len(self.graph.neighbors(idx))
                cluster.total_connections = conn_count
        
        return clusters
    
    def _analyze_community_structure(self) -> Dict[str, Any]:
        """分析社群結構"""
        print("\n中間過程: 分析社群結構...")
        
        if len(self.graph.vs) < 2:
            return {'num_communities': 0, 'modularity': 0, 'community_sizes': []}
        
        try:
            dendrogram = self.graph.community_fastgreedy()
            communities = dendrogram.as_clustering()
            
            community_sizes = [len(c) for c in communities]
            modularity = self.graph.modularity(communities.membership)
            
            community_info = {}
            for i, community in enumerate(communities):
                tags = [self.graph.vs[idx]['tag_name'] for idx in community]
                community_info[f'Community_{i+1}'] = {
                    'size': len(community),
                    'tags': tags,
                }
            
            return {
                'num_communities': len(communities),
                'modularity': modularity,
                'community_sizes': community_sizes,
                'community_info': community_info,
            }
        except Exception as e:
            print(f"社群偵測失敗: {e}")
            return {'num_communities': 1, 'modularity': 0, 'community_sizes': [len(self.graph.vs)]}
    
    def _generate_summary(self, clusters: List[TagCluster], community: Dict[str, Any]) -> Dict[str, Any]:
        """生成分析摘要"""
        print("\n中間過程: 生成分析摘要...")
        
        summary = {
            'total_tags': len(self.graph.vs),
            'total_cooccurrences': len(self.graph.es),
            'num_domains': len(clusters),
            'num_communities': community['num_communities'],
            'modularity': community['modularity'],
            'domain_details': {
                c.name: {
                    'tag_count': len(c.tags),
                    'avg_popularity': c.avg_popularity,
                    'total_connections': c.total_connections,
                    'tags': c.tags[:10],
                }
                for c in clusters
            },
        }
        
        return summary
    
    def get_tag_centrality(self) -> pd.DataFrame:
        """取得標籤中心度排名"""
        if self.graph is None:
            return pd.DataFrame()
        
        degree = self.graph.degree()
        betweenness = self.graph.betweenness()
        
        df = pd.DataFrame({
            'tag_name': self.graph.vs['tag_name'],
            'popularity': self.graph.vs['popularity'],
            'degree': degree,
            'betweenness': betweenness,
        })
        
        return df.sort_values('betweenness', ascending=False)
    
    def get_domain_distribution(self) -> pd.DataFrame:
        """取得領域分佈"""
        clusters = self._identify_technology_domains()
        
        return pd.DataFrame([{
            'domain': c.name,
            'tag_count': len(c.tags),
            'avg_popularity': c.avg_popularity,
            'total_connections': c.total_connections,
        } for c in clusters])
