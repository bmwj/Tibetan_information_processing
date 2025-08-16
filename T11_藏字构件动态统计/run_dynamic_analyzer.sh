#!/bin/bash

# 藏字构件动态统计分析器启动脚本
# 创建者：Pemawangchuk
# 版本：v1.0
# 日期：2025-04-06

echo "========================================="
echo "      藏字构件动态统计分析器"
echo "  Dynamic Tibetan Component Statistics"
echo "========================================="
echo ""

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "错误: 未找到 Python，请先安装 Python3"
        exit 1
    else
        PY_CMD="python"
    fi
else
    PY_CMD="python3"
fi

# 检查tkinter模块是否可用
$PY_CMD -c "import tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "错误: 未找到 tkinter 模块"
    echo "请安装 tkinter："
    echo "  - Ubuntu/Debian: sudo apt-get install python3-tk"
    echo "  - CentOS/RHEL: sudo yum install tkinter"
    echo "  - macOS: tkinter 通常已预装"
    exit 1
fi

# 检查ttkbootstrap模块是否安装
$PY_CMD -c "import ttkbootstrap" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  未找到 ttkbootstrap 模块，正在安装..."
    pip3 install ttkbootstrap || pip install ttkbootstrap
    if [ $? -ne 0 ]; then
        echo "❌ ttkbootstrap 安装失败，请手动安装："
        echo "   pip install ttkbootstrap"
        echo ""
        echo "或者使用系统默认的tkinter主题继续运行"
        read -p "是否继续运行？(y/n): " choice
        if [[ ! "$choice" =~ ^[Yy]$ ]]; then
            exit 1
        fi
    else
        echo "✅ ttkbootstrap 安装成功"
    fi
fi

# 检查pillow模块是否安装（用于图标生成）
$PY_CMD -c "import PIL" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  未找到 Pillow 模块，正在安装..."
    pip3 install pillow || pip install pillow
    if [ $? -ne 0 ]; then
        echo "❌ Pillow 安装失败，但这不影响核心功能"
    else
        echo "✅ Pillow 安装成功"
    fi
fi

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 切换到脚本目录
cd "$SCRIPT_DIR"

echo "正在启动藏字构件动态统计分析器..."
echo "执行路径: $SCRIPT_DIR"
echo ""

# 检查图标文件是否存在
icon_file="icon.png"
if [ -f "$icon_file" ]; then
    echo "✅ 找到图标文件: $icon_file"
else
    echo "⚠️  未找到图标文件: $icon_file"
    echo "   尝试生成图标文件..."
    $PY_CMD -c "from utils import create_icon; create_icon()" 2>/dev/null
    if [ -f "$icon_file" ]; then
        echo "✅ 图标文件生成成功"
    else
        echo "⚠️  图标生成失败，将使用默认图标"
    fi
fi

# 检查示例藏文文件
example_files=(
    "../全藏字.txt"
    "../T00_全藏字生成/全藏字.txt"
    "../T01_藏字构件识别/全藏字.txt"
    "test_words.txt"
    "sample_tibetan.txt"
)

found_files=()
for file in "${example_files[@]}"; do
    if [ -f "$file" ]; then
        found_files+=("$file")
    fi
done

if [ ${#found_files[@]} -gt 0 ]; then
    echo "✅ 找到以下可用的藏文示例文件："
    for file in "${found_files[@]}"; do
        line_count=$(wc -l < "$file" 2>/dev/null || echo "未知")
        echo "   - $file ($line_count 行)"
    done
    echo ""
else
    echo "ℹ️  未找到示例藏文文件，您需要手动选择文件进行分析"
    echo ""
fi

echo "🔧 功能特性："
echo "  ✅ 藏文构件动态统计"
echo "  ✅ 多文件批量处理"
echo "  ✅ 实时进度显示"
echo "  ✅ 详细统计结果"
echo "  ✅ 多主题GUI界面"
echo "  ✅ 结果导出功能"
echo ""

echo "🚀 正在启动GUI应用程序..."
echo ""

# 设置环境变量以支持中文显示
export LANG=zh_CN.UTF-8
export LC_ALL=zh_CN.UTF-8

# 执行Python GUI程序
$PY_CMD main.py

# 检查执行结果
exit_code=$?
echo ""

if [ $exit_code -eq 0 ]; then
    echo "========================================="
    echo "✅ 程序正常退出"
    echo "感谢使用藏字构件动态统计分析器！"
    echo "========================================="
else
    echo "========================================="
    echo "❌ 程序异常退出 (退出码: $exit_code)"
    echo ""
    echo "🔧 故障排除建议："
    echo "  1. 检查Python环境是否正确安装"
    echo "  2. 确认tkinter模块可用"
    echo "  3. 检查ttkbootstrap模块是否正确安装"
    echo "  4. 确认文件编码是UTF-8"
    echo "  5. 检查是否有足够的系统资源"
    echo "  6. 确认系统支持GUI显示"
    echo ""
    echo "如果问题持续存在，请检查错误信息"
    echo "========================================="
    exit $exit_code
fi
