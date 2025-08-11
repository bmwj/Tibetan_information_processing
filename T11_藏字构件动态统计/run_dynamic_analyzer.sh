#!/bin/bash

# 藏字构件动态统计分析器执行脚本
# 创建者：Pemawangchuk
# 版本：v1.0
# 日期：2025-04-06

echo "========================================="
echo "    藏字构件动态统计分析器"
echo "  Dynamic Tibetan Component Analyzer"
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

echo "正在启动藏字构件动态统计分析器..."
echo "执行路径: $SCRIPT_DIR"
echo ""

# 检查必需的依赖文件
echo "🔍 检查依赖文件..."
required_files=(
    "Dynamic-Component-Statistics.py"
)

missing_files=()
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        missing_files+=("$file")
    fi
done

if [ ${#missing_files[@]} -gt 0 ]; then
    echo "❌ 缺少必需的文件："
    for file in "${missing_files[@]}"; do
        echo "   - $file"
    done
    echo ""
    echo "请确保所有必需文件都在当前目录中"
    exit 1
else
    echo "✅ 主程序文件检查完成"
fi
#!/bin/bash

# 藏字构件动态统计分析器执行脚本
# 创建者：Pemawangchuk
# 版本：v1.0
# 日期：2025-04-06

echo "========================================="
echo "    藏字构件动态统计分析器"
echo "  Dynamic Tibetan Component Analyzer"
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

echo "正在启动藏字构件动态统计分析器..."
echo "执行路径: $SCRIPT_DIR"
echo ""


echo "📋 代码合并完成："
echo "  ✅ Creat_18785Componet 代码已内置到主程序中"
echo "  ✅ 无需外部依赖文件"
echo "  ✅ 支持18785个藏文构件的完整分析"
echo ""

# 显示功能介绍
echo ""
echo "🔧 功能特性："
echo "  ✅ 基于18785构件的动态统计"
echo "  ✅ 支持多文件和文件夹批量处理"
echo "  ✅ 现代化GUI界面设计"
echo "  ✅ 实时进度显示"
echo "  ✅ 详细构件分类统计"
echo "  ✅ 结果导出功能"
echo "  ✅ 多主题界面切换"
echo "  ✅ 黏着词智能识别"
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
#     "../T14_多文本藏文音节统计/test_tibetan.txt"
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
#     echo "   2. 选择包含藏文文件的文件夹进行批量处理"
#     echo "   3. 使用其他模块生成的藏文文件进行测试"
#     echo ""
# fi

# 显示使用说明
echo "📖 使用说明："
echo "  1. 点击'选择文件/文件夹'按钮选择要分析的藏文文本"
echo "  2. 支持单个文件、多个文件或整个文件夹的批量处理"
echo "  3. 文件加载完成后，点击'开始统计'进行构件分析"
echo "  4. 查看详细的构件统计结果，包括各类构件的频次和占比"
echo "  5. 可以将分析结果保存为文本文件"
echo "  6. 支持切换不同的界面主题"
echo ""

# echo "📊 构件分析包括："
# echo "  • 前加字统计 (ག、ད、བ、མ、འ)"
# echo "  • 上加字统计 (ར、ལ、ས)"
# echo "  • 基字统计 (30个基本字母)"
# echo "  • 叠加基字统计"
# echo "  • 下加字统计 (ྭ、ྱ、ྲ、ླ)"
# echo "  • 再下加字统计"
# echo "  • 元音统计 (ི、ུ、ེ、ོ)"
# echo "  • 后加字统计"
# echo "  • 再后加字统计"
# echo "  • 分隔符统计"
# echo ""

echo "🚀 正在启动GUI应用程序..."
echo ""

# 设置环境变量以支持中文显示
export LANG=zh_CN.UTF-8
export LC_ALL=zh_CN.UTF-8

# 执行Python GUI程序
python3 Dynamic-Component-Statistics.py

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
    echo "  4. 确认Creat_18785Componet.py文件存在且可用"
    echo "  5. 检查输入文件为UTF-8编码的藏文文本"
    echo "  6. 确认文件权限是否正确"
    echo "  7. 检查系统支持GUI显示"
    echo "  8. 确认内存足够处理大文件"
    echo ""
    echo "如果问题持续存在，请检查错误信息"
    echo "========================================="
    exit $exit_code
fi