# -*- coding: utf-8 -*-
# 创建者：Pemawangchuk
# 版本：v1.7
# 日期：2025-08-17
# 描述：藏字排序算法集合
'''
Multi_Sort_GUI.py 藏文字符排序GUI界面
This module implements an optimized GUI interface for sorting Tibetan characters with manual save and additional clear/exit buttons.
'''

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import time
import os
import math
import threading
import sys
from tkinter import font

# 获取项目根目录路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# 导入common目录下的模块
try:
    from common.Comparator import cmp
    from common.TibetanSyllableSegmenter import Split_component
except ImportError:
    print("警告：未找到Comparator或TibetanSyllableSegmenter模块，使用模拟函数")
    def cmp(a, b): return a < b
    class Split_component:
        def Split(self, text): return [text, 0, 0, 0, 0, 0, 0, 0, 0]

# 模拟排序类（实际开发中保留原Insertion、Heap_sort、Merge_sort、Quick_sort类）
class MockSorter:
    def __init__(self): pass
    def sort(self, arr, reverse=False, progress_callback=None):
        time.sleep(1)
        arr.sort(key=lambda x: x[0], reverse=reverse)
        if progress_callback:
            for i in range(0, 101, 10):
                progress_callback(i)
                time.sleep(0.1)
        return 1.0

Insertion = Heap_sort = Merge_sort = Quick_sort = MockSorter

def load_file(file_path, progress_callback=None):
    """加载文件并处理藏文数据（简化版）"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
        words = [[line, 0, 0, 0, 0, 0, 0, 0, 0] for line in lines]
        if progress_callback:
            for i in range(0, 101, 10):
                progress_callback(i)
                time.sleep(0.1)
        return words, f"文件加载完成，共读取{len(words)}个藏文词条"
    except Exception as e:
        return None, f"文件加载异常：{str(e)}"

def save_file(file_path, words):
    """保存排序后的结果到文件"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            for word in words:
                f.write(f"{word[0]}\n")
        return True, f"文件已保存至：{file_path}"
    except Exception as e:
        return False, f"保存文件异常：{str(e)}"

class SortApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("藏文排序工具")
        self.geometry("1200x900")
        self.resizable(True, True)
        self.configure(bg="#f5f5f5")

        # 加载藏文字体
        try:
            self.tibetan_font = font.Font(family="Noto Serif Tibetan", size=12)
        except:
            self.tibetan_font = font.Font(family="Helvetica", size=12)

        # 主题颜色（藏式风格）
        self.colors = {
            "bg": "#f5f5f5",
            "card_bg": "#ffffff",
            "text": "#1B4965",  # 藏蓝
            "accent": "#7B2D26",  # 深红
            "button": "#D4A017",  # 金色
            "button_active": "#b38f00",
            "progress": "#1B4965",
            "success": "#4caf50",
            "error": "#f44336"
        }

        # 设置样式
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TButton", padding=10, font=('Helvetica', 12, 'bold'),
                            background=self.colors["button"], foreground="#ffffff", borderwidth=0)
        self.style.map("TButton", background=[('active', self.colors["button_active"]), ('disabled', '#cccccc')],
                      foreground=[('disabled', '#666666')])
        self.style.configure("TLabel", font=self.tibetan_font, background=self.colors["card_bg"],
                           foreground=self.colors["text"])
        self.style.configure("TEntry", fieldbackground=self.colors["card_bg"], foreground=self.colors["text"],
                           font=self.tibetan_font)
        # 进度条样式
        self.style.configure("Horizontal.TProgressbar",
                             troughcolor=self.colors['bg'],
                             background=self.colors['progress'],
                             thickness=12)
        try:
            # 显式复制布局以解决macOS等系统的样式问题
            self.style.layout('Success.TProgressbar', self.style.layout('Horizontal.TProgressbar'))
            self.style.configure('Success.TProgressbar', background=self.colors['success'])
        except tk.TclError:
            # 回退方案
            self.style.configure("Success.TProgressbar", background=self.colors['success'])
        self.style.configure("TRadiobutton", font=self.tibetan_font, background=self.colors["card_bg"],
                           foreground=self.colors["text"])
        self.style.configure("Card.TFrame", background=self.colors["card_bg"], relief="raised", borderwidth=2)

        # 主框架
        self.main_frame = tk.Frame(self, bg=self.colors["bg"], padx=30, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # 顶部标题栏
        self.create_header()

        # --- 新布局 ---

        # 1. 顶部文件选择区
        self.create_file_bar()

        # 2. 主内容区 (结果 + 控制)
        self.content_frame = tk.Frame(self.main_frame, bg=self.colors["bg"])
        self.content_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        self.content_frame.grid_columnconfigure(0, weight=7) # 结果区占70%
        self.content_frame.grid_columnconfigure(1, weight=3) # 控制区占30%
        self.content_frame.grid_rowconfigure(0, weight=1)

        # 结果显示区 (左侧70%)
        self.create_result_display()

        # 控制面板区 (右侧30%)
        self.create_control_panel()

        # 底部状态栏
        self.status_frame = tk.Frame(self.main_frame, bg=self.colors["bg"], height=30)
        self.status_frame.pack(fill=tk.X, pady=(10, 0))
        self.status_label = tk.Label(self.status_frame, text="就绪", font=('Helvetica', 12),
                                   bg=self.colors["bg"], fg=self.colors["text"])
        self.status_label.pack(expand=True)

        # 初始化变量
        self.words = None
        self.sorting_thread = None

    def create_header(self):
        """创建顶部标题栏"""
        header = tk.Frame(self.main_frame, bg=self.colors["accent"], pady=15)
        header.pack(fill=tk.X)
        title = tk.Label(header, text="📚 藏文字符排序工具", font=('Helvetica', 30, 'bold'),
                        bg=self.colors["accent"], fg="#ffffff")
        title.pack(pady=5)

    def create_file_bar(self):
        """创建顶部文件选择栏"""
        card = ttk.Frame(self.main_frame, style="Card.TFrame", padding=15)
        card.pack(fill=tk.X)
        ttk.Label(card, text="输入文件:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.input_path = tk.StringVar()
        ttk.Entry(card, textvariable=self.input_path).grid(row=0, column=1, sticky="ew", padx=10)
        ttk.Button(card, text="浏览", command=self.browse_input_file).grid(row=0, column=2, padx=10)
        card.columnconfigure(1, weight=1)

    def create_result_display(self):
        """创建结果显示区域"""
        card = ttk.Frame(self.content_frame, style="Card.TFrame", padding=20)
        card.grid(row=0, column=0, sticky="nsew", padx=(0, 15))
        card.grid_rowconfigure(1, weight=1)
        card.grid_columnconfigure(0, weight=1)

        ttk.Label(card, text="排序结果").grid(row=0, column=0, sticky="w", padx=10, pady=(0, 5))
        
        text_frame = tk.Frame(card, bg=self.colors["card_bg"])
        text_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)

        self.result_text = tk.Text(text_frame, wrap=tk.WORD, font=self.tibetan_font, 
                                bg=self.colors["card_bg"], relief="flat", borderwidth=2)
        self.result_text.grid(row=0, column=0, sticky="nsew")
        
        scrollbar = ttk.Scrollbar(text_frame, command=self.result_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.result_text.config(yscrollcommand=scrollbar.set)
        
        self.result_text.insert(tk.END, "排序结果将在此处显示...\n\n请选择文件并开始排序。")
        self.result_text.config(state=tk.DISABLED)

    def create_control_panel(self):
        """创建右侧垂直控制面板"""
        panel = ttk.Frame(self.content_frame, style="Card.TFrame", padding=20)
        panel.grid(row=0, column=1, sticky="nsew")

        # 排序算法
        algo_frame = ttk.Frame(panel, style="Card.TFrame", padding=10)
        algo_frame.pack(fill=tk.X, pady=5)
        ttk.Label(algo_frame, text="排序算法:").pack(anchor="w", padx=5)
        self.algorithm = tk.StringVar(value="quick")
        algorithms = [("快速排序", "quick"), ("堆排序", "heap"), ("归并排序", "merge"), ("插入排序", "insertion")]
        for text, value in algorithms:
            ttk.Radiobutton(algo_frame, text=text, value=value, variable=self.algorithm).pack(anchor="w", padx=15)

        # 排序方向
        dir_frame = ttk.Frame(panel, style="Card.TFrame", padding=10)
        dir_frame.pack(fill=tk.X, pady=5)
        ttk.Label(dir_frame, text="排序方向:").pack(anchor="w", padx=5)
        self.reverse = tk.BooleanVar(value=False)
        ttk.Radiobutton(dir_frame, text="升序", value=False, variable=self.reverse).pack(anchor="w", padx=15)
        ttk.Radiobutton(dir_frame, text="降序", value=True, variable=self.reverse).pack(anchor="w", padx=15)

        # 开始按钮
        ttk.Button(panel, text="开始排序", command=self.start_sorting).pack(fill=tk.X, pady=10, ipady=5)

        # 进度条
        prog_frame = ttk.Frame(panel, style="Card.TFrame", padding=10)
        prog_frame.pack(fill=tk.X, pady=5)
        ttk.Label(prog_frame, text="进度状态:").pack(anchor="w", padx=5)
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(prog_frame, orient=tk.HORIZONTAL, mode='determinate', variable=self.progress_var)
        self.progress.pack(fill=tk.X, pady=5)
        self.progress_label = ttk.Label(prog_frame, text="就绪")
        self.progress_label.pack(anchor="w", padx=5)

        # 操作按钮
        btn_frame = ttk.Frame(panel, style="Card.TFrame", padding=10)
        btn_frame.pack(fill=tk.X, pady=5)
        ttk.Button(btn_frame, text="💾 保存结果", command=self.save_results).pack(fill=tk.X, pady=3)
        ttk.Button(btn_frame, text="📋 复制到剪贴板", command=self.copy_to_clipboard).pack(fill=tk.X, pady=3)
        ttk.Button(btn_frame, text="🗑 清空", command=self.clear_results).pack(fill=tk.X, pady=3)
        ttk.Button(btn_frame, text="🚪 退出", command=self.quit_app).pack(fill=tk.X, pady=3)

    def update_progress(self, value):
        """更新进度条"""
        self.progress_var.set(value)
        self.progress_label.config(text=f"进度: {value}%")
        self.update()

    def update_status(self, message, is_success=None, progress_message=None):
        """更新状态信息"""
        color = self.colors["text"] if is_success is None else self.colors["success"] if is_success else self.colors["error"]
        self.status_label.config(text=message, fg=color)
        p_message = progress_message if progress_message is not None else message
        self.progress_label.config(text=p_message, foreground=color)

    def save_results(self):
        """保存排序结果"""
        if not self.words:
            messagebox.showerror("错误", "没有可保存的排序结果")
            return
        algorithm_names = {
            "quick": "quick",
            "heap": "heap",
            "merge": "merge",
            "insertion": "insertion"
        }
        algo = algorithm_names.get(self.algorithm.get(), "sort")
        direction = "升序" if not self.reverse.get() else "降序"
        default_filename = f"{algo}_{direction}_sort.txt"
        filename = filedialog.asksaveasfilename(filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")],
                                               initialfile=default_filename)
        if filename:
            success, message = save_file(filename, self.words)
            messagebox.showinfo("提示", message) if success else messagebox.showerror("错误", message)

    def copy_to_clipboard(self):
        """复制结果到剪贴板"""
        if not self.words:
            messagebox.showerror("错误", "没有可复制的排序结果")
            return
        try:
            result_text = "\n".join([word[0] for word in self.words[:50]])
            self.clipboard_clear()
            self.clipboard_append(result_text)
            messagebox.showinfo("提示", "前50个结果已复制到剪贴板")
        except Exception as e:
            messagebox.showerror("错误", f"复制失败: {str(e)}")

    def clear_results(self):
        """清空结果"""
        self.words = None
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "排序结果将在此处显示...\n\n请选择文件并开始排序。")
        self.result_text.config(state=tk.DISABLED)
        self.progress_var.set(0)
        self.progress.config(style="Horizontal.TProgressbar")
        self.update_status("已清空结果", True, progress_message="就绪")

    def quit_app(self):
        """退出程序"""
        self.quit()
        self.destroy()

    def update_result(self, message):
        """更新结果文本框"""
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, message)
        self.result_text.config(state=tk.DISABLED)

    def browse_input_file(self):
        """浏览输入文件"""
        filename = filedialog.askopenfilename(filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")])
        if filename:
            self.input_path.set(filename)

    def start_sorting(self):
        """开始排序"""
        if not self.input_path.get():
            messagebox.showerror("错误", "请选择输入文件")
            return
        if not os.path.exists(self.input_path.get()):
            messagebox.showerror("错误", f"输入文件不存在: {self.input_path.get()}")
            return

        self.progress.config(style="Horizontal.TProgressbar")
        self.find_widget(self.main_frame, "开始排序")["state"] = "disabled"
        self.update_status("正在加载文件...", None)
        self.sorting_thread = threading.Thread(target=self.perform_sorting)
        self.sorting_thread.daemon = True
        self.sorting_thread.start()

    def perform_sorting(self):
        """执行排序操作（无自动保存）"""
        try:
            self.words, message = load_file(self.input_path.get(), self.update_progress)
            if self.words is None:
                self.after(0, lambda: messagebox.showerror("错误", message))
                self.after(0, lambda: self.update_status("加载文件失败", False))
                self.after(0, self.enable_sort_button)
                return

            self.after(0, lambda: self.update_status("加载完成，开始排序", None))
            algorithm = self.algorithm.get()
            reverse = self.reverse.get()

            sorter = {
                "quick": Quick_sort(),
                "heap": Heap_sort(),
                "merge": Merge_sort(),
                "insertion": Insertion()
            }[algorithm]
            sort_time = sorter.sort(self.words, reverse, self.update_progress)

            self.after(0, lambda: self.update_progress(100))
            self.after(0, lambda: self.progress.config(style="Success.TProgressbar"))
            self.after(0, lambda: self.update_status(f"排序完成，用时 {sort_time:.2f} 秒", True, progress_message="排序完成"))

            preview = "排序结果前50个词条:\n\n" + "\n".join(f"{i+1}. {word[0]}" for i, word in enumerate(self.words[:50]))
            self.after(0, lambda: self.update_result(preview))

        except Exception as e:
            self.after(0, lambda: messagebox.showerror("错误", f"排序过程中出错：{str(e)}"))
            self.after(0, lambda: self.update_status("排序失败", False))
        finally:
            self.after(0, self.enable_sort_button)

    def enable_sort_button(self):
        """启用排序按钮"""
        self.find_widget(self.main_frame, "开始排序")["state"] = "normal"

    def find_widget(self, parent, text):
        """递归查找控件"""
        for widget in parent.winfo_children():
            if isinstance(widget, ttk.Button) and widget.cget("text") == text:
                return widget
            found = self.find_widget(widget, text)
            if found:
                return found
        return None

if __name__ == "__main__":
    app = SortApp()
    app.mainloop()

