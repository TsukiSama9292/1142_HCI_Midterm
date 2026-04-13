# Stack Overflow 社會網路分析 (SNA)

## 專案概述

本研究旨在透過社會網路分析 (Social Network Analysis, SNA) 方法，解構全球最大技術問答社群 Stack Overflow 的知識流動與互動結構。

### 為什麼選擇這個研究方向？

Stack Overflow 具備獨特的聲望機制與標籤系統，為學術探討網路社群生態提供了量化依據。不同於傳統論壇，其「聲望獎勵機制」驅動知識分享，形成典型的「冪律分布」結構——少數核心貢獻者產出大部分高品質內容。

### 為什麼這麼設計？

1. **igraph 圖形建模**：選擇 Python 的 `igraph` 庫而非圖形界面工具，是因為能進行大規模圖形建模與中心性分析，適合處理數百萬筆資料的網路結構運算。

2. **BigQuery 資料來源**：使用 Google BigQuery 公共數據集 (`bigquery-public-data.stackoverflow`)，無需下載龐大資料即可進行 SQL 查詢分析。

3. **15 個分析維度**：涵蓋 15 個社會網路分析主題，形成完整的社群生態分析框架。

## 安裝

```bash
# 建立虛擬環境
python3 -m venv .venv
source .venv/bin/activate

# 安裝依賴
pip install pandas numpy scipy scikit-learn igraph matplotlib google-cloud-bigquery
```

## 使用方式

### 執行所有分析 (預設取 100 筆資料)

```bash
python main.py
# 或
python main.py --run all
```

### 執行特定分析

```bash
# 分析 1: 使用者聲望與網路中心度
python main.py --run 1

# 分析 2: 網路核心結構與解答效率
python main.py --run 2

# 分析 3: 技術標籤共現與領域地圖
python main.py --run 3

# 分析 4: 知識孤島與連通分量分析
python main.py --run 4

# 分析 5: 內容特徵與互動反響
python main.py --run 5

# 分析 6: 帳號年資與社群貢獻
python main.py --run 6

# 分析 7: 投票行為網路
python main.py --run 7

# 分析 8: 評論互動網路
python main.py --run 8

# 分析 9: 徽章成就網路
python main.py --run 9

# 分析 10: 編輯協作網路
python main.py --run 10

# 分析 11: 引用與重複問題網路
python main.py --run 11

# 分析 12: 審核任務網路
python main.py --run 12

# 分析 13: 賞金懸賞網路
python main.py --run 13

# 分析 14: 使用者地理分布網路
python main.py --run 14

# 分析 15: 時間序列活躍度網路
python main.py --run 15
```

### 分析模組詳細表格

| 分析編號 | 分析名稱 | 研究問題 | 圖形節點 | 圖形邊 | 視覺化屬性 |
|----------|----------|----------|----------|--------|------------|
| 1 | CentralityAnalyzer | 高聲望使用者是否處於網路核心位置？ | 使用者 | 回答關係 | 顏色:聲望等級, 形狀:中心度 |
| 2 | CoreEfficiencyAnalyzer | 核心發問者的問題是否更快解決？ | 使用者 | 互動關係 | 顏色:解答時間, 形狀:核心/邊緣 |
| 3 | TagCooccurrenceAnalyzer | 如何建構技術發展地圖？ | 標籤 | 共現關係 | 顏色:技術領域, 大小:熱度 |
| 4 | ConnectedComponentAnalyzer | 是否存在技術孤島？ | 使用者 | 技術交流 | 顏色:連通性, 形狀:互動類型 |
| 5 | ContentFeatureAnalyzer | 程式碼區塊對回饋的影響 | 貼文 | 相似標籤 | 顏色:分數, 形狀:程式碼存在 |
| 6 | AccountAgeAnalyzer | 老手與新手行為差異 | 使用者 | 問答關係 | 顏色:年資, 形狀:發文類型 |
| 7 | VotingBehaviorAnalyzer | 投票行為與使用者影響力的關係 | 使用者 | 投票關係 | 顏色:投票類型 |
| 8 | CommentNetworkAnalyzer | 評論者之間是否存在緊密的社交網路？ | 使用者 | 評論關係 | 顏色:評論數量 |
| 9 | BadgeNetworkAnalyzer | 徽章與專業領域的關係 | 使用者 | 共同徽章 | 顏色:徽章等級 |
| 10 | EditCollaborationAnalyzer | 哪些使用者之間存在編輯協作關係？ | 使用者 | 共同編輯 | 顏色:編輯者等級 |
| 11 | PostLinkAnalyzer | 引用網路與知識傳播 | 貼文 | 引用關係 | 顏色:連結類型 |
| 12 | ReviewTaskAnalyzer | 哪些使用者積極參與社群審核任務？ | 使用者 | 共同審核 | 顏色:審核者等級 |
| 13 | BountyNetworkAnalyzer | 賞金效能分析 | 使用者 | 賞金關係 | 顏色:賞金等級 |
| 14 | UserLocationAnalyzer | 地理位置分布 | 國家/城市 | 連接 | 顏色:區域 |
| 15 | TimeSeriesAnalyzer | 使用者上線模式的時間規律 | 月份 | 活動關係 | 顏色:活躍度 |

### 自訂參數

```bash
# 指定資料筆數
python main.py --run 3 --limit 200

# 指定輸出目錄
python main.py --run all -o output/
```

## 研究方法對應

