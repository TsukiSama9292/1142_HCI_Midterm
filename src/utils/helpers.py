"""
輔助工具函數
"""

import json
from datetime import datetime
from typing import Any, Dict, List, Optional
from pathlib import Path
import pandas as pd
import numpy as np


def format_number(value: float, precision: int = 2) -> str:
    """格式化數字顯示"""
    if abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.{precision}f}M"
    elif abs(value) >= 1_000:
        return f"{value / 1_000:.{precision}f}K"
    else:
        return f"{value:.{precision}f}"


def classify_level(value: float, thresholds: List[float], labels: List[str]) -> str:
    """根據閾值分類數值"""
    for i, threshold in enumerate(sorted(thresholds, reverse=True)):
        if value >= threshold:
            return labels[i] if i < len(labels) else f"Level_{i}"
    return labels[-1] if labels else "Unknown"


def save_json(data: Any, file_path: str):
    """儲存 JSON 檔案"""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    def convert_value(val):
        """Convert values to JSON serializable types"""
        if val is None:
            return None
        if isinstance(val, (pd.Timestamp, datetime)):
            return str(val)
        if isinstance(val, (np.integer,)):
            return int(val)
        if isinstance(val, (np.floating,)):
            if np.isnan(val) or np.isinf(val):
                return None
            return float(val)
        if isinstance(val, (np.bool_,)):
            return bool(val)
        if isinstance(val, np.ndarray):
            return val.tolist()
        if isinstance(val, dict):
            return {k: convert_value(v) for k, v in val.items()}
        if isinstance(val, (list, tuple)):
            return [convert_value(v) for v in val]
        if isinstance(val, (pd.DataFrame,)):
            return val.to_dict(orient='records')
        return val
    
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(convert_value(data), f, ensure_ascii=False, indent=2)


def load_json(file_path: str) -> Any:
    """載入 JSON 檔案"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def create_summary_table(data: List[Dict[str, Any]], columns: Optional[List[str]] = None) -> str:
    """建立摘要表格"""
    if not data:
        return "No data available"
    
    if columns is None:
        columns = list(data[0].keys())
    
    header = " | ".join(columns)
    separator = "|" + "|".join(["---" for _ in columns]) + "|"
    
    rows = []
    for item in data:
        row = " | ".join(str(item.get(col, "")) for col in columns)
        rows.append(row)
    
    return f"{header}\n{separator}\n" + "\n".join(rows)
