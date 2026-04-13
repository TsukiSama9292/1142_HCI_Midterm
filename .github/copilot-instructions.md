# Stack Overflow SNA - AI Agent Guidelines

## High-Level Architecture

**Data Flow Pipeline:**
```
BigQuery Public Dataset (9 tables)
    └─ DataLoader (caching layer)
       └─ GraphBuilder subclasses (igraph construction)
          └─ 15 Analyzer classes (SNA algorithms)
             └─ SNAPlotter + JSON output (results/)
```

**Key Design**: The project uses the **Builder Pattern** to avoid duplicating BigQuery queries:
- **Shared Builders**: `UserNetworkBuilder` (used by Analyses 1, 2, 4, 6)
- **Specialized Builders**: One per analysis when custom logic needed (e.g., `TagNetworkBuilder`, `BountyNetworkBuilder`)
- This reduces code duplication and enables cache reuse

**Fundamental Contract** (all 15 analyzers follow this):
```python
class *Analyzer:
    def __init__(self, data_loader: DataLoader = None):
        self.data_loader = data_loader or DataLoader()
        self.builder = SomeGraphBuilder(self.data_loader)
    
    def run(self, limit: int = 100) -> Dict[str, Any]:
        # 1. build graph via self.builder.build_*()
        # 2. compute metrics (calculations, statistical tests)
        # 3. return {graph, dataframes, metrics, summary}
```

All analyzers print: **Input** → **Process** → **Output** (matches research methodology).

---

## Quick Analyzer Reference

Use this when modifying, debugging, or creating analyzers. See [REPORT.md](../REPORT.md) for full research questions.

| RQ | Analysis | Builder | Key Output | Output File |
|---|---|---|---|---|
| RQ1 | CentralityAnalyzer | UserNetworkBuilder | Betweenness/PageRank correlation with reputation | `centrality_analysis.png` |
| RQ2 | CoreEfficiencyAnalyzer | UserNetworkBuilder | Core vs. periphery answer speed | `core_efficiency_analysis.png` |
| RQ3 | TagCooccurrenceAnalyzer | TagNetworkBuilder | Technology domains (Web, Backend, etc.) | `tag_domains.png` |
| RQ4 | ConnectedComponentAnalyzer | UserNetworkBuilder | Network fragmentation: isolated vs. connected users | `components_analysis.png` |
| RQ5 | ContentFeatureAnalyzer | SimilarityBuilder | Code block impact on post score | `content_features.png` |
| RQ6 | AccountAgeAnalyzer | UserNetworkBuilder | New vs. veteran contribution patterns | `age_patterns.png` |
| RQ7 | VotingBehaviorAnalyzer | VotingNetworkBuilder | Voting patterns & influence dynamics | `voting_network.png` |
| RQ8 | CommentNetworkAnalyzer | CommentNetworkBuilder | Comment interaction structure | `comment_network.png` |
| RQ9 | BadgeNetworkAnalyzer | BadgeNetworkBuilder | Achievement & specialization networks | `badge_network.png` |
| RQ10 | EditCollaborationAnalyzer | EditNetworkBuilder | Post editing collaboration patterns | `edit_collaboration.png` |
| RQ11 | PostLinkAnalyzer | LinkNetworkBuilder | Duplicate/related post networks | `post_links.png` |
| RQ12 | ReviewTaskAnalyzer | ReviewNetworkBuilder | Review queue task networks | `review_tasks.png` |
| RQ13 | BountyNetworkAnalyzer | BountyNetworkBuilder | Bounty offering & claiming patterns | `bounty_network.png` |
| RQ14 | UserLocationAnalyzer | LocationNetworkBuilder | Geographic user clustering | `location_network.png` |
| RQ15 | TimeSeriesAnalyzer | TimeSeriesBuilder | Activity trends over time | `timeseries_activity.png` |

---

## Understanding an Analyzer (The Pattern)

### 1. Metrics Dataclass
Every analyzer defines a `*Metrics` dataclass that wraps computed values:
```python
@dataclass
class CentralityMetrics:
    betweenness: List[float]
    degree: List[int]
    closeness: List[float]
    pagerank: List[float]
    
    def to_dataframe(self) -> pd.DataFrame:
        # Enables easy plotting + CSV export
        return pd.DataFrame({...})
```

### 2. The `run()` Method Structure
```python
def run(self, limit: int = 100) -> Dict[str, Any]:
    # STEP 1: Build graph
    graph, df = self.builder.build_something(limit=limit)
    print(f"INPUT: Loaded {len(df)} records")
    
    # STEP 2: Compute metrics
    metrics = self._calculate_metrics(graph)
    print(f"PROCESS: Computed {len(metrics.betweenness)} centrality scores")
    
    # STEP 3: Statistical analysis
    correlation = self._compute_correlation(metrics, df)
    result = self._generate_summary(...)
    print(f"OUTPUT: Correlation = {correlation:.4f}")
    
    # STEP 4: Return dict with all intermediate outputs
    return {
        "graph": graph,
        "metrics_df": metrics.to_dataframe(),
        "correlation": correlation,
        "summary": result,
    }
```

