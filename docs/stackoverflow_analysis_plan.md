# Stack Overflow 社會網路分析：數據分析計劃 (Data Analysis Plan)

## 一、數據集概述

### 數據來源
- **BigQuery 公共數據集**: `bigquery-public-data.stackoverflow`
- **查詢方式**: 直接使用 BigQuery SQL，無需下載數據
- **測試數據量**: 100 筆（使用 `LIMIT 100` 或 `WHERE` 條件限制）

### 可用數據表
| 數據表 | 說明 | 主要欄位 |
|--------|------|----------|
| `users` | 用戶資料 | id, display_name, reputation, up_votes, down_votes, views, creation_date, last_access_date, location |
| `posts_questions` | 問題資料 | id, title, body, accepted_answer_id, answer_count, comment_count, creation_date, score, tags, view_count, owner_user_id |
| `posts_answers` | 回答資料 | id, title, body, parent_id, score, creation_date, owner_user_id |
| `comments` | 評論資料 | id, post_id, user_id, creation_date, score, text |
| `votes` | 投票資料 | id, user_id, post_id, vote_type_id, creation_date, bounty_amount |
| `badges` | 徽章資料 | id, user_id, name, class, tag_based, creation_date |
| `tags` | 標籤資料 | id, tag_name, count, excerpt_post_id, wiki_post_id |

---

## 二、分析目標與 BigQuery SQL 查詢

### 分析主題 1: 使用者聲望與網路中心度

**研究目標**: 驗證高聲望使用者的核心作用，分析高聲望用戶是否在網路結構中具有更高的介性中心度。

#### 可用指標

| 指標名稱 | BigQuery 欄位 | 分類方式 | 可計算性 |
|----------|--------------|----------|----------|
| `reputation` | `users.reputation` | 四級分類: 1-100, 101-1000, 1001-10000, 10001+ | ✅ 直接可用 |
| `answer_count` | `users.answer_count` | 數值型態 | ✅ 直接可用 |
| `question_count` | `users.question_count` | 數值型態 | ✅ 直接可用 |
| `upvotes` | `users.up_vote_count` | 數值型態 | ✅ 直接可用 |
| `downvotes` | `users.down_vote_count` | 數值型態 | ✅ 直接可用 |

#### BigQuery SQL 查詢（測試 100 筆）

```sql
-- 查詢高聲望用戶及其回答關係
SELECT
  u.id AS user_id,
  u.display_name,
  u.reputation,
  u.answer_count,
  u.question_count,
  u.up_vote_count,
  u.down_vote_count,
  -- 聲望四級分類
  CASE
    WHEN u.reputation BETWEEN 1 AND 100 THEN '1_Low (1-100)'
    WHEN u.reputation BETWEEN 101 AND 1000 THEN '2_Medium-Low (101-1000)'
    WHEN u.reputation BETWEEN 1001 AND 10000 THEN '3_Medium-High (1001-10000)'
    WHEN u.reputation > 10000 THEN '4_High (10001+)'
    ELSE '0_None'
  END AS reputation_level
FROM `bigquery-public-data.stackoverflow.users` u
WHERE u.reputation IS NOT NULL
LIMIT 100
```

```sql
-- 建立回答關係網路（回答者 → 發問者）
SELECT
  a.owner_user_id AS answerer_id,
  q.owner_user_id AS questioner_id,
  q.accepted_answer_id,
  a.creation_date AS answer_date,
  q.creation_date AS question_date,
  -- 計算獲納解答時間（小時）
  TIMESTAMP_DIFF(a.creation_date, q.creation_date, HOUR) AS time_to_accept_hours
FROM `bigquery-public-data.stackoverflow.posts` a
INNER JOIN `bigquery-public-data.stackoverflow.posts` q
  ON a.parent_id = q.id
WHERE a.post_type_id = 2  -- 回答類型
  AND q.post_type_id = 1  -- 問題類型
  AND a.owner_user_id IS NOT NULL
  AND q.owner_user_id IS NOT NULL
LIMIT 100
```

