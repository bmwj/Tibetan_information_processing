# -*- coding: utf-8 -*-
# 创建者：Pemawangchuk
# 版本：v1.3
# 日期：2025-05-05
# 描述：本模块实现了多种排序算法的GUI界面，用于对藏文字符进行排序
'''
Multi_Sort_GUI.py 藏文字符排序GUI界面
This module implements a GUI interface for sorting Tibetan characters using multiple sorting algorithms.
'''
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import time
import os
import math
import threading
import sys
# 获取项目根目录路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)  # 将项目根目录添加到Python路径
# 导入common目录下的模块
from common.Comparator import cmp
from common.TibetanSyllableSegmenter import Split_component
# 从新文件中导入真实的排序算法类
from T06_藏字排序算法集合.sorting_algorithms import Insertion, Heap_sort, Merge_sort, Quick_sort

def load_file(file_path, progress_callback=None):
    """加载文件并处理藏文数据"""
    split_com = Split_component()
    word_18785_ns = []
    
    encodings = ['utf-8', 'utf-16', 'utf-16-le', 'utf-16-be', 'gb18030']
    
    encoding = None
    for enc in encodings:
        try:
            with open(file=file_path, mode='r', encoding=enc) as f:
                lines = [f.readline().strip('\n') for _ in range(5) if f.readline().strip('\n')]
                if lines:
                    encoding = enc
                    print(f"使用 {encoding} 编码读取文件")
                    break
        except:
            continue
    if encoding is None:
        return None, "无法确定文件编码，请检查文件格式"
    
    try:
        with open(file=file_path, mode='r', encoding=encoding) as f:
            all_lines = f.readlines()
            total_lines = len(all_lines)
            
            for i, line in enumerate(all_lines):
                Tibetan = line.strip('\n')
                if not Tibetan:
                    continue
                    
                try:
                    word = split_com.Split(Tibetan)[:-1]
                    for j in range(1, len(word)):
                        word[j] = ord(word[j]) if word[j] != '' else 0
                    word[1], word[3] = word[3], word[1]
                    for j in range(1, 9):
                        if 0x0F90 <= word[j] <= 0x0FB8:
                            word[j] -= 80
                    word_18785_ns.append(word)
                except Exception as e:
                    print(f"处理第{i+1}行时出错: {str(e)}")
                
                if progress_callback is not None and i % 10 == 0:
                    progress_callback(min(int((i + 1) * 100 / total_lines), 100))
            
        if progress_callback is not None:
            progress_callback(100)
            
        return word_18785_ns, f"文件加载完成，共读取{len(word_18785_ns)}个藏文词条"
    except Exception as e:
        return None, f"文件加载异常：{str(e)}，请检查文件路径和格式"

