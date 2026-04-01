# 项目配置

## 概述
本项目使用`pyproject.toml`进行所有配置管理，取代了传统的`setup.py`、`requirements.txt`和`pytest.ini`文件。

## pyproject.toml 配置详解

### 项目元数据
```toml
[project]
name = "1141-hci-midterm"
version = "0.1.0"
description = "HCI Midterm Project"
readme = "README.md"
authors = [
    { name = "xuanyou-lin", email = "a0985821880@gmail.com" }
]
requires-python = ">=3.11"
```

### 依赖管理
```toml
# 运行时依赖
dependencies = [
    "gunicorn>=21.0.0",
    "fastapi>=0.110.0",
    "uvicorn>=0.27.0"
]

# 开发依赖组
[dependency-groups]
dev = [
    "pytest>=7.0.0",
    "httpx>=0.25.0"
]
```

### Pytest配置
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
pythonpath = ["."]
```

## 依赖管理命令

### 安装依赖
```bash
# 安装所有依赖（包括开发依赖）
uv sync --dev

# 仅安装运行时依赖
uv sync --no-dev

# 安装特定依赖组
uv sync --group dev
```

### 添加依赖
```bash
# 添加运行时依赖
uv add fastapi

# 添加开发依赖
uv add --dev pytest

# 添加特定版本的依赖
uv add "fastapi>=0.110.0,<1.0.0"

# 添加可选依赖
uv add --optional ml torch
```

### 更新依赖
```bash
# 更新所有依赖
uv lock --upgrade

# 更新特定依赖
uv lock --upgrade-package fastapi

# 同步环境
uv sync
```

### 移除依赖
```bash
uv remove package_name
```

## 虚拟环境管理

### 创建虚拟环境
```bash
# uv会自动创建虚拟环境
uv sync

# 手动创建虚拟环境
uv venv

# 使用特定Python版本
uv venv --python 3.12
```

### 激活虚拟环境
```bash
# Linux/macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### 停用虚拟环境
```bash
deactivate
```

## Python版本管理

### 安装Python版本
```bash
# 安装特定Python版本
uv python install 3.12

# 安装最新稳定版本
uv python install

# 列出可用版本
uv python list

# 列出已安装版本
uv python list --only-installed
```

### 项目Python版本
项目根目录的`.python-version`文件指定了项目所需的Python版本。

## 配置文件位置

### 项目级配置
- `pyproject.toml` - 主配置文件
- `uv.lock` - 依赖锁定文件
- `.python-version` - Python版本指定

### 用户级配置
- `~/.config/uv/uv.toml` - 用户配置

### 环境变量
```bash
# 设置uv配置
export UV_PYTHON_PREFERENCE=managed
export UV_CACHE_DIR=/path/to/cache
```

## 构建和分发

### 构建包
```bash
# 构建源代码分发和wheel
uv build

# 构建特定格式
uv build --sdist
uv build --wheel
```

### 发布到PyPI
```bash
# 配置PyPI仓库
uv publish --repository testpypi

# 发布到PyPI
uv publish
```

## 项目结构
```
1141_HCI_Midterm/
├── .python-version      # Python版本指定
├── pyproject.toml       # 项目配置
├── uv.lock             # 依赖锁定
├── main.py             # 应用入口
├── README.md           # 项目说明
├── docs/               # 文档目录
│   ├── features.md
│   ├── deployment.md
│   ├── configuration.md
│   └── testing.md
├── tests/              # 测试目录
│   ├── conftest.py
│   └── test_*.py
└── .venv/              # 虚拟环境
```

## 故障排除

### 常见问题

#### 依赖解析失败
```bash
# 清理缓存
uv cache clean

# 重新解析依赖
uv lock --refresh
```

#### 虚拟环境问题
```bash
# 删除并重新创建虚拟环境
rm -rf .venv
uv sync
```

#### 导入错误
确保`pythonpath`配置正确：
```toml
[tool.pytest.ini_options]
pythonpath = ["."]
```

## 最佳实践

### 版本锁定
- 始终提交`uv.lock`文件到版本控制
- 定期更新依赖以获取安全补丁
- 使用精确版本号进行生产部署

### 依赖分组
- 将开发工具放在`dev`组
- 将可选功能放在单独的组
- 避免不必要的依赖

### 配置管理
- 使用环境变量进行敏感配置
- 不要提交敏感信息到版本控制
- 为不同环境使用不同的配置文件