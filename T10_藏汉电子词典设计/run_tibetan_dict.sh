#!/bin/bash

# 藏汉电子词典执行脚本
# 创建者：Pemawangchuk
# 版本：v1.0
# 日期：2025-04-06

echo "========================================="
echo "        藏汉电子词典"
echo "   Tibetan-Chinese Dictionary"
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

# 检查ttkbootstrap模块是否安装
python3 -c "import ttkbootstrap" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  未找到 ttkbootstrap 模块，正在安装..."
    pip3 install ttkbootstrap
    if [ $? -ne 0 ]; then
        echo "❌ ttkbootstrap 安装失败，请手动安装："
        echo "   pip3 install ttkbootstrap"
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

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 切换到脚本目录
cd "$SCRIPT_DIR"

echo "正在启动藏汉电子词典..."
echo "执行路径: $SCRIPT_DIR"
echo ""

# 检查藏文字体文件是否存在
font_file="Qomolangma-Dunhuang.ttf"
if [ -f "$font_file" ]; then
    echo "✅ 找到藏文字体文件: $font_file"
else
    echo "⚠️  未找到藏文字体文件: $font_file"
    echo "   程序将使用系统默认字体，可能影响藏文显示效果"
fi

# 检查词典数据文件
dict_files=(
    "藏汉词典.txt"
    "tibetan_dict.txt"
    "dictionary.txt"
)

found_dict=false
for dict_file in "${dict_files[@]}"; do
    if [ -f "$dict_file" ]; then
        echo "✅ 找到词典文件: $dict_file"
        line_count=$(wc -l < "$dict_file" 2>/dev/null || echo "未知")
        echo "   词条数量: $line_count 行"
        found_dict=true
        break
    fi
done

if [ "$found_dict" = false ]; then
    echo "⚠️  未找到词典数据文件，程序将使用内置示例数据"
    echo "   建议准备以下格式的词典文件："
    echo "   - 文件名: 藏汉词典.txt"
    echo "   - 格式: 藏文词汇[TAB]中文释义"
    echo "   - 编码: UTF-8 或 UTF-16"
fi

echo ""

# 显示功能介绍
echo "🔧 功能特性："
echo "  ✅ 藏文词汇查询"
echo "  ✅ 中文释义显示"
echo "  ✅ 多主题GUI界面"
echo "  ✅ 实时搜索功能"
echo "  ✅ 词条详细信息"
echo "  ✅ 支持藏文字体显示"
echo ""

# 检查可用的测试文件
# echo "📄 检查可用的相关文件..."
# possible_files=(
#     "../全藏字.txt"
#     "../T00_全藏字生成/全藏字.txt"
#     "../T01_藏字构件识别/全藏字.txt"
#     "test_words.txt"
#     "sample_dict.txt"
# )

# found_files=()
# for file in "${possible_files[@]}"; do
#     if [ -f "$file" ]; then
#         found_files+=("$file")
#     fi
# done

# if [ ${#found_files[@]} -gt 0 ]; then
#     echo "✅ 找到以下相关文件："
#     for file in "${found_files[@]}"; do
#         line_count=$(wc -l < "$file" 2>/dev/null || echo "未知")
#         echo "   - $file ($line_count 行)"
#     done
#     echo ""
# else
#     echo "ℹ️  未找到相关测试文件，程序将使用内置词典数据"
#     echo ""
# fi

echo "🚀 正在启动GUI应用程序..."
echo ""

# 设置环境变量以支持中文显示
export LANG=zh_CN.UTF-8
export LC_ALL=zh_CN.UTF-8

# 执行Python GUI程序
python3 tibetan-dict-design.py

# 检查执行结果
exit_code=$?
echo ""

if [ $exit_code -eq 0 ]; then
    echo "========================================="
    echo "✅ 程序正常退出"
    echo "感谢使用藏汉电子词典！"
    echo "========================================="
else
    echo "========================================="
    echo "❌ 程序异常退出 (退出码: $exit_code)"
    echo ""
    echo "🔧 故障排除建议："
    echo "  1. 检查Python环境是否正确安装"
    echo "  2. 确认tkinter模块可用"
    echo "  3. 检查ttkbootstrap模块是否正确安装"
    echo "  4. 确认藏文字体文件存在"
    echo "  5. 检查词典数据文件格式"
    echo "  6. 确认系统支持GUI显示"
    echo "  7. 检查文件编码是否正确"
    echo ""
    echo "如果问题持续存在，请检查错误信息"
    echo "========================================="
    exit $exit_code
fi