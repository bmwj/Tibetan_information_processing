#!/bin/bash

# 藏文-拉丁文转换器增强版启动脚本
# Enhanced Tibetan-Latin Converter Launcher

echo "🏔️ 启动藏文-拉丁文转换器增强版..."
echo "Starting Enhanced Tibetan-Latin Converter..."

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到Python3，请先安装Python3"
    echo "Error: Python3 not found, please install Python3 first"
    exit 1
fi

# 检查tkinter是否可用
python3 -c "import tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ 错误: tkinter模块不可用，请安装python3-tk"
    echo "Error: tkinter module not available, please install python3-tk"
    echo "Ubuntu/Debian: sudo apt-get install python3-tk"
    echo "CentOS/RHEL: sudo yum install tkinter"
    echo "macOS: tkinter should be included with Python"
    exit 1
fi

# 切换到脚本所在目录
cd "$(dirname "$0")"

echo "✅ 环境检查完成，启动程序..."
echo "Environment check completed, launching application..."

# 运行程序
python3 Tibetan2Latin.py

echo "👋 程序已退出"
echo "Application exited"