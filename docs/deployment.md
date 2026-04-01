# 部署指南

## 概述
本项目使用FastAPI作为Web框架，Gunicorn作为生产服务器。

## 开发环境运行

### 直接运行
```bash
# 使用uvicorn运行开发服务器
uv run main.py

# 或者直接使用uvicorn
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 开发服务器特性
- 自动重载代码更改
- 详细错误信息
- Swagger文档：`http://localhost:8000/docs`
- ReDoc文档：`http://localhost:8000/redoc`

## 生产环境部署

### 使用Gunicorn
```bash
# 使用Gunicorn运行生产服务器
uv run gunicorn main:app -c main.py

# 或者指定配置参数
uv run gunicorn main:app \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --access-logfile - \
    --error-logfile - \
    --log-level info
```

### Gunicorn配置参数
主要配置参数已在`main.py`中定义：
- `bind`: 绑定地址和端口
- `workers`: 工作进程数（建议：CPU核心数 × 2 + 1）
- `worker_class`: 工作类（使用UvicornWorker以支持异步）
- `accesslog`: 访问日志
- `errorlog`: 错误日志
- `loglevel`: 日志级别

### 生产环境最佳实践

#### 1. 使用反向代理
建议使用Nginx或Apache作为反向代理：
```nginx
# nginx配置示例
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### 2. 使用systemd服务
创建systemd服务文件：
```ini
# /etc/systemd/system/hci-midterm.service
[Unit]
Description=HCI Midterm Project
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/1141_HCI_Midterm
Environment="PATH=/path/to/1141_HCI_Midterm/.venv/bin"
ExecStart=/path/to/1141_HCI_Midterm/.venv/bin/gunicorn main:app -c main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

#### 3. 使用Docker
```dockerfile
FROM python:3.12-slim

WORKDIR /app

# 安装uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 复制依赖文件
COPY pyproject.toml uv.lock ./

# 安装依赖
RUN uv sync --frozen --no-dev --no-editable

# 复制源代码
COPY . .

# 运行应用
CMD ["uv", "run", "gunicorn", "main:app", "-c", "main.py"]
```

## 环境变量
可以通过环境变量配置应用：
```bash
# 设置环境变量
export HOST=0.0.0.0
export PORT=8000
export WORKERS=4
export LOG_LEVEL=info
```

## 健康检查
应用提供健康检查端点：
```bash
curl http://localhost:8000/health
# 返回: {"status": "healthy"}
```

## 监控和日志

### 日志配置
应用使用Python标准日志模块，可以通过以下方式调整：
```python
import logging
logging.basicConfig(level=logging.INFO)
```

### 性能监控
建议使用以下工具监控应用性能：
- Prometheus + Grafana
- New Relic
- Datadog

## 安全建议

### HTTPS
生产环境必须使用HTTPS：
```python
# 使用SSL证书
uv run uvicorn main:app --ssl-keyfile=key.pem --ssl-certfile=cert.pem
```

### 安全头
考虑添加安全头：
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应限制来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```