# Stack Overflow 社會網路分析 - 專案概覽

## 專案目標

本專案旨在透過社會網路分析 (Social Network Analysis, SNA) 方法，利用 Python 的 `igraph` 函式庫對 Stack Overflow 社群數據進行大規模圖形建模與中心性分析。

## 數據來源

- **BigQuery 公共數據集**: `bigquery-public-data.stackoverflow`
- **查詢方式**: 直接使用 BigQuery SQL，無需下載數據
- **測試數據量**: 100 筆（使用 `LIMIT 100`）

## 分析主題

| # | 分析主題 | 研究問題 |
|---|----------|----------|
| 1 | 使用者聲望與網路中心度 | 高聲望用戶是否在網路結構中具有更高的介性中心度？ |
| 2 | 網路核心結構與解答效率 | 位於網路核心區域的發問者是否能更快獲得獲納解答？ |
| 3 | 技術標籤共現與領域地圖 | 不同程式語言或框架之間的群聚效應和技術關聯性？ |
| 4 | 知識孤島與連通分量分析 | 是否存在資訊流動障礙的邊緣化現象？ |
| 5 | 內容特徵與互動反響 | 程式碼區塊對 Upvotes 的影響？ |
| 6 | 帳號資歷與社群貢獻 | 老手與新手的行為差異？ |

## 需要的套件

```bash
# 安裝需要的 Python 套件
uv add google-cloud-bigquery pandas igraph matplotlib
```

## 查詢示例

```python
from google.cloud import bigquery
import pandas as pd

# 初始化客戶端
client = bigquery.Client()

# 查詢高聲望用戶
sql = """
SELECT id, display_name, reputation, answer_count, question_count
FROM `bigquery-public-data.stackoverflow.users`
WHERE reputation > 1000
LIMIT 100
"""

df = client.query(sql).result().to_dataframe()
print(df.head())
```

## 文件結構

```
docs/
├── stackoverflow_analysis_plan.md  # 完整的數據分析計劃
└── features.md                      # 專案功能說明
```

## BigQuery 表結構

| 表名 | 說明 | 主要用途 |
|------|------|----------|
| users | 用戶資料 | 聲望、發文數據 |
| posts | 貼文資料 | 問題/回答關係 |
| comments | 評論資料 | 互動關係 |
| votes | 投票資料 | 讚/踩數據 |
| badges | 徽章資料 | 成就系統 |
| tags | 標籤資料 | 技術分類 |

## 快速開始

1. 設定 Google Cloud 專案
2. 安裝套件：`uv sync --dev`
3. 執行 BigQuery 查詢
4. 使用 igraph 建立網路圖
5. 計算中心性指標

詳見 [stackoverflow_analysis_plan.md](stackoverflow_analysis_plan.md)