---

### 分析主題 2: 網路核心結構與解答效率

**研究目標**: 評估核心發問者的問題解決速度，判斷位於網路核心區域的發問者是否能更快獲得獲納解答。

#### 可用指標

| 指標名稱 | BigQuery 欄位 | 分類方式 | 可計算性 |
|----------|--------------|----------|----------|
| `accepted_answer_id` | `posts.accepted_answer_id` | 有/無 | ✅ 直接可用 |
| `answer_count` | `posts.answer_count` | 四級分類: 0, 1-3, 4-10, 11+ | ✅ 直接可用 |
| `time_to_accept` | 計算欄位 | 四級分類: <1h, 1-24h, 1-7d, >7d | ✅ 可計算 |
| `score` | `posts.score` | 數值型態 | ✅ 直接可用 |
| `view_count` | `posts.view_count` | 數值型態 | ✅ 直接可用 |

#### BigQuery SQL 查詢

```sql
-- 查詢獲納解答時間分析
SELECT
  q.id AS question_id,
  q.owner_user_id,
  q.accepted_answer_id,
  q.answer_count,
  q.score AS question_score,
  q.view_count,
  q.creation_date AS question_date,
  a.creation_date AS accepted_answer_date,
  -- 獲納解答時間（小時）
  TIMESTAMP_DIFF(a.creation_date, q.creation_date, HOUR) AS hours_to_accept,
  -- 四級分類
  CASE
    WHEN TIMESTAMP_DIFF(a.creation_date, q.creation_date, HOUR) < 1 THEN '1_Very Fast (<1h)'
    WHEN TIMESTAMP_DIFF(a.creation_date, q.creation_date, HOUR) BETWEEN 1 AND 24 THEN '2_Fast (1-24h)'
    WHEN TIMESTAMP_DIFF(a.creation_date, q.creation_date, HOUR) BETWEEN 25 AND 168 THEN '3_Medium (1-7d)'
    ELSE '4_Slow (>7d)'
  END AS acceptance_time_level
FROM `bigquery-public-data.stackoverflow.posts` q
INNER JOIN `bigquery-public-data.stackoverflow.posts` a
  ON q.accepted_answer_id = a.id
WHERE q.post_type_id = 1
  AND q.accepted_answer_id IS NOT NULL
  AND q.accepted_answer_id > 0
LIMIT 100
```

```sql
-- 查詢回答數量分布
SELECT
  CASE
    WHEN answer_count = 0 THEN '1_No Answer (0)'
    WHEN answer_count BETWEEN 1 AND 3 THEN '2_Few (1-3)'
    WHEN answer_count BETWEEN 4 AND 10 THEN '3_Moderate (4-10)'
    ELSE '4_Many (11+)'
  END AS answer_count_level,
  COUNT(*) AS question_count,
  AVG(score) AS avg_score,
  AVG(view_count) AS avg_views
FROM `bigquery-public-data.stackoverflow.posts`
WHERE post_type_id = 1
GROUP BY answer_count_level
ORDER BY question_count DESC
LIMIT 100
```

---

### 分析主題 3: 技術標籤共現與領域地圖

**研究目標**: 透過技術標籤的共現分析，描繪不同程式語言或框架之間的群聚效應。

#### 可用指標

| 指標名稱 | BigQuery 欄位 | 分類方式 | 可計算性 |
|----------|--------------|----------|----------|
| `tags` | `posts.tags` | 技術群聚分類 | ✅ 直接可用 |
| `tag_count` | 計算欄位 | 數值型態 | ✅ 可計算 |
| `score` | `posts.score` | 數值型態 | ✅ 直接可用 |
| `view_count` | `posts.view_count` | 標籤熱度 | ✅ 直接可用 |

#### BigQuery SQL 查詢

