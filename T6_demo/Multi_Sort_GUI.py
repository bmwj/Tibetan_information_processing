# -*- coding: utf-8 -*-
# 创建者：Pemawangchuk
# 版本：1.0
# 日期：2025-04-06
# 描述：本模块实现了多种排序算法的GUI界面，用于对藏文数据进行排序。

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import time
import os
import math
import threading
import sys
import os
# 获取项目根目录路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)  # 将项目根目录添加到Python路径
# 导入common目录下的模块
from common.Cmp import cmp
from common.SplitComponent import Split_component

constant_unconverted = [0x0F90, 0x0F91, 0x0F92, 0x0F94, 0x0F95, 0x0F96, 0x0F97, 0x0F99, 0x0F9F, 0x0FA0,
                    0x0FA1, 0x0FA3, 0x0FA4, 0x0FA5,0x0FA6, 0x0FA8, 0x0FA9, 0x0FAA, 0x0FAB, 0x0FAE,
                    0x0FAF, 0x0FB0, 0x0FB3, 0x0FB4, 0x0FB6, 0x0FB7, 0x0FB8, 0x0FBA, 0x0FBB, 0x0FBC]

class Insertion():
    def insertion_sort(self, arr, reverse=False, progress_callback=None):
        """插入排序主函数"""
        timA = time.time()
        
        # 防止空列表
        if not arr:
            return 0
            
        # 估计排序操作次数（插入排序的平均比较次数约为 n²/4）
        n = len(arr)
        total_operations = int(n * n / 4) if n > 1 else 1
        
        # 记录已完成的操作数
        completed_operations = 0
        last_percent = 0
        
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            
            # 升序排序
            if not reverse:
                while j >= 0 and cmp(key, arr[j]):
                    arr[j + 1] = arr[j]
                    j -= 1
            # 降序排序
            else:
                while j >= 0 and not cmp(key, arr[j]):
                    arr[j + 1] = arr[j]
                    j -= 1
                    
            arr[j + 1] = key
            
            # 更新已完成操作数和进度
            completed_operations += (i + 1) / 2  # 平均比较次数
            if progress_callback is not None and total_operations > 0:
                # 计算百分比进度
                progress_percent = min(int(completed_operations * 100 / total_operations), 100)
                # 只有百分比变化时才更新进度
                if progress_percent > last_percent:
                    progress_callback(progress_percent)
                    last_percent = progress_percent
        
        timB = time.time()
        return timB - timA

