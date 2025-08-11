#!/bin/bash

# 藏字构件识别执行脚本
# 创建者：Pemawangchuk
# 版本：1.0
# 日期：2025-01-04

echo "========================================="
echo "        藏字构件识别系统"
echo "    Tibetan Character Classification"
echo "========================================="
echo ""

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 Python3，请先安装 Python3"
    exit 1
fi

# 检查xlwt模块是否安装
python3 -c "import xlwt" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "警告: 未找到 xlwt 模块，正在尝试安装..."
    pip3 install xlwt
    if [ $? -ne 0 ]; then
        echo "错误: xlwt 模块安装失败，请手动安装: pip3 install xlwt"
        exit 1
    fi
    echo "✅ xlwt 模块安装成功"
    echo ""
fi

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 切换到脚本目录
cd "$SCRIPT_DIR"

echo "正在执行藏字构件识别程序..."
echo "执行路径: $SCRIPT_DIR"
echo ""

# 检查输入文件是否存在
if [ ! -f "全藏字.txt" ]; then
    echo "警告: 未找到输入文件 '全藏字.txt'"
    echo "正在检查上级目录..."
    
    # 检查上级目录的T00文件夹
    if [ -f "../T00_全藏字生成/全藏字.txt" ]; then
        echo "✅ 在上级目录找到文件，正在复制..."
        cp "../T00_全藏字生成/全藏字.txt" "./全藏字.txt"
        echo "✅ 文件复制成功"
    else
        echo "❌ 未找到输入文件，请先运行 T00_全藏字生成 程序生成 '全藏字.txt' 文件"
        echo "或者手动将 '全藏字.txt' 文件放置在当前目录"
        exit 1
    fi
fi

echo "📄 输入文件: 全藏字.txt ($(wc -l < 全藏字.txt) 行)"
echo ""

# 执行Python脚本
python3 Classification.py

# 检查执行结果
if [ $? -eq 0 ]; then
    echo ""
    echo "========================================="
    echo "✅ 藏字构件识别完成！"
    
    # 检查输出文件
    if [ -f "Classified.xls" ]; then
        echo "📊 输出文件: Classified.xls"
        echo "📍 文件位置: $SCRIPT_DIR/Classified.xls"
        
        # 显示文件大小
        file_size=$(ls -lh Classified.xls | awk '{print $5}')
        echo "📏 文件大小: $file_size"
    fi
    
    echo ""
    echo "🔍 分析结果已保存到 Excel 文件中"
    echo "📋 包含以下信息："
    echo "   - 藏文音节结构分析"
    echo "   - 构件位置识别"
    echo "   - 分类统计信息"
    echo "========================================="
else
    echo ""
    echo "========================================="
    echo "❌ 程序执行失败，请检查错误信息"
    echo "========================================="
    exit 1
fi