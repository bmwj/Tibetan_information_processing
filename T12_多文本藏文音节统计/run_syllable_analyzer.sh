#!/bin/bash

# 多文本藏文音节统计分析器执行脚本
# 创建者：Pemawangchuk
# 版本：v1.0
# 日期：2025-04-06

echo "========================================="
echo "    多文本藏文音节统计分析器"
echo "  Multi-Text Tibetan Syllable Analyzer"
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

echo "正在启动多文本藏文音节统计分析器..."
echo "执行路径: $SCRIPT_DIR"
echo ""

# 显示功能介绍
echo "🔧 功能特性："
echo "  ✅ 多文件藏文文本处理"
echo "  ✅ 基于哈希表的高效音节统计"
echo "  ✅ 现代化GUI界面设计"
echo "  ✅ 实时进度显示"
echo "  ✅ 详细统计信息展示"
echo "  ✅ 结果导出功能"
echo "  ✅ 多主题界面切换"
echo ""

# # 检查可用的测试文件
# echo "📄 检查可用的测试文件..."
# possible_files=(
#     "test_tibetan.txt"
#     "sample.txt"
#     "../全藏字.txt"
#     "../T00_全藏字生成/全藏字.txt"
#     "../T01_藏字构件识别/全藏字.txt"
#     "../T02_藏字插入排序/sorted_output.txt"
# )

# found_files=()
# for file in "${possible_files[@]}"; do
#     if [ -f "$file" ]; then
#         found_files+=("$file")
#     fi
# done

# if [ ${#found_files[@]} -gt 0 ]; then
#     echo "✅ 找到以下可用的测试文件："
#     for file in "${found_files[@]}"; do
#         line_count=$(wc -l < "$file" 2>/dev/null || echo "未知")
#         file_size=$(wc -c < "$file" 2>/dev/null || echo "未知")
#         echo "   - $file ($line_count 行, $file_size 字符)"
#     done
#     echo ""
# else
#     echo "ℹ️  未找到测试文件，您可以："
#     echo "   1. 在GUI中选择要分析的藏文文本文件"
#     echo "   2. 使用其他模块生成的藏文文件进行测试"
#     echo "   3. 准备自己的藏文文档进行分析"
#     echo ""
# fi

# 显示使用说明
echo "📖 使用说明："
echo "  1. 点击'选择文件'按钮选择一个或多个藏文文本文件"
echo "  2. 文件加载完成后，点击'开始统计'进行音节分析"
echo "  3. 查看统计结果，包括音节频次和占比信息"
echo "  4. 可以将分析结果保存为文本文件"
echo "  5. 支持切换不同的界面主题"
echo ""

echo "🚀 正在启动GUI应用程序..."
echo ""

# 设置环境变量以支持中文显示
export LANG=zh_CN.UTF-8
export LC_ALL=zh_CN.UTF-8

# 执行Python GUI程序
python3 MultiTextTibetanStats.py

# 检查执行结果
exit_code=$?
echo ""

if [ $exit_code -eq 0 ]; then
    echo "========================================="
    echo "✅ 程序正常退出"
    echo "感谢使用多文本藏文音节统计分析器！"
    echo "========================================="
else
    echo "========================================="
    echo "❌ 程序异常退出 (退出码: $exit_code)"
    echo ""
    echo "🔧 故障排除建议："
    echo "  1. 检查Python环境是否正确安装"
    echo "  2. 确认tkinter模块可用"
    echo "  3. 检查ttkbootstrap模块是否正确安装"
    echo "  4. 确认输入文件为UTF-8编码的藏文文本"
    echo "  5. 检查文件权限是否正确"
    echo "  6. 确认系统支持GUI显示"
    echo "  7. 检查内存是否足够处理大文件"
    echo ""
    echo "如果问题持续存在，请检查错误信息"
    echo "========================================="
    exit $exit_code
fi