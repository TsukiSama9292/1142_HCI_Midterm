"""
專案配置設定
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"
DOCS_DIR = PROJECT_ROOT / "docs"

DATA_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

BIGQUERY_CONFIG = {
    "project_id": "onlyme-920902",
    "dataset": "bigquery-public-data.stackoverflow",
    "credential_path": "~/.config/gcloud/legacy_credentials/a0985821880@gmail.com/adc.json",
}

QUERY_LIMITS = {
    "users": 100,
    "posts": 100,
    "tags": 100,
    "connectivity": 100,
    "code_analysis": 100,
    "account_age": 100,
}

GRAPH_CONFIG = {
    "directed": True,
    "edge_attributes": ["weight"],
    "node_attributes": ["reputation", "label"],
}

VISUALIZATION_CONFIG = {
    " figsize": (12, 8),
    "dpi": 150,
    "font_size": 10,
    "node_size_min": 100,
    "node_size_max": 2000,
}
