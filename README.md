# Stack Overflow Social Network Analysis (SNA)

本專案利用社會網路分析 (Social Network Analysis, SNA) 方法，使用 Python 的 `igraph` 函式庫對 Stack Overflow 社群數據進行大規模圖形建模與中心性分析，以量化數據解構開發者社群的知識流動生態。

## 安裝

```bash
# 建立虛擬環境
python3 -m venv .venv
source .venv/bin/activate

# 安裝依賴
pip install pandas numpy scipy scikit-learn igraph matplotlib google-cloud-bigquery pytest
```

## 使用方式

### 查看所有分析主題

```bash
python main.py --list
```

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
```

### 自訂參數

```bash
# 指定資料筆數
python main.py --run 3 --limit 200

# 指定輸出目錄
python main.py --run all -o my_output/
```

## 6 個分析主題

| # | 分析主題 | 目標 |
|---|---------|------|
| 1 | **使用者聲望與網路中心度** | 驗證高聲望使用者的核心作用 |
| 2 | **網路核心結構與解答效率** | 評估核心發問者的問題解決速度 |
| 3 | **技術標籤共現與領域地圖** | 建構技術領域發展地圖 |
| 4 | **知識孤島與連通分量分析** | 識別社群中的「技術孤島」 |
| 5 | **內容特徵與互動反響** | 量化程式碼區塊對 Upvotes 的影響 |
| 6 | **帳號年資與社群貢獻** | 分析老手與新手的行為差異 |

## 執行測試

```bash
pytest tests/ -v
```

## 專案結構

```
1141_HCI_Midterm/
├── main.py                  # 命令列工具主程式
├── src/
│   ├── config.py           # 設定檔
│   ├── sna_runner.py       # 分析執行器
│   ├── data/
│   │   ├── bigquery_client.py   # BigQuery 客戶端
│   │   └── data_loader.py      # 資料載入器
│   ├── models/
│   │   └── graph_builder.py    # igraph 圖形建構器
│   ├── analysis/
│   │   ├── centrality.py       # 分析 1
│   │   ├── core_efficiency.py  # 分析 2
│   │   ├── tag_cooccurrence.py # 分析 3
│   │   ├── connected_components.py  # 分析 4
│   │   ├── content_features.py # 分析 5
│   │   └── account_age.py      # 分析 6
│   ├── visualization/
│   │   └── plots.py           # 視覺化工具
│   └── utils/
│       └── helpers.py          # 輔助函數
├── tests/                   # 測試檔案 (20 個測試)
├── scripts/
│   └── bigquery_queries.py  # BigQuery 查詢範例
└── docs/                   # 文件目錄
```

## 資料來源

- **BigQuery 公共數據集**: `bigquery-public-data.stackoverflow`
- **認證**: 使用 Google Cloud 應用程式預設憑證

## 作者

- **TsukiSama9292** - a0985821880@gmail.com
