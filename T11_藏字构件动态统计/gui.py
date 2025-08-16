# -*- coding: UTF-8 -*-
# GUI模块 - 包含GUI相关的类和方法

import time
import tkinter as tk
from tkinter import filedialog, messagebox, Frame, ttk
import os

# 尝试导入ttkbootstrap，如果不存在则使用标准ttk
try:
    import ttkbootstrap as ttk_bs
    from ttkbootstrap import Style
    from ttkbootstrap.constants import *
    USE_BOOTSTRAP = True
except ImportError:
    USE_BOOTSTRAP = False
    # 定义与ttkbootstrap兼容的常量
    LEFT, RIGHT, TOP, BOTTOM = tk.LEFT, tk.RIGHT, tk.TOP, tk.BOTTOM
    X, Y, BOTH, NONE = tk.X, tk.Y, tk.BOTH, tk.NONE
    CENTER, N, S, E, W = tk.CENTER, tk.N, tk.S, tk.E, tk.W
    HORIZONTAL, VERTICAL = tk.HORIZONTAL, tk.VERTICAL
    END = tk.END
    # 定义ttkbootstrap样式常量
    PRIMARY, SECONDARY, SUCCESS, INFO, WARNING, DANGER = "primary", "secondary", "success", "info", "warning", "danger"

from data_structures import reset_counters
from component_analyzer import ComponentAnalyzer
from utils import format_results