class Heap_sort():
    def __init__(self):
        self.progress_callback = None
        self.total_operations = 0
        self.completed_operations = 0
        self.last_percent = 0

    def heap_sort(self, arr, reverse=False, progress_callback=None):
        """堆排序主函数"""
        self.progress_callback = progress_callback
        timA = time.time()
        
        # 防止空列表
        if not arr:
            return 0
            
        n = len(arr)
        # 估计排序操作次数（堆排序的比较次数约为 2n*log(n)）
        self.total_operations = int(2 * n * math.log2(n)) if n > 1 else 1
        self.completed_operations = 0
        self.last_percent = 0
        
        # 构建最大堆
        for i in range(n // 2 - 1, -1, -1):
            self._heapify(arr, n, i, reverse)
            
        # 逐个从堆中取出元素
        for i in range(n - 1, 0, -1):
            arr[i], arr[0] = arr[0], arr[i]
            self._heapify(arr, i, 0, reverse)
            
            # 更新进度
            self.completed_operations += math.log2(n)
            if self.progress_callback is not None:
                progress_percent = min(int(self.completed_operations * 100 / self.total_operations), 100)
                if progress_percent > self.last_percent:
                    self.progress_callback(progress_percent)
                    self.last_percent = progress_percent
        
        timB = time.time()
        return timB - timA
        
    def _heapify(self, arr, n, i, reverse):
        """调整堆"""
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        
        # 根据排序方向比较左子节点
        if left < n:
            if not reverse:
                if not cmp(arr[largest], arr[left]):
                    largest = left
            else:
                if cmp(arr[largest], arr[left]):
                    largest = left
        
        # 根据排序方向比较右子节点
        if right < n:
            if not reverse:
                if not cmp(arr[largest], arr[right]):
                    largest = right
            else:
                if cmp(arr[largest], arr[right]):
                    largest = right
        
        # 如果最大值不是根节点，则交换并继续调整
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            self._heapify(arr, n, largest, reverse)

class Merge_sort():
    def __init__(self):
        self.progress_callback = None
        self.total_operations = 0
        self.completed_operations = 0
        self.last_percent = 0
        
    def merge_sort(self, arr, reverse=False, progress_callback=None):
        """归并排序主函数"""
        self.progress_callback = progress_callback
        timA = time.time()
        
        # 防止空列表
        if not arr:
            return 0
            
        # 估计排序操作次数（归并排序的比较次数约为 n*log(n)）
        n = len(arr)
        self.total_operations = int(n * math.log2(n)) if n > 1 else 1
        self.completed_operations = 0
        self.last_percent = 0
        
        # 执行归并排序
        self._merge_sort_recursive(arr, 0, len(arr) - 1, reverse)
        
        timB = time.time()
        return timB - timA
        
    def _merge_sort_recursive(self, arr, left, right, reverse):
        """归并排序递归函数"""
        if left < right:
            mid = (left + right) // 2
            
            # 分别对左右两部分进行排序
            self._merge_sort_recursive(arr, left, mid, reverse)
            self._merge_sort_recursive(arr, mid + 1, right, reverse)
            
            # 合并两个有序数组
            self._merge(arr, left, mid, right, reverse)
            
            # 更新进度
            self.completed_operations += (right - left)
            if self.progress_callback is not None and self.total_operations > 0:
                progress_percent = min(int(self.completed_operations * 100 / self.total_operations), 100)
                if progress_percent > self.last_percent:
                    self.progress_callback(progress_percent)
                    self.last_percent = progress_percent
    
    def _merge(self, arr, left, mid, right, reverse):
        """合并两个有序数组"""
        # 创建临时数组
        L = arr[left:mid + 1]
        R = arr[mid + 1:right + 1]
        
        # 初始化指针
        i = j = 0
        k = left
        
        # 合并两个数组
        while i < len(L) and j < len(R):
            if not reverse:
                # 升序排序
                if cmp(L[i], R[j]):
                    arr[k] = L[i]
                    i += 1
                else:
                    arr[k] = R[j]
                    j += 1
            else:
                # 降序排序
                if not cmp(L[i], R[j]):
                    arr[k] = L[i]
                    i += 1
                else:
                    arr[k] = R[j]
                    j += 1
            k += 1
        
        # 处理剩余元素
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
            
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

class Quick_sort():
    def __init__(self):
        self.progress_callback = None
        self.total_operations = 0
        self.completed_operations = 0
        self.last_percent = 0
        
    def quick_sort(self, arr, reverse=False, progress_callback=None):
        """快速排序主函数"""
        self.progress_callback = progress_callback
        timA = time.time()
        
        # 防止空列表
        if not arr:
            return 0
            
        # 估计排序操作次数（快速排序的平均比较次数约为 1.39n*log(n)）
        n = len(arr)
        self.total_operations = int(1.39 * n * math.log2(n)) if n > 1 else 1
        self.completed_operations = 0
        self.last_percent = 0
        
        # 执行快速排序
        self._quick_sort_recursive(arr, 0, len(arr) - 1, reverse)
        
        timB = time.time()
        return timB - timA
        
    def _quick_sort_recursive(self, arr, low, high, reverse):
        """快速排序递归函数"""
        if low < high:
            # 分区操作，获取分区点
            pi = self._partition(arr, low, high, reverse)
            
            # 分别对左右两部分进行排序
            self._quick_sort_recursive(arr, low, pi - 1, reverse)
            self._quick_sort_recursive(arr, pi + 1, high, reverse)
            
            # 更新进度
            self.completed_operations += (high - low)
            if self.progress_callback is not None and self.total_operations > 0:
                progress_percent = min(int(self.completed_operations * 100 / self.total_operations), 100)
                if progress_percent > self.last_percent:
                    self.progress_callback(progress_percent)
                    self.last_percent = progress_percent
    
    def _partition(self, arr, low, high, reverse):
        """分区函数"""
        # 选择最右边的元素作为基准
        pivot = arr[high]
        i = low - 1
        
        for j in range(low, high):
            if not reverse:
                # 升序排序
                if cmp(arr[j], pivot):
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
            else:
                # 降序排序
                if not cmp(arr[j], pivot):
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
                    
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

def load_file(file_path, progress_callback=None):
    """加载文件并处理藏文数据"""
    split_com = Split_component()
    word_18785_ns = []
    
    # 尝试不同的编码方式
    encodings = ['utf-8', 'utf-16', 'utf-16-le', 'utf-16-be', 'gb18030']
    
    for encoding in encodings:
        try:
            with open(file=file_path, mode='r', encoding=encoding) as f:
                # 读取文件的前几行来确认编码是否正确
                try:
                    lines = []
                    for _ in range(5):
                        line = f.readline().strip('\n')
                        if line:
                            lines.append(line)
                    if not lines:
                        continue  # 如果没有读到内容，尝试下一种编码
                    
                    # 如果能够成功读取，则使用此编码
                    print(f"使用 {encoding} 编码读取文件")
                    break
                except:
                    continue
        except:
            continue
    else:
        # 如果所有编码都失败
        return None, "无法确定文件编码，请检查文件格式"
    
    try:
        # 重新打开文件并读取全部内容
        with open(file=file_path, mode='r', encoding=encoding) as f:
            # 获取文件总行数
            all_lines = f.readlines()
            total_lines = len(all_lines)
            
            # 处理每一行
            for i, line in enumerate(all_lines):
                Tibetan = line.strip('\n')
                if not Tibetan:
                    continue
                    
                try:
                    word = split_com.Split(Tibetan)[:-1]
                    for j in range(1, 9):
                        if (word[j] != ''):
                            word[j] = ord(word[j])
                        else:
                            word[j] = 0
                    word[1], word[3] = word[3], word[1]
                    for j in range(1, 9):
                        if (0x0F90 <= word[j] <= 0x0FB8):
                            word[j] = word[j] - 80
                    word_18785_ns.append(word)
                except Exception as e:
                    print(f"处理第{i+1}行时出错: {str(e)}")
                
                # 更新进度
                if progress_callback is not None and i % 10 == 0:
                    progress_callback(min(int((i + 1) * 100 / total_lines), 100))
            
        if progress_callback is not None:
            progress_callback(100)  # 确保进度条到达100%
            
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
        self.title("藏文排序工具 - 排序可视化系统")
        self.geometry("900x700")
        self.resizable(True, True)
        self.configure(bg="#f5f5f5")  # 设置窗口背景色
        
        # 设置样式
        self.style = ttk.Style()
        self.style.theme_use('clam')  # 使用clam主题，更现代的外观
        
        # 按钮样式
        self.style.configure("TButton", 
                            padding=8, 
                            relief="flat", 
                            background="#4a86e8", 
                            foreground="#ffffff",
                            font=('微软雅黑', 10, 'bold'))
        
        # 标签样式
        self.style.configure("TLabel", 
                            padding=6, 
                            font=('微软雅黑', 10))
        
        # 标签框架样式
        self.style.configure("TLabelframe", 
                            padding=10, 
                            relief="groove", 
                            borderwidth=2)
        
        self.style.configure("TLabelframe.Label", 
                            font=('微软雅黑', 11, 'bold'),
                            foreground="#333333")
        
        # 单选按钮样式
        self.style.configure("TRadiobutton", 
                            font=('微软雅黑', 10))
        
        # 进度条样式
        self.style.configure("TProgressbar", 
                            thickness=25,
                            troughcolor="#f0f0f0",
                            background="#4caf50")
        
        # 创建主框架
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 创建文件选择框架
        self.create_file_frame()
        
        # 创建排序选项框架
        self.create_sort_options_frame()
        
        # 创建进度框架
        self.create_progress_frame()
        
        # 创建结果框架
        self.create_result_frame()
        
        # 初始化变量
        self.words = None
        self.sorting_thread = None
        
    def create_file_frame(self):
        """创建文件选择框架"""
        file_frame = ttk.LabelFrame(self.main_frame, text="文件选择")
        file_frame.pack(fill=tk.X, pady=10)
        
        # 内部框架，用于更好的布局
        inner_frame = ttk.Frame(file_frame)
        inner_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 输入文件
        ttk.Label(inner_frame, text="输入文件:").grid(row=0, column=0, sticky=tk.W, pady=8)
        self.input_path = tk.StringVar()
        input_entry = ttk.Entry(inner_frame, textvariable=self.input_path, width=60)
        input_entry.grid(row=0, column=1, padx=10, pady=8, sticky=tk.W+tk.E)
        browse_input_btn = ttk.Button(inner_frame, text="浏览...", command=self.browse_input_file)
        browse_input_btn.grid(row=0, column=2, padx=5, pady=8)
        
        # 输出文件
        ttk.Label(inner_frame, text="输出文件:").grid(row=1, column=0, sticky=tk.W, pady=8)
        self.output_path = tk.StringVar()
        output_entry = ttk.Entry(inner_frame, textvariable=self.output_path, width=60)
        output_entry.grid(row=1, column=1, padx=10, pady=8, sticky=tk.W+tk.E)
        browse_output_btn = ttk.Button(inner_frame, text="浏览...", command=self.browse_output_file)
        browse_output_btn.grid(row=1, column=2, padx=5, pady=8)
        
        # 配置列权重，使输入框可以自适应宽度
        inner_frame.columnconfigure(1, weight=1)
        
    def create_sort_options_frame(self):
        """创建排序选项框架"""
        options_frame = ttk.LabelFrame(self.main_frame, text="排序选项")
        options_frame.pack(fill=tk.X, pady=10)
        
        # 内部框架，用于更好的布局
        inner_frame = ttk.Frame(options_frame)
        inner_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 排序算法选择
        algo_frame = ttk.Frame(inner_frame)
        algo_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(algo_frame, text="排序算法:", font=('微软雅黑', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        
        self.algorithm = tk.StringVar(value="quick")
        algorithms = [
            ("快速排序", "quick"),
            ("堆排序", "heap"),
            ("归并排序", "merge"),
            ("插入排序", "insertion")
        ]
        
        # 创建算法选择的单选按钮组
        algo_buttons_frame = ttk.Frame(algo_frame)
        algo_buttons_frame.pack(side=tk.LEFT, padx=20)
        
        for i, (text, value) in enumerate(algorithms):
            ttk.Radiobutton(
                algo_buttons_frame, 
                text=text, 
                value=value, 
                variable=self.algorithm
            ).pack(side=tk.LEFT, padx=15)
        
        # 排序方向
        direction_frame = ttk.Frame(inner_frame)
        direction_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(direction_frame, text="排序方向:", font=('微软雅黑', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        
        self.reverse = tk.BooleanVar(value=False)
        
        direction_buttons_frame = ttk.Frame(direction_frame)
        direction_buttons_frame.pack(side=tk.LEFT, padx=20)
        
        ttk.Radiobutton(
            direction_buttons_frame, 
            text="升序", 
            value=False, 
            variable=self.reverse
        ).pack(side=tk.LEFT, padx=15)
        
        ttk.Radiobutton(
            direction_buttons_frame, 
            text="降序", 
            value=True, 
            variable=self.reverse
        ).pack(side=tk.LEFT, padx=15)
        
        # 开始排序按钮
        button_frame = ttk.Frame(inner_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        # 自定义按钮样式
        self.style.configure("Start.TButton", 
                            background="#4caf50", 
                            foreground="white",
                            font=('微软雅黑', 11, 'bold'),
                            padding=10)
        
        start_button = ttk.Button(
            button_frame, 
            text="开始排序", 
            command=self.start_sorting,
            style="Start.TButton"
        )
        start_button.pack(pady=5, ipadx=20, ipady=5)
        
    def create_progress_frame(self):
        """创建进度框架"""
        progress_frame = ttk.LabelFrame(self.main_frame, text="排序进度")
        progress_frame.pack(fill=tk.X, pady=10)
        
        # 内部框架
        inner_frame = ttk.Frame(progress_frame)
        inner_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 进度条
        self.progress_var = tk.IntVar()
        self.progress = ttk.Progressbar(
            inner_frame, 
            orient=tk.HORIZONTAL, 
            length=100, 
            mode='determinate', 
            variable=self.progress_var
        )
        self.progress.pack(fill=tk.X, padx=5, pady=10)
        
        # 进度标签
        self.progress_label = ttk.Label(
            inner_frame, 
            text="就绪", 
            font=('微软雅黑', 10),
            anchor=tk.CENTER
        )
        self.progress_label.pack(pady=5, fill=tk.X)
        
    def create_result_frame(self):
        """创建结果框架"""
        result_frame = ttk.LabelFrame(self.main_frame, text="排序结果预览")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # 内部框架
        inner_frame = ttk.Frame(result_frame)
        inner_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 结果文本框
        self.result_text = tk.Text(
            inner_frame, 
            wrap=tk.WORD, 
            height=10,
            font=('微软雅黑', 11),
            bg="#ffffff",
            relief="sunken",
            borderwidth=1
        )
        self.result_text.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        # 滚动条
        scrollbar = ttk.Scrollbar(inner_frame, command=self.result_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.config(yscrollcommand=scrollbar.set)
        
    def update_progress(self, value):
        """更新进度条"""
        self.progress_var.set(value)
        self.progress_label.config(text=f"排序进度: {value}%")
        
    def update_status(self, message):
        """更新状态信息"""
        self.progress_label.config(text=message, foreground="#333333")
        
    def update_result(self, message):
        """更新结果文本框"""
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, message)
        
        # 为标题添加标签
        self.result_text.tag_configure("title", font=('微软雅黑', 12, 'bold'), foreground="#4a86e8")
        self.result_text.tag_configure("item", font=('微软雅黑', 11), foreground="#333333")
        
        # 应用标签
        self.result_text.tag_add("title", "1.0", "1.end+1c")
        
        # 为每个项目添加标签
        line_count = int(self.result_text.index('end-1c').split('.')[0])
        for i in range(3, line_count + 1):  # 从第3行开始（跳过标题和空行）
            self.result_text.tag_add("item", f"{i}.0", f"{i}.end+1c")
            
    def browse_input_file(self):
        """浏览输入文件"""
        filename = filedialog.askopenfilename(
            title="选择输入文件", 
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        if filename:
            self.input_path.set(filename)
            # 自动设置输出文件名
            input_dir = os.path.dirname(filename)
            input_name = os.path.basename(filename)
            name_parts = os.path.splitext(input_name)
            output_name = f"{name_parts[0]}_sorted{name_parts[1]}"
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
        # 检查输入和输出路径
        input_path = self.input_path.get()
        output_path = self.output_path.get()
        
        if not input_path:
            messagebox.showerror("错误", "请选择输入文件")
            return
            
        if not output_path:
            messagebox.showerror("错误", "请选择输出文件")
            return
            
        if not os.path.exists(input_path):
            messagebox.showerror("错误", f"输入文件不存在: {input_path}")
            return
            
        # 禁用排序按钮
        for widget in self.winfo_children():
            if isinstance(widget, ttk.Button) and widget["text"] == "开始排序":
                widget["state"] = "disabled"
                
        # 重置进度条
        self.progress_var.set(0)
        self.update_status("正在加载文件...")
        
        # 在新线程中执行排序
        self.sorting_thread = threading.Thread(target=self.perform_sorting)
        self.sorting_thread.daemon = True
        self.sorting_thread.start()
        
    def perform_sorting(self):
        """执行排序操作"""
        try:
            # 加载文件
            self.words, message = load_file(self.input_path.get(), self.update_progress)
            
            if self.words is None:
                self.after(0, lambda: messagebox.showerror("错误", message))
                self.after(0, lambda: self.update_status("加载文件失败"))
                self.after(0, lambda: self.enable_sort_button())
                return
                
            self.after(0, lambda: self.update_status("文件加载完成，开始排序..."))
            self.after(0, lambda: self.progress_var.set(0))
            
            # 选择排序算法
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
                
            self.after(0, lambda: self.update_status(f"排序完成，用时 {sort_time:.2f} 秒，正在保存..."))
            
            # 保存结果
            success, message = save_file(self.output_path.get(), self.words)
            
            if success:
                self.after(0, lambda: self.update_status(f"排序完成，用时 {sort_time:.2f} 秒"))
                
                # 显示排序结果前10个
                preview = "排序结果前10个词条:\n\n"
                for i in range(min(10, len(self.words))):
                    preview += f"{i+1}. {self.words[i][0]}\n"
                    
                self.after(0, lambda: self.update_result(preview))
                self.after(0, lambda: messagebox.showinfo("成功", message))
            else:
                self.after(0, lambda: messagebox.showerror("错误", message))
                self.after(0, lambda: self.update_status("保存文件失败"))
                
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("错误", f"排序过程中出错: {str(e)}"))
            self.after(0, lambda: self.update_status("排序失败"))
            
        finally:
            # 启用排序按钮
            self.after(0, self.enable_sort_button)
            
    def enable_sort_button(self):
        """启用排序按钮"""
        for widget in self.winfo_children():
            if isinstance(widget, ttk.Button) and widget["text"] == "开始排序":
                widget["state"] = "normal"

if __name__ == "__main__":
    app = SortApp()
    app.mainloop()
