#!/bin/bash

# 藏文字符生成器执行脚本
# 创建者：Pemawangchuk
# 版本：1.0
# 日期：2025-01-01

echo "========================================="
echo "        藏文字符生成器"
echo "    Tibetan Character Generator"
echo "========================================="
echo ""

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 Python3，请先安装 Python3"
    exit 1
fi

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 切换到脚本目录
cd "$SCRIPT_DIR"

echo "正在执行藏文字符生成程序..."
echo "执行路径: $SCRIPT_DIR"
echo ""

# 执行Python脚本
python3 TibetCharacterGenerator.py

# 检查执行结果
if [ $? -eq 0 ]; then
    echo ""
    echo "========================================="
    echo "✅ 藏文字符生成完成！"
    echo "📄 输出文件: 全藏字.txt"
    
    # 检查输出文件是否存在
    if [ -f "全藏字.txt" ]; then
        echo "📊 文件大小: $(wc -l < 全藏字.txt) 行"
        echo "📍 文件位置: $SCRIPT_DIR/全藏字.txt"
    fi
    echo "========================================="
else
    echo ""
    echo "========================================="
    echo "❌ 程序执行失败，请检查错误信息"
    echo "========================================="
    exit 1
fi