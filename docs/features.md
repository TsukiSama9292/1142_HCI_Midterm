# 项目功能介绍

## 项目概述
本项目是一个基于FastAPI的人机交互中期项目，提供了基础的API端点。

## 可用功能

### 1. 根端点 (Root Endpoint)
- **路径**: `/`
- **方法**: GET
- **功能**: 返回欢迎信息
- **响应**: `{"message": "Welcome to HCI Midterm Project"}`
- **使用示例**:
  ```bash
  curl http://localhost:8000/
  ```

### 2. 健康检查端点 (Health Check Endpoint)
- **路径**: `/health`
- **方法**: GET
- **功能**: 检查服务健康状态
- **响应**: `{"status": "healthy"}`
- **使用示例**:
  ```bash
  curl http://localhost:8000/health
  ```

## 相关设定

### Gunicorn配置
项目已配置Gunicorn作为生产服务器，主要配置如下：

- **绑定地址**: `0.0.0.0:8000`
- **工作进程数**: CPU核心数 × 2 + 1
- **工作类**: `uvicorn.workers.UvicornWorker`
- **日志级别**: `info`

### FastAPI配置
FastAPI应用配置：
- **标题**: HCI Midterm Project
- **描述**: A Human-Computer Interaction midterm project
- **版本**: 0.1.0

## 开发环境

### 运行项目
```bash
# 安装依赖
uv sync --dev

# 运行开发服务器
uv run main.py

# 或使用gunicorn运行生产服务器
uv run gunicorn main:app -c main.py
```

### 测试
```bash
# 运行所有测试
uv run pytest

# 运行特定测试文件
uv run pytest tests/test_api.py

# 运行测试并显示详细输出
uv run pytest -v
```

## 依赖管理
项目使用uv进行依赖管理，主要依赖包括：
- `fastapi>=0.110.0` - Web框架
- `uvicorn>=0.27.0` - ASGI服务器
- `gunicorn>=21.0.0` - WSGI HTTP服务器

开发依赖：
- `pytest>=7.0.0` - 测试框架

## Stack Overflow 社會網路分析功能

本專案包含 Stack Overflow 數據的社會網路分析功能：

### 數據來源
- **BigQuery 公共數據集**: `bigquery-public-data.stackoverflow`
- **查詢方式**: 直接使用 BigQuery SQL（無需下載數據）
- **測試數據量**: 100 筆

### 分析主題
| # | 分析主題 | 研究問題 |
|---|----------|----------|
| 1 | 使用者聲望與網路中心度 | 高聲望用戶是否在網路結構中具有更高的介性中心度？ |
| 2 | 網路核心結構與解答效率 | 位於網路核心區域的發問者是否能更快獲得獲納解答？ |
| 3 | 技術標籤共現與領域地圖 | 不同程式語言或框架之間的群聚效應？ |
| 4 | 知識孤島與連通分量分析 | 是否存在邊緣化的孤立組件？ |
| 5 | 內容特徵與互動反響 | 程式碼區塊對 Upvotes 的影響？ |
| 6 | 帳號資歷與社群貢獻 | 老手與新手的行為差異？ |

### 需要的額外套件
```bash
uv add google-cloud-bigquery pandas igraph matplotlib
```

### BigQuery 表結構
| 表名 | 說明 | 主要用途 |
|------|------|----------|
| users | 用戶資料 | 聲望、發文數據 |
| posts_questions | 問題資料 | 問題內容、獲納解答 |
| posts_answers | 回答資料 | 回答關係 |
| comments | 評論資料 | 互動關係 |
| votes | 投票資料 | 讚/踩數據 |
| badges | 徽章資料 | 成就系統 |
| tags | 標籤資料 | 技術分類 |

### 可用欄位
- **users**: id, display_name, reputation, up_votes, down_votes, views, creation_date, location
- **posts_questions**: id, title, body, accepted_answer_id, answer_count, score, tags, owner_user_id
- **posts_answers**: id, parent_id, owner_user_id, score, creation_date
- **tags**: tag_name, count

### 查詢示例
```python
from google.cloud import bigquery
client = bigquery.Client()

sql = """
SELECT id, display_name, reputation, answer_count
FROM `bigquery-public-data.stackoverflow.users`
LIMIT 100
"""
df = client.query(sql).result().to_dataframe()
```

詳細分析計劃請參閱：
- [stackoverflow_analysis_plan.md](stackoverflow_analysis_plan.md)
- [stackoverflow_overview.md](stackoverflow_overview.md)