class DynamicTibetanComponentGUI:
    """藏字构件动态统计分析器GUI界面"""
    
    def __init__(self):
        self.essay = ''
        self.analyzer = ComponentAnalyzer()
        self.setup_gui()
        
    def setup_gui(self):
        """设置GUI界面"""
        if USE_BOOTSTRAP:
            # 使用ttkbootstrap现代主题
            self.style = Style(theme='darkly')  # 更现代的深色主题
            self.window = self.style.master
        else:
            # 使用标准tkinter
            self.window = tk.Tk()
            self.style = ttk.Style()
            self.window.configure(bg='#333333')  # 深色背景
        
        # 窗口基本设置
        self.window.title('🏔️ 藏字构件动态统计分析器')
        self.window.geometry('1400x1000+200+50')
        self.window.minsize(1200, 800)
        
        # 设置窗口图标（如果有）
        try:
            self.window.iconphoto(True, tk.PhotoImage(file="T11_藏字构件动态统计/icon.png"))
        except:
            pass  # 如果图标不存在，忽略错误
        
        # 创建主容器
        self.create_main_container()
        
        # 创建各个组件
        self.create_header()
        self.create_file_section()
        self.create_content_section()
        self.create_control_section()
        self.create_progress_section()
        self.create_status_bar()
        
    def create_main_container(self):
        """创建主容器"""
        if USE_BOOTSTRAP:
            self.main_frame = ttk_bs.Frame(self.window, padding=20)
        else:
            self.main_frame = ttk.Frame(self.window, padding=20)
            self.main_frame.configure(style='Main.TFrame')
            # 创建兼容样式
            self.style.configure('Main.TFrame', background='#333333')
            
        self.main_frame.pack(fill=BOTH, expand=True)
        
    def create_header(self):
        """创建标题区域"""
        header_frame = ttk_bs.Frame(self.main_frame)
        header_frame.pack(fill=X, pady=(0, 20))
        
        # 主标题
        title_label = ttk_bs.Label(
            header_frame,
            text="藏字构件动态统计分析器",
            font=('Microsoft YaHei UI', 26, 'bold'),
            bootstyle=PRIMARY
        )
        title_label.pack(side=LEFT)
        
        # 副标题
        subtitle_label = ttk_bs.Label(
            header_frame,
            text="Dynamic Tibetan Component Statistics Analyzer",
            font=('Arial', 13, 'italic'),
            bootstyle=SECONDARY
        )
        subtitle_label.pack(side=LEFT, padx=(20, 0), pady=(5, 0))
        
        # 主题切换
        theme_frame = ttk_bs.Frame(header_frame)
        theme_frame.pack(side=RIGHT)
        
        ttk_bs.Label(theme_frame, text="主题:", font=('Microsoft YaHei UI', 10)).pack(side=LEFT, padx=(0, 5))
        
        self.theme_var = tk.StringVar(value='darkly')
        theme_combo = ttk_bs.Combobox(
            theme_frame,
            textvariable=self.theme_var,
            values=['darkly', 'superhero', 'solar', 'cyborg', 'vapor', 'morph'],
            width=10,
            state='readonly',
            bootstyle='primary'
        )
        theme_combo.pack(side=LEFT)
        theme_combo.bind('<<ComboboxSelected>>', self.change_theme)
        
    def create_file_section(self):
        """创建文件选择区域"""
        file_frame = ttk_bs.LabelFrame(
            self.main_frame,
            text="📁 文件选择",
            padding=15,
            bootstyle=INFO
        )
        file_frame.pack(fill=X, pady=(0, 20))
        
        # 文件路径显示
        path_frame = ttk_bs.Frame(file_frame)
        path_frame.pack(fill=X, pady=(0, 10))
        
        ttk_bs.Label(
            path_frame,
            text="选择的文件:",
            font=('Microsoft YaHei UI', 12)
        ).pack(anchor=W, pady=(0, 5))
        
        self.file_path_var = tk.StringVar()
        self.file_entry = ttk_bs.Entry(
            path_frame,
            textvariable=self.file_path_var,
            font=('Microsoft YaHei UI', 11),
            state='readonly'
        )
        self.file_entry.pack(fill=X, pady=(0, 10))
        
        # 按钮区域
        button_frame = ttk_bs.Frame(file_frame)
        button_frame.pack(fill=X)
        
        # 选择文件按钮
        select_btn = ttk_bs.Button(
            button_frame,
            text="📂 选择文件/文件夹",
            command=self.open_file,
            bootstyle=(SUCCESS, "outline"),
            width=18
        )
        select_btn.pack(side=LEFT, padx=(0, 10))
        
        # 清空按钮
        clear_btn = ttk_bs.Button(
            button_frame,
            text="🗑️ 清空",
            command=self.clear_data,
            bootstyle=(WARNING, "outline"),
            width=15
        )
        clear_btn.pack(side=LEFT, padx=(0, 10))
        
        # 文件信息显示
        self.file_info_label = ttk_bs.Label(
            button_frame,
            text="未选择文件",
            font=('Microsoft YaHei UI', 10),
            bootstyle=SECONDARY
        )
        self.file_info_label.pack(side=RIGHT, padx=(10, 0))
        
    def create_content_section(self):
        """创建内容显示区域"""
        content_frame = ttk_bs.Frame(self.main_frame)
        content_frame.pack(fill=BOTH, expand=True)
        
        # 左侧：文本预览
        left_frame = ttk_bs.LabelFrame(
            content_frame,
            text="📄 文本预览",
            padding=10,
            bootstyle=INFO
        )
        left_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 10))
        
        # 创建带滚动条的文本框
        text_frame = ttk_bs.Frame(left_frame)
        text_frame.pack(fill=BOTH, expand=True)
        
        self.text_display = tk.Text(
            text_frame,
            font=('Microsoft YaHei UI', 12),
            wrap=tk.WORD,
            padx=15,
            pady=15,
            bg='#2b2b2b',  # 深色背景
            fg='#e6e6e6',  # 浅色文字
            insertbackground='white',  # 光标颜色
            selectbackground='#0078d7',  # 选中背景
            selectforeground='white',  # 选中文字颜色
            relief=tk.FLAT,  # 扁平化边框
            borderwidth=0  # 无边框
        )
        
        # 滚动条
        scrollbar1 = ttk_bs.Scrollbar(text_frame, orient=VERTICAL)
        self.text_display.config(yscrollcommand=scrollbar1.set)
        scrollbar1.config(command=self.text_display.yview)
        
        self.text_display.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar1.pack(side=RIGHT, fill=Y)
        
        # 右侧：统计结果
        right_frame = ttk_bs.LabelFrame(
            content_frame,
            text="📊 构件统计结果",
            padding=10,
            bootstyle=PRIMARY
        )
        right_frame.pack(side=RIGHT, fill=BOTH, expand=True)
        
        # 创建带滚动条的结果显示区
        result_frame = ttk_bs.Frame(right_frame)
        result_frame.pack(fill=BOTH, expand=True)
        
        self.result_text = tk.Text(
            result_frame,
            font=('Consolas', 11),
            wrap=tk.WORD,
            padx=15,
            pady=15,
            bg='#2b2b2b',  # 深色背景
            fg='#e6e6e6',  # 浅色文字
            insertbackground='white',  # 光标颜色
            selectbackground='#0078d7',  # 选中背景
            selectforeground='white',  # 选中文字颜色
            relief=tk.FLAT,  # 扁平化边框
            borderwidth=0  # 无边框
        )
        
        # 滚动条
        scrollbar2 = ttk_bs.Scrollbar(result_frame, orient=VERTICAL)
        self.result_text.config(yscrollcommand=scrollbar2.set)
        scrollbar2.config(command=self.result_text.yview)
        
        self.result_text.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar2.pack(side=RIGHT, fill=Y)
        
    def create_control_section(self):
        """创建控制区域"""
        control_frame = ttk_bs.LabelFrame(
            self.main_frame,
            text="🎛️ 控制面板",
            padding=15,
            bootstyle=SUCCESS
        )
        control_frame.pack(fill=X, pady=(20, 0))
        
        # 左侧：主要操作按钮
        left_controls = ttk_bs.Frame(control_frame)
        left_controls.pack(side=LEFT, fill=X, expand=True)
        
        button_frame = ttk_bs.Frame(left_controls)
        button_frame.pack(anchor=W)
        
        # 统计按钮
        self.analyze_btn = ttk_bs.Button(
            button_frame,
            text="📈 开始统计",
            command=self.analyze_text,
            bootstyle=(SUCCESS, "outline"),
            width=15
        )
        self.analyze_btn.pack(side=LEFT, padx=(0, 10))
        
        # 保存按钮
        save_btn = ttk_bs.Button(
            button_frame,
            text="💾 保存结果",
            command=self.save_file,
            bootstyle=(INFO, "outline"),
            width=15
        )
        save_btn.pack(side=LEFT, padx=(0, 10))
        
        # 退出按钮
        exit_btn = ttk_bs.Button(
            button_frame,
            text="❌ 退出",
            command=self.window.destroy,
            bootstyle=(DANGER, "outline"),
            width=15
        )
        exit_btn.pack(side=LEFT, padx=(0, 10))
        
        # 右侧：统计信息
        right_controls = ttk_bs.LabelFrame(
            control_frame,
            text="📋 统计信息",
            padding=10,
            bootstyle=INFO
        )
        right_controls.pack(side=RIGHT, padx=(20, 0))
        
        self.stats_labels = {}
        stats_items = [
            ('总字符数', 'total_chars'),
            ('藏文音节', 'tibetan_count'),
            ('处理时间', 'process_time'),
            ('当前状态', 'current_status')
        ]
        
        for i, (label, key) in enumerate(stats_items):
            row_frame = ttk_bs.Frame(right_controls)
            row_frame.pack(fill=X, pady=2)
            
            ttk_bs.Label(
                row_frame,
                text=f"{label}:",
                font=('Microsoft YaHei UI', 10)
            ).pack(side=LEFT)
            
            self.stats_labels[key] = ttk_bs.Label(
                row_frame,
                text="0" if key != 'current_status' else "就绪",
                font=('Microsoft YaHei UI', 10, 'bold'),
                bootstyle=PRIMARY
            )
            self.stats_labels[key].pack(side=RIGHT)
        
    def create_progress_section(self):
        """创建进度条区域"""
        progress_frame = ttk_bs.LabelFrame(
            self.main_frame,
            text="📊 处理进度",
            padding=15,
            bootstyle=WARNING
        )
        progress_frame.pack(fill=X, pady=(20, 0))
        
        # 进度条容器（确保可见）
        progress_container = ttk_bs.Frame(progress_frame, height=40)
        progress_container.pack(fill=X, pady=(5, 10))
        progress_container.pack_propagate(False)  # 防止子组件影响容器大小
        
        # 进度条
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk_bs.Progressbar(
            progress_container,
            variable=self.progress_var,
            bootstyle=(SUCCESS, "striped"),  # 条纹效果更美观
            mode='determinate'
        )
        self.progress_bar.pack(fill=BOTH, expand=True)
        
        # 进度标签
        self.progress_label = ttk_bs.Label(
            progress_frame,
            text="等待开始...",
            font=('Microsoft YaHei UI', 10, 'bold'),
            bootstyle=INFO
        )
        self.progress_label.pack(pady=(0, 5))
        
    def create_status_bar(self):
        """创建状态栏"""
        self.status_frame = ttk_bs.Frame(self.main_frame)
        self.status_frame.pack(fill=X, pady=(10, 0))
        
        # 状态标签
        self.status_label = ttk_bs.Label(
            self.status_frame,
            text="就绪 | 请选择要分析的藏文文件",
            font=('Microsoft YaHei UI', 9),
            bootstyle=SECONDARY
        )
        self.status_label.pack(side=LEFT)
        
        # 版本信息
        version_label = ttk_bs.Label(
            self.status_frame,
            text="v1.0 | 基于18785构件的动态统计",
            font=('Microsoft YaHei UI', 9),
            bootstyle=INFO
        )
        version_label.pack(side=RIGHT)

    def update_progress(self, current, total, progress):
        """更新进度条和标签"""
        self.progress_var.set(current)
        self.progress_label.config(text=f"处理进度: {progress:.1f}% ({current}/{total})")
        # 强制更新UI
        self.progress_bar.update()
        self.progress_label.update()
        self.window.update_idletasks()

    def analyze_text(self):
        """分析藏文构件"""
        if not self.essay:
            messagebox.showwarning('警告', '请先选择文件！')
            return
        
        # 更新状态
        self.update_status("正在分析藏文构件...")
        self.stats_labels['current_status'].config(text="分析中...")
        self.analyze_btn.config(state='disabled')
        
        # 设置进度条
        total_chars = len(self.essay)
        self.progress_var.set(0)
        self.progress_bar.config(maximum=total_chars)
        
        # 确保进度条可见
        self.progress_bar.update()
        self.window.update_idletasks()
        
        # 清空结果显示
        self.result_text.delete('1.0', 'end')
        
        # 执行分析
        process_time, total_chars, tib_count = self.analyzer.analyze_text(
            self.essay, 
            update_callback=self.update_progress
        )
        
        # 显示结果
        self.display_results(process_time, total_chars, tib_count)
        
        # 更新状态
        self.progress_var.set(total_chars)  # 设置为最大值
        self.progress_label.config(text="分析完成！")
        self.analyze_btn.config(state='normal')
        self.stats_labels['current_status'].config(text="完成")
        self.stats_labels['total_chars'].config(text=f"{total_chars:,}")
        self.stats_labels['tibetan_count'].config(text=f"{tib_count:,}")
        self.stats_labels['process_time'].config(text=f"{process_time:.3f}s")
        self.update_status(f"分析完成 | 处理了 {tib_count} 个藏文音节")

    def display_results(self, process_time, total_chars, tib_count):
        """显示统计结果"""
        # 获取统计结果
        results = self.analyzer.get_statistics_results()
        
        # 格式化并显示结果
        formatted_results = format_results(results, process_time, total_chars, tib_count)
        self.result_text.insert('1.0', formatted_results)

    def open_file(self):
        """打开文件或文件夹"""
        self.text_display.delete('1.0', 'end')
        
        # 询问用户选择文件还是文件夹
        choice = messagebox.askyesnocancel(
            '选择模式',
            '选择处理模式：\n\n是(Yes) - 选择多个文件\n否(No) - 选择文件夹\n取消 - 退出选择'
        )
        
        if choice is None:  # 用户点击取消
            return
        elif choice:  # 用户选择文件模式
            self.select_files()
        else:  # 用户选择文件夹模式
            self.select_folder()
    
    def select_files(self):
        """选择多个文件"""
        files = filedialog.askopenfilenames(
            title='选择藏文文件',
            initialdir=os.path.expanduser('./'),
            filetypes=[
                ('文本文件', '*.txt'),
                ('所有文件', '*.*')
            ]
        )
        
        if files:
            self.load_files(files)
    
    def select_folder(self):
        """选择文件夹"""
        folder_path = filedialog.askdirectory(
            title='选择包含藏文文件的文件夹',
            initialdir=os.path.expanduser('./')
        )
        
        if not folder_path:
            return
        
        # 搜索文件夹中的所有文本文件
        txt_files = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith(('.txt', '.text')):
                    txt_files.append(os.path.join(root, file))
        
        if not txt_files:
            messagebox.showwarning('警告', f'在文件夹 "{folder_path}" 中未找到任何文本文件！')
            return
        
        # 询问用户是否处理所有找到的文件
        result = messagebox.askyesno(
            '确认处理',
            f'在文件夹中找到 {len(txt_files)} 个文本文件。\n\n是否处理所有这些文件？'
        )
        if result:
            self.load_files(txt_files)
    
    def load_files(self, files):
        """加载文件列表"""
        if not files:
            return
            
        self.essay = ''
        file_count = 0
        total_size = 0
        failed_files = []
        
        # 显示加载进度
        self.update_status("正在加载文件...")
        self.progress_var.set(0)
        self.progress_bar.config(maximum=len(files))
        self.progress_label.config(text="正在加载文件...")
        
        for i, file_path in enumerate(files):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # 去除换行符和空格，保持原有逻辑
                    content = ''.join(content.strip('\n').strip().split())
                    self.essay += content
                    file_count += 1
                    total_size += len(content)
                
                # 更新进度
                self.progress_var.set(i + 1)
                self.progress_label.config(text=f"已加载 {i+1}/{len(files)} 个文件")
                # 强制更新UI
                self.progress_bar.update()
                self.progress_label.update()
                self.window.update_idletasks()
                    
            except Exception as e:
                failed_files.append((file_path, str(e)))
                continue
        
        # 重置进度条
        self.progress_var.set(0)
        
        if file_count > 0:
            # 更新文件路径显示
            if file_count == 1:
                self.file_path_var.set(files[0])
            else:
                self.file_path_var.set(f"已选择 {file_count} 个文件")
            
            # 更新文件信息
            self.file_info_label.config(
                text=f"{file_count} 个文件 | {total_size:,} 字符"
            )
            
            # 显示加载结果
            result_info = f"文件加载完成\n{'='*50}\n"
            result_info += f"成功加载: {file_count} 个文件\n"
            result_info += f"总字符数: {total_size:,}\n"
            
            if failed_files:
                result_info += f"加载失败: {len(failed_files)} 个文件\n\n"
                result_info += "失败文件列表:\n"
                for file_path, error in failed_files:
                    result_info += f"- {os.path.basename(file_path)}: {error}\n"
                result_info += "\n"
            
            # 显示文件预览（如果不太大）
            if len(self.essay) < 12000:
                result_info += "文件内容预览:\n" + "-"*30 + "\n"
                result_info += self.essay[:5000]
                if len(self.essay) > 5000:
                    result_info += "\n\n... (内容过长，已截断)\n"
            else:
                result_info += "文本已加载，由于文本数量过多，暂不显示在组件内\n"
            
            result_info += "\n点击'开始统计'按钮进行构件分析"
            
            self.text_display.insert('1.0', result_info)
            self.update_status(f"已加载 {file_count} 个文件，共 {total_size:,} 个字符")
            
            # 如果有失败的文件，显示警告
            if failed_files:
                messagebox.showwarning(
                    '部分文件加载失败',
                    f'成功加载 {file_count} 个文件\n失败 {len(failed_files)} 个文件\n\n详细信息请查看预览区域'
                )
        else:
            self.update_status("所有文件加载失败")
            messagebox.showerror('错误', '所有文件都加载失败！请检查文件格式和编码。')

    def save_file(self):
        """保存结果"""
        content = self.result_text.get('1.0', 'end-1c')
        if not content.strip():
            messagebox.showwarning('警告', '没有可保存的内容！')
            return
            
        file_path = filedialog.asksaveasfilename(
            title='保存统计结果',
            defaultextension='.txt',
            filetypes=[
                ('文本文件', '*.txt'),
                ('所有文件', '*.*')
            ]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                messagebox.showinfo('成功', '文件保存成功！')
                self.update_status(f"结果已保存到: {file_path}")
            except Exception as e:
                messagebox.showerror('错误', f'保存失败: {str(e)}')

    def clear_data(self):
        """清空数据"""
        self.essay = ''
        self.file_path_var.set('')
        self.file_info_label.config(text="未选择文件")
        self.text_display.delete('1.0', 'end')
        self.result_text.delete('1.0', 'end')
        self.progress_var.set(0)
        self.progress_label.config(text="等待开始...")
        
        # 重置统计信息
        for key, label in self.stats_labels.items():
            if key == 'current_status':
                label.config(text="就绪")
            else:
                label.config(text="0")
        
        # 重置计数器
        reset_counters()
        
        self.update_status("数据已清空")

    def change_theme(self, event=None):
        """切换主题"""
        new_theme = self.theme_var.get()
        self.style.theme_use(new_theme)
        self.update_status(f"已切换到 {new_theme} 主题")

    def update_status(self, message):
        """更新状态栏"""
        self.status_label.config(text=message)
        self.window.update()

    def run(self):
        """运行应用程序"""
        self.window.mainloop()