# 研究方法

本章節說明本研究採用的資料來源、分析架構與參數設定，並說明如何透過實証流程支撐結論。

## 資料來源

本研究主要使用 Google BigQuery 的 Stack Overflow 公共資料，並以 2021 年的歷史資料作為分析基礎。資料來源涵蓋多個表格，分別提供使用者屬性、貼文內容、評價行為、評論互動、成就徽章、技術標籤、問題連結與治理過程等面向。

主要資料項目包括：

- users：使用者 account age、reputation、location 與基本屬性。
- posts_questions / posts_answers：問題與回答的內容特徵、score、creation_date 與 tag 標記資訊。
- votes：投票類型、accepted answer、bounty start / close、upvote / downvote 等互動行為。
- comments：評論發文者、回應關係與共同評論現象。
- badges：徽章類別、tag-based badge 與成就獲取分布。
- tags：技術標籤名稱與共現關係，用於建構領域群聚。
- post_links：問題之間的引用連結與 duplicate 連結，揭示知識重複與傳播路徑。
- post_history / review_tasks：編輯歷程與審核任務資料，反映治理協作與審核分工。

這些資料項目使本研究得以從多維度描述 Stack Overflow 社群的結構、互動與演化特徵。特別是對於 network analysis 而言，使用者、貼文、投票、評論與標籤關係共同構成分析節點與邊的基礎。

## 分析架構

本研究採用系統性量化分析架構，分為資料擷取、網路建構與結果整理三個階段。

1. **資料擷取與預處理**：從上述資料來源抽取符合研究問題的樣本，進行欄位清理、缺值處理與資料對應。
2. **網路建構與指標計算**：以節點與邊表示使用者、貼文、tag 與互動關係，計算 centrality、connected components、community detection、density、temporal patterns 等指標。
3. **結果整理與呈現**：將量化結果彙整成摘要表與圖像，比對多項分析面向的觀察，並說明樣本限制對結論的影響。

雖然本研究以程式化流程實現，但論述重點在於方法論、資料來源與結果意涵，而非著重程式碼細節。

## 分析面向說明

本研究涵蓋 15 個分析面向，對應 Stack Overflow 社群中的主要互動形式：

- 使用者 centrality 與 reputation 之間的關係。
- 核心/邊緣結構與回答採納效率。
- tag co-occurrence 的技術領域群聚。
- 連通分量與知識孤島。
- 貼文內容特徵與評價分數。
- account age 與貢獻型態。
- voting 行為與影響力分布。
- comment network 的互動稀疏性。
- badge 與成就分布。
- editing collaboration 的協作網路。
- post link 的引用與 duplicate 關係。
- review task 的審核參與型態。
- bounty network 的懸賞流動。
- user location 的地理分布。
- time series 的活動趨勢。

這些面向依據資料層次進行分類，從使用者屬性、內容特徵、互動行為到治理機制，形成完整的分析框架。

## 參數與限制設定

本研究採用一組分析參數範本，定義每個面向的抽樣上限與最小樣本量。此設計是在保持結果比較性的同時，避免部分複雜分析因資料不足而導致不穩定。

- 預設抽樣上限為 100。
- centrality、core efficiency 與 content features 等基礎網路分析多數採用 200~300。
- tag co-occurrence、connected components 與 account age 等分析通常採用 300 以上。
- voting、comment、user location、review task 與 time series 等較複雜面向則採用 500 以上。
- bounty network 等高互動動態分析採用 2000 以上，以確保樣本充分。

採樣參數有助於維持本研究各面向的比較穩定性，也讓結果解讀時更容易連結到資料量與取樣策略。

## 方法論重點

本研究關注以下核心原則：

- 資料一致性：確保分析結果可追溯至相同的資料來源與處理程序。
- 取樣穩定性：以合理的最小樣本量減少片段化資料對分析結果的影響。
- 分析可重現性：保持流程可複製，便於後續比較研究與結果驗證。

## 評估面向說明

以下為各分析面向的重點說明：

- **Centrality Analysis**：評估使用者在回答網路中的影響力、橋接角色與資訊中介特性。
- **Core Efficiency**：比較位於核心與邊緣結構使用者在回答採納時間上的差異。
- **Tag Co-occurrence**：由標籤共現關係探索技術領域的群聚與跨域連結。
- **Connected Components**：檢視網路中是否存在孤立子群或小型知識孤島。
- **Content Features**：評估 code snippet 與其他內容特徵對 score 的影響。
- **Account Age**：分析使用者年資與問答行為之間的關聯。
- **Voting Behavior**：研究投票類型分布、接受率與使用者投票行為的聚集性。
- **Comment Network**：檢視評論互動網路的密度、共現關係與分布特性。
- **Badge Network**：分析徽章成就與使用者參與之間的關係。
- **Edit Collaboration**：呈現共同編輯的協作網路結構。
- **Post Link**：分析問題之間的引用與重複關係結構。
- **Review Task**：觀察審核任務的類型分布與參與節點。
- **Bounty Network**：檢視懸賞活動的活躍度與流向。
- **User Location**：探討使用者地理訊息與區域群聚特徵。
- **Time Series**：描繪月度與時段之活動趨勢。

以上面向構成本研究的方法論基礎，並強調從資料到結果的透明邏輯鏈結。
