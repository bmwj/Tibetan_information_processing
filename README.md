<div align="center">

# 🏔️ 藏文信息处理-藏文字符的自动分析🏔️
[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)](https://github.com/)
[![GUI](https://img.shields.io/badge/GUI-Tkinter-orange.svg)](https://docs.python.org/3/library/tkinter.html)

</div>

### 📝 项目简介

本项目是一个藏文信息处理工具集，专注于藏文字符的分析、处理和转换。项目包含多个独立的模块，每个模块实现不同的藏文处理功能，从字符生成到排序算法，从编码转换到电子词典设计。

### 🚀 功能模块

本项目包含以下功能模块：

**[全藏字生成](https://github.com/bmwj/Tibetan_information_processing/tree/main/T00_%E5%85%A8%E8%97%8F%E5%AD%97%E7%94%9F%E6%88%90)** - 生成全藏字集 \
**[藏字构件识别](https://github.com/bmwj/Tibetan_information_processing/tree/main/T01_%E8%97%8F%E5%AD%97%E6%9E%84%E4%BB%B6%E8%AF%86%E5%88%AB)** - 识别和分类藏文字符的构件\
**[藏字插入排序](https://github.com/bmwj/Tibetan_information_processing/tree/main/T02_%E8%97%8F%E5%AD%97%E6%8F%92%E5%85%A5%E6%8E%92%E5%BA%8F)** - 使用插入排序算法对藏文字符进行排序\
**[藏字堆排序](https://github.com/bmwj/Tibetan_information_processing/tree/main/T03_%E8%97%8F%E5%AD%97%E5%A0%86%E6%8E%92%E5%BA%8F)** - 使用堆排序算法对藏文字符进行排序\
**[藏字归并排序](https://github.com/bmwj/Tibetan_information_processing/tree/main/T04_%E8%97%8F%E5%AD%97%E5%BD%92%E5%B9%B6%E6%8E%92%E5%BA%8F)** - 使用归并排序算法对藏文字符进行排序\
**[藏字快速排序](https://github.com/bmwj/Tibetan_information_processing/tree/main/T05_%E8%97%8F%E5%AD%97%E5%BF%AB%E9%80%9F%E6%8E%92%E5%BA%8F)** - 使用快速排序算法对藏文字符进行排序\
**[藏字排序算法集合](https://github.com/bmwj/Tibetan_information_processing/tree/main/T06_%E8%97%8F%E5%AD%97%E6%8E%92%E5%BA%8F%E7%AE%97%E6%B3%95%E9%9B%86%E5%90%88)** - 集成多种排序算法的GUI界面\
**[藏文编码转换](https://github.com/bmwj/Tibetan_information_processing/tree/main/T07_%E8%97%8F%E6%96%87%E7%BC%96%E7%A0%81%E8%BD%AC%E6%8D%A2)** - 在不同藏文编码格式之间进行转换\
**[藏文转拉丁](https://github.com/bmwj/Tibetan_information_processing/tree/main/T08_%E8%97%8F%E6%96%87%E8%BD%AC%E6%8B%89%E4%B8%81)** - 将藏文转换为拉丁字母表示\
**[藏文字符转数字编码](https://github.com/bmwj/Tibetan_information_processing/tree/main/T09_%E8%97%8F%E6%96%87%E5%AD%97%E7%AC%A6%E8%BD%AC%E6%95%B0%E5%AD%97%E7%BC%96%E7%A0%81)** - 将藏文字符转换为数字编码\
**[藏汉电子词典设计](https://github.com/bmwj/Tibetan_information_processing/tree/main/T10_%E8%97%8F%E6%B1%89%E7%94%B5%E5%AD%90%E8%AF%8D%E5%85%B8%E8%AE%BE%E8%AE%A1)** - 藏汉双语电子词典的实现\
**[藏字构件动态统计](https://github.com/bmwj/Tibetan_information_processing/tree/main/T11_%E8%97%8F%E5%AD%97%E6%9E%84%E4%BB%B6%E5%8A%A8%E6%80%81%E7%BB%9F%E8%AE%A1)** - 动态统计藏文构件的使用情况\
**[多文本藏文音节统计](https://github.com/bmwj/Tibetan_information_processing/tree/main/T12_%E5%A4%9A%E6%96%87%E6%9C%AC%E8%97%8F%E6%96%87%E9%9F%B3%E8%8A%82%E7%BB%9F%E8%AE%A1)** - 对多个藏文文本进行音节统计分析

### 🛠️ 技术栈

- **编程语言**: Python 3.6+
- **GUI框架**: Tkinter
- **数据处理**: 自定义算法和数据结构
- **文件格式**: 纯文本、Excel

### 📥 安装与使用

#### 系统要求
- Python 3.6+
- 操作系统: Windows/macOS/Linux

#### 安装步骤
1. 克隆仓库到本地
```bash
git clone https://github.com/yourusername/Tibetan_information_processing.git
cd Tibetan_information_processing
```

2. 安装依赖
```bash
pip install -r requirements.txt  
```

#### 使用方法
每个模块都可以独立运行，大多数模块提供了shell脚本来简化运行过程：

```bash
# 例如，运行藏汉电子词典
cd T10_藏汉电子词典设计
./run_tibetan_dict.sh

# 或者直接使用Python运行
python tibetan-dict-design.py
```

### 📊 示例

每个模块都有自己的README文件和示例数据，请参考各模块目录下的说明文件获取详细信息。

### 📚 项目结构

```
Tibetan_information_processing/
├── common/                          # 公共组件
│   ├── Comparator.py                       # 比较器
│   └── TibetanSyllableSegmenter.py            # 藏文音节分割器
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

### 🤝 贡献

欢迎对本项目进行贡献！请遵循以下步骤：

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request


### 📧 联系方式
- 项目维护者: [PemaWangchuk](bmwjtibet@gmail.com)
- 项目主页: [GitHub仓库](https://github.com/bmwj/Tibetan_information_processing)