```sql
-- 查詢標籤熱度（頻率）
SELECT
  tag,
  COUNT(*) AS post_count,
  AVG(score) AS avg_score,
  SUM(view_count) AS total_views
FROM `bigquery-public-data.stackoverflow.posts`,
UNNEST(SPLIT(tags, '<')) AS tag
WHERE post_type_id = 1
  AND tags IS NOT NULL
  AND tag != ''
GROUP BY tag
ORDER BY post_count DESC
LIMIT 100
```

```sql
-- 查詢標籤共現關係（同時出現在同一貼文）
WITH question_tags AS (
  SELECT
    id AS post_id,
    SPLIT(REPLACE(REPLACE(tags, '>', ''), '<', ','), ',') AS tags_array
  FROM `bigquery-public-data.stackoverflow.posts`
  WHERE post_type_id = 1
    AND tags IS NOT NULL
)
SELECT
  t1 AS tag1,
  t2 AS tag2,
  COUNT(*) AS co_occurrence_count
FROM question_tags,
UNNEST(tags_array) AS t1,
UNNEST(tags_array) AS t2
WHERE t1 < t2  -- 避免重複
  AND t1 != ''
  AND t2 != ''
GROUP BY t1, t2
ORDER BY co_occurrence_count DESC
LIMIT 100
```

---

### 分析主題 4: 知識孤島與連通分量分析

**研究目標**: 利用連通分量分析找出僅有少數人互動的孤立組件。

#### 可用指標

| 指標名稱 | BigQuery 欄位 | 分類方式 | 可計算性 |
|----------|--------------|----------|----------|
| `post_count` | 計算欄位 | 用戶發文數 | ✅ 可計算 |
| `comment_count` | 用戶評論數 | 數值型態 | ✅ 可計算 |
| `interaction_count` | 計算欄位 | 用戶互動總數 | ✅ 可計算 |
| `connected_component` | - | 主連通/孤立 | ⚠️ 需圖論算法 |

#### BigQuery SQL 查詢

```sql
-- 查詢用戶互動行為（識別低互動用戶）
SELECT
  u.id AS user_id,
  u.display_name,
  u.reputation,
  u.creation_date,
  COUNT(DISTINCT p.id) AS post_count,
  COUNT(DISTINCT c.id) AS comment_count,
  COUNT(DISTINCT v.id) AS vote_count,
  -- 總互動數
  (COUNT(DISTINCT p.id) + COUNT(DISTINCT c.id) + COUNT(DISTINCT v.id)) AS total_interactions,
  -- 連通性分類
  CASE
    WHEN (COUNT(DISTINCT p.id) + COUNT(DISTINCT c.id) + COUNT(DISTINCT v.id)) = 0 THEN '1_Isolated (0)'
    WHEN (COUNT(DISTINCT p.id) + COUNT(DISTINCT c.id) + COUNT(DISTINCT v.id)) BETWEEN 1 AND 5 THEN '2_Low (1-5)'
    WHEN (COUNT(DISTINCT p.id) + COUNT(DISTINCT c.id) + COUNT(DISTINCT v.id)) BETWEEN 6 AND 20 THEN '3_Medium (6-20)'
    ELSE '4_Active (21+)'
  END AS connectivity_level
FROM `bigquery-public-data.stackoverflow.users` u
LEFT JOIN `bigquery-public-data.stackoverflow.posts` p ON u.id = p.owner_user_id
LEFT JOIN `bigquery-public-data.stackoverflow.comments` c ON u.id = c.user_id
LEFT JOIN `bigquery-public-data.stackoverflow.votes` v ON u.id = v.user_id
GROUP BY u.id, u.display_name, u.reputation, u.creation_date
ORDER BY total_interactions ASC
LIMIT 100
```

