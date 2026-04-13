# 03 分析結果

本章節彙整 `output/analysis_results.json` 中的實際結果，並搭配 `output/analysis_*.png` 圖片說明每個分析面向的觀察。

## 3.1 概覽

本研究透過 `src/sna_runner.py` 執行 15 個分析，生成的結果包括圖形網路、資料表與摘要統計。以下為各面向的實際觀察：

- `analysis_1_centrality`：146 名使用者節點，85 位低聲望使用者；高聲望使用者在本樣本中未被分類為高聲望群組。
- `analysis_2_core_efficiency`：100 筆問題樣本全部被判定為核心用戶，平均回應時間 2932.42 小時，結果未顯示核心更快。
- `analysis_3_tag_cooccurrence`：88 個標籤、100 次共現，分成 8 個領域與 13 個社群，模組度 0.7322。
- `analysis_4_connected_components`：100 個連通分量，主成分大小 2，隔離比率 1.0，顯示樣本以極小成分為主。
- `analysis_5_content_features`：100 篇貼文中 82 篇含程式碼，含程式碼貼文平均分 0.585，未含程式碼貼文平均分 0.944；差異未達顯著（p=0.2056）。
- `analysis_6_account_age`：119 位使用者分布在 Mature、Established、Senior 三類，平均帳號年齡 3202 天；新手與資深假設均未被樣本支持。
- `analysis_7_voting_behavior`：20,000 次投票、18,481 位獨立投票者，平均每人 1.08 次，主要為 upvote。
- `analysis_8_comment_network`：20,000 則評論、3,002 名評論者，網路密度 0.00034。
- `analysis_9_badge_network`：500 枚徽章、491 位使用者，平均每人 1.02 枚徽章。
- `analysis_10_edit_collaboration`：100,000 次編輯、16,830 位編輯者，平均 5.86 次編輯。
- `analysis_11_post_link`：500 條連結、636 篇貼文，重複問題比例 29.4%。
- `analysis_12_review_task`：500 次審核、112 位審核者，平均 2.55 次審核。
- `analysis_13_bounty_network`：26,346 次賞金行為、500 位使用者，平均 2.11 次賞金，`BountyStart` 17,868 次、`BountyClose` 8,478 次。
- `analysis_14_user_location`：500 位使用者分布於 8 個區域，歐洲為最大區域（167 人）。
- `analysis_15_time_series`：100,000 篇貼文、12 個月資料，最高月份為 2021-03，平均每月 8,333 篇；每日高峰為週四，時間高峰為 14–15 點。

## 3.2 各分析重點與圖像說明

### 3.2.1 使用者聲望與網路中心度

![RQ1 使用者聲望與網路中心度](../output/analysis_1_network.png)

本圖展示 `analysis_1_network.png` 的使用者中心性網路，呈現節點依聲望與連接模式分布。樣本中的低聲望節點數量多於高聲望節點，且高聲望組未被完整建立。

### 3.2.2 網路核心結構與解答效率

![RQ2 網路核心結構與解答效率](../output/analysis_2_network.png)

`analysis_2_network.png` 顯示核心與邊緣的回答效率結構。本次樣本中所有節點皆被歸類為核心，因此圖像重點在核心網路結構與回應時間分布。

### 3.2.3 技術標籤共現與領域地圖

![RQ3 技術標籤共現](../output/analysis_3_network.png)

此圖形表示 `analysis_3_network.png` 的標籤共現網路，標示 88 個標籤在 8 個領域中的群聚。模組度 0.7322 顯示標籤網路具有明顯社群分群。

### 3.2.4 知識孤島與連通分量

![RQ4 知識孤島與連通分量](../output/analysis_4_network.png)

`analysis_4_network.png` 呈現連通分量分布。由於主成分大小僅 2，本圖反映大量微小組合與孤立子網路。

### 3.2.5 內容特徵與互動反饋

![RQ5 內容特徵與互動反饋](../output/analysis_5_network.png)

本圖為 `analysis_5_network.png`，用以視覺化含程式碼與不含程式碼貼文的互動關係。結果顯示含程式碼貼文並不一定獲得更高評分。

### 3.2.6 帳號年資與行為差異

![RQ6 帳號年資與行為差異](../output/analysis_6_network.png)

`analysis_6_network.png` 描述使用者帳號年資分布與行為類型。樣本主要包含 Mature、Established、Senior 年資群，並未顯示新手占比。

### 3.2.7 投票行為網路

![RQ7 投票行為網路](../output/analysis_7_network.png)

此圖呈現投票者與投票類型之間的關係結構。大量 `upvote` 投票使得網路中正向投票聯繫顯著。

### 3.2.8 評論互動網路

![RQ8 評論互動網路](../output/analysis_8_network.png)

`analysis_8_network.png` 呈現評論者在同一問題上的共現網路。稀疏的連結與低網路密度顯示評論互動多為分散型。

### 3.2.9 徽章成就網路

![RQ9 徽章成就網路](../output/analysis_9_network.png)

本圖說明徽章擁有者的網路分布。平均每位擁有徽章的使用者約 1 枚，呈現多數使用者僅擁有少量徽章的特徵。

### 3.2.10 編輯協作網路

![RQ10 編輯協作網路](../output/analysis_10_network.png)

`analysis_10_network.png` 顯示共同編輯行為構成的協作網路。100,000 次編輯與 16,830 位編輯者反映出廣泛的維護參與。

### 3.2.11 引用與重複問題網路

![RQ11 引用與重複問題網路](../output/analysis_11_network.png)

`analysis_11_network.png` 以 `post_links` 為基礎，呈現問題間的 `Linked` 與 `Duplicate` 關係。重複問題比例達 29.4%。

### 3.2.12 審核任務網路

![RQ12 審核任務網路](../output/analysis_12_network.png)

本圖呈現不同審核類型與審核者之間的網路結構。`SuggestedEdit` 及 `Close` 是本樣本中最常見的審核行為。

### 3.2.13 賞金懸賞網路

![RQ13 賞金懸賞網路](../output/analysis_13_network.png)

`analysis_13_network.png` 表示賞金相關行為網路。活躍的 `BountyStart` 與 `BountyClose` 標示賞金活動的流動。

### 3.2.14 使用者地理分布

![RQ14 使用者地理分布](../output/analysis_14_network.png)

此圖描述使用者位置群聚。歐洲為最大區域，顯示地理分布的區域集中現象。

### 3.2.15 時間序列活躍度

![RQ15 時間序列活躍度](../output/analysis_15_network.png)

`analysis_15_network.png` 呈現時間序列活動網路，反映每月與每日的活躍趨勢，最高活動時間出現在 14–15 點。

## 3.3 結果與方法的對應

本章結果直接取自 `output/analysis_results.json`，並與 `src/sna_runner.py` 的分析流程對應。這些數據說明了哪些假設被支援、哪些假設未被支援，與哪部分結果顯示樣本選取的特殊性。
