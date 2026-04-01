# Stack Overflow 社會網路分析 (Social Network Analysis)

## 專案概述

本專案使用 BigQuery 公共數據集對 Stack Overflow 進行社會網路分析，研究開發者社群的知識流動生態。

## 分析目標

| # | 分析主題 | 研究問題 |
|---|----------|----------|
| 1 | 使用者聲望與網路中心度 | 高聲望用戶是否在網路結構中具有更高的介性中心度？ |
| 2 | 網路核心結構與解答效率 | 位於網路核心區域的發問者是否能更快獲得獲納解答？ |
| 3 | 技術標籤共現與領域地圖 | 不同程式語言或框架之間的群聚效應和技術關聯性？ |
| 4 | 知識孤島與連通分量分析 | 是否存在資訊流動障礙的邊緣化現象？ |
| 5 | 內容特徵與互動反響 | 程式碼區塊對 Upvotes 的影響？ |
| 6 | 帳號資歷與社群貢獻 | 老手與新手的行為差異？ |

## 使用的技術

- **BigQuery**: Google Cloud 大數據分析平台
- **Python**: 數據分析
  - `google-cloud-bigquery`: BigQuery 客戶端
  - `pandas`: 數據處理
  - `igraph`: 圖論分析
  - `matplotlib`: 視覺化

## 快速開始

### 1. 環境設定

```bash
# 安裝依賴
uv sync --dev

# 設定 Google Cloud 認證
# 方式一：使用服務帳戶金鑰
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"

# 方式二：使用 gcloud CLI
gcloud auth application-default login
```

### 2. 測試 BigQuery 查詢

```bash
# 執行查詢範例
uv run python scripts/bigquery_queries.py
```

### 3. BigQuery 數據表結構

#### users 表
```sql
SELECT id, display_name, reputation, answer_count, question_count
FROM `bigquery-public-data.stackoverflow.users`
LIMIT 100
```

#### posts 表
```sql
SELECT id, post_type_id, owner_user_id, accepted_answer_id, score
FROM `bigquery-public-data.stackoverflow.posts`
WHERE post_type_id = 1  -- 問題
LIMIT 100
```

## 指標總表

### 可直接使用的指標

| 指標名稱 | 數據表 | 欄位 | 說明 |
|----------|--------|------|------|
| 用戶 ID | users | id | 主鍵 |
| 聲望 | users | reputation | 核心指標 |
| 回答數 | users | answer_count | 用戶回答數 |
| 提問數 | users | question_count | 用戶提問數 |
| 貼文 ID | posts | id | 主鍵 |
| 貼文類型 | posts | post_type_id | 1=問題, 2=回答 |
| 父貼文 ID | posts | parent_id | 用於關聯回答與問題 |
| 獲納解答 ID | posts | accepted_answer_id | 標記最佳解答 |
| 分數 | posts | score | Upvotes 指標 |
| 標籤 | posts | tags | 技術分類 |

### 分類指標

| 指標名稱 | 分類級別 |
|----------|----------|
| 聲望等級 | 4 級 (1-100, 101-1000, 1001-10000, 10001+) |
| 獲納解答時間 | 4 級 (<1h, 1-24h, 1-7d, >7d) |
| 回答數等級 | 4 級 (0, 1-3, 4-10, 11+) |
| 分數等級 | 6 級 (Very Negative 到 Extremely Positive) |
| 帳號年資 | 5 級 (<30d, 30d-6m, 6m-2y, 2-5y, 5y+) |
| 發文類型 | 4 型 (Both, Questions Only, Answers Only, Neither) |
| 連通性等級 | 4 級 (Isolated, Low, Medium, Active) |

## 查詢範例

### 用戶聲望分析
```sql
SELECT
    id,
    display_name,
    reputation,
    CASE
        WHEN reputation <= 100 THEN 'Low'
        WHEN reputation <= 1000 THEN 'Medium-Low'
        WHEN reputation <= 10000 THEN 'Medium-High'
        ELSE 'High'
    END AS reputation_level
FROM `bigquery-public-data.stackoverflow.users`
LIMIT 100
```

### 回答關係網路
```sql
SELECT
    a.owner_user_id AS answerer_id,
    q.owner_user_id AS questioner_id,
    TIMESTAMP_DIFF(a.creation_date, q.creation_date, HOUR) AS hours_to_accept
FROM `bigquery-public-data.stackoverflow.posts` a
INNER JOIN `bigquery-public-data.stackoverflow.posts` q
    ON a.parent_id = q.id
WHERE a.post_type_id = 2
    AND q.post_type_id = 1
LIMIT 100
```

## 文件結構

```
docs/
├── stackoverflow_analysis_plan.md   # 完整的數據分析計劃
├── stackoverflow_overview.md        # 專案概覽
└── features.md                      # 功能說明

scripts/
└── bigquery_queries.py             # BigQuery 查詢範例
```

## 注意事項

1. **BigQuery 免費配額**: 每月 1TB 免費查詢
2. **數據延遲**: 數據集可能有延遲
3. **認證需求**: 需要 Google Cloud 專案
4. **費用**: 超過免費配額後按查詢量收費

## 詳細文檔

- [數據分析計劃](docs/stackoverflow_analysis_plan.md)
- [專案概覽](docs/stackoverflow_overview.md)
- [功能說明](docs/features.md)
