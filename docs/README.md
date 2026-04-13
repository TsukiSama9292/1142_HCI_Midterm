# Docs 生成計畫

本文件說明如何從專案現有內容整理出 `docs/*.md`，並使用 `scripts/generate-pdf.sh` 生成最終 PDF 報告書。

## 目的

- 將 `REPORT.md`、`DATASET_FEATURES.md`、專案程式碼與分析結果統整成一本結構化的繁體中文報告。
- 讓 PDF 報告可直接透過 `pandoc` 生成。
- 提供 `docs/` 內各章節的章節分工、內容來源與完成策略。

## 目標成果

- `docs/README.md`：本計畫說明文件。
- `docs/metadata.yaml`：Pandoc PDF 生成 metadata。
- `docs/01_PROJECT_OVERVIEW.md`~`docs/15_TROUBLESHOOTING.md`：單章節 Markdown 檔案。
- `scripts/generate-pdf.sh`：已準備好，可直接生成 `docs/complete_book.pdf`。

## 章節架構建議

以下章節名稱對應至 `scripts/generate-pdf.sh` 中的 `FILES` 內容：

1. `01_PROJECT_OVERVIEW.md`：專案整體概述、研究動機、背景。
2. `02_SYSTEM_ARCHITECTURE.md`：系統架構與模組說明。
3. `03_FEATURE_MODULES.md`：功能模組與分析流程。
4. `04_DATABASE_SCHEMA.md`：資料集與資料欄位特徵。
5. `05_INSTALLATION_SETUP.md`：環境安裝、相依套件、執行方式。
6. `06_DEVELOPMENT_WORKFLOW.md`：開發流程、程式碼執行邏輯、分析步驟。
7. `07_TESTING_GUIDE.md`：測試方式、單元測試、驗證流程。
8. `08_DEPLOYMENT_GUIDE.md`：部署與執行報告書的步驟。
9. `09_USER_MANUAL_OVERVIEW.md`：使用手冊概覽與操作指南。
10. `10_USER_GUIDE_INSTRUCTOR.md`：指導者使用手冊，包含分析結果解讀。
11. `11_USER_GUIDE_ADMIN.md`：維運者與管理員手冊，包含資料來源、憑證設定、報表生成。
12. `12_QUICK_START_GUIDE.md`：快速上手步驟與常見命令。
13. `13_API_REFERENCE.md`：專案 API、模組、類別與主要函式說明。
14. `14_FRONTEND_COMPONENTS.md`：若有前端介面，可描述；若無則改為「圖表與輸出說明」。
15. `15_TROUBLESHOOTING.md`：常見問題與排除方法。

## 內容來源對應

| 章節 | 來源內容 | 主要整理方向 |
|------|----------|--------------|
| 01 | `REPORT.md` | 研究背景、目的、核心架構、AI 時代前後比較 |
| 02 | `README.md` + `src/` | 系統架構、專案結構、資料流程 |
| 03 | `src/sna_runner.py` + 各分析模組 | 15 個分析主題、演算法流程、圖表生成邏輯 |
| 04 | `DATASET_FEATURES.md` | BigQuery 資料表、重要欄位、SNA 應用方向 |
| 05 | `README.md` | 安裝依賴、環境、BigQuery 認證、執行方式 |
| 06 | `README.md` + `scripts/generate-pdf.sh` | 開發運行流程、報表生成流程 |
| 07 | `tests/` | 測試策略、單元測試、輸出驗證 |
| 08 | `scripts/generate-pdf.sh` | 報告生成流程、PDF 參數 |
| 09 | `main.py` + `README.md` | 使用者操作說明、CLI 範例 |
| 10 | `output/` | 分析圖表與報表解讀要點 |
| 11 | `src/` | 程式碼 API、模組說明、函式用途 |
| 12 | `output/` + `scripts/generate-pdf.sh` | 圖片與報告編排說明 |
| 13 | `src/visualization/plots.py` | 圖表生成策略、樣式設定 |
| 15 | 專案整體 | 錯誤修正、排除流程、生成報告關鍵步驟 |

## 建議章節內容分工

### `01_PROJECT_OVERVIEW.md`
- 研究動機與背景
- Stack Overflow 平台特色
- 2021 年資料分析的重要性
- 研究目的與問題
- 本專案的 15 個分析主題概述

### `02_SYSTEM_ARCHITECTURE.md`
- 專案架構圖（可用文字描述圖、或未來插入 SVG/PNG）
- `main.py`、`src/data/`、`src/models/`、`src/analysis/`、`src/visualization/` 的職責
- BigQuery 與 `igraph` 在系統中的角色

