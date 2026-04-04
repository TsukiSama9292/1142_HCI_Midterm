# AGENTS.md - Stack Overflow SNA

## 1. Project Overview
- **Python**: >=3.11 | **Package Manager**: uv | **Test**: pytest | **Linter**: ruff

## 2. Commands

### Run Application
```bash
uv run main.py                              # Default limit=100
uv run main.py --run 1 --limit 1000         # Specific analysis
uv run main.py --run all                    # All 15 analyses
uv run main.py --list                       # List analyses
```

### Tests
```bash
uv run pytest -v                                          # All tests
uv run pytest -v tests/test_analysis.py::TestClassName   # Single class
uv run pytest -v tests/test_analysis.py::TestClassName::test_method  # Single test
uv run pytest -v -k "pattern"                           # Match pattern
```

### Lint/Format
```bash
uv run ruff check . --fix    # Lint + auto-fix
uv run ruff format .         # Format code
uv sync                      # Install deps
```

## 3. Code Style

### Imports
```python
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import pandas as pd
from src.data.data_loader import DataLoader
```
- Group: stdlib → third-party → local (blank line between)

### Formatting
- 4 spaces indentation, max 100 chars/line
- Blank line between top-level defs
- Use `uv run ruff format .` for auto-format

### Type Hints
```python
def process(self, data: pd.DataFrame, limit: Optional[int] = None) -> Dict[str, Any]: ...
```

### Naming
- **Classes**: `PascalCase` (`CentralityAnalyzer`)
- **Functions**: `snake_case` (`run_analysis`, `_private_method`)
- **Constants**: `SCREAMING_SNAKE_CASE`
- **Tests**: `TestPascalCase` class, `test_snake_case` function

### Data Classes
```python
@dataclass
class Metrics:
    values: List[float]
    def to_df(self) -> pd.DataFrame: ...
```

### Error Handling
```python
if limit <= 0:
    raise ValueError(f"Limit must be positive, got {limit}")
```

### Docstrings
- Google-style: `Args:`, `Returns:`
- Use for all public classes/functions

## 4. Project Structure
```
src/
├── analysis/           # 15 analyzer modules (centrality.py, etc.)
├── data/data_loader.py # BigQuery + caching
├── models/graph_builder.py
├── visualization/plots.py
└── utils/helpers.py
tests/test_analysis.py
main.py
```

## 5. Testing Conventions
- Tests: print input → process → print output
- Mock external deps: `@patch('src.data.data_loader.BigQueryClient')`
- Each analyzer: `test_analyzer_initialization` + `test_*_dataclass`

## 6. BigQuery
- Cache: `DataLoader._cache`, clear with `loader.clear_cache()`
- Mock `BigQueryClient` in tests

## 7. Visualization
- Output: `output/` directory, `dpi=150` PNG files
- Results: `output/analysis_results.json`