```sql
-- 查詢孤立組件（僅提問或僅回答的用戶）
SELECT
  u.id AS user_id,
  u.display_name,
  u.reputation,
  COUNT(DISTINCT CASE WHEN p.post_type_id = 1 THEN p.id END) AS question_count,
  COUNT(DISTINCT CASE WHEN p.post_type_id = 2 THEN p.id END) AS answer_count,
  CASE
    WHEN COUNT(DISTINCT CASE WHEN p.post_type_id = 1 THEN p.id END) > 0
     AND COUNT(DISTINCT CASE WHEN p.post_type_id = 2 THEN p.id END) = 0
    THEN '1_Question_Only'
    WHEN COUNT(DISTINCT CASE WHEN p.post_type_id = 1 THEN p.id END) = 0
     AND COUNT(DISTINCT CASE WHEN p.post_type_id = 2 THEN p.id END) > 0
    THEN '2_Answer_Only'
    WHEN COUNT(DISTINCT CASE WHEN p.post_type_id = 1 THEN p.id END) > 0
     AND COUNT(DISTINCT CASE WHEN p.post_type_id = 2 THEN p.id END) > 0
    THEN '3_Both'
    ELSE '0_None'
  END AS activity_type
FROM `bigquery-public-data.stackoverflow.users` u
LEFT JOIN `bigquery-public-data.stackoverflow.posts` p ON u.id = p.owner_user_id
GROUP BY u.id, u.display_name, u.reputation
HAVING activity_type IN ('1_Question_Only', '2_Answer_Only')
LIMIT 100
```

---

### 分析主題 5: 內容特徵與互動反響（補充）

**研究目標**: 探討貼文內容特徵（是否包含程式碼區塊）對 Upvotes 的影響。

#### 可用指標

| 指標名稱 | BigQuery 欄位 | 分類方式 | 可計算性 |
|----------|--------------|----------|----------|
| `has_code` | `posts.body` 包含 ``` | 是/否 | ⚠️ 需正規表達式 |
| `score` | `posts.score` | 六級分類 | ✅ 直接可用 |
| `upvotes` | `posts.score` (正值) | 數值型態 | ✅ 直接可用 |
| `view_count` | `posts.view_count` | 數值型態 | ✅ 直接可用 |

#### BigQuery SQL 查詢

```sql
-- 檢測是否包含程式碼區塊
SELECT
  id,
  post_type_id,
  title,
  score,
  view_count,
  answer_count,
  comment_count,
  creation_date,
  -- 檢測是否包含程式碼（使用正則表達式）
  CASE
    WHEN REGEXP_CONTAINS(body, r'```') THEN 1
    WHEN REGEXP_CONTAINS(body, r'<code>') THEN 1
    ELSE 0
  END AS has_code_block,
  -- 六級分類
  CASE
    WHEN score <= -5 THEN '1_Very Negative (<=-5)'
    WHEN score BETWEEN -4 AND -1 THEN '2_Negative (-4 to -1)'
    WHEN score = 0 THEN '3_Neutral (0)'
    WHEN score BETWEEN 1 AND 5 THEN '4_Positive (1-5)'
    WHEN score BETWEEN 6 AND 20 THEN '5_Very Positive (6-20)'
    ELSE '6_Extremely Positive (>20)'
  END AS score_level
FROM `bigquery-public-data.stackoverflow.posts`
WHERE post_type_id = 1
  AND body IS NOT NULL
