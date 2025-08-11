#!/bin/bash

# 藏字排序算法集合GUI执行脚本
# 创建者：Pemawangchuk
# 版本：v1.3
# 日期：2025-05-05

echo "========================================="
echo "      藏字排序算法集合GUI工具"
echo "   Multi-Algorithm Tibetan Sort GUI"
echo "========================================="
echo ""

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 Python3，请先安装 Python3"
    exit 1
fi

# 检查tkinter模块是否可用
python3 -c "import tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "错误: 未找到 tkinter 模块"
    echo "请安装 tkinter："
    echo "  - Ubuntu/Debian: sudo apt-get install python3-tk"
    echo "  - CentOS/RHEL: sudo yum install tkinter"
    echo "  - macOS: tkinter 通常已预装"
    exit 1
fi

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 切换到脚本目录
cd "$SCRIPT_DIR"

echo "正在启动藏字排序算法集合GUI..."
echo "执行路径: $SCRIPT_DIR"
echo ""

# 检查依赖的common目录是否存在
if [ ! -d "../common" ]; then
    echo "警告: 未找到 common 目录"
    echo "请确保项目结构完整，common 目录应位于项目根目录"
    echo ""
fi

# 显示功能介绍
echo "🔧 功能特性："
echo "  ✅ 支持多种排序算法："
echo "     - 快速排序 (Quick Sort)"
echo "     - 堆排序 (Heap Sort)"
echo "     - 归并排序 (Merge Sort)"
echo "     - 插入排序 (Insertion Sort)"
echo ""
echo "  ✅ 支持升序/降序排序"
echo "  ✅ 实时进度显示"
echo "  ✅ 排序结果预览"
echo "  ✅ 友好的图形界面"
echo ""

# 检查是否有可用的输入文件
echo "📁 检查可用的输入文件..."
possible_files=(
    "全藏字.txt"
    "../T00_全藏字生成/全藏字.txt"
    "../T01_藏字构件识别/全藏字.txt"
    "../T02_藏字插入排序/全藏字.txt"
)

found_files=()
for file in "${possible_files[@]}"; do
    if [ -f "$file" ]; then
        found_files+=("$file")
    fi
done

if [ ${#found_files[@]} -gt 0 ]; then
    echo "✅ 找到以下可用的输入文件："
    for file in "${found_files[@]}"; do
        line_count=$(wc -l < "$file" 2>/dev/null || echo "未知")
        echo "   - $file ($line_count 行)"
    done
    echo ""
else
    echo "⚠️  未找到输入文件，您可以："
    echo "   1. 运行 T00_全藏字生成/run_generator.sh 生成全藏字文件"
    echo "   2. 在GUI中手动选择其他文件"
    echo ""
fi

echo "🚀 正在启动GUI应用程序..."
echo ""

# 设置环境变量以支持中文显示
export LANG=zh_CN.UTF-8
export LC_ALL=zh_CN.UTF-8

# 执行Python GUI程序
python3 Multi_Sort_GUI.py

# 检查执行结果
exit_code=$?
echo ""

if [ $exit_code -eq 0 ]; then
    echo "========================================="
    echo "✅ 程序正常退出"
    echo "感谢使用藏字排序算法集合GUI工具！"
    echo "========================================="
else
    echo "========================================="
    echo "❌ 程序异常退出 (退出码: $exit_code)"
    echo ""
    echo "🔧 故障排除建议："
    echo "  1. 检查Python环境是否正确安装"
    echo "  2. 确认tkinter模块可用"
    echo "  3. 检查项目目录结构是否完整"
    echo "  4. 确认common目录及其模块存在"
    echo ""
    echo "如果问题持续存在，请检查错误信息"
    echo "========================================="
    exit $exit_code
fi