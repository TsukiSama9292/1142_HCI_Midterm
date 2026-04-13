# 02 研究方法

本章說明本研究採用的資料來源、分析流程與程式設計對應，並具體說明 `analysis_limits.example.json` 如何影響分析執行。

## 2.1 資料來源

本研究主要使用 Google BigQuery 公共資料集：`bigquery-public-data.stackoverflow`。資料集包含多個資料表，供構建社會網路分析所需的節點與關係。

使用的資料表包括：

- `users`
- `posts_questions`
- `posts_answers`
- `votes`
- `comments`
- `badges`
- `tags`
- `post_links`
- `post_history`
- `review_tasks`

這些資料表提供使用者資訊、貼文內容、投票行為、評論互動、徽章成就、標籤共現、問題引用、編輯協作與審核任務等多維資料。

## 2.2 研究設計與程式對應

本研究設計 15 個社會網路分析面向，對應 `src/analysis` 下的 15 個分析模組：

- RQ1: `src/analysis/centrality.py`
- RQ2: `src/analysis/core_efficiency.py`
- RQ3: `src/analysis/tag_cooccurrence.py`
- RQ4: `src/analysis/connected_components.py`
- RQ5: `src/analysis/content_features.py`
- RQ6: `src/analysis/account_age.py`
- RQ7: `src/analysis/voting_behavior.py`
- RQ8: `src/analysis/comment_network.py`
- RQ9: `src/analysis/badge_network.py`
- RQ10: `src/analysis/edit_collaboration.py`
- RQ11: `src/analysis/post_link.py`
- RQ12: `src/analysis/review_task.py`
- RQ13: `src/analysis/bounty_network.py`
- RQ14: `src/analysis/user_location.py`
- RQ15: `src/analysis/time_series.py`

這些分析由 `src/sna_runner.py` 統一執行，採用 `DataLoader` 讀取資料並生成節點/邊、計算指標，最後輸出摘要與視覺化結果。

## 2.3 分析參數與限制設定

分析執行參數由 `analysis_limits.example.json` 控制。`src/sna_runner.py` 中的 `SNARunner._build_analysis_limits()` 會依此設定，並針對某些分析自動施加最小限制。

`analysis_limits.example.json` 範例值如下：

- default: 100
- 1: 200
- 2: 200
- 3: 300
- 4: 300
- 5: 300
- 6: 300
- 7: 1000
- 8: 1000
- 9: 500
- 10: 100000
- 11: 500
- 12: 500
- 13: 2000
- 14: 500
- 15: 1000

若未指定分析限制，`SNARunner` 會使用 `default`，並對 RQ7~RQ14 施加最小 500、RQ15 最小 1000 的資料限制。這可確保較複雜的分析有合理樣本量。

## 2.4 分析流程

分析流程可分三個階段：

1. **資料擷取與預處理**：由 `DataLoader` 查詢 BigQuery，取得符合分析需求的樣本，並將原始資料轉換成適合構建網路的格式。
2. **網路建構與指標計算**：各分析模組以節點與邊表示關係，並計算中心性、連通性、社群結構與時間趨勢等指標。
3. **結果整理與輸出**：將摘要與資料表整理成 JSON，匯出至 `output/analysis_results.json`，供報告撰寫與視覺化使用。

## 2.5 主要分析面向說明

以下說明 15 個分析面向的重點設計與分類規則：

- **RQ1 使用者聲望與網路中心度**：分析使用者回答關係網路，檢查高聲望與低聲望使用者的 betweenness 與相關性。
- **RQ2 網路核心結構與解答效率**：以 k-core 與度數區分核心與邊緣，並比較回答採納時間。
- **RQ3 技術標籤共現與領域地圖**：建構標籤共現網路，並將標籤分類為 Web、Backend、Database、Mobile、AI_ML、DevOps、DataScience、Other。
- **RQ4 知識孤島與連通分量分析**：檢視回答網路的連通分量分布，找出主流成分與小型孤島。
- **RQ5 內容特徵與互動反響**：比較含程式碼與不含程式碼貼文的分數差異，並以統計測試檢查顯著性。
- **RQ6 帳號年資與社群貢獻**：依帳號年資與貼文類型分析使用者行為差異。
- **RQ7 投票行為網路**：分析投票類型分布與使用者投票活躍度。
- **RQ8 評論互動網路**：以共評論同一問題為基礎構建評論互動關係。
- **RQ9 徽章成就網路**：檢視徽章數量與使用者成就分布。
- **RQ10 編輯協作網路**：分析共同編輯行為與編輯者合作網路。
- **RQ11 引用與重複問題網路**：基於 `post_links` 建構問題之間的引用與重複關係。
- **RQ12 審核任務網路**：分析審核類型與審核者參與程度。
- **RQ13 賞金懸賞網路**：檢視賞金起始與結束行為，並分析賞金使用者的技術興趣重疊。
- **RQ14 使用者地理分布網路**：以使用者位置文字映射區域，分析地理分布結構。
- **RQ15 時間序列活躍度網路**：分析月度、每日與每小時貼文分布的時間趨勢。

