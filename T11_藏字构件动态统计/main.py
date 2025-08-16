# -*- coding: UTF-8 -*-
# 主程序文件 - 包含程序入口点

"""
藏字构件动态统计分析器
Dynamic Tibetan Component Statistics Analyzer

创建者：Pemawangchuk
版本：1.0
日期：2025-04-06
描述：藏字构件动态统计
"""

import sys
import tkinter as tk
from tkinter import messagebox

def check_dependencies():
    """检查必要的依赖项"""
    missing_deps = []
    
    try:
        import ttkbootstrap
    except ImportError:
        missing_deps.append("ttkbootstrap")
    
    if missing_deps:
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口
        
        message = "缺少以下必要的依赖项:\n\n"
        for dep in missing_deps:
            message += f"- {dep}\n"
        message += "\n请使用以下命令安装:\n\npip install ttkbootstrap\n\n是否现在尝试安装?"
        
        if messagebox.askyesno("缺少依赖项", message):
            try:
                import subprocess
                for dep in missing_deps:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
                messagebox.showinfo("安装成功", "依赖项已成功安装，程序将继续运行。")
                root.destroy()
                return True
            except Exception as e:
                messagebox.showerror("安装失败", f"安装依赖项时出错:\n{str(e)}\n\n请手动安装后再运行程序。")
                root.destroy()
                return False
        else:
            root.destroy()
            return False
    
    return True

def main():
    """程序入口点"""
    if check_dependencies():
        from gui import DynamicTibetanComponentGUI
        app = DynamicTibetanComponentGUI()
        app.run()

if __name__ == '__main__':
    main()
