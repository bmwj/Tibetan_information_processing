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

constant_unconverted = [0x0F90, 0x0F91, 0x0F92, 0x0F94, 0x0F95, 0x0F96, 0x0F97, 0x0F99, 0x0F9F, 0x0FA0,
                        0x0FA1, 0x0FA3, 0x0FA4, 0x0FA5, 0x0FA6, 0x0FA8, 0x0FA9, 0x0FAA, 0x0FAB, 0x0FAE,
                        0x0FAF, 0x0FB0, 0x0FB3, 0x0FB4, 0x0FB6, 0x0FB7, 0x0FB8, 0x0FBA, 0x0FBB, 0x0FBC]

class Insertion:
    def insertion_sort(self, arr, reverse=False, progress_callback=None):
        """插入排序主函数"""
        timA = time.time()
        
        if not arr:
            return 0
            
        n = len(arr)
        total_operations = int(n * n / 4) if n > 1 else 1
        completed_operations = 0
        last_percent = 0
        
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            
            if not reverse:
                while j >= 0 and cmp(key, arr[j]):
                    arr[j + 1] = arr[j]
                    j -= 1
            else:
                while j >= 0 and not cmp(key, arr[j]):
                    arr[j + 1] = arr[j]
                    j -= 1
                    
            arr[j + 1] = key
            
            completed_operations += (i + 1) / 2
            if progress_callback is not None and total_operations > 0:
                progress_percent = min(int(completed_operations * 100 / total_operations), 100)
                if progress_percent > last_percent:
                    progress_callback(progress_percent)
                    last_percent = progress_percent
        
        if progress_callback is not None:
            progress_callback(100)  # 确保进度达到100%
        
        timB = time.time()
        return timB - timA

