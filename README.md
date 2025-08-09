<div align="center">

# 🏔️ 藏文信息处理系统 🏔️

[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)](https://github.com/)
[![GUI](https://img.shields.io/badge/GUI-Tkinter-orange.svg)](https://docs.python.org/3/library/tkinter.html)

</div>

<!-- <p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Tibet_flag.svg/200px-Tibet_flag.svg.png" alt="藏文图标" width="150">
</p> -->

## 📝 项目简介

本项目是一个专门用于藏文信息处理的综合系统，包含多个功能模块，从基础的藏文字符生成、分类，到高效的藏文排序算法实现。项目采用Python语言开发，提供了命令行和图形用户界面两种使用方式，能够满足藏文数据处理的各种需求。

> 🌟 **特色**：专为藏文设计的排序算法和处理流程，支持多种藏文结构分析和分类。

## 🗂️ 项目结构

<details>
<summary>点击展开完整项目结构</summary>

```
Tibetan_information_processing/
├── common/                     # 公共模块
│   ├── Cmp.py                  # 藏文比较函数
│   └── SplitComponent.py       # 藏文音节分解工具
├── T0_demo/                    # 全藏字生成模块
│   ├── 全藏字.txt               # 生成的全藏字文件
│   ├── code.py                 # 全藏字生成代码
│   └── README.md               # 模块说明
├── T1_demo/                    # 藏文音节分类模块
│   ├── 全藏字.txt               # 输入文件
│   ├── Classified.xls          # 分类结果
│   └── code.py                 # 分类代码
├── T2_demo/                    # 插入排序算法实现
│   ├── insertion_Sort.py       # 插入排序代码
│   ├── tibet.txt               # 测试数据
│   ├── output_asc.txt          # 升序排序结果
│   └── output_desc.txt         # 降序排序结果
├── T3_demo/                    # 堆排序算法实现
│   ├── Heap_Sort.py            # 堆排序代码
│   ├── tibet.txt               # 测试数据
│   ├── output_asc.txt          # 升序排序结果
│   └── output_desc.txt         # 降序排序结果
├── T4_demo/                    # 归并排序算法实现
│   ├── Merge_Sort.py           # 归并排序代码
│   ├── tibet.txt               # 测试数据
│   ├── output_asc.txt          # 升序排序结果
│   └── output_desc.txt         # 降序排序结果
├── T5_demo/                    # 快速排序算法实现
│   ├── Quick_Sort.py           # 快速排序代码
│   ├── tibet.txt               # 测试数据
│   ├── output_asc.txt          # 升序排序结果
│   └── output_desc.txt         # 降序排序结果
└── T6_demo/                    # 多算法排序GUI实现
    ├── Multi_Sort_GUI.py       # GUI界面代码
    ├── output.txt              # 排序结果
    └── README.md               # 模块说明
```
</details>

## ✨ 功能模块

### 1️⃣ 公共模块 (common)

<table>
  <tr>
    <td><b>Cmp.py</b></td>
    <td>实现藏文字符的比较函数，为排序算法提供基础支持</td>
  </tr>
  <tr>
    <td><b>SplitComponent.py</b></td>
    <td>提供藏文音节分解功能，将藏文音节分解为前加字、上加字、基字、下加字、再下加字、元音、后加字、再后加字等组件</td>
  </tr>
</table>

### 2️⃣ 全藏字生成 (T0_demo)

<!-- <div align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b8/Tibetan_script.svg/200px-Tibetan_script.svg.png" alt="藏文字符示例" width="120">
</div> -->

- **功能**：生成藏文字符的各种组合形式
- **实现**：通过组合基础字、元音、后加字等，生成完整的藏文字符集
- **输出**：生成的全藏字保存在文本文件中

### 3️⃣ 藏文音节分类 (T1_demo)

- **功能**：对藏文音节进行结构分类
- **实现**：根据藏文音节的构成规则，将音节分为53种不同的结构类别
- **输出**：分类结果保存在Excel文件中，包含音节及其各个组件的详细信息

### 4️⃣ 藏文排序算法

项目实现了四种经典排序算法，并针对藏文特性进行了优化：

<div align="center">

| 算法 | 模块 | 特点 | 适用场景 |
|:----:|:----:|:----:|:----:|
| **插入排序** | T2_demo | 简单直观 | 小规模数据 |
| **堆排序** | T3_demo | 稳定的O(n log n)时间复杂度 | 大规模数据 |
| **归并排序** | T4_demo | 稳定排序 | 大规模数据 |
| **快速排序** | T5_demo | 平均情况下效率高 | 大规模数据 |

</div>

### 5️⃣ 多算法排序GUI (T6_demo)

<!-- <div align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Tkinter_demo.png/300px-Tkinter_demo.png" alt="GUI示例" width="300">
  <p><i>GUI界面示例（非实际项目截图）</i></p>
</div> -->

- **功能**：提供图形用户界面，集成所有排序算法
- **特点**：
  - ✅ 支持四种排序算法：快速排序、堆排序、归并排序、插入排序
  - ✅ 支持升序和降序两种排序方式
  - ✅ 提供文件读取和保存功能
  - ✅ 实时显示排序进度
  - ✅ 排序完成后显示结果预览和排序用时

## 🔧 技术特点

<div align="center">
  <table>
    <tr>
      <th>类别</th>
      <th>特点</th>
    </tr>
    <tr>
      <td rowspan="3">🔤 <b>藏文处理技术</b></td>
      <td>专门的藏文分词和比较模块</td>
    </tr>
    <tr>
      <td>藏文音节结构分析和分类</td>
    </tr>
    <tr>
      <td>藏文特殊排序规则实现</td>
    </tr>
    <tr>
      <td rowspan="2">⚙️ <b>算法优化</b></td>
      <td>针对藏文特性优化的排序算法</td>
    </tr>
    <tr>
      <td>基于算法复杂度理论的进度估算</td>
    </tr>
    <tr>
      <td rowspan="3">🖥️ <b>用户界面</b></td>
      <td>现代化的Tkinter界面设计</td>
    </tr>
    <tr>
      <td>清晰的操作流程和状态反馈</td>
    </tr>
    <tr>
      <td>多线程处理，保持界面响应</td>
    </tr>
    <tr>
      <td rowspan="3">📁 <b>文件处理</b></td>
      <td>自动检测文件编码</td>
    </tr>
    <tr>
      <td>灵活的文件选择和保存功能</td>
    </tr>
    <tr>
      <td>排序结果预览</td>
    </tr>
  </table>
</div>

## 💻 系统要求

<div align="center">

| 要求 | 详情 |
|:----:|:----:|
| **Python版本** | 3.6+ |
| **操作系统** | Windows / macOS / Linux |
| **内存要求** | 最低4GB (推荐8GB) |
| **依赖库** | tkinter, xlwt, tqdm |

</div>

```bash
# 安装依赖库
pip install xlwt tqdm
```

## 📚 使用方法

### 🔍 全藏字生成

```bash
python T0_demo/code.py
```

### 📊 藏文音节分类

```bash
python T1_demo/code.py
```

### 🔄 排序算法使用

以快速排序为例：

```bash
python T5_demo/Quick_Sort.py input.txt output.txt --reverse false --preview
```

<details>
<summary>参数说明</summary>

- `input.txt`: 输入文件路径
- `output.txt`: 输出文件路径
- `--reverse`: 是否逆序排序 (true/false)
- `--preview`: 是否显示排序结果前10个词条
</details>

### 🖱️ 图形界面排序工具

```bash
python T6_demo/Multi_Sort_GUI.py
```

<div align="center">
  <table>
    <tr>
      <th>步骤</th>
      <th>操作</th>
    </tr>
    <tr>
      <td>1</td>
      <td>点击"浏览..."按钮选择输入文件</td>
    </tr>
    <tr>
      <td>2</td>
      <td>设置输出文件路径</td>
    </tr>
    <tr>
      <td>3</td>
      <td>选择排序算法和排序方向</td>
    </tr>
    <tr>
      <td>4</td>
      <td>点击"开始排序"按钮</td>
    </tr>
    <tr>
      <td>5</td>
      <td>等待排序完成，查看结果</td>
    </tr>
  </table>
</div>

## ⚠️ 注意事项

<div align="center">
  <table>
    <tr>
      <td>⏱️</td>
      <td>大文件排序可能需要较长时间，请耐心等待</td>
    </tr>
    <tr>
      <td>💾</td>
      <td>排序过程中请勿关闭程序，以免数据丢失</td>
    </tr>
    <tr>
      <td>🔣</td>
      <td>如遇到编码问题，可尝试先将文件转换为UTF-8编码</td>
    </tr>
  </table>
</div>

## 👨‍💻 开发者

<div align="center">
  <table>
    <tr>
      <td><b>创建者</b></td>
      <td>Pemawangchuk</td>
    </tr>
    <tr>
      <td><b>版本</b></td>
      <td>1.0</td>
    </tr>
    <tr>
      <td><b>日期</b></td>
      <td>2025年</td>
    </tr>
  </table>
</div>

<div align="center">
  <p>
    <a href="#"><img src="https://img.shields.io/badge/贡献-欢迎-brightgreen.svg" alt="贡献"></a>
    <a href="#"><img src="https://img.shields.io/badge/问题反馈-开放-yellow.svg" alt="问题反馈"></a>
  </p>
  <p>🙏 感谢使用藏文信息处理系统 🙏</p>
</div>