### 3. Return Contract
Every `run()` must return `Dict[str, Any]` containing:
- `graph`: igraph.Graph object (for visualization)
- At least one DataFrame (e.g., `metrics_df`, `users_df`)
- Summary statistics (e.g., correlation, clustering coefficient)
- Optional: `summary` dict with human-readable findings

---

## Adding a New Analyzer

Example: Adding Analysis #16 (hypothetical "Mentor Relationships").

### Step 1: Create Builder (if needed)
If no existing builder fits, create in `src/models/graph_builder.py`:
```python
class MentorNetworkBuilder(GraphBuilder):
    """Builds mentorship graph from answer patterns."""
    
    def build_mentor_network(self, limit: int = 100) -> Tuple[ig.Graph, pd.DataFrame]:
        # Query: high-rep users who answer newcomers
        query = """
            SELECT u.id, u.reputation, COUNT(a.id) as answers
            FROM `bigquery-public-data.stackoverflow.users` u
            LEFT JOIN `bigquery-public-data.stackoverflow.posts_answers` a ON u.id = a.owner_user_id
            WHERE u.reputation > 1000 LIMIT @limit
        """
        df = self.data_loader.query_bigquery(query, params={'limit': limit})
        
        # Build graph from dataframe
        g = ig.Graph()
        # ... add vertices, edges ...
        return g, df
```

### Step 2: Create Analyzer Class
In `src/analysis/mentor_network.py`:
```python
from dataclasses import dataclass
from typing import Dict, Any, List
import pandas as pd
from src.data.data_loader import DataLoader
from src.models.graph_builder import MentorNetworkBuilder

@dataclass
class MentorMetrics:
    mentor_centrality: List[float]
    mentee_count: List[int]
    
    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame({
            "mentor_centrality": self.mentor_centrality,
            "mentee_count": self.mentee_count,
        })

class MentorNetworkAnalyzer:
    """Analysis: Mentor-mentee relationship networks."""
    
    def __init__(self, data_loader: DataLoader = None):
        self.data_loader = data_loader or DataLoader()
        self.builder = MentorNetworkBuilder(self.data_loader)
    
    def run(self, limit: int = 100) -> Dict[str, Any]:
        print("\n" + "=" * 60)
        print("分析主題 16: 導師關係分析")
        
        self.graph, self.users_df = self.builder.build_mentor_network(limit=limit)
        print(f"INPUT: Built graph with {len(self.graph.vs)} mentors, {len(self.graph.es)} relationships")
        
        metrics = self._calculate_metrics()
        print(f"PROCESS: Computed centrality for {len(metrics.mentor_centrality)} mentors")
        
        result = self._generate_summary(metrics)
        print(f"OUTPUT: Average mentee count = {sum(metrics.mentee_count)/len(metrics.mentee_count):.1f}")
        
        return {
            "graph": self.graph,
            "mentor_metrics_df": metrics.to_dataframe(),
            "summary": result,
        }
    
    def _calculate_metrics(self) -> MentorMetrics:
        betweenness = self.graph.betweenness()
        in_degree = self.graph.indegree()
        return MentorMetrics(mentor_centrality=betweenness, mentee_count=in_degree)
    
    def _generate_summary(self, metrics: MentorMetrics) -> Dict[str, Any]:
        return {
            "avg_centrality": sum(metrics.mentor_centrality) / len(metrics.mentor_centrality),
            "max_mentees": max(metrics.mentee_count),
        }
```

### Step 3: Register in SNARunner
In `src/sna_runner.py`, add to the `run_analysis()` method:
```python
elif run_id == 16:
    from src.analysis.mentor_network import MentorNetworkAnalyzer
    analyzer = MentorNetworkAnalyzer()
    return analyzer.run(limit=limit)
```

### Step 4: Add Test
In `tests/test_analysis.py`:
```python
def test_mentor_analyzer_initialization(self):
    with patch('src.analysis.mentor_network.DataLoader'):
        from src.analysis.mentor_network import MentorNetworkAnalyzer
        analyzer = MentorNetworkAnalyzer()
        assert analyzer is not None
        assert analyzer.builder is not None

def test_mentor_metrics_dataclass(self):
    from src.analysis.mentor_network import MentorMetrics
    metrics = MentorMetrics(
        mentor_centrality=[0.1, 0.2],
        mentee_count=[5, 10]
    )
    df = metrics.to_dataframe()
    assert len(df) == 2
```

