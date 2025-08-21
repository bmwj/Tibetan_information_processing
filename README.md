<div align="center">

# 🏔️ 藏文信息处理工具集 (Tibetan Information Processing Toolkit) 🏔️

[![Python Version](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Code Style](https://img.shields.io/badge/Code%20Style-Black-black.svg)](https://github.com/psf/black)
[![Contributions Welcome](https://img.shields.io/badge/Contributions-Welcome-brightgreen.svg?style=flat)](https://github.com/bmwj/Tibetan_information_processing/pulls)



</div>

---

### 📝 项目简介

**藏文信息处理工具集** 是一个集多种功能于一体的开源项目，致力于解决藏文在数字化处理中遇到的各种挑战。从基础的字符构件分析，到复杂的排序算法实现，再到实用的编码转换和电子词典，本项目提供了一系列模块化的解决方案。

无论您是从事语言学研究、开发藏文相关应用，还是对藏文技术感兴趣，这个工具集都将为您提供强有力的支持。

### ✨ 功能模块概览

本项目包含一系列精心设计的独立模块，每个模块都专注于一个特定的处理任务。

| 模块 (T00-T12) | 功能描述 | 核心技术 |
| :--- | :--- | :--- |
| **T00_全藏字生成** | 生成完整的藏文字符集，为后续处理提供基础数据。 | 字符编码、文件I/O |
| **T01_藏字构件识别** | 深入分析藏文字符，识别并分类其基本构件。 | 语言学规则、GUI |
| **T02-T05_藏字排序** | 实现四种经典的排序算法（插入、堆、归并、快速）对藏文进行排序。 | 算法实现、比较器 |
| **T06_藏字排序算法集合** | 提供一个图形界面，用于动态演示和比较不同的藏文排序算法。 | Tkinter、算法可视化 |
| **T07_藏文编码转换** | 在多种藏文编码标准之间进行无损转换。 | 编码映射、文本处理 |
| **T08_藏文转拉丁** | 实现藏文与Wylie转写（拉丁字母）之间的精确互转。 | `ttkbootstrap`、国际化 |
| **T09_藏文字符转数字编码**| 将藏文字符映射为唯一的数字编码，便于计算处理。 | 数据映射、文本解析 |
| **T10_藏汉电子词典设计**| 一个基础但功能齐全的藏汉双语电子词典。 | 数据检索、GUI |
| **T11_藏字构件动态统计**| 对大规模文本进行分析，动态统计藏文构件的出现频率。 | 数据结构、统计分析 |
| **T12_多文本藏文音节统计**| 批量处理多个文本文件，进行藏文音节的统计与分析。 | 文件批处理、音节分割 |

### 🛠️ 技术栈

- **核心语言**: Python 3.7+
- **GUI 框架**: Tkinter, `ttkbootstrap`
- **数据处理**: 自定义算法、数据结构
- **代码风格**: Black
- **文件格式**: `.txt`, `.xls`, `.json`

### 🚀 快速开始

#### 1. 环境准备

- 确保您的系统中已安装 **Python 3.7** 或更高版本。
- 克隆本仓库到您的本地计算机：
```bash
  git clone https://github.com/bmwj/Tibetan_information_processing.git
  cd Tibetan_information_processing
```

#### 2. 安装依赖

项目依赖项已在 `requirements.txt` 中列出。运行以下命令进行安装：
```bash
pip install -r requirements.txt
```

#### 3. 字体安装 (非常重要)

> 为了确保所有模块中的藏文都能正确、美观地显示，请务必安装项目提供的字体。

所有必需的字体都位于根目录的 `fontfile/` 文件夹下。请将此文件夹中的所有 `.ttf` 文件安装到您的操作系统中。

- **Windows**: 全选所有字体文件，右键点击，选择“为所有用户安装”。
- **macOS**: 全选所有字体文件，双击打开，在字体册应用中完成安装。
- **Linux**: 将字体文件复制到 `~/.local/share/fonts` 目录，然后运行 `fc-cache -f -v` 刷新字体缓存。

#### 4. 运行模块

每个功能模块都可以独立运行。大多数模块提供了 `run_*.sh` 脚本来简化启动过程。

```bash
# 示例：运行 "T08_藏文转拉丁" 模块
cd T08_藏文转拉丁/
sh ./run_tibetan2latin.sh

# 如果没有 .sh 脚本，可以直接运行主 Python 文件
# 例如，运行 "T10_藏汉电子词典设计"
cd T10_藏汉电子词典设计/
python tibetan-dict-design.py
```

### 📁 项目结构

```
Tibetan_information_processing/
├── common/                # 存放跨模块使用的公共代码
├── fontfile/              # 存放项目所需的所有藏文字体
├── T00_.../               # 各功能模块 (T00-T12)
│   ├── *.py               # 模块的 Python 源代码
│   ├── run_*.sh           # 便捷启动脚本
│   └── README.md          # 模块专属的详细说明
├── .gitignore             # Git 忽略文件配置
├── README.md              # 本项目主说明文件
└── requirements.txt       # 项目依赖库列表
```

### 🤝 欢迎贡献

我们热烈欢迎任何形式的贡献！无论是**报告Bug**、**提交新功能**还是**改进文档**，都对项目意义重大。请遵循以下步骤：

1.  **Fork** 本仓库。
2.  创建您的特性分支 (`git checkout -b feature/YourAmazingFeature`)。
3.  提交您的更改 (`git commit -m 'Add some AmazingFeature'`)。
4.  将您的分支推送到远程仓库 (`git push origin feature/YourAmazingFeature`)。
5.  创建一个 **Pull Request**，并详细描述您的改动。

### 展望未来

- [ ] **API化**: 将核心功能封装成易于调用的API。
- [ ] **Web化**: 开发一个基于Web的在线版本，方便更广泛的用户使用。
- [ ] **模型集成**: 集成基于深度学习的藏文NLP模型。
- [ ] **更全面的文档**: 提供更详尽的开发者文档和API参考。

### 📧 联系方式

- **项目维护者**: [PemaWangchuk](https://github.com/bmwj)
- **项目主页**: [https://github.com/bmwj/Tibetan_information_processing](https://github.com/bmwj/Tibetan_information_processing)