class Heap_sort:
    def __init__(self):
        self.progress_callback = None
        self.total_operations = 0
        self.completed_operations = 0
        self.last_percent = 0

    def heap_sort(self, arr, reverse=False, progress_callback=None):
        """堆排序主函数"""
        self.progress_callback = progress_callback
        timA = time.time()
        
        if not arr:
            return 0
            
        n = len(arr)
        self.total_operations = int(2 * n * math.log2(n)) if n > 1 else 1
        self.completed_operations = 0
        self.last_percent = 0
        
        # 构建堆并更新进度
        for i in range(n // 2 - 1, -1, -1):
            self._heapify(arr, n, i, reverse)
            self.completed_operations += math.log2(n) if n > 1 else 1
            if self.progress_callback is not None:
                progress_percent = min(int(self.completed_operations * 100 / self.total_operations), 100)
                if progress_percent > self.last_percent:
                    self.progress_callback(progress_percent)
                    self.last_percent = progress_percent
            
        # 提取元素并更新进度
        for i in range(n - 1, 0, -1):
            arr[i], arr[0] = arr[0], arr[i]
            self._heapify(arr, i, 0, reverse)
            self.completed_operations += math.log2(n) if n > 1 else 1
            if self.progress_callback is not None:
                progress_percent = min(int(self.completed_operations * 100 / self.total_operations), 100)
                if progress_percent > self.last_percent:
                    self.progress_callback(progress_percent)
                    self.last_percent = progress_percent
        
        if self.progress_callback is not None:
            self.progress_callback(100)  # 确保进度达到100%
        
        timB = time.time()
        return timB - timA
        
    def _heapify(self, arr, n, i, reverse):
        """调整堆"""
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        
        if left < n:
            if not reverse:
                if not cmp(arr[largest], arr[left]):
                    largest = left
            else:
                if cmp(arr[largest], arr[left]):
                    largest = left
        
        if right < n:
            if not reverse:
                if not cmp(arr[largest], arr[right]):
                    largest = right
            else:
                if cmp(arr[largest], arr[right]):
                    largest = right
        
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            self._heapify(arr, n, largest, reverse)

class Merge_sort:
    def __init__(self):
        self.progress_callback = None
        self.total_operations = 0
        self.completed_operations = 0
        self.last_percent = 0
        
    def merge_sort(self, arr, reverse=False, progress_callback=None):
        """归并排序主函数"""
        self.progress_callback = progress_callback
        timA = time.time()
        
        if not arr:
            return 0
            
        n = len(arr)
        self.total_operations = int(n * math.log2(n)) if n > 1 else 1
        self.completed_operations = 0
        self.last_percent = 0
        
        self._merge_sort_recursive(arr, 0, len(arr) - 1, reverse)
        
        if self.progress_callback is not None:
            self.progress_callback(100)  # 确保进度达到100%
        
        timB = time.time()
        return timB - timA
        
    def _merge_sort_recursive(self, arr, left, right, reverse):
        """归并排序递归函数"""
        if left < right:
            mid = (left + right) // 2
            self._merge_sort_recursive(arr, left, mid, reverse)
            self._merge_sort_recursive(arr, mid + 1, right, reverse)
            self._merge(arr, left, mid, right, reverse)
            
            self.completed_operations += (right - left + 1)
            if self.progress_callback is not None and self.total_operations > 0:
                progress_percent = min(int(self.completed_operations * 100 / self.total_operations), 100)
                if progress_percent > self.last_percent:
                    self.progress_callback(progress_percent)
                    self.last_percent = progress_percent
    
    def _merge(self, arr, left, mid, right, reverse):
        """合并两个有序数组"""
        L = arr[left:mid + 1]
        R = arr[mid + 1:right + 1]
        i = j = 0
        k = left
        
        while i < len(L) and j < len(R):
            if not reverse:
                if cmp(L[i], R[j]):
                    arr[k] = L[i]
                    i += 1
                else:
                    arr[k] = R[j]
                    j += 1
            else:
                if not cmp(L[i], R[j]):
                    arr[k] = L[i]
                    i += 1
                else:
                    arr[k] = R[j]
                    j += 1
            k += 1
        
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
            
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

class Quick_sort:
    def __init__(self):
        self.progress_callback = None
        self.total_operations = 0
        self.completed_operations = 0
        self.last_percent = 0
        
    def quick_sort(self, arr, reverse=False, progress_callback=None):
        """快速排序主函数 - 迭代版本以避免递归深度问题"""
        self.progress_callback = progress_callback
        timA = time.time()
        
        if not arr:
            return 0
            
        n = len(arr)
        self.total_operations = int(1.39 * n * math.log2(n)) if n > 1 else 1
        self.completed_operations = 0
        self.last_percent = 0
        
        stack = [(0, n - 1)]
        
        while stack:
            low, high = stack.pop()
            if low < high:
                pi = self._partition(arr, low, high, reverse)
                
                stack.append((low, pi - 1))
                stack.append((pi + 1, high))
                
                self.completed_operations += (high - low + 1)
                if self.progress_callback is not None and self.total_operations > 0:
                    progress_percent = min(int(self.completed_operations * 100 / self.total_operations), 100)
                    if progress_percent > self.last_percent:
                        self.progress_callback(progress_percent)
                        self.last_percent = progress_percent
        
        if self.progress_callback is not None:
            self.progress_callback(100)  # 确保进度达到100%
        
        timB = time.time()
        return timB - timA
    
    def _partition(self, arr, low, high, reverse):
        """分区函数"""
        pivot = arr[high]
        i = low - 1
        
        for j in range(low, high):
            if not reverse:
                if cmp(arr[j], pivot):
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
            else:
                if not cmp(arr[j], pivot):
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
                    
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

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
        
        # 按钮样式
        self.style.configure("TButton", 
                             padding=15,
                             relief="flat",
                             background="#5c6bc0",
                             foreground="#ffffff",
                             font=('Helvetica', 12, 'bold'),
                             borderwidth=0)
        
        self.style.map("TButton",
                       background=[('active', '#3f51b5'), ('disabled', '#c5cae9')],
                       foreground=[('disabled', '#ffffff')])
        
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
        
        # 创建两列布局的主容器
        content_frame = tk.Frame(self.main_frame, bg="#ffffff")
        content_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # 左列 - 控制面板 (70%)
        left_column = tk.Frame(content_frame, bg="#ffffff")
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20))
        
        # 右列 - 结果显示 (30%)
        right_column = tk.Frame(content_frame, bg="#ffffff")
        right_column.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)
        right_column.configure(width=int(1200 * 0.3))  # 30% 宽度
        
        # 左列内容
        # 文件选择卡片
        file_card = tk.Frame(left_column, bg="#ffffff", bd=1, relief="solid", borderwidth=1, highlightbackground="#e0e0e0", pady=20, padx=20)
        file_card.pack(fill=tk.X, pady=10)
        self.create_file_frame(file_card)
        
        # 选项卡片
        options_card = tk.Frame(left_column, bg="#ffffff", bd=1, relief="solid", borderwidth=1, highlightbackground="#e0e0e0", pady=20, padx=20)
        options_card.pack(fill=tk.X, pady=10)
        self.create_sort_options_frame(options_card)
        
        # 进度卡片
        progress_card = tk.Frame(left_column, bg="#ffffff", bd=1, relief="solid", borderwidth=1, highlightbackground="#e0e0e0", pady=20, padx=20)
        progress_card.pack(fill=tk.X, pady=10)
        self.create_progress_frame(progress_card)
        
        # 右列内容 - 结果卡片
        result_card = tk.Frame(right_column, bg="#ffffff", bd=1, relief="solid", borderwidth=1, highlightbackground="#e0e0e0", pady=20, padx=20)
        result_card.pack(fill=tk.BOTH, expand=True)
        self.create_result_frame(result_card)
        
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
        """创建文件选择框架"""
        ttk.Label(parent, text="输入文件:", font=('Helvetica', 12, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=10, padx=5)
        self.input_path = tk.StringVar()
        input_entry = ttk.Entry(parent, textvariable=self.input_path, width=35)
        input_entry.grid(row=0, column=1, padx=5, pady=10, sticky=tk.EW)
        browse_input_btn = ttk.Button(parent, text="浏览", command=self.browse_input_file)
        browse_input_btn.grid(row=0, column=2, padx=5, pady=10)
        
        ttk.Label(parent, text="输出文件:", font=('Helvetica', 12, 'bold')).grid(row=1, column=0, sticky=tk.W, pady=10, padx=5)
        self.output_path = tk.StringVar()
        output_entry = ttk.Entry(parent, textvariable=self.output_path, width=35)
        output_entry.grid(row=1, column=1, padx=5, pady=10, sticky=tk.EW)
        browse_output_btn = ttk.Button(parent, text="浏览", command=self.browse_output_file)
        browse_output_btn.grid(row=1, column=2, padx=5, pady=10)
        
        parent.columnconfigure(1, weight=1)
        
    def create_sort_options_frame(self, parent):
        """创建排序选项框架"""
        # 算法选择
        algo_label = ttk.Label(parent, text="排序算法:", font=('Helvetica', 12, 'bold'))
        algo_label.grid(row=0, column=0, sticky=tk.W, pady=10, padx=5)
        
        self.algorithm = tk.StringVar(value="quick")
        algorithms = [("快速排序", "quick"), ("堆排序", "heap"), ("归并排序", "merge"), ("插入排序", "insertion")]
        
        # 将算法选项分为两行显示以适应较窄的左列
        for i, (text, value) in enumerate(algorithms[:2]):
            ttk.Radiobutton(parent, text=text, value=value, variable=self.algorithm).grid(row=0, column=i+1, padx=10, sticky=tk.W)
        
        for i, (text, value) in enumerate(algorithms[2:]):
            ttk.Radiobutton(parent, text=text, value=value, variable=self.algorithm).grid(row=1, column=i+1, padx=10, sticky=tk.W)
        
        # 方向选择
        direction_label = ttk.Label(parent, text="排序方向:", font=('Helvetica', 12, 'bold'))
        direction_label.grid(row=2, column=0, sticky=tk.W, pady=10, padx=5)
        
        self.reverse = tk.BooleanVar(value=False)
        ttk.Radiobutton(parent, text="升序", value=False, variable=self.reverse).grid(row=2, column=1, padx=10, sticky=tk.W)
        ttk.Radiobutton(parent, text="降序", value=True, variable=self.reverse).grid(row=2, column=2, padx=10, sticky=tk.W)
        
        # 开始按钮
        start_button = ttk.Button(parent, text="开始排序", command=self.start_sorting)
        start_button.grid(row=3, column=0, columnspan=3, pady=20, sticky=tk.EW)
        
    def create_progress_frame(self, parent):
        """创建进度框架"""
        ttk.Label(parent, text="进度状态:", font=('Helvetica', 12, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
        
        self.progress_var = tk.IntVar()
        self.progress = ttk.Progressbar(parent, orient=tk.HORIZONTAL, mode='determinate', variable=self.progress_var)
        self.progress.grid(row=1, column=0, sticky=tk.EW, pady=10, padx=5)
        
        self.progress_label = ttk.Label(parent, text="就绪", anchor=tk.CENTER, font=('Helvetica', 11))
        self.progress_label.grid(row=2, column=0, pady=5)
        
        parent.columnconfigure(0, weight=1)
        
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
        
        # 添加按钮框架
        button_frame = tk.Frame(parent, bg="#ffffff", pady=10)
        button_frame.pack(fill=tk.X)
        
        # 保存结果按钮
        save_button = ttk.Button(button_frame, text="保存结果", command=self.save_results)
        save_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # 复制到剪贴板按钮
        copy_button = ttk.Button(button_frame, text="复制到剪贴板", command=self.copy_to_clipboard)
        copy_button.pack(side=tk.LEFT)
        
    def update_progress(self, value):
        """更新进度条"""
        self.progress_var.set(value)
        self.progress_label.config(text=f"进度: {value}%")
        
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
        
        algorithm = self.algorithm.get()
        algorithm_name = algorithm_names.get(algorithm, algorithm)
        
        # 设置默认文件名为 "排序算法名_sort.txt"
        default_filename = f"{algorithm_name}_sort.txt"
        
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
            input_dir = os.path.dirname(filename)
            input_name = os.path.basename(filename)
            name_parts = os.path.splitext(input_name)
            output_name = f"{name_parts[0]}_sorted{name_parts[1]}"
            self.output_path.set(os.path.join(input_dir, output_name))
            self.output_path.set(os.path.join(input_dir, output_name))
            
    def browse_output_file(self):
        """浏览输出文件"""
        filename = filedialog.asksaveasfilename(
            title="选择输出文件",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        if filename:
            self.output_path.set(filename)
            
    def start_sorting(self):
        """开始排序"""
        input_path = self.input_path.get()
        output_path = self.output_path.get()
        
        if not input_path:
            self.update_bottom_status("错误：请选择输入文件", False)
            return
            
        if not output_path:
            self.update_bottom_status("错误：请选择输出文件", False)
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
            if algorithm == "quick":
                sorter = Quick_sort()
                sort_time = sorter.quick_sort(self.words, reverse, self.update_progress)
            elif algorithm == "heap":
                sorter = Heap_sort()
                sort_time = sorter.heap_sort(self.words, reverse, self.update_progress)
            elif algorithm == "merge":
                sorter = Merge_sort()
                sort_time = sorter.merge_sort(self.words, reverse, self.update_progress)
            elif algorithm == "insertion":
                sorter = Insertion()
                sort_time = sorter.insertion_sort(self.words, reverse, self.update_progress)
            
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