def save_file(file_path, words):
    """保存排序后的结果到文件"""
    try:
        with open(file=file_path, mode='w', encoding='utf-8') as f:
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
        self.configure(bg="#ffffff")  # 白色背景
        
        # 设置样式 - 全新现代风格
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # --- 按钮样式 ---
        # 主要操作按钮 (例如 "开始排序")
        self.style.configure("Primary.TButton", 
                             padding=(10, 8), 
                             relief="flat",
                             background="#5c6bc0",
                             foreground="#ffffff",
                             font=('Helvetica', 11, 'bold'),
                             borderwidth=0,
                             focuscolor="none")
        self.style.map("Primary.TButton",
                       background=[('active', '#3f51b5'), ('pressed', '#303f9f'), ('disabled', '#c5cae9')],
                       foreground=[('disabled', '#ffffff')],
                       relief=[('pressed', 'sunken')])

        # 标准操作按钮 (例如 "保存", "复制")
        self.style.configure("Action.TButton", 
                             padding=(8, 6),
                             relief="flat",
                             background="#7986cb", # 稍浅的蓝色
                             foreground="#ffffff",
                             font=('Helvetica', 9, 'bold'),
                             borderwidth=0,
                             focuscolor="none")
        self.style.map("Action.TButton",
                       background=[('active', '#5c6bc0'), ('pressed', '#3f51b5'), ('disabled', '#c5cae9')],
                       foreground=[('disabled', '#ffffff')],
                       relief=[('pressed', 'sunken')])

        # 次要/危险操作按钮 (例如 "清空", "退出")
        self.style.configure("Secondary.TButton", 
                             padding=(8, 6),
                             relief="flat",
                             background="#e0e0e0", # 灰色
                             foreground="#424242", # 深灰色文字
                             font=('Helvetica', 9, 'bold'),
                             borderwidth=0,
                             focuscolor="none")
        self.style.map("Secondary.TButton",
                       background=[('active', '#bdbdbd'), ('pressed', '#9e9e9e'), ('disabled', '#f5f5f5')],
                       foreground=[('disabled', '#bdbdbd')],
                       relief=[('pressed', 'sunken')])
        
        # 标签样式
        self.style.configure("TLabel",
                             font=('Helvetica', 12),
                             background="#ffffff",
                             foreground="#333333")
        
        # 标签框架样式 - 无边框，卡片风格
        self.style.configure("TLabelframe",
                             relief="flat",
                             background="#ffffff",
                             padding=0)
        
        self.style.configure("TLabelframe.Label",
                             font=('Helvetica', 14, 'bold'),
                             foreground="#5c6bc0",
                             background="#ffffff")
        
        # 单选按钮样式
        self.style.configure("TRadiobutton",
                             font=('Helvetica', 12),
                             background="#ffffff",
                             foreground="#333333")
        
        # 进度条样式
        self.style.configure("TProgressbar",
                             thickness=8,
                             troughcolor="#e8eaf6",
                             background="#4caf50",
                             borderwidth=0)
        
        # 入口框样式
        self.style.configure("TEntry",
                             fieldbackground="#f5f5f5",
                             foreground="#333333",
                             font=('Helvetica', 12),
                             relief="flat")
        
        # 主框架 - 两列布局
        self.main_frame = tk.Frame(self, bg="#ffffff", padx=40, pady=40)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 顶部标题
        title_frame = tk.Frame(self.main_frame, bg="#5c6bc0", pady=20)
        title_frame.pack(fill=tk.X)
        title_label = tk.Label(title_frame, text="🔧藏文字符排序工具🔧", font=('Helvetica', 24, 'bold'), bg="#5c6bc0", fg="#ffffff")
        title_label.pack()
        
        # 顶部文件选择区域
        file_card = tk.Frame(self.main_frame, bg="#ffffff", bd=1, relief="solid", borderwidth=1, highlightbackground="#e0e0e0", pady=10, padx=20)
        file_card.pack(fill=tk.X, pady=10)
        self.create_file_frame(file_card)
        
        # 主内容区域 - 两列布局
        content_frame = tk.Frame(self.main_frame, bg="#ffffff")
        content_frame.pack(fill=tk.BOTH, expand=True, pady=15)
        content_frame.grid_columnconfigure(0, weight=78)  # 左列78%
        content_frame.grid_columnconfigure(1, weight=22)  # 右列22%
        content_frame.grid_rowconfigure(0, weight=1)
        
        # 左列 - 结果显示区域 (78%)
        result_card = tk.Frame(content_frame, bg="#ffffff", bd=1, relief="solid", borderwidth=1, highlightbackground="#e0e0e0", pady=15, padx=15)
        result_card.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        self.create_result_frame(result_card)
        
        # 右列 - 控制面板 (22%)
        control_panel = tk.Frame(content_frame, bg="#ffffff")
        control_panel.grid(row=0, column=1, sticky="nsew")
        
        # 排序选项卡片
        options_card = tk.Frame(control_panel, bg="#ffffff", bd=1, relief="solid", borderwidth=1, highlightbackground="#e0e0e0", pady=10, padx=10)
        options_card.pack(fill=tk.X, pady=(0, 6))
        self.create_sort_options_frame(options_card)
        
        # 进度卡片
        progress_card = tk.Frame(control_panel, bg="#ffffff", bd=1, relief="solid", borderwidth=1, highlightbackground="#e0e0e0", pady=10, padx=10)
        progress_card.pack(fill=tk.X, pady=(0, 6))
        self.create_progress_frame(progress_card)
        
        # 按钮卡片
        button_card = tk.Frame(control_panel, bg="#ffffff", bd=1, relief="solid", borderwidth=1, highlightbackground="#e0e0e0", pady=10, padx=10)
        button_card.pack(fill=tk.X)
        self.create_button_frame(button_card)
        
        # 底部状态栏
        self.status_frame = tk.Frame(self.main_frame, bg="#ffffff", height=50)
        self.status_frame.pack(fill=tk.X, pady=(10, 0))
        self.status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            self.status_frame, 
            text="就绪", 
            font=('Helvetica', 12, 'bold'),
            bg="#ffffff",
            fg="#666666",
            anchor=tk.CENTER
        )
        self.status_label.pack(expand=True, fill=tk.BOTH)
        
        # 初始化变量
        self.words = None
        self.sorting_thread = None
        
    def create_file_frame(self, parent):
        """创建文件选择框架（移除输出文件）"""
        ttk.Label(parent, text="输入文件:", font=('Helvetica', 12, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
        self.input_path = tk.StringVar()
        input_entry = ttk.Entry(parent, textvariable=self.input_path, width=35)
        input_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        browse_input_btn = ttk.Button(parent, text="浏览", command=self.browse_input_file)
        browse_input_btn.grid(row=0, column=2, padx=5, pady=5)
        
        parent.columnconfigure(1, weight=1)
        
    def create_sort_options_frame(self, parent):
        """创建排序选项框架（网格布局）"""
        # 算法选择
        algo_label = ttk.Label(parent, text="排序算法:", font=('Helvetica', 10, 'bold'))
        algo_label.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 3))
        
        self.algorithm = tk.StringVar(value="quick")
        algorithms = [("快速排序", "quick"), ("堆排序", "heap"), ("归并排序", "merge"), ("插入排序", "insertion")]
        
        # 配置小字体样式
        self.style.configure("Compact.TRadiobutton", font=('Helvetica', 9), background="#ffffff")
        
        # 2x2 网格布局
        ttk.Radiobutton(parent, text=algorithms[0][0], value=algorithms[0][1], variable=self.algorithm, style="Compact.TRadiobutton").grid(row=1, column=0, sticky=tk.W, padx=2, pady=1)
        ttk.Radiobutton(parent, text=algorithms[1][0], value=algorithms[1][1], variable=self.algorithm, style="Compact.TRadiobutton").grid(row=1, column=1, sticky=tk.W, padx=2, pady=1)
        ttk.Radiobutton(parent, text=algorithms[2][0], value=algorithms[2][1], variable=self.algorithm, style="Compact.TRadiobutton").grid(row=2, column=0, sticky=tk.W, padx=2, pady=1)
        ttk.Radiobutton(parent, text=algorithms[3][0], value=algorithms[3][1], variable=self.algorithm, style="Compact.TRadiobutton").grid(row=2, column=1, sticky=tk.W, padx=2, pady=1)

        # 方向选择
        direction_label = ttk.Label(parent, text="排序方向:", font=('Helvetica', 10, 'bold'))
        direction_label.grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(8, 3))
        
        self.reverse = tk.BooleanVar(value=False)
        # 1x2 网格布局
        ttk.Radiobutton(parent, text="升序", value=False, variable=self.reverse, style="Compact.TRadiobutton").grid(row=4, column=0, sticky=tk.W, padx=2, pady=1)
        ttk.Radiobutton(parent, text="降序", value=True, variable=self.reverse, style="Compact.TRadiobutton").grid(row=4, column=1, sticky=tk.W, padx=2, pady=1)
        
        # 开始按钮 - 使用主要按钮样式
        start_button = ttk.Button(parent, text="开始排序", command=self.start_sorting, style="Primary.TButton")
        start_button.grid(row=5, column=0, columnspan=2, pady=(10, 0), sticky=tk.EW)
        
    def create_progress_frame(self, parent):
        """创建进度框架（纵向排列）"""
        ttk.Label(parent, text="进度状态:", font=('Helvetica', 10, 'bold')).pack(anchor=tk.W, pady=(0, 3))
        
        self.progress_var = tk.IntVar()
        # 配置紧凑进度条样式
        self.style.configure("Compact.Horizontal.TProgressbar", thickness=6)
        self.progress = ttk.Progressbar(parent, orient=tk.HORIZONTAL, mode='determinate', variable=self.progress_var, style="Compact.Horizontal.TProgressbar")
        self.progress.pack(fill=tk.X, pady=(0, 6))
        
        self.progress_label = ttk.Label(parent, text="就绪", anchor=tk.CENTER, font=('Helvetica', 9))
        self.progress_label.pack(pady=(0, 3))
        
    def create_result_frame(self, parent):
        """创建结果框架"""
        # 添加标题
        title_label = ttk.Label(parent, text="排序结果", font=('Helvetica', 14, 'bold'))
        title_label.pack(pady=(0, 10))
        
        # 创建文本框和滚动条的容器
        text_frame = tk.Frame(parent, bg="#ffffff")
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.result_text = tk.Text(text_frame, wrap=tk.WORD, font=('Helvetica', 12), bg="#f5f5f5", relief="flat", bd=1)
        self.result_text.pack(fill=tk.BOTH, expand=True, side=tk.LEFT, padx=(0, 5))
        
        scrollbar = ttk.Scrollbar(text_frame, command=self.result_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.config(yscrollcommand=scrollbar.set)
        
        # 添加初始提示文本
        self.result_text.insert(tk.END, "排序结果将在此处显示...\n\n请选择文件并开始排序。")
        self.result_text.config(state=tk.DISABLED)
        
    def update_progress(self, value):
        """更新进度条"""
        self.progress_var.set(value)
        self.progress_label.config(text=f"进度: {value}%")
        
    def create_button_frame(self, parent):
        """创建操作按钮框架（纵向排列，带图标）"""
        # 保存结果按钮
        save_button = ttk.Button(parent, text="💾 保存结果", command=self.save_results, style="Action.TButton")
        save_button.pack(fill=tk.X, pady=(0, 3))
        
        # 复制到剪贴板按钮
        copy_button = ttk.Button(parent, text="📋 复制到剪贴板", command=self.copy_to_clipboard, style="Action.TButton")
        copy_button.pack(fill=tk.X, pady=(0, 3))
        
        # 清空内容按钮
        clear_button = ttk.Button(parent, text="🗑️ 清空内容", command=self.clear_results, style="Secondary.TButton")
        clear_button.pack(fill=tk.X, pady=(0, 3))
        
        # 退出程序按钮
        quit_button = ttk.Button(parent, text="🚪 退出程序", command=self.quit_app, style="Secondary.TButton")
        quit_button.pack(fill=tk.X, pady=0)
        
    def update_status(self, message):
        """更新状态信息"""
        self.progress_label.config(text=message)
        
    def save_results(self):
        """保存排序结果到文件"""
        if not hasattr(self, 'words') or not self.words:
            self.update_bottom_status("没有可保存的排序结果", False)
            return
        
        # 获取当前选择的排序算法名称
        algorithm_names = {
            "quick": "快速排序",
            "heap": "堆排序",
            "merge": "归并排序",
            "insertion": "插入排序"
        }
        
        # 获取排序方向
        direction_names = {
            False: "升序",
            True: "降序"
        }
        
        algorithm = self.algorithm.get()
        algorithm_name = algorithm_names.get(algorithm, algorithm)
        direction = self.reverse.get()
        direction_name = direction_names.get(direction, "升序")
        
        # 设置默认文件名为 "算法名称_算法方向_sort.txt"
        default_filename = f"{algorithm_name}_{direction_name}_sort.txt"
        
        filename = filedialog.asksaveasfilename(
            title="保存排序结果",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")],
            initialfile=default_filename
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    for word in self.words:
                        f.write(f"{word[0]}\n")
                self.update_bottom_status(f"结果已保存至: {filename}", True)
            except Exception as e:
                self.update_bottom_status(f"保存失败: {str(e)}", False)
    
    def copy_to_clipboard(self):
        """复制排序结果到剪贴板"""
        if not hasattr(self, 'words') or not self.words:
            self.update_bottom_status("没有可复制的排序结果", False)
            return
            
        try:
            result_text = "\n".join([word[0] for word in self.words[:50]])
            self.clipboard_clear()
            self.clipboard_append(result_text)
            self.update_bottom_status("前50个结果已复制到剪贴板", True)
        except Exception as e:
            self.update_bottom_status(f"复制失败: {str(e)}", False)
    
    def clear_results(self):
        """清空结果内容"""
        self.words = None
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "排序结果将在此处显示...\n\n请选择文件并开始排序。")
        self.result_text.config(state=tk.DISABLED)
        self.progress_var.set(0)
        self.update_status("就绪")
        self.update_bottom_status("已清空结果", True)
    
    def quit_app(self):
        """退出程序"""
        self.quit()
        self.destroy()
    
    def update_result(self, message):
        """更新结果文本框"""
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, message)
        
        self.result_text.tag_configure("title", font=('Helvetica', 14, 'bold'), foreground="#5c6bc0")
        self.result_text.tag_configure("item", font=('Helvetica', 12), foreground="#333333")
        
        self.result_text.tag_add("title", "1.0", "1.end+1c")
        
        line_count = int(self.result_text.index('end-1c').split('.')[0])
        for i in range(3, line_count + 1):
            self.result_text.tag_add("item", f"{i}.0", f"{i}.end+1c")
        
        self.result_text.config(state=tk.DISABLED)
    
    def update_bottom_status(self, message, is_success=None):
        """更新底部状态栏"""
        if is_success is True:
            # 成功 - 绿色
            self.status_label.config(text=message, fg="#4caf50")
        elif is_success is False:
            # 失败 - 红色
            self.status_label.config(text=message, fg="#f44336")
        else:
            # 普通状态 - 灰色
            self.status_label.config(text=message, fg="#666666")
            
    def browse_input_file(self):
        """浏览输入文件"""
        filename = filedialog.askopenfilename(
            title="选择输入文件",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        if filename:
            self.input_path.set(filename)
            
    def start_sorting(self):
        """开始排序"""
        input_path = self.input_path.get()
        
        if not input_path:
            self.update_bottom_status("错误：请选择输入文件", False)
            return
            
        if not os.path.exists(input_path):
            self.update_bottom_status(f"错误：输入文件不存在: {input_path}", False)
            return
            
        # 禁用开始按钮
        self.find_widget(self.main_frame, "开始排序")["state"] = "disabled"
                
        self.progress_var.set(0)
        self.update_status("正在加载文件...")
        self.update_bottom_status("正在加载文件...")
        
        self.sorting_thread = threading.Thread(target=self.perform_sorting)
        self.sorting_thread.daemon = True
        self.sorting_thread.start()
        
    def perform_sorting(self):
        """执行排序操作"""
        try:
            self.words, message = load_file(self.input_path.get(), self.update_progress)
            
            if self.words is None:
                self.after(0, lambda: self.update_bottom_status(f"加载文件失败：{message}", False))
                self.after(0, lambda: self.update_status("加载文件失败"))
                self.after(0, lambda: self.enable_sort_button())
                return
                
            self.after(0, lambda: self.update_status("文件加载完成，开始排序..."))
            self.after(0, lambda: self.update_bottom_status("文件加载完成，开始排序..."))
            self.after(0, lambda: self.progress_var.set(0))
            
            algorithm = self.algorithm.get()
            reverse = self.reverse.get()
            
            sort_time = 0
            sorter_class = {
                "quick": Quick_sort,
                "heap": Heap_sort,
                "merge": Merge_sort,
                "insertion": Insertion
            }.get(algorithm)

            if sorter_class:
                sorter = sorter_class()
                sort_time = sorter.sort(self.words, reverse, self.update_progress)
            
            # 确保排序后进度为100%
            self.after(0, lambda: self.update_progress(100))
                
            self.after(0, lambda: self.update_status(f"排序完成，用时 {sort_time:.2f} 秒"))
            self.after(0, lambda: self.update_bottom_status(f"排序完成，用时 {sort_time:.2f} 秒", True))
            
            # 显示排序结果预览
            preview = "排序结果前50个词条:\n\n"
            for i in range(min(50, len(self.words))):
                preview += f"{i+1}. {self.words[i][0]}\n"
                
            self.after(0, lambda: self.update_result(preview))
                
        except Exception as e:
            self.after(0, lambda: self.update_bottom_status(f"排序过程中出错：{str(e)}", False))
            self.after(0, lambda: self.update_status("排序失败"))
            
        finally:
            self.after(0, self.enable_sort_button)
            
    def enable_sort_button(self):
        """启用排序按钮"""
        self.find_widget(self.main_frame, "开始排序")["state"] = "normal"
        
    def find_widget(self, parent, text):
        """递归查找 widget"""
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