---

## Troubleshooting & Debugging

### BigQuery Authentication Fails

**Error**: `google.auth.exceptions.DefaultCredentialsError`

**Solution**:
```bash
# Configure gcloud with your credentials
gcloud auth login
gcloud config set project onlyme-920902

# Verify config
gcloud config list
```

The project expects credentials at: `~/.config/gcloud/legacy_credentials/a0985821880@gmail.com/adc.json` (see `src/config.py`).

### BigQuery Query Timeout or Quota Exceeded

**Solution**: Reduce `limit` parameter or use the cache:
```bash
uv run main.py --run 1 --limit 100  # Start small
```

Check cache status:
```python
from src.data.data_loader import DataLoader
loader = DataLoader()
loader.clear_cache()  # Force fresh queries
```

### Graph Has Too Few Nodes/Edges

**Common causes**:
1. **Limit too low**: Some analyses need ≥500 records. Critical analyses auto-scale:
   - Analyses 7-14: minimum 500 (see `SNARunner.run_analysis()`)
   - Analysis 15: minimum 1,000

2. **Query returns no data**: Check `DATASET_FEATURES.md` for which tables have relevant data

3. **Builder filter too strict**: Review the builder's `WHERE` clause in BigQuery query

**Debug**:
```python
from src.analysis.centrality import CentralityAnalyzer
analyzer = CentralityAnalyzer()
graph, df = analyzer.builder.build_answer_network_with_reputation(limit=1000)
print(f"Nodes: {len(graph.vs)}, Edges: {len(graph.es)}")
print(df.head())  # Check data shape
```

### Visualization Not Generating

**Issue**: PNG not created in `output/`

**Check**:
1. matplotlib using Agg backend: `matplotlib.use("Agg")` in `src/visualization/plots.py`
2. `output/` directory exists
3. SNAPlotter called correctly with `save_plot=True`

**Debug**:
```bash
ls -la output/
# If empty, check src/sna_runner.py L85-95 (plot generation logic)
```

### Tests Fail with "Mocking DataLoader ineffective"

**Issue**: Real BigQuery queries running in tests

**Solution**: Ensure `@patch` path matches import location:
```python
# WRONG (patches copy-after-import):
@patch('DataLoader')

# CORRECT (patches in-module reference):
@patch('src.analysis.centrality.DataLoader')
```

See `tests/test_analysis.py` for correct pattern.

---

## Performance Notes

### Typical Graph Sizes (by Analysis)

| Analysis | Typical Nodes | Typical Edges | Query Time |
|---|---|---|---|
| RQ1-RQ2 (User network) | 100-5,000 | 500-50,000 | 2-10s |
| RQ3 (Tag co-occurrence) | 50-500 | 100-5,000 | 1-5s |
| RQ6 (Account age) | 100-2,000 | 200-10,000 | 2-8s |
| RQ7-RQ14 (Specialized) | 100-1,000 | 200-5,000 | 3-15s |
| RQ15 (Time series, 1000 limit) | 1,000+ | 10,000+ | 10-30s |

### Optimization Tips

1. **Use limit parameter strategically**:
   ```bash
   uv run main.py --run 3 --limit 100  # Quick test
   uv run main.py --run 3 --limit 1000 # Full analysis
   ```

2. **Reuse DataLoader cache**: Running multiple analyses benefits from queries cached in memory

3. **Visualizations are bottleneck**: `SNAPlotter` uses matplotlib force-directed layout (O(n²) algorithm). Disable plotting for testing:
   ```python
   # In src/sna_runner.py, comment out plot generation
   ```

---

## Common Pitfalls

❌ **Don't**: Create metrics without `.to_dataframe()` method  
✅ **Do**: Always include `def to_dataframe(self) -> pd.DataFrame` in metrics dataclass

❌ **Don't**: Hardcode BigQuery table names in analyzers  
✅ **Do**: Let builders handle queries; analyzers receive DataFrames

❌ **Don't**: Return raw igraph.Graph without documentation  
✅ **Do**: Include `metrics_df` and `summary` dict so results are interpretable

❌ **Don't**: Skip the print statements (Input → Process → Output)  
✅ **Do**: Match research methodology by printing at each stage

---

## See Also

- **AGENTS.md**: Commands, code style, project structure, testing conventions
- **REPORT.md**: Full research context, 15 research questions, dataset schema
- **DATASET_FEATURES.md**: BigQuery table details and column→SNA mappings
- **[src/config.py](../src/config.py)**: BigQuery credentials and query limits
- **[src/sna_runner.py](../src/sna_runner.py)**: Analyzer orchestration and output pipeline
