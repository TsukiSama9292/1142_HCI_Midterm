#!/bin/bash
# 启动HCI Midterm项目的脚本

echo "启动HCI Midterm项目..."

# 检查是否安装了uv
if ! command -v uv &> /dev/null; then
    echo "错误: 未找到uv命令"
    echo "请安装uv: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# 安装依赖
echo "安装依赖..."
uv sync --dev

# 运行开发服务器
echo "启动开发服务器..."
uv run main.py