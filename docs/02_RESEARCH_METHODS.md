# 02 研究方法

本章節說明本研究採用的資料來源、分析流程與研究設計，強調方法的邏輯而非技術細節。

## 2.1 資料來源

本研究主要使用 Google BigQuery 公共資料集：`bigquery-public-data.stackoverflow`。資料集包含多個相關資料表，主要用於構建社會網路分析所需的節點與關係。

使用的資料表包括：

- `users`
- `posts_questions` / `posts_answers`
- `votes`
- `comments`
- `badges`
- `tags`
- `post_links`
- `post_history`
- `review_tasks`

這些資料表提供了使用者資訊、貼文內容、投票行為、評論互動、徽章成就、標籤關係、問題引用與審核任務等多維度資料。

## 2.2 研究設計

本研究設計 15 個社會網路分析面向，對應不同的研究問題：

1. 使用者聲望與網路中心度
2. 網路核心結構與解答效率
3. 技術標籤共現與領域地圖
4. 知識孤島與連通分量分析
5. 內容特徵與互動反響
6. 帳號年資與社群貢獻
7. 投票行為網路分析
8. 評論互動網路分析
9. 徽章成就網路分析
10. 編輯協作網路分析
11. 引用與重複問題網路分析
12. 審核任務網路分析
13. 賞金懸賞網路分析
14. 使用者地理分布網路分析
15. 時間序列活躍度網路分析

每個分析面向皆以社會網路圖（節點與邊）表示不同的關係，例如使用者之間的回答、投票、評論、共編輯、同標籤共現、引用關係與地理分佈。

## 2.3 研究目的與程式碼對應

本研究的 15 個分析面向對應到現有程式碼模組如下：

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

這些分析由 `src/sna_runner.py` 統一呼叫，並使用 `DataLoader` 綁定 BigQuery 查詢、`SNAPlotter` 生成視覺化圖表。

## 2.4 分析流程

本研究的分析流程可概括為三個階段：

1. **資料取得與預處理**：從 BigQuery 抽取原始資料，依照分析需求清理並轉換為可建構網路的格式。
2. **網路建構與指標計算**：將使用者、貼文或標籤視為節點，將回答、共現、投票等關係視為邊，並計算中心性、連通分量、社群結構等指標。
3. **結果整理與視覺化**：匯整各分析結果，產出摘要與圖表，並比較不同面向間的特徵。

## 2.5 主要分析面向說明

以下為各面向的設計重點與聚合規則：

- **RQ1 使用者聲望與網路中心度**：以回答關係建構使用者網路，並依使用者聲望分為 `1_Low`, `2_Medium`, `3_Senior`, `4_Expert`。同時以介性中心度的中位數區分 `high` / `low` 兩類節點，檢驗聲望與網路橋樑角色的相關性。
- **RQ2 網路核心結構與解答效率**：以 k-core 和節點度數識別核心與邊緣使用者；若節點的 coreness ≥ 最大 coreness的一半，則視為核心。解答效率則依 `hours_to_accept` 列為 `1_VeryFast` (<1 小時)、`2_Fast` (1~12 小時)、`3_Slow` (13~24 小時)、`4_VerySlow` (>24 小時)，並在結果分析中進一步分類為 `high` / `medium` / `low`。
- **RQ3 技術標籤共現與領域地圖**：將標籤依關鍵字映射到領域分類，包括 Web、Backend、Database、Mobile、AI_ML、DevOps、DataScience。未匹配標籤歸入 `Other`，以共現次數建構技術領域圖。
- **RQ4 知識孤島與連通分量分析**：分析回答網路的連通分量，將最大連通分量視為主流社群，將大小 ≤ 5 或非主流的組件視為知識孤島。
- **RQ5 內容特徵與互動反響**：比較是否包含程式碼區塊的貼文，依 `has_code_block` 區分樣本，並根據 `score_level`（從 `1_VeryNegative` 到 `6_ExtremelyPositive`）評估分數分佈。使用 t 檢定驗證有無顯著差異（p < 0.05）。
- **RQ6 帳號年資與社群貢獻**：依註冊時長將使用者分為 `1_New`, `2_Young`, `3_Mature`, `4_Established`, `5_Senior`；並依發文類型分為 `1_Both`, `2_QuestionsOnly`, `3_AnswersOnly`, `4_Neither`，比較各年資群的問題與回答行為。
- **RQ7 投票行為網路分析**：投票數量分為 `1_NoVotes`, `2_Low`, `3_Medium`, `4_High`，並根據使用者最常見的投票類型標記 `accepted`、`upvote`、`downvote`，分析同類投票行為之間的關聯。
- **RQ8 評論互動網路分析**：若兩位評論者曾在同一問題上發表評論，則在評論網路中建構連結。重點在分析評論網路密度與每位評論者的平均評論數。
- **RQ9 徽章成就網路分析**：依使用者的最高徽章類別標記為 `1_Gold`、`2_Silver`、`3_Bronze`、`0_None`，並使用金、銀、銅三色對應視覺符號。
- **RQ10 編輯協作網路分析**：以共同編輯同一篇貼文的使用者建構協作邊，並依編輯次數將使用者分為 `0_None`, `1_Casual`, `2_Active`, `3_Power`。
- **RQ11 引用與重複問題網路分析**：基於 `post_links` 建構有向圖，區分連結類型 `Linked` 與 `Duplicate`，衡量問題之間引導與複製的傳播路徑。
- **RQ12 審核任務網路分析**：將審核操作區分為 `Close`、`Reopen`、`Delete`、`Undelete`、`SuggestedEdit`，並依審核次數將審核者分為 `0_None`, `1_Casual` (≤3), `2_Active` (≤10), `3_Power` (>10)。
- **RQ13 賞金懸賞網路分析**：以懸賞起始／結束投票建立樣本，依每位使用者的賞金次數分為 `0_None`, `1_Meager` (<2), `2_Normal` (2~5), `3_Generous` (6~10), `4_Extravagant` (>10)，並根據共同標籤建立使用者間的相似度連結。
- **RQ14 使用者地理分布網路分析**：根據使用者位置文字映射地區，將位置分類為 North America、Europe、Asia、Oceania、South America、Africa、Middle East、Other，並以區域專屬顏色標記節點。
- **RQ15 時間序列活躍度網路分析**：依每月貼文數量計算活動強度，將月度活動分為 `high` (>1.5×中位數)、`medium` (0.5~1.5×中位數)、`low` (<0.5×中位數)，並分析小時與週日分布。