## 2.6 研究流程與軟體架構對應

本研究的軟體架構對應如下：

- `src/data/data_loader.py`：BigQuery 查詢與緩存管理。
- `src/models/graph_builder.py`：構建各分析所需的 igraph 網路。
- `src/analysis/*.py`：各分析主題的邏輯與指標計算。
- `src/sna_runner.py`：統一執行 15 個分析，根據 `analysis_limits.example.json` 設定執行限制。
- `src/visualization/plots.py`：視覺化與報告生成。
- `output/analysis_results.json`：分析結果摘要與資料輸出。

## 2.7 方法檢視重點

本研究強調「資料、程式碼與結果的一致性」，其核心包括：

- `analysis_limits.example.json` 決定每個分析的查詢上限。
- `SNARunner` 的最小限制確保複雜分析仍有合理樣本。
- 所有結果以 JSON 儲存，可直接對應到報告文字說明。

以上方法設計意在讓資料來源、程式碼實作與最終報告保持一致。

### 2.7.3 評論網路 (Comments)

| 欄位 | 類型 | 社會網路分析用途 |
|------|------|-----------------|
| `id` | INT | 評論ID |
| `post_id` | INT | 所屬貼文ID |
| `user_id` | INT | 評論者ID |
| `score` | INT | 評論分數 |
| `text` | TEXT | 評論內容 |
| `creation_date` | DATETIME | 創建時間 |

#### SNA 分析方向
- 使用者→貼文 評論網路
- 評論者之間的回覆關係
- 評論情緒分析

### 2.7.4 投票網路 (Votes)

| 欄位 | 類型 | 社會網路分析用途 |
|------|------|-----------------|
| `id` | INT | 投票ID |
| `post_id` | INT | 被投票貼文ID |
| `vote_type_id` | INT | 投票類型 (見下方) |
| `user_id` | INT | 投票者ID |
| `creation_date` | DATETIME | 投票時間 |
| `bounty_amount` | INT | 賞金金額 |

#### VoteTypeId 類型
- `1` = AcceptedByOriginator (提問者接受答案)
- `2` = UpMod (讚)
- `3` = DownMod (噓)
- `4` = Offensive (攻擊性)
- `5` = Favorite (收藏)
- `7` = Reopen
- `8` = BountyStart (懸賞開始)
- `9` = BountyClose (懸賞結束)
- `10` = Deletion
- `11` = Undeletion
- `12` = Spam
- `15` = ModeratorReview

#### SNA 分析方向
- 投票行為網路: User→Post 投票關係
- 賞金網路 (懸賞者→回答者)
- 攻擊性舉報網路

### 2.7.5 徽章網路 (Badges)

| 欄位 | 類型 | 社會網路分析用途 |
|------|------|-----------------|
| `id` | INT | 徽章ID |
| `user_id` | INT | 獲得者ID |
| `name` | STRING | 徽章名稱 |
| `date` | DATETIME | 獲得時間 |
| `class` | INT | 等級: 1=Gold, 2=Silver, 3=Bronze |
| `tag_based` | BOOLEAN | 是否為標籤徽章 |

#### SNA 分析方向
- 成就網路 (誰獲得了什麼徽章)
- 標籤專家網路 (tag-based badges)
- 社群參與度分析

### 2.7.6 標籤網路 (Tags)

| 欄位 | 類型 | 社會網路分析用途 |
|------|------|-----------------|
| `id` | INT | 標籤ID |
| `tag_name` | STRING | 標籤名稱 |
| `count` | INT | 使用次數 |
| `is_moderator_only` | BOOLEAN | 是否僅管理員可用 |
| `is_required` | BOOLEAN | 是否必需 |

#### TagSynonyms (標籤同義詞)
- 標籤別名網路

#### SNA 分析方向
- 標籤共現網路: 哪些標籤常一起出現
- 技術熱度趨勢
- 標籤階層結構

### 2.7.7 貼文歷史網路 (PostHistory)