LIMIT 100
```

---

### 分析主題 6: 帳號資歷與社群貢獻（補充）

**研究目標**: 分析不同帳號年資的使用者在社群中的發文類型差異。

#### 可用指標

| 指標名稱 | BigQuery 欄位 | 分類方式 | 可計算性 |
|----------|--------------|----------|----------|
| `account_age` | `users.creation_date` | 五級分類 | ✅ 可計算 |
| `post_type` | 計算欄位 | 圓形/三角形/正方形 | ✅ 可計算 |
| `reputation` | `users.reputation` | 數值型態 | ✅ 直接可用 |
| `last_access` | `users.last_access_date` | 數值型態 | ✅ 直接可用 |

#### BigQuery SQL 查詢

```sql
-- 查詢帳號年資與發文類型
SELECT
  u.id AS user_id,
  u.display_name,
  u.reputation,
  u.creation_date AS account_creation_date,
  u.last_access_date,
  -- 計算帳號年資（天）
  DATE_DIFF(CURRENT_DATE(), DATE(u.creation_date), DAY) AS account_age_days,
  COUNT(DISTINCT CASE WHEN p.post_type_id = 1 THEN p.id END) AS question_count,
  COUNT(DISTINCT CASE WHEN p.post_type_id = 2 THEN p.id END) AS answer_count,
  -- 發文類型（五級分類）
  CASE
    WHEN COUNT(DISTINCT CASE WHEN p.post_type_id = 1 THEN p.id END) > 0
     AND COUNT(DISTINCT CASE WHEN p.post_type_id = 2 THEN p.id END) > 0
    THEN '1_Both (Both)'
    WHEN COUNT(DISTINCT CASE WHEN p.post_type_id = 1 THEN p.id END) > 0
     AND COUNT(DISTINCT CASE WHEN p.post_type_id = 2 THEN p.id END) = 0
    THEN '2_Questions_Only'
    WHEN COUNT(DISTINCT CASE WHEN p.post_type_id = 1 THEN p.id END) = 0
     AND COUNT(DISTINCT CASE WHEN p.post_type_id = 2 THEN p.id END) > 0
    THEN '3_Answers_Only'
    WHEN COUNT(DISTINCT CASE WHEN p.post_type_id = 1 THEN p.id END) = 0
     AND COUNT(DISTINCT CASE WHEN p.post_type_id = 2 THEN p.id END) = 0
    THEN '4_Neither'
    ELSE '5_Other'
  END AS post_type,
  -- 帳號年資五級分類
  CASE
    WHEN DATE_DIFF(CURRENT_DATE(), DATE(u.creation_date), DAY) < 30 THEN '1_New (<30d)'
    WHEN DATE_DIFF(CURRENT_DATE(), DATE(u.creation_date), DAY) BETWEEN 30 AND 180 THEN '2_Young (30d-6m)'
    WHEN DATE_DIFF(CURRENT_DATE(), DATE(u.creation_date), DAY) BETWEEN 181 AND 730 THEN '3_Mature (6m-2y)'
    WHEN DATE_DIFF(CURRENT_DATE(), DATE(u.creation_date), DAY) BETWEEN 731 AND 1825 THEN '4_Established (2-5y)'
    ELSE '5_Senior (5y+)'
  END AS account_age_level
