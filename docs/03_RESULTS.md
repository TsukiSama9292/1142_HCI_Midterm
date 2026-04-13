# 分析結果

本章節彙整 `output/analysis_results.json` 中的實際結果，並搭配 `output/analysis_*.png` 圖片說明每個分析面向的觀察。

本報告同時提供兩種圖像版本：
- **raw**：原始網路輸出圖，顯示分析結果的基礎節點與邊結構。
- **aggregated**：聚合後的圖表，強調分群、區域或主題之間的關係。

## 圖像總覽表

| 分析編號 | 原始圖 (raw) | 聚合圖 | 圖像說明 |
|---|---|---|---|
| RQ1 | ![RQ1 raw](../output/analysis_1_network_raw.png) | ![RQ1 agg](../output/analysis_1_network.png) | 原始圖刻畫使用者回答網路，聚合圖強調聲望與中心性分群。此樣本中高聲望節點未形成明顯核心。 |
| RQ2 | ![RQ2 raw](../output/analysis_2_network_raw.png) | ![RQ2 agg](../output/analysis_2_network.png) | 原始圖呈現回答核心與邊緣的連結，聚合圖顯示回應時間與效率。樣本中所有節點皆被歸為核心。 |
| RQ3 | ![RQ3 raw](../output/analysis_3_network_raw.png) | ![RQ3 agg](../output/analysis_3_network.png) | 原始圖顯示標籤之間全部共現連結，聚合圖按照技術領域分群。共現網路模組度 0.7322，展現 8 個領域。 |
| RQ4 | ![RQ4 raw](../output/analysis_4_network_raw.png) | ![RQ4 agg](../output/analysis_4_network.png) | 原始圖展示連通分量完整結構，聚合圖強調主成分與孤立子網路。此樣本大量小型連通分量，隔離比率 1.0。 |
| RQ5 | ![RQ5 raw](../output/analysis_5_network_raw.png) | ![RQ5 agg](../output/analysis_5_network.png) | 原始圖呈現含程式碼與不含程式碼貼文之間的連結，聚合圖顯示分數與內容特徵比較。含程式碼貼文平均分 0.585，低於不含程式碼貼文。 |
| RQ6 | ![RQ6 raw](../output/analysis_6_network_raw.png) | ![RQ6 agg](../output/analysis_6_network.png) | 原始圖為年資與行為網路，聚合圖強調年資分層與貢獻模式。樣本主要為 Mature、Established、Senior。 |
| RQ7 | ![RQ7 raw](../output/analysis_7_network_raw.png) | ![RQ7 agg](../output/analysis_7_network.png) | 原始圖顯示投票者與投票目標的細節連結，聚合圖呈現投票類型分布。20,000 次投票中 upvote 佔 16,751 次。 |
| RQ8 | ![RQ8 raw](../output/analysis_8_network_raw.png) | ![RQ8 agg](../output/analysis_8_network.png) | 原始圖展示評論者共現連結，聚合圖強調評論網路密度。網路密度 0.00034，顯示評論互動稀疏。 |
| RQ9 | ![RQ9 raw](../output/analysis_9_network_raw.png) | ![RQ9 agg](../output/analysis_9_network.png) | 原始圖呈現徽章與使用者的詳細關係，聚合圖強調徽章類別與使用者分布。500 枚徽章分布於 491 位使用者。 |
| RQ10 | ![RQ10 raw](../output/analysis_10_network_raw.png) | ![RQ10 agg](../output/analysis_10_network.png) | 原始圖顯示共同編輯的細節連結，聚合圖呈現協作網路核心。100,000 次編輯與 16,830 位編輯者指出高編輯協作活躍度。 |
| RQ11 | ![RQ11 raw](../output/analysis_11_network_raw.png) | ![RQ11 agg](../output/analysis_11_network.png) | 原始圖展示每條 post link 連結，聚合圖呈現 Linked / Duplicate 結構。Duplicate 比例 29.4%。 |
| RQ12 | ![RQ12 raw](../output/analysis_12_network_raw.png) | ![RQ12 agg](../output/analysis_12_network.png) | 原始圖呈現各審核操作的細節，聚合圖強調主要審核類型。`SuggestedEdit` 與 `Close` 是本樣本中最常見的審核行為。 |
| RQ13 | ![RQ13 raw](../output/analysis_13_network_raw.png) | ![RQ13 agg](../output/analysis_13_network.png) | 原始圖呈現賞金起始與結束關係，聚合圖強調賞金行為流動。26,346 次賞金行為顯示高頻率懸賞活動。 |
| RQ14 | ![RQ14 raw](../output/analysis_14_network_raw.png) | ![RQ14 agg](../output/analysis_14_network.png) | 原始圖展示地理位置與使用者的所有連結，聚合圖強調區域分布。歐洲為最大區域（167 人）。 |
| RQ15 | ![RQ15 raw](../output/analysis_15_network_raw.png) | ![RQ15 agg](../output/analysis_15_network.png) | 原始圖顯示時間序列活動完整節點與邊，聚合圖強調月度與時段趨勢。最高活動時間出現在 14–15 點。 |

## 每個分析的圖像解讀

### RQ1 使用者聲望與網路中心度

`analysis_1_network_raw.png` 呈現回答互動網路的完整連結結構，節點大小與連結反映使用者活動程度。`analysis_1_network.png` 則按聲望與中心性聚合，顯示高聲望節點並未形成明顯核心分群，這支持 `analysis_results.json` 中聲望與介性中心度相關係數為 0.0 的觀察。

### RQ2 網路核心結構與解答效率

`analysis_2_network_raw.png` 顯示問題與回答者之間的原始互動。`analysis_2_network.png` 聚合出核心/邊緣結構，結果顯示所有樣本皆歸為核心，且平均回應時間 2932.42 小時，未支援核心回答速度優勢。

### RQ3 技術標籤共現與領域地圖

`analysis_3_network_raw.png` 呈現每個標籤之間的所有共現連結。`analysis_3_network.png` 則將標籤聚成 8 個技術領域，顯示 `Other`、`DataScience`、`Backend`、`Web`、`Database`、`Mobile`、`DevOps`、`AI_ML` 等群聚。這與 `domain_details` 中所提示的 13 個社群一致。

### RQ4 知識孤島與連通分量

`analysis_4_network_raw.png` 展示完整的連通分量結構，包含多個小型子網路。`analysis_4_network.png` 聚合後強調主成分與孤立成分，顯示 100 個連通分量、主成分大小 2、隔離比率 1.0。

### RQ5 內容特徵與互動反饋

`analysis_5_network_raw.png` 顯示每篇貼文是否含程式碼及其分數連結。`analysis_5_network.png` 聚合後比較含程式碼與無程式碼貼文的平均分，結果為 0.585 vs 0.944，且 p 值 0.2056，顯示差異不顯著。

### RQ6 帳號年資與行為差異

`analysis_6_network_raw.png` 呈現使用者年資與行為類型的原始連結。`analysis_6_network.png` 聚合出 Mature、Established、Senior 三個年資群，反映出新手樣本不足、平均帳號年齡 3202 天。

### RQ7 投票行為網路

`analysis_7_network_raw.png` 顯示投票者對貼文的原始連結，`analysis_7_network.png` 聚合出投票類型分布。20,000 次投票中 upvote 佔 16,751 次，`downvote` 佔 3,249 次，說明投票結構高度偏向正向互動。

### RQ8 評論互動網路

`analysis_8_network_raw.png` 表示評論者在相同問題上的共現連結。`analysis_8_network.png` 聚合後顯示網路密度 0.00034、平均每人 6.66 則評論，說明評論互動較為分散。

### RQ9 徽章成就網路

`analysis_9_network_raw.png` 呈現徽章與使用者之間的原始連結，`analysis_9_network.png` 聚合展示徽章類別與使用者分布。500 枚徽章、491 位使用者，呈現多數使用者僅擁有少量徽章。

### RQ10 編輯協作網路

`analysis_10_network_raw.png` 展示共同編輯的全量連結，`analysis_10_network.png` 聚合指出協作網路中的核心維護者。100,000 次編輯與 16,830 位編輯者顯示高度協作參與。

### RQ11 引用與重複問題網路

`analysis_11_network_raw.png` 顯示每條引用或重複連結的原始結構，`analysis_11_network.png` 聚合突出 Linked 與 Duplicate 兩類關係。Duplicate 比例 29.4%，意味近三成連結屬於重複問題。 

### RQ12 審核任務網路

`analysis_12_network_raw.png` 呈現不同審核操作的詳細連結，`analysis_12_network.png` 聚合出主要審核類型。210 次 SuggestedEdit 及 176 次 Close 顯示此樣本中審核行為的主要方向。

### RQ13 賞金懸賞網路

`analysis_13_network_raw.png` 展示賞金開始與結束的完整連結，`analysis_13_network.png` 聚合後重點呈現賞金活動的流動。26,346 次賞金行為代表賞金系統具有高活躍度。

### RQ14 使用者地理分布

`analysis_14_network_raw.png` 顯示使用者位置與地理分布的完整節點，`analysis_14_network.png` 聚合後強調區域專屬群聚。歐洲為最大區域，167 人。 

### RQ15 時間序列活躍度

`analysis_15_network_raw.png` 呈現時間序列活動的原始節點與邊，`analysis_15_network.png` 聚合後突顯月度、日間的活躍趨勢。12 個月資料與 14–15 點高峰一致，支持時間分布結論。

## 結果與方法的對應

本章結果直接取自 `output/analysis_results.json`，並與 `src/sna_runner.py` 的分析流程對應。這些圖表與 `analysis_results.json` 定量摘要共同說明了哪些假設被支援、哪些假設未被支援，並指出樣本取樣對結果的影響。
