#!/bin/bash

# 藏文字符转数字编码工具执行脚本
# 创建者：Pemawangchuk
# 版本：v1.0
# 日期：2025-04-06

echo "========================================="
echo "      藏文字符转数字编码工具"
echo "   Tibetan Text to Numeric Encoder"
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

echo "正在启动藏文字符转数字编码工具..."
echo "执行路径: $SCRIPT_DIR"
echo ""

# 检查依赖的common目录是否存在
if [ ! -d "../common" ]; then
    echo "警告: 未找到 common 目录"
    echo "请确保项目结构完整，common 目录应位于项目根目录"
    echo ""
fi

# 检查编码表文件是否存在
echo "📁 检查编码表文件..."
table_files=(
    "Table/TibtFront.txt"
    "Table/TibtBase.txt"
    "Table/TibetVowelrear.txt"
)

missing_tables=()
for table in "${table_files[@]}"; do
    if [ ! -f "$table" ]; then
        missing_tables+=("$table")
    fi
done

if [ ${#missing_tables[@]} -eq 0 ]; then
    echo "✅ 所有编码表文件都存在："
    for table in "${table_files[@]}"; do
        line_count=$(wc -l < "$table" 2>/dev/null || echo "未知")
        echo "   - $table ($line_count 行)"
    done
    echo ""
else
    echo "❌ 缺少以下编码表文件："
    for table in "${missing_tables[@]}"; do
        echo "   - $table"
    done
    echo ""
    echo "请确保以下文件存在："
    echo "  - Table/TibtFront.txt (前字编码表)"
    echo "  - Table/TibtBase.txt (基字编码表)"
    echo "  - Table/TibetVowelrear.txt (元音后字编码表)"
    echo ""
    read -p "是否继续运行？(y/n): " choice
    if [[ ! "$choice" =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 显示功能介绍
echo "🔧 功能特性："
echo "  ✅ 藏文字符转数字编码"
echo "  ✅ 数字编码转藏文字符"
echo "  ✅ 支持批量文本处理"
echo "  ✅ 多主题GUI界面"
echo "  ✅ 智能内容类型检测"
echo "  ✅ 黏着词自动处理"
echo "  ✅ 文件导入导出功能"
echo ""

# 检查是否有可用的测试文件
echo "📄 检查可用的测试文件..."
possible_files=(
    "test_tibetan.txt"
    "sample.txt"
    "../全藏字.txt"
    "../T00_全藏字生成/全藏字.txt"
    "../T01_藏字构件识别/全藏字.txt"
)

found_files=()
for file in "${possible_files[@]}"; do
    if [ -f "$file" ]; then
        found_files+=("$file")
    fi
done

if [ ${#found_files[@]} -gt 0 ]; then
    echo "✅ 找到以下可用的测试文件："
    for file in "${found_files[@]}"; do
        line_count=$(wc -l < "$file" 2>/dev/null || echo "未知")
        echo "   - $file ($line_count 行)"
    done
    echo ""
else
    echo "⚠️  未找到测试文件，您可以："
    echo "   1. 在GUI中手动选择要转换的藏文文本文件"
    echo "   2. 使用其他模块生成的藏文文件进行测试"
    echo "   3. 直接在文本框中输入藏文内容进行转换"
    echo ""
fi

echo "🚀 正在启动GUI应用程序..."
echo ""

# 设置环境变量以支持中文显示
export LANG=zh_CN.UTF-8
export LC_ALL=zh_CN.UTF-8

# 执行Python GUI程序
python3 tibetan_text_encoder.py

# 检查执行结果
exit_code=$?
echo ""

if [ $exit_code -eq 0 ]; then
    echo "========================================="
    echo "✅ 程序正常退出"
    echo "感谢使用藏文字符转数字编码工具！"
    echo "========================================="
else
    echo "========================================="
    echo "❌ 程序异常退出 (退出码: $exit_code)"
    echo ""
    echo "🔧 故障排除建议："
    echo "  1. 检查Python环境是否正确安装"
    echo "  2. 确认tkinter模块可用"
    echo "  3. 检查ttkbootstrap模块是否正确安装"
    echo "  4. 确认编码表文件是否存在"
    echo "  5. 检查common目录及其模块存在"
    echo "  6. 确认系统支持GUI显示"
    echo "  7. 检查藏文字体是否正确安装"
    echo ""
    echo "如果问题持续存在，请检查错误信息"
    echo "========================================="
    exit $exit_code
fi