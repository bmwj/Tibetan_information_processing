<div align="center">

# 🏔️ 藏文信息处理工具集
## Tibetan Information Processing Toolkit

[![Python Version](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Code Style](https://img.shields.io/badge/Code%20Style-Black-black.svg)](https://github.com/psf/black)
[![Contributions Welcome](https://img.shields.io/badge/Contributions-Welcome-brightgreen.svg?style=flat)](https://github.com/bmwj/Tibetan_information_processing/pulls)
[![Stars](https://img.shields.io/github/stars/bmwj/Tibetan_information_processing?style=social)](https://github.com/bmwj/Tibetan_information_processing/stargazers)

</div>

---

## 📝 项目简介

**藏文信息处理工具集** 是一个集多种功能于一体的开源项目，致力于解决藏文在数字化处理中遇到的各种挑战。从基础的字符构件分析，到复杂的排序算法实现，再到实用的编码转换和电子词典，本项目提供了一系列模块化的解决方案。

> 🎯 **项目愿景**: 为藏文数字化处理提供专业、易用、可靠的工具集，推动藏文信息技术的发展。

无论您是从事语言学研究、开发藏文相关应用，还是对藏文技术感兴趣，这个工具集都将为您提供强有力的支持。

## ✨ 核心特性

<div align="center">

| 🔤 字符处理 | 🔄 排序算法 | 🔧 编码转换 | 📚 应用工具 |
|:---:|:---:|:---:|:---:|
| 字符生成 | 插入排序 | Unicode转换 | 电子词典 |
| 构件识别 | 堆排序 | Wylie转写 | 统计分析 |
| 音节分割 | 归并排序 | 数字编码 | 可视化界面 |
| 动态统计 | 快速排序 | 批量处理 | 多文本处理 |

</div>

## 🗂️ 功能模块

本项目包含13个精心设计的独立模块，每个模块都专注于特定的藏文处理任务：

<details>
<summary><b>📦 点击展开查看所有模块</b></summary>

### 🔤 基础处理模块

| 模块编号 | 模块名称 | 功能描述 | 主要特性 |
|:---:|:---|:---|:---|
| **T00** | [全藏字生成](./T00_全藏字生成/) | 生成完整的藏文字符集 | 🔸 系统化字符生成<br>🔸 多种组合规则<br>🔸 统计分析功能 |
| **T01** | [藏字构件识别](./T01_藏字构件识别/) | 深入分析藏文字符构件 | 🔸 智能构件识别<br>🔸 可视化界面<br>🔸 批量处理支持 |

### 🔄 排序算法模块

| 模块编号 | 模块名称 | 功能描述 | 算法特性 |
|:---:|:---|:---|:---|
| **T02** | [插入排序](./T02_藏字插入排序/) | 插入排序算法实现 | 🔸 O(n²) 时间复杂度<br>🔸 稳定排序<br>🔸 适合小数据集 |
| **T03** | [堆排序](./T03_藏字堆排序/) | 堆排序算法实现 | 🔸 O(n log n) 时间复杂度<br>🔸 原地排序<br>🔸 性能稳定 |
| **T04** | [归并排序](./T04_藏字归并排序/) | 归并排序算法实现 | 🔸 O(n log n) 时间复杂度<br>🔸 稳定排序<br>🔸 适合大数据 |
| **T05** | [快速排序](./T05_藏字快速排序/) | 快速排序算法实现 | 🔸 平均 O(n log n)<br>🔸 原地排序<br>🔸 实际性能优秀 |
| **T06** | [排序算法集合](./T06_藏字排序算法集合/) | 多算法集成界面 | 🔸 图形化界面<br>🔸 性能对比<br>🔸 可视化演示 |

### 🔧 编码转换模块

| 模块编号 | 模块名称 | 功能描述 | 转换特性 |
|:---:|:---|:---|:---|
| **T07** | [编码转换](./T07_藏文编码转换/) | 多种编码格式转换 | 🔸 Unicode 支持<br>🔸 批量转换<br>🔸 格式检测 |
| **T08** | [藏文转拉丁](./T08_藏文转拉丁/) | Wylie转写系统 | 🔸 双向转换<br>🔸 标准Wylie<br>🔸 精确转写 |
| **T09** | [字符转数字编码](./T09_藏文字符转数字编码/) | 数字编码映射 | 🔸 唯一编码<br>🔸 机器学习友好<br>🔸 压缩存储 |

### 📚 应用工具模块

| 模块编号 | 模块名称 | 功能描述 | 应用特性 |
|:---:|:---|:---|:---|
| **T10** | [藏汉电子词典](./T10_藏汉电子词典设计/) | 双语电子词典系统 | 🔸 双向查询<br>🔸 模糊搜索<br>🔸 发音功能 |
| **T11** | [构件动态统计](./T11_藏字构件动态统计/) | 构件频率统计分析 | 🔸 实时统计<br>🔸 可视化图表<br>🔸 趋势分析 |
| **T12** | [多文本音节统计](./T12_多文本藏文音节统计/) | 批量音节统计分析 | 🔸 批量处理<br>🔸 对比分析<br>🔸 报告生成 |

</details>

## 🚀 快速开始

### 📋 环境要求

<div align="center">

| 系统要求 | 最低配置 | 推荐配置 |
|:---:|:---:|:---:|
| **操作系统** | Windows 10 / macOS 10.14 / Ubuntu 18.04 | 最新版本 |
| **Python版本** | 3.7+ | 3.9+ |
| **内存** | 4GB | 8GB+ |
| **存储空间** | 500MB | 1GB+ |

</div>

### ⚡ 一键安装

```bash
# 1. 克隆项目
git clone https://github.com/bmwj/Tibetan_information_processing.git
cd Tibetan_information_processing

# 2. 创建虚拟环境（推荐）
python -m venv tibetan_env

# 3. 激活虚拟环境
# Linux/macOS:
source tibetan_env/bin/activate
# Windows:
tibetan_env\Scripts\activate

# 4. 安装依赖
pip install -r requirements.txt
```

### 🎨 字体安装

> ⚠️ **重要提示**: 为确保藏文正确显示，请务必安装项目字体！

<details>
<summary><b>📝 详细安装步骤</b></summary>

#### Windows 系统
1. 打开 `fontfile/` 文件夹
2. 全选所有 `.ttf` 字体文件
3. 右键点击 → 选择"为所有用户安装"

#### macOS 系统
1. 打开 `fontfile/` 文件夹
2. 全选所有 `.ttf` 字体文件
3. 双击打开 → 在字体册中点击"安装字体"

#### Linux 系统
```bash
# 复制字体到系统目录
cp fontfile/*.ttf ~/.local/share/fonts/
# 刷新字体缓存
fc-cache -f -v
```

</details>

### 🎮 运行示例

<details>
<summary><b>🚀 点击查看运行示例</b></summary>

```bash
# 🔤 基础处理示例
# 生成全藏字字符集
cd T00_全藏字生成/
python TibetCharacterGenerator.py

# 运行藏字构件识别GUI
cd T01_藏字构件识别/
python run_gui.py

# 🔄 排序算法示例
# 藏文插入排序
cd T02_藏字插入排序/
python insertion_Sort.py input.txt output.txt --preview

# 藏文堆排序
cd T03_藏字堆排序/
python Heap_Sort.py input.txt output.txt --reverse true

# 运行排序算法集合GUI
cd T06_藏字排序算法集合/
python Multi_Sort_GUI.py

# 📚 应用工具示例
# 藏汉电子词典
cd T10_藏汉电子词典设计/
python tibetan-dict-design.py

# 多文本音节统计
cd T12_多文本藏文音节统计/
python syllable_stats.py input_folder/ --output results.json
```

</details>


## 📊 性能指标

### 🚀 处理能力

| 功能模块 | 数据规模 | 处理时间 | 内存占用 |
|:---:|:---:|:---:|:---:|
| **字符生成** | 18,785字符 | < 1秒 | < 10MB |
| **构件识别** | 10,000字符 | < 30秒 | < 50MB |
| **排序算法** | 18,785条目 | 5-15秒 | < 100MB |
| **编码转换** | 1MB文本 | < 5秒 | < 20MB |
| **统计分析** | 100个文件 | < 60秒 | < 200MB |

### 📈 算法复杂度

| 排序算法 | 时间复杂度 | 空间复杂度 | 稳定性 |
|:---:|:---:|:---:|:---:|
| **插入排序** | O(n²) | O(1) | ✅ 稳定 |
| **堆排序** | O(n log n) | O(1) | ❌ 不稳定 |
| **归并排序** | O(n log n) | O(n) | ✅ 稳定 |
| **快速排序** | O(n log n) | O(log n) | ❌ 不稳定 |


<div align="center">

### ⭐ 如果这个项目对您有帮助，请给我们一个Star！

[![Star History Chart](https://api.star-history.com/svg?repos=bmwj/Tibetan_information_processing&type=Date)](https://star-history.com/#bmwj/Tibetan_information_processing&Date)

---

</div>