### `03_FEATURE_MODULES.md`
- 各分析模組說明
- 15 個研究問題對映
- 自訂分析輸入參數與輸出格式

### `04_DATABASE_SCHEMA.md`
- 資料表總覽
- 重要欄位解釋與 SNA 應用
- `Posts`、`Users`、`Votes`、`Comments`、`Badges`、`Tags`、`PostLinks`、`PostHistory` 等表簡述

### `05_INSTALLATION_SETUP.md`
- 環境建置步驟
- Python 套件清單
- BigQuery 認證與 ADC 設定
- `uv` / `python3` 執行方式

### `06_DEVELOPMENT_WORKFLOW.md`
- 專案開發流程
- 如何新增分析模組
- 如何調整 `analysis_limits.example.json`
- 如何從 `output/` 取圖表

### `07_TESTING_GUIDE.md`
- 測試架構
- 目前有哪些測試檔案
- 如何執行 `pytest` 或 `python -m unittest`
- 測試重點：`DataLoader` mock、分析模組初始化、視覺化匯出

### `08_DEPLOYMENT_GUIDE.md`
- 報告書生成流程
- `scripts/generate-pdf.sh` 說明
- 產生 `complete_book.pdf` 的步驟
- 輸出路徑與檔案命名

### `09_USER_MANUAL_OVERVIEW.md`
- 使用者操作流程
- CLI 參數說明
- 執行單一分析與全部分析的範例
- 如何讀取 `output/analysis_results.json`

### `10_USER_GUIDE_INSTRUCTOR.md`
- 指導者閱讀要點
- 如何講解 15 個報表圖
- 重點結論與應用場景建議

### `11_USER_GUIDE_ADMIN.md`
- 管理員操作手冊
- BigQuery 憑證設定
- 產出報表維護方法
- 例行更新與資料重跑

### `12_QUICK_START_GUIDE.md`
- 最短上手流程
- 只要三步驟跑完整分析
- 常用指令表

### `13_API_REFERENCE.md`
- 重要模組與類別總覽
- `DataLoader`, `GraphBuilder`, `SNAPlotter`, 各分析器類別
- 參數與回傳格式

### `14_FRONTEND_COMPONENTS.md`
- 如果沒有前端，改寫成「圖表與輸出說明」
- 描述各分析圖檔名稱與對應意義
- 建議報告中的圖表插入位置

### `15_TROUBLESHOOTING.md`
- 常見錯誤與排除方法
- 例如：BigQuery 憑證錯誤、資料查詢失敗、圖檔命名不一致
- `output/` 中舊圖檔清理建議

## 生成流程

### 1. 確認檔案
- `docs/metadata.yaml` 已建立
- `docs/01_PROJECT_OVERVIEW.md` ~ `docs/15_TROUBLESHOOTING.md` 全部存在
- `scripts/generate-pdf.sh` 可執行

### 2. 生成 PDF
```bash
bash scripts/generate-pdf.sh
```

### 3. 檢查結果
- 生成檔案位置：`docs/complete_book.pdf`
- 若需要附帶圖片，請將 `output/` 中對應圖檔複製到 `docs/`，或在 Markdown 中加上相對連結。

## 圖片與報告整合建議

- 各分析章節應引用對應 `output/analysis_*.png` 圖片。`
- 建議在 `docs/` 中加入圖表說明段落，並說明「Raw network」與「Aggregated network」的差異。`
- 建議把 `analysis_3_network.png`、`analysis_3_network_raw.png` 等圖檔一同納入報告資料夾，例如 `docs/images/`。

## 檔名與格式建議

- Markdown 檔名請保留 `01_`, `02_` 的數字前綴，方便 Pandoc 依照順序合併。`
- 內文請使用繁體中文。`
- 如需插入程式碼區塊，請使用
  ```markdown
  ```python
  # code
  ```
  ```

## 後續工作

1. 先依章節建立 `docs/01_PROJECT_OVERVIEW.md`~`docs/15_TROUBLESHOOTING.md`。
2. 以 `REPORT.md` 為主軸，將研究動機、背景、方法、結果與結論拆成章節。
3. 以 `DATASET_FEATURES.md` 補足資料集與欄位說明。
4. 以 `src/` 程式碼補足分析流程與模組說明。
5. 以 `output/` 圖片補足分析結果視覺化。`

---

## 立即可用的文件

- `docs/README.md`：本計畫來源與生成流程說明。
- `docs/metadata.yaml`：Pandoc PDF 生成 metadata。