| 欄位 | 類型 | 社會網路分析用途 |
|------|------|-----------------|
| `id` | INT | 歷史記錄ID |
| `post_id` | INT | 貼文ID |
| `post_history_type_id` | INT | 歷史類型 |
| `user_id` | INT | 執行者ID |
| `creation_date` | DATETIME | 時間 |
| `comment` | TEXT | 備註 |
| `text` | TEXT | 變更內容 |

#### PostHistoryTypeId 類型
- `1-3` = 初始 (標題/內文/標籤)
- `4-6` = 編輯 (標題/內文/標籤)
- `7-9` = 回滾
- `10` = 關閉
- `11` = 重新開啟
- `12` = 刪除
- `13` = 恢復
- `14-15` = 鎖定/解鎖
- `24` = 建議編輯套用

#### SNA 分析方向
- 編輯協作網路: 共同編輯的使用者
- 貼文生命週期
- 關閉/刪除決策網路

### 2.7.8 貼文連結網路 (PostLinks)

| 欄位 | 類型 | 社會網路分析用途 |
|------|------|-----------------|
| `id` | INT | 連結ID |
| `post_id` | INT | 來源貼文ID |
| `related_post_id` | INT | 目標貼文ID |
| `link_type_id` | INT | 連結類型 |
| `creation_date` | DATETIME | 創建時間 |

#### LinkTypeId
- `1` = Linked (引用)
- `3` = Duplicate (重複問題)

#### SNA 分析方向
- 問題引用網路
- 重複問題網路
- 知識傳播路徑

### 2.7.9 建議編輯網路 (SuggestedEdits)

| 欄位 | 類型 | 社會網路分析用途 |
|------|------|-----------------|
| `id` | INT | 編輯ID |
| `post_id` | INT | 目標貼文ID |
| `owner_user_id` | INT | 編輯者ID |
| `creation_date` | DATETIME | 創建時間 |
| `approval_date` | DATETIME | 批准時間 |
| `rejection_date` | DATETIME | 拒絕時間 |

#### SuggestedEditVotes
- 編輯審核網路

#### SNA 分析方向
- 編輯審核網路: 編輯者→審核者
- 新手貢獻網路

### 2.7.10 審核任務網路 (ReviewTasks)

| 欄位 | 類型 | 社會網路分析用途 |
|------|------|-----------------|
| `id` | INT | 任務ID |
| `review_task_type_id` | INT | 任務類型 |
| `post_id` | INT | 貼文ID |
| `creation_date` | DATETIME | 創建時間 |
| `deletion_date` | INT | 刪除時間 |
| `review_task_state_id` | INT | 狀態 |

#### ReviewTaskTypeId
- `1` = Suggested Edit
- `2` = Close Votes
- `3` = Low Quality Posts
- `4` = First Post
- `5` = Late Answer
- `6` = Reopen Vote

#### SNA 分析方向
- 審核協作網路: 審核者之間的互動
- 社群自律網路

### 2.7.11 懸賞網路 (可從 Votes 表提取)

- 懸賞問題 → 懸賞答案
- 賞金分配網路

### 2.7.12 跨站台使用者網路 (sede_users)

- 使用者跨站台帳號關聯
- 網路效應分析

## 2.8 相關研究

本研究的方法論與 Stack Overflow、社會網路分析領域的既有研究對話。例如：

- Ugander et al. (2011) 與 Anderson et al. (2012) 的核心-邊緣網路發現，驗證了線上社群中的結構性中心性與影響力分布。
- Movshovitz-Attias et al. (2013) 與 Bosu et al. (2013) 的聲望系統分析，支撐了本研究聲望與網路角色的探討。
- Edrees (2020) 與 Chen & Xing (2017) 的標籤共現研究，提供了本研究技術領域地圖的分析框架。
- Dunbar（2016）與 Twitter 研究的社交規模理論，為本研究的社群邊緣化與資訊孤島探討提供理論背景。

## 2.9 使用的工具與資料流程

本研究透過 Python 數據分析管線，搭配 Google Cloud SDK 存取 BigQuery 取得 Stack Overflow 資料。分析過程包括：

- 從 BigQuery 抽取 `users`, `posts_questions`, `posts_answers`, `votes`, `comments`, `badges`, `tags`, `post_links`, `post_history`, `review_tasks` 等資料表；
- 清理與轉換資料為社會網路中的節點與關係；
- 以網路指標（如中心性、連通分量、社群結構）量化使用者與標籤互動；
- 匯整分析結果，並以色彩與分類標籤呈現不同群體與行為層次。

這樣的流程讓報告聚焦於研究功能與發現，而不是實作細節。 