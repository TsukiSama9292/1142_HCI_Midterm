# 测试指南

## 测试概述
本项目使用pytest进行测试，测试文件位于`tests/`目录中。

## 运行测试

### 基本命令
```bash
# 运行所有测试
uv run pytest

# 运行特定测试文件
uv run pytest tests/test_api.py

# 运行特定测试函数
uv run pytest tests/test_api.py::test_root_function

# 运行测试并显示详细输出
uv run pytest -v

# 运行测试并显示print输出
uv run pytest -s
```

### 测试结构
```
tests/
├── conftest.py        # 共享fixtures
├── test_api.py        # API端点测试
└── __pycache__/       # 缓存文件
```

## 编写测试

### 测试文件命名
- 测试文件必须以`test_`开头
- 测试函数必须以`test_`开头
- 测试类必须以`Test`开头

### 测试示例
```python
def test_example_function():
    """测试示例功能"""
    print("测试示例功能")
    print("输入值: 示例输入")
    print("中间过程: 处理过程")
    print("最终输出值: 示例输出")
    assert True
```

### 使用Fixtures
```python
import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    """创建测试客户端"""
    return TestClient(app)

def test_with_fixture(client):
    """使用fixture的测试"""
    response = client.get("/")
    assert response.status_code == 200
```

### 参数化测试
```python
import pytest

@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
])
def test_parametrized(input, expected):
    """参数化测试"""
    assert input * 2 == expected
```

## 测试配置
测试配置在`pyproject.toml`中：
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
pythonpath = ["."]
```

## 测试覆盖率
要检查测试覆盖率，可以使用pytest-cov：
```bash
uv add --dev pytest-cov
uv run pytest --cov=main tests/
```

## 持续集成
建议在CI/CD流程中运行测试：
```yaml
# 示例GitHub Actions配置
- name: Run tests
  run: uv run pytest -v
```