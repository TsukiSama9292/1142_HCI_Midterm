# BigQuery Stack Overflow 查詢快速參考

## 執行查詢

```bash
export PATH="$HOME/.local/bin:$PATH"
uv run python scripts/bigquery_queries.py
```

## 查詢結果摘要

### 1. 用戶查詢（100 筆）
- 取得高聲望用戶及其聲望等級分類
- 欄位：id, display_name, reputation, up_votes, down_votes, views, reputation_level

### 2. 問題-回答關係（100 筆）
- 取得獲納解答的問題與其回答者關係
- 欄位：question_id, questioner_id, answerer_id, hours_to_accept, tags

### 3. 標籤熱度（100 筆）
- 取得最熱門的技術標籤
- 欄位：tag_name, usage_count
- 前5名：javascript, python, java, c#, php

### 4. 用戶連通性（100 筆）
- 識別知識孤島（低互動用戶）
- 欄位：user_id, display_name, total_interactions, connectivity_level

### 5. 程式碼區塊（100 筆）
- 檢測問題是否包含程式碼區塊
- 欄位：id, title, score, has_code_block, score_level

### 6. 帳號年資（100 筆）
- 分析老手與新手的發文類型差異
- 欄位：user_id, account_age_days, question_count, answer_count, post_type, account_age_level

## BigQuery 表結構

### users 表
| 欄位 | 類型 | 說明 |
|------|------|------|
| id | INTEGER | 用戶 ID |
| display_name | STRING | 用戶名稱 |
| reputation | INTEGER | 聲望 |
| up_votes | INTEGER | 獲得讚數 |
| down_votes | INTEGER | 獲得踩數 |
| views | INTEGER | 個人頁面瀏覽數 |
| creation_date | TIMESTAMP | 帳號創建日期 |
| location | STRING | 位置 |

### posts_questions 表
| 欄位 | 類型 | 說明 |
|------|------|------|
| id | INTEGER | 問題 ID |
| title | STRING | 標題 |
| body | STRING | 內容 |
| accepted_answer_id | INTEGER | 獲納解答 ID |
| answer_count | INTEGER | 回答數 |
| score | INTEGER | 分數 |
| tags | STRING | 標籤（逗號分隔） |
| owner_user_id | INTEGER | 發問者 ID |
| creation_date | TIMESTAMP | 創建日期 |

### posts_answers 表
| 欄位 | 類型 | 說明 |
|------|------|------|
| id | INTEGER | 回答 ID |
| parent_id | INTEGER | 父問題 ID |
| owner_user_id | INTEGER | 回答者 ID |
| score | INTEGER | 分數 |
| creation_date | TIMESTAMP | 創建日期 |

### tags 表
| 欄位 | 類型 | 說明 |
|------|------|------|
| tag_name | STRING | 標籤名稱 |
| count | INTEGER | 使用次數 |
| excerpt_post_id | INTEGER | 摘錄文章 ID |
| wiki_post_id | INTEGER | Wiki 文章 ID |

## 認證問題排除

如果遇到認證錯誤，執行以下命令：

```bash
# 1. 確保 gcloud 已設定
source ~/google-cloud-sdk/path.bash.inc
gcloud auth list

# 2. 設定專案
gcloud config set project onlyme-920902

# 3. 設定應用程式認證
gcloud auth application-default login
```

## 資料量估算

測試查詢（100 筆）：
- BigQuery 處理費用：極少（約 0.1 MB）
- 每月免費配額：1 TB

完整數據查詢可能產生的費用：
- users 表：~10 MB
- posts_questions 表：~500 MB
- posts_answers 表：~500 MB