## 2.6 聚合條件與色彩規則

以下表格整理 RQ1–RQ15 的資料流程、分類標籤與視覺對應。

### RQ1 使用者聲望與網路中心度

| 條件 | 來源 | 規則 | 顏色/標籤 |
|------|------|------|-----------|
| 聲望等級 | Stack Overflow `users` 資料 | `<1000 → 1_Low`; `1000-10000 → 2_Medium`; `10001-50000 → 3_Senior`; `>50000 → 4_Expert`; 其他 `0_None` | 聲望分群可對應色彩梯度 |
| 中心度分組 | 使用者回答互動網路 | `betweenness >= median → high`; 否則 `low` | 高/低網路橋樑分群 |

### RQ2 網路核心結構與解答效率

| 條件 | 來源 | 規則 | 顏色/標籤 |
|------|------|------|-----------|
| 核心判斷 | Stack Overflow `posts` 與使用者互動關係 | `degree >= median_deg → is_core` | 核心/邊緣 |
| 解答效率 | Stack Overflow 問題 / 回答時差 | `<1h → 1_VeryFast`; `1-12h → 2_Fast`; `13-24h → 3_Slow`; `>24h → 4_VerySlow`; 否則 `0_Unresolved` | 綠/黃/淺紅/紅/灰 |
| 效率分群 | 回答採納時間分佈 | `0-1 → VeryFast`; `1-24 → Fast`; `24-168 → Slow`; `>168 → VerySlow` | 進一步檢視長尾回應時間 |

### RQ3 技術標籤共現與領域地圖

| 條件 | 來源 | 規則 | 顏色/標籤 |
|------|------|------|-----------|
| 技術領域分類 | Stack Overflow 標籤共現資料 | 根據標籤文字匹配 keyword lists 將標籤歸類為 Web、Backend、Database、Mobile、AI_ML、DevOps、DataScience，其他歸入 `Other` | 不同領域可用不同色彩群組 |

### RQ4 知識孤島與連通分量

| 條件 | 來源 | 規則 | 顏色/標籤 |
|------|------|------|-----------|
| 主流組件 | `ConnectedComponentAnalyzer._analyze_connected_components` | 最大連通分量視為主連通分量 | 主/次成分區分 |
| 孤島判斷 | `ConnectedComponentAnalyzer._identify_knowledge_islands` | `size <= 5` 或 `not is_main_component` → 知識孤島 | 灰色、低互動區塊 |
| 連通性等級 | BigQuery 連通性查詢 | `0 → 1_Isolated`; `1-5 → 2_Low`; `6-20 → 3_Medium`; `>20 → 4_Active` | 互動強度分層 |

