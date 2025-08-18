#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
藏文构件识别与分析工具 - 启动脚本
"""
import os
import sys
# 获取项目根目录路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)  # 将项目根目录添加到Python路径
# 导入common目录下的模块
import tkinter as tk
from T01_藏字构件识别.tibetan_analyzer_gui import TibetanAnalyzerApp

def main():
    """主函数"""
    root = tk.Tk()
    app = TibetanAnalyzerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()