| # | 研究問題 | 分析主題 | 圖形節點 | 圖形邊 | 視覺化屬性 |
|---|---------|---------|---------|--------|-----------|
| 1 | 高聲望使用者是否處於網路核心位置？ | 使用者聲望與網路中心度 | 使用者 | 回答關係 | 顏色:聲望等級, 形狀:中心度 |
| 2 | 核心發問者的問題是否更快解決？ | 網路核心結構與解答效率 | 使用者 | 互動關係 | 顏色:解答時間, 形狀:核心/邊緣 |
| 3 | 如何建構技術發展地圖？ | 技術標籤共現與領域地圖 | 標籤 | 共現關係 | 顏色:技術領域, 大小:熱度 |
| 4 | 是否存在技術孤島？ | 知識孤島與連通分量分析 | 使用者 | 技術交流 | 顏色:連通性, 形狀:互動類型 |
| 5 | 程式碼區塊對回饋的影響 | 內容特徵與互動反響 | 貼文 | 相似標籤 | 顏色:分數, 形狀:程式碼存在 |
| 6 | 老手與新手行為差異 | 帳號年資與社群貢獻 | 使用者 | 問答關係 | 顏色:年資, 形狀:發文類型 |
| 7 | 投票行為與使用者影響力的關係 | 投票行為網路 | 使用者 | 投票關係 | 顏色:投票類型 |
| 8 | 評論者之間是否存在緊密的社交網路？ | 評論互動網路 | 使用者 | 評論關係 | 顏色:評論數量 |
| 9 | 徽章與專業領域的關係 | 徽章成就網路 | 使用者 | 共同徽章 | 顏色:徽章等級 |
| 10 | 哪些使用者之間存在編輯協作關係？ | 編輯協作網路 | 使用者 | 共同編輯 | 顏色:編輯者等級 |
| 11 | 引用網路與知識傳播 | 引用與重複問題網路 | 貼文 | 引用關係 | 顏色:連結類型 |
| 12 | 哪些使用者積極參與社群審核任務？ | 審核任務網路 | 使用者 | 共同審核 | 顏色:審核者等級 |
| 13 | 賞金效能分析 | 賞金懸賞網路 | 使用者 | 賞金關係 | 顏色:賞金等級 |
| 14 | 地理位置分布 | 使用者地理分布網路 | 國家/城市 | 連接 | 顏色:區域 |
| 15 | 使用者上線模式的時間規律 | 時間序列活躍度網路 | 月份 | 活動關係 | 顏色:活躍度 |

## 專案結構

```
1141_HCI_Midterm/
├── main.py                  # 命令列工具
├── src/
│   ├── config.py           # 設定
│   ├── sna_runner.py       # 分析執行器 (整合15個分析)
│   ├── data/
│   │   ├── bigquery_client.py  # BigQuery API 封裝
│   │   └── data_loader.py      # 資料載入器 (SQL查詢)
│   ├── models/
│   │   └── graph_builder.py    # igraph 圖形建構器
│   ├── analysis/
│   │   ├── centrality.py       # 分析1: 中心度計算
│   │   ├── core_efficiency.py  # 分析2: 核心效率
│   │   ├── tag_cooccurrence.py # 分析3: 標籤共現
│   │   ├── connected_components.py # 分析4: 連通分量
│   │   ├── content_features.py # 分析5: 內容特徵
│   │   ├── account_age.py      # 分析6: 帳號年資
│   │   ├── voting_behavior.py  # 分析7: 投票行為
│   │   ├── comment_network.py  # 分析8: 評論互動
│   │   ├── badge_network.py    # 分析9: 徽章成就
│   │   ├── edit_collaboration.py # 分析10: 編輯協作
│   │   ├── post_link.py        # 分析11: 引用與重複
│   │   ├── review_task.py      # 分析12: 審核任務
│   │   ├── bounty_network.py   # 分析13: 賞金懸賞
│   │   ├── user_location.py    # 分析14: 使用者地理
│   │   └── time_series.py      # 分析15: 時間序列
│   └── visualization/
│       └── plots.py           # igraph 視覺化工具
├── tests/                   # 測試
└── output/                  # 分析結果輸出
```

## 程式碼流程說明

### 1. 資料載入 (data_loader.py)

```
DataLoader.load_posts_with_answers() 
  -> BigQuery SQL 查詢
  -> 回傳含解答時間的問題資料

DataLoader.load_users() 
  -> BigQuery SQL 查詢  
  -> 回傳含聲望等級的用戶資料
```

### 2. 圖形建構 (graph_builder.py)

```
UserNetworkBuilder.build_answer_network_with_reputation()
  -> 建立回答者->發問者的有向圖
  -> 計算 betweenness centrality
  -> 設定節點屬性 (reputation, centrality_level)
```

### 3. 分析執行 (analysis/*.py)

```
CentralityAnalyzer.run()
  -> 建構網路圖
  -> 計算中心度指標 (betweenness, degree, closeness, pagerank)
  -> 計算聲望與中心度相關係數
  -> 回傳分析結果
```

### 4. 視覺化 (plots.py)

```
SNAPlotter.plot_network_graph()
  -> 使用 igraph layout (Fruchterman-Reingold)
  -> 根據屬性設定顏色/形狀/大小
  -> 輸出 PNG 圖片
```

## 資料來源

- **BigQuery 公共數據集**: `bigquery-public-data.stackoverflow`
- **認證**: 使用 Google Cloud 應用程式預設憑證 (ADC)

## 作者

TsukiSama9292 - a0985821880@gmail.com
