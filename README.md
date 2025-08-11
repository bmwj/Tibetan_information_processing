<div align="center">

# 🏔️ 藏文信息处理-藏文字符的分析🏔️

[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)](https://github.com/)
[![GUI](https://img.shields.io/badge/GUI-Tkinter-orange.svg)](https://docs.python.org/3/library/tkinter.html)

</div>

## 📝 项目简介

本项目是一个藏文信息处理工具集，专注于藏文字符的分析、处理和转换。项目包含多个独立的模块，每个模块实现不同的藏文处理功能，从字符生成到排序算法，从编码转换到电子词典设计。

## 🚀 功能模块

本项目包含以下功能模块：

1. **[全藏字生成](#t00_全藏字生成)** - 生成全藏字集
2. **[藏字构件识别](#t01_藏字构件识别)** - 识别和分类藏文字符的构件
3. **[藏字插入排序](#t02-t05_藏字排序算法)** - 使用插入排序算法对藏文字符进行排序
4. **[藏字堆排序](#t02-t05_藏字排序算法)** - 使用堆排序算法对藏文字符进行排序
5. **[藏字归并排序](#t02-t05_藏字排序算法)** - 使用归并排序算法对藏文字符进行排序
6. **[藏字快速排序](#t02-t05_藏字排序算法)** - 使用快速排序算法对藏文字符进行排序
7. **[藏字排序算法集合](#t06_藏字排序算法集合)** - 集成多种排序算法的GUI界面
8. **[藏文编码转换](#t07_藏文编码转换)** - 在不同藏文编码格式之间进行转换
9. **[藏文转拉丁](#t08_藏文转拉丁)** - 将藏文转换为拉丁字母表示
10. **[藏文字符转数字编码](#t09_藏文字符转数字编码)** - 将藏文字符转换为数字编码
11. **[藏汉电子词典设计](#t10_藏汉电子词典设计)** - 藏汉双语电子词典的实现
12. **[藏字构件动态统计](#t11_藏字构件动态统计)** - 动态统计藏文构件的使用情况
13. **[多文本藏文音节统计](#t12_多文本藏文音节统计)** - 对多个藏文文本进行音节统计分析

## 🛠️ 技术栈

- **编程语言**: Python 3.6+
- **GUI框架**: Tkinter
- **数据处理**: 自定义算法和数据结构
- **文件格式**: 纯文本、Excel

## 📥 安装与使用

### 系统要求
- Python 3.6+
- 操作系统: Windows/macOS/Linux

### 安装步骤
1. 克隆仓库到本地
```bash
git clone https://github.com/yourusername/Tibetan_information_processing.git
cd Tibetan_information_processing
```

2. 安装依赖
```bash
pip install -r requirements.txt  # 如果有requirements.txt文件
```

### 使用方法
每个模块都可以独立运行，大多数模块提供了shell脚本来简化运行过程：

```bash
# 例如，运行藏汉电子词典
cd T10_藏汉电子词典设计
./run_tibetan_dict.sh

# 或者直接使用Python运行
python tibetan-dict-design.py
```

## 📊 示例

每个模块都有自己的README文件和示例数据，请参考各模块目录下的说明文件获取详细信息。

## 📚 项目结构

```
Tibetan_information_processing/
├── common/                          # 公共组件
│   ├── Cmp.py                       # 比较函数
│   └── SplitComponent.py            # 分割组件
├── T00_全藏字生成/                   # 全藏字生成模块
├── T01_藏字构件识别/                 # 藏字构件识别模块
├── T02_藏字插入排序/                 # 藏字插入排序模块
├── T03_藏字堆排序/                   # 藏字堆排序模块
├── T04_藏字归并排序/                 # 藏字归并排序模块
├── T05_藏字快速排序/                 # 藏字快速排序模块
├── T06_藏字排序算法集合/             # 排序算法集合GUI
├── T07_藏文编码转换/                 # 藏文编码转换模块
├── T08_藏文转拉丁/                   # 藏文转拉丁模块
├── T09_藏文字符转数字编码/           # 藏文字符转数字编码模块
├── T10_藏汉电子词典设计/             # 藏汉电子词典模块
├── T11_藏字构件动态统计/             # 藏字构件动态统计模块
└── T12_多文本藏文音节统计/           # 多文本藏文音节统计模块
```

## 🤝 贡献

欢迎对本项目进行贡献！请遵循以下步骤：

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详情请参阅 [LICENSE](LICENSE) 文件。

## 📧 联系方式

如有任何问题或建议，请通过以下方式联系我们：

- 项目维护者: [PemaWangchuk](mailto:your.email@example.com)
- 项目主页: [GitHub仓库](https://github.com/bmwj/Tibetan_information_processing)

## 🙏 致谢

感谢所有为藏文信息处理研究做出贡献的研究人员和开发者。