FROM `bigquery-public-data.stackoverflow.users` u
LEFT JOIN `bigquery-public-data.stackoverflow.posts` p ON u.id = p.owner_user_id
GROUP BY u.id, u.display_name, u.reputation, u.creation_date, u.last_access_date
ORDER BY account_age_days DESC
LIMIT 100
```

---

## 三、指標總表

### 可直接使用的指標

| 指標名稱 | 數據表 | 欄位 | 資料類型 | 備註 |
|----------|--------|------|----------|------|
| 用戶 ID | users | id | INTEGER | 主鍵 |
| 用戶名稱 | users | display_name | STRING | |
| 聲望 | users | reputation | INTEGER | 核心指標 |
| 帳號創建日期 | users | creation_date | TIMESTAMP | |
| 最後訪問日期 | users | last_access_date | TIMESTAMP | |
| 讚數 | users | up_votes | INTEGER | |
| 踩數 | users | down_votes | INTEGER | |
| 瀏覽數 | users | views | INTEGER | |
| 位置 | users | location | STRING | |
| 問題 ID | posts_questions | id | INTEGER | 主鍵 |
| 標題 | posts_questions | title | STRING | |
| 內容 | posts_questions | body | STRING | |
| 獲納解答 ID | posts_questions | accepted_answer_id | INTEGER | |
| 回答數 | posts_questions | answer_count | INTEGER | |
| 評論數 | posts_questions | comment_count | INTEGER | |
| 創建日期 | posts_questions | creation_date | TIMESTAMP | |
| 分數 | posts_questions | score | INTEGER | Upvotes 指標 |
| 瀏覽數 | posts_questions | view_count | INTEGER | |
| 標籤 | posts_questions | tags | STRING | |
| 擁有者用戶 ID | posts_questions | owner_user_id | INTEGER | |
| 回答 ID | posts_answers | id | INTEGER | 主鍵 |
| 父貼文 ID | posts_answers | parent_id | INTEGER | 用於關聯回答與問題 |
| 擁有者用戶 ID | posts_answers | owner_user_id | INTEGER | |
| 創建日期 | posts_answers | creation_date | TIMESTAMP | |
| 分數 | posts_answers | score | INTEGER | |

### 需要計算的指標

| 指標名稱 | 計算方式 | 分類級別 | 可計算性 |
|----------|----------|----------|----------|
| 聲望等級 | CASE WHEN reputation | 4 級 | ✅ |
| 獲納解答時間 | TIMESTAMP_DIFF | 4 級 | ✅ |
| 回答數等級 | CASE WHEN answer_count | 4 級 | ✅ |
| 分數等級 | CASE WHEN score | 6 級 | ✅ |
| 帳號年資 | DATE_DIFF | 5 級 | ✅ |
| 發文類型 | CASE WHEN COUNT | 4 型 | ✅ |
| 連通性等級 | CASE WHEN total_interactions | 4 級 | ✅ |
| 程式碼區塊 | REGEXP_CONTAINS | 2 值 | ✅ |
| 標籤熱度 | COUNT, SUM | 連續 | ✅ |
| 標籤共現 | UNNEST, SPLIT | 矩陣 | ✅ |

### BigQuery 標籤表額外欄位
| 欄位名稱 | 類型 | 說明 |
|----------|------|------|
| excerpt_post_id | INTEGER | 摘錄文章 ID |
| wiki_post_id | INTEGER | Wiki 文章 ID |

---

## 四、測試數據查詢腳本

### 快速測試腳本（100 筆）

```sql
-- 測試 1: 用戶基礎資料
SELECT *
FROM `bigquery-public-data.stackoverflow.users`
LIMIT 100;

-- 測試 2: 提問資料
SELECT *
FROM `bigquery-public-data.stackoverflow.posts`
WHERE post_type_id = 1
LIMIT 100;

-- 測試 3: 回答資料
SELECT *
FROM `bigquery-public-data.stackoverflow.posts`
WHERE post_type_id = 2
LIMIT 100;

-- 測試 4: 評論資料
SELECT *
FROM `bigquery-public-data.stackoverflow.comments`
LIMIT 100;

-- 測試 5: 投票資料
SELECT *
FROM `bigquery-public-data.stackoverflow.votes`
LIMIT 100;

-- 測試 6: 徽章資料
SELECT *
FROM `bigquery-public-data.stackoverflow.badges`
LIMIT 100;
```

---

## 五、Python igraph 社會網路分析整合

### 需要的 Python 套件

```python
# 需要的套件
from google.cloud import bigquery  # BigQuery 客戶端
import pandas as pd              # 數據處理
import igraph as ig              # 圖論分析
import matplotlib.pyplot as plt   # 視覺化
```

### BigQuery 連接設定

```python
from google.cloud import bigquery

# 初始化 BigQuery 客戶端
client = bigquery.Client()

# 執行查詢並轉換為 DataFrame
def query_to_dataframe(sql: str, limit: int = 100) -> pd.DataFrame:
    query_job = client.query(sql)
    results = query_job.result()
    return results.to_dataframe()
```

---

## 六、注意事項

1. **查詢限制**: BigQuery 每月提供 1TB 免費查詢配額，建議使用 `LIMIT` 進行測試
2. **數據延遲**: Stack Overflow 數據集有延遲，可能不是最新數據
3. **費用**: 超過免費配額後按查詢量收費
4. **認證**: 需要 Google Cloud 項目才能訪問 BigQuery 公共數據集