### RQ5 內容特徵與互動反響

| 條件 | 來源 | 規則 | 顏色/標籤 |
|------|------|------|-----------|
| 是否含程式碼 | Stack Overflow 帖文內容分析 | `body` 含 ` ``` ` 或 `<code>` → `has_code_block = 1`; 否則 `0` | 有程式碼 / 無程式碼 |
| 分數等級 | Stack Overflow 帖文分數資料 | `<= -5 → 1_VeryNegative`; `-4~-1 → 2_Negative`; `0 → 3_Neutral`; `1~5 → 4_Positive`; `6~20 → 5_VeryPositive`; 其他 → `6_ExtremelyPositive` | 可視化為情緒色彩梯度 |

### RQ6 帳號年資與社群貢獻

| 條件 | 來源 | 規則 | 顏色/標籤 |
|------|------|------|-----------|
| 年資等級 | BigQuery 帳號年資查詢 | `<365d → 1_New`; `365-1095d → 2_Young`; `1096-2190d → 3_Mature`; `2191-3650d → 4_Established`; `>3650d → 5_Senior` | 年資色彩漸層 |
| 發文類型 | 使用者貼文類型統計 | 具有問答雙向 → `1_Both`; 只有問題 → `2_QuestionsOnly`; 只有回答 → `3_AnswersOnly`; 否則 `4_Neither` | 區分問題型 / 回答型 / 混合型 |

### RQ7 投票行為網路

| 條件 | 來源 | 規則 | 顏色/標籤 |
|------|------|------|-----------|
| 投票類型 | Stack Overflow `votes` 資料處理 | `1 → accepted`; `2 → upvote`; `3 → downvote` | `accepted`, `upvote`, `downvote` |
| 投票等級 | 投票數量統計 | `0 → 1_NoVotes`; `1-3 → 2_Low`; `4-10 → 3_Medium`; `>10 → 4_High` | 投票活躍度分層 |
| 主導投票 | 投票行為聚合 | 以最多次出現的投票類型為 `vote_type` | 典型行為標籤 |

### RQ8 評論互動網路

| 條件 | 來源 | 規則 | 顏色/標籤 |
|------|------|------|-----------|
| 評論連結 | `comments` 資料分析 | 同一貼文上出現兩位評論者 → 建立邊 | 評論共現網路 |
| 節點屬性 | 評論者統計資料 | `comment_count`、`reputation` | 互動強度 / 信任度 |

### RQ9 徽章成就網路

| 條件 | 來源 | 規則 | 顏色/標籤 |
|------|------|------|-----------|
| 徽章類別 | `badges` 資料統計 | `class=1 → Gold`; `2 → Silver`; `3 → Bronze` | `#FFD700`, `#C0C0C0`, `#CD7F32` |
| 使用者級別 | 徽章成就彙整 | `gold > 0 → 1_Gold`; 否則 `silver > 0 → 2_Silver`; 否則 `bronze > 0 → 3_Bronze`; 否則 `0_None` | 成就層級視覺化 |

### RQ10 編輯協作網路

| 條件 | 來源 | 規則 | 顏色/標籤 |
|------|------|------|-----------|
| 協作連結 | `post_history` 編輯協作分析 | 同一貼文上出現兩位編輯者 → 建立邊 | 協作網路 |
| 編輯等級 | 編輯次數統計 | `0 → 0_None`; `1-2 → 1_Casual`; `3-5 → 2_Active`; `>5 → 3_Power` | 參與強度分層 |

### RQ11 引用與重複問題網路

| 條件 | 來源 | 規則 | 顏色/標籤 |
|------|------|------|-----------|
| 連結類型 | `post_links` 資料處理 | `link_type_id=1 → Linked`; `3 → Duplicate`; 其他 → Other | `Linked` / `Duplicate` |
| 有向關係 | 問題引用方向分析 | 設定 `source_post_id → target_post_id` 的有向邊 | 知識傳播方向 |

### RQ12 審核任務網路

| 條件 | 來源 | 規則 | 顏色/標籤 |
|------|------|------|-----------|
| 審核類型 | `post_history` / 審核任務資料分析 | `10 → Close`; `11 → Reopen`; `12 → Delete`; `13 → Undelete`; `24 → SuggestedEdit`; 其他 → Other | 審核行為類別 |
| 審核等級 | 審核參與次數統計 | `0 → 0_None`; `1-3 → 1_Casual`; `4-10 → 2_Active`; `>10 → 3_Power` | 治理參與分層 |

### RQ13 賞金懸賞網路

| 條件 | 來源 | 規則 | 顏色/標籤 |
|------|------|------|-----------|
| 賞金類型 | `votes` 資料中賞金相關票種 | `8 → BountyStart`; `9 → BountyClose`; 其他 → Other | 賞金行為類別 |
| 賞金等級 | 懸賞次數統計 | `0 → 0_None`; `1 → 1_Meager`; `2-5 → 2_Normal`; `6-10 → 3_Generous`; `>10 → 4_Extravagant` | 參與強度分層 |
| 技術相似度 | 懸賞問題標籤共現 | 共同標籤數量 >0 → 連結邊 | 懸賞話題重疊 |

### RQ14 使用者地理分布網路

| 條件 | 來源 | 規則 | 顏色/標籤 |
|------|------|------|-----------|
| 地區分類 | 使用者位置文字分析 | 依 location 文字匹配 North America、Europe、Asia、Oceania、South America、Africa、Middle East，未匹配為 `Other` | `#2196F3`, `#4CAF50`, `#FFC107`, `#9E9E9E`, `#FF5722`, `#795548`, `#607D8B`, `#BDBDBD` |
| 地理強度 | 地理區域使用者計數 | `user_count` 代表該區域使用者數量 | 區域節點大小/色彩 |

### RQ15 時間序列活躍度網路

| 條件 | 來源 | 規則 | 顏色/標籤 |
|------|------|------|-----------|
| 月度活動 | 月度貼文量統計 | `post_count >= 1.5*median → high`; `>= 0.5*median → medium`; 否則 `low` | 活躍度等級 |
| 時段分布 | 貼文時間分布分析 | 依 `hour`、`day_of_week` 聚合貼文數 | 時間規律分析 |

## 2.7 資料集特徵概覽

本研究使用的 BigQuery 公共資料集是 `bigquery-public-data.stackoverflow`，其資料表提供了構建社會網路分析所需的節點資訊與關係資訊。以下依表格與主要分析方向，說明各資料表的欄位角色與社會網路分析用途。

### 2.7.1 使用者網路 (Users)

| 欄位 | 類型 | 社會網路分析用途 |
|------|------|-----------------|
| `id` | INT | 使用者節點識別碼 |
| `reputation` | INT | **聲望值** - 核心社交資本指標 |
| `creation_date` | DATETIME | 帳號創建時間 |
| `last_access_date` | DATETIME | 最後上線時間 |
| `display_name` | STRING | 使用者名稱 |
| `location` | STRING | 地理位置 |
| `about_me` | TEXT | 個人簡介 |
| `views` | INT | 個人頁面瀏覽次數 |
| `up_votes` | INT | 投出讚數 |
| `down_votes` | INT | 投出噓數 |
| `website_url` | STRING | 個人網站 |

#### SNA 分析方向
- 聲望分布分析 (冪律驗證)
- 使用者活躍度網路
- 地理位置網路
- 新手→老手成長網路

### 2.7.2 貼文網路 (Posts)

| 欄位 | 類型 | 社會網路分析用途 |
|------|------|-----------------|
| `id` | INT | 貼文識別碼 |
| `post_type_id` | INT | 類型: 1=Question, 2=Answer, 3-17=其他 |
| `accepted_answer_id` | INT | 獲納答案ID |
| `parent_id` | INT | (Answer專用) 所屬問題ID |
| `score` | INT | 分數 (讚-噓) |
| `view_count` | INT | 瀏覽次數 |
| `answer_count` | INT | 答案數量 |
| `comment_count` | INT | 評論數量 |
| `favorite_count` | INT | 收藏數 |
| `owner_user_id` | INT | 發文者ID |
| `creation_date` | DATETIME | 創建時間 |
| `last_edit_date` | DATETIME | 最後編輯時間 |
| `last_activity_date` | DATETIME | 最後活動時間 |
| `title` | STRING | 標題 |
| `tags` | STRING | 標籤 (以\|分隔) |
| `closed_date` | DATETIME | 關閉時間 |
| `body` | TEXT | 內文 (HTML) |

#### SNA 分析方向
- 問答網路: Question→Answer 關係
- 引用網路: 問題之間的 duplicate/linked 關係
- 編輯網路: 共同編輯同一貼文的使用者
- 獲納答案時間分析
- 熱門問題傳播網路

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