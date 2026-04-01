#!/bin/bash
# 运行测试的脚本

echo "运行HCI Midterm项目测试..."

# 检查是否安装了uv
if ! command -v uv &> /dev/null; then
    echo "错误: 未找到uv命令"
    echo "请安装uv: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# 安装依赖
echo "安装依赖..."
uv sync --dev

# 运行测试
echo "运行测试..."
uv run pytest -v