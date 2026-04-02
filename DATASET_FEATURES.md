# Stack Overflow 資料集社會網路分析特徵總覽

## 資料來源
- **BigQuery**: `bigquery-public-data.stackoverflow`
- **Schema 文件**: https://meta.stackexchange.com/questions/2677/database-schema-documentation-for-the-public-data-dump-and-sede

---

## 一、使用者網路 (Users)

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

### SNA 分析方向
- 聲望分布分析 (冪律驗證)
- 使用者活跃度網路
- 地理位置網路
- 新手→老手成長網路

---

## 二、貼文網路 (Posts)

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

### SNA 分析方向
- **問答網路**: Question→Answer 關係
- **引用網路**: 問題之間的 duplicate/linked 關係
- **編輯網路**: 共同編輯同一貼文的使用者
- 獲納答案時間分析
- 熱門問題傳播網路

---

## 三、評論網路 (Comments)

| 欄位 | 類型 | 社會網路分析用途 |
|------|------|-----------------|
| `id` | INT | 評論ID |
| `post_id` | INT | 所屬貼文ID |
| `user_id` | INT | 評論者ID |
| `score` | INT | 評論分數 |
| `text` | TEXT | 評論內容 |
| `creation_date` | DATETIME | 創建時間 |

### SNA 分析方向
- 使用者→貼文 評論網路
- 評論者之間的回覆關係
- 評論情緒分析

---

## 四、投票網路 (Votes)

| 欄位 | 類型 | 社會網路分析用途 |
|------|------|-----------------|
| `id` | INT | 投票ID |
| `post_id` | INT | 被投票貼文ID |
| `vote_type_id` | INT | 投票類型 (見下方) |
| `user_id` | INT | 投票者ID |
| `creation_date` | DATETIME | 投票時間 |
| `bounty_amount` | INT | 賞金金額 |

### VoteTypeId 類型
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

### SNA 分析方向
- **投票行為網路**: User→Post 投票關係
- 賞金網路 (懸賞者→回答者)
- 攻擊性舉報網路

---

## 五、徽章網路 (Badges)

| 欄位 | 類型 | 社會網路分析用途 |
|------|------|-----------------|
| `id` | INT | 徽章ID |
| `user_id` | INT | 獲得者ID |
| `name` | STRING | 徽章名稱 |
| `date` | DATETIME | 獲得時間 |
| `class` | INT | 等級: 1=Gold, 2=Silver, 3=Bronze |
| `tag_based` | BOOLEAN | 是否為標籤徽章 |

### SNA 分析方向
- 成就網路 (誰獲得了什麼徽章)
- 標籤專家網路 (tag-based badges)
- 社群參與度分析

---

## 六、標籤網路 (Tags)

| 欄位 | 類型 | 社會網路分析用途 |
|------|------|-----------------|
| `id` | INT | 標籤ID |
| `tag_name` | STRING | 標籤名稱 |
| `count` | INT | 使用次數 |
| `is_moderator_only` | BOOLEAN | 是否僅管理員可用 |
| `is_required` | BOOLEAN | 是否必需 |

### TagSynonyms (標籤同義詞)
- 標籤別名網路

### SNA 分析方向
- **標籤共現網路**: 哪些標籤常一起出現
- 技術熱度趨勢
- 標籤階層結構

---

## 七、貼文歷史網路 (PostHistory)

| 欄位 | 類型 | 社會網路分析用途 |
|------|------|-----------------|
| `id` | INT | 歷史記錄ID |
| `post_id` | INT | 貼文ID |
| `post_history_type_id` | INT | 歷史類型 |
| `user_id` | INT | 執行者ID |
| `creation_date` | DATETIME | 時間 |
| `comment` | TEXT | 備註 |
| `text` | TEXT | 變更內容 |

### PostHistoryTypeId 類型
- `1-3` = 初始 (標題/內文/標籤)
- `4-6` = 編輯 (標題/內文/標籤)
- `7-9` = 回滾
- `10` = 關閉
- `11` = 重新開啟
- `12` = 刪除
- `13` = 恢復
- `14-15` = 鎖定/解鎖
- `24` = 建議編輯套用

### SNA 分析方向
- **編輯協作網路**: 共同編輯的使用者
- 貼文生命週期
- 關閉/刪除決策網路

---

## 八、貼文連結網路 (PostLinks)

| 欄位 | 類型 | 社會網路分析用途 |
|------|------|-----------------|
| `id` | INT | 連結ID |
| `post_id` | INT | 來源貼文ID |
| `related_post_id` | INT | 目標貼文ID |
| `link_type_id` | INT | 連結類型 |
| `creation_date` | DATETIME | 創建時間 |

### LinkTypeId
- `1` = Linked (引用)
- `3` = Duplicate (重複問題)

### SNA 分析方向
- **問題引用網路**
- 重複問題網絡
- 知識傳播路徑

---

## 九、建議編輯網路 (SuggestedEdits)

| 欄位 | 類型 | 社會網路分析用途 |
|------|------|-----------------|
| `id` | INT | 編輯ID |
| `post_id` | INT | 目標貼文ID |
| `owner_user_id` | INT | 編輯者ID |
| `creation_date` | DATETIME | 創建時間 |
| `approval_date` | DATETIME | 批准時間 |
| `rejection_date` | DATETIME | 拒絕時間 |

### SuggestedEditVotes
- 編輯審核網路

### SNA 分析方向
- **編輯審核網路**: 編輯者→審核者
- 新手貢獻網路

---

## 十、審核任務網路 (ReviewTasks)

| 欄位 | 類型 | 社會網路分析用途 |
|------|------|-----------------|
| `id` | INT | 任務ID |
| `review_task_type_id` | INT | 任務類型 |
| `post_id` | INT | 貼文ID |
| `creation_date` | DATETIME | 創建時間 |
| `deletion_date` | DATETIME | 刪除時間 |
| `review_task_state_id` | INT | 狀態 |

### ReviewTaskTypeId
- `1` = Suggested Edit
- `2` = Close Votes
- `3` = Low Quality Posts
- `4` = First Post
- `5` = Late Answer
- `6` = Reopen Vote

### SNA 分析方向
- **審核協作網路**: 審核者之間的互動
- 社群自律網路

---

## 十一、懸賞網路 (可從 Votes 表提取)

- 懸賞問題 → 懸賞答案
- 賞金分配網路

---

## 十二、跨站台使用者網路 (sede_users)

- 使用者跨站台帳號關聯
- 網路效應分析

---

## 社會網路分析類型總整理

### 1. 互動網路 (Interaction Networks)
| 網路類型 | 節點 | 邊 | 資料表 |
|----------|------|-----|--------|
| 問答網路 | 使用者 | 回答關係 | Posts |
| 評論網路 | 使用者 | 評論關係 | Comments |
| 投票網路 | 使用者 | 投票關係 | Votes |
| 編輯網路 | 使用者 | 共同編輯 | PostHistory |
| 審核網路 | 使用者 | 審核關係 | ReviewTasks |

### 2. 內容網路 (Content Networks)
| 網路類型 | 節點 | 邊 | 資料表 |
|----------|------|-----|--------|
| 標籤共現網路 | 標籤 | 共現關係 | Posts.tags |
| 引用網路 | 貼文 | 引用關係 | PostLinks |
| 重複問題網路 | 貼文 | 重複關係 | PostLinks |

### 3. 聲望/權力網路 (Reputation/Power Networks)
| 網路類型 | 節點 | 邊 | 資料表 |
|----------|------|-----|--------|
| 聲望傳播網路 | 使用者 | 聲望流動 | Votes + Posts |
| 徽章成就網路 | 使用者 | 獲得關係 | Badges |
| 懸賞網路 | 使用者 | 賞金關係 | Votes |

### 4. 時間序列網路 (Temporal Networks)
- 使用者上線模式
- 問題熱度傳播
- 技術趨勢演變

---

## 推薦的擴展分析主題

基於完整資料集，建議新增以下分析：

1. **投票行為分析**: 分析 UpVote/DownVote 模式
2. **編輯協作分析**: 多人共同編輯的協作網路
3. **審核網路**: Close/Reopen 投票網路
4. **賞金網路**: 懸賞問答的知識流動
5. **引用網路**: PostLinks 的知識傳播
6. **建議編輯網路**: 新手貢獻審核網路
7. **跨標籤技術發展地圖**: 更完整的標籤分析
8. **使用者活躍度週期**: 建立時間→最後上線分析
9. **攻擊性行為網路**: 識別 VoteTypeId=4, 12 的惡意行為
10. **版主行為網路**: ModeratorReview 類型的審核行為
