# -*- coding: UTF-8 -*-
# 创建者：Pemawangchuk
# 版本：1.0
# 日期：2025-04-06
# 描述：多文本藏文音节统计
'''
MultiTextTibetanStats.py - 多文本藏文音节统计
This program is a multi-text tibetan syllable statistics program.
'''
import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext, Frame
import tkinter.font as tkFont
import os
import ttkbootstrap as ttk_bs
from ttkbootstrap import Style
from ttkbootstrap.constants import *

essay = '' # 存储所有文本
words_count = [[] for i in range(18785)] # 散列表

# 给每个藏文构字字符初始化一个值，作为Hash计算中的一个变量
id_m = {
    'ཀ': 1, 'ཁ': 2, 'ག': 3, 'གྷ': 4, 'ང': 5, 'ཅ': 6, 'ཆ': 7, 'ཇ': 8, 'ཉ': 10, 'ཊ': 11, 'ཋ': 12, 'ཌ': 13,
    'ཌྷ': 14, 'ཎ': 15, 'ཏ': 16, 'ཐ': 17, 'ད': 18, 'དྷ': 19, 'ན': 20, 'པ': 21, 'ཕ': 22, 'བ': 23, 'བྷ': 24, 'མ': 25,
    'ཙ': 26, 'ཚ': 27, 'ཛ': 28, 'ཛྷ': 29, 'ཝ': 30, 'ཞ': 31, 'ཟ': 32, 'འ': 33, 'ཡ': 34, 'ར': 35, 'ལ': 36, 'ཤ': 37,
    'ཥ': 38, 'ས': 39, 'ཧ': 40, 'ཨ': 41, 'ཀྵ': 42, 'ཪ': 43, 'ཫ': 44, 'ཬ': 45, 'ཱ': 50, 'ི': 51, 'ཱི': 52, 'ུ': 53,
    'ཱུ': 54, 'ྲྀ': 55, 'ཷ': 56, 'ླྀ': 57, 'ཹ': 58, 'ེ': 59, 'ཻ': 60, 'ོ': 61, 'ཽ': 62, 'ཾ': 63, 'ཿ': 64, 'ྀ': 65, 'ཱྀ': 66,
    'ྂ': 67, 'ྃ': 68, '྄': 69, '྅': 70, '྆': 71, '྇': 72, 'ྈ': 73, 'ྉ': 74, 'ྊ': 75, 'ྋ': 76, 'ྌ': 77, 'ྍ': 78,
    'ྎ': 79, 'ྏ': 80, 'ྐ': 81, 'ྑ': 82, 'ྒ': 83, 'ྒྷ': 84, 'ྔ': 85, 'ྕ': 86, 'ྖ': 87, 'ྗ': 88, 'ྙ': 90, 'ྚ': 91, 'ྛ': 92,
    'ྜ': 93, 'ྜྷ': 94, 'ྞ': 95, 'ྟ': 96, 'ྠ': 97, 'ྡ': 98, 'ྡྷ': 99, 'ྣ': 100, 'ྤ': 101, 'ྥ': 102, 'ྦ': 103, 'ྦྷ': 104,
    'ྨ': 105, 'ྩ': 106, 'ྪ': 107, 'ྫ': 108, 'ྫྷ': 109, 'ྭ': 110, 'ྮ': 111, 'ྯ': 112, 'ྰ': 113, 'ྱ': 114, 'ྲ': 115,
    'ླ': 116, 'ྴ': 117, 'ྵ': 118, 'ྶ': 119, 'ྷ': 120, 'ྸ': 121, 'ྐྵ': 122, 'ྺ': 123, 'ྻ': 124
}

# 分隔符
split_char = ['ༀ', '༁', '༂', '༃', '༄', '༆', '༇', '༈', '༉', '༊',
          '་', '༌', '།', '༎', '༏', '༐', '༑', '༒', '༓', '༔', '༕',
          '༖', '༗', '༘', '༙', '༚', '༛', '༜', '༝', '༞', '༟',
          '༠', '༡', '༢', '༣', '༤', '༥', '༦', '༧', '༨', '༩', '༪',
          '༫', '༬', '༭', '༮', '༯', '༰', '༱', '༲', '༳', '༴', '༵',
          '༶', '༷', '༸', '༺', '༻', '༼', '༽', '༾', '༿', '྾', '྿',
          '࿀', '࿁', '࿂', '࿃', '࿄', '࿅', '࿆', '࿇', '࿈', '࿉', '࿊',
          '࿋', '࿌', '࿎', '࿏', '࿐', '࿑', '࿒', '࿓', '࿔', '࿕', '࿖',
          '࿗', '࿘', '࿙', '࿚']

class TibetanSyllableAnalyzer:
    """藏文音节统计分析器"""
    
    def __init__(self):
        self.essay = ''
        self.words_count = [[] for i in range(18785)]
        self.setup_gui()
        
    def setup_gui(self):
        """设置GUI界面"""
        # 使用现代主题
        self.style = Style(theme='superhero')  # 深色主题
        self.window = self.style.master
        
        # 窗口基本设置
        self.window.title('🏔️ 多文本藏文音节统计分析器')
        self.window.geometry('1200x800+300+100')
        self.window.minsize(1000, 700)
        
        # 创建主容器
        self.create_main_container()
        
        # 创建各个组件
        self.create_header()
        self.create_file_section()
        self.create_results_section()
        self.create_control_section()
        self.create_status_bar()
        
    def create_main_container(self):
        """创建主容器"""
        self.main_frame = ttk_bs.Frame(self.window, padding=20)
        self.main_frame.pack(fill=BOTH, expand=True)
        
    def create_header(self):
        """创建标题区域"""
        header_frame = ttk_bs.Frame(self.main_frame)
        header_frame.pack(fill=X, pady=(0, 20))
        
        # 主标题
        title_label = ttk_bs.Label(
            header_frame,
            text="多文本藏文音节统计分析器",
            font=('Microsoft YaHei UI', 24, 'bold'),
            bootstyle=PRIMARY
        )
        title_label.pack(side=LEFT)
        
        # 副标题
        subtitle_label = ttk_bs.Label(
            header_frame,
            text="Multi-Text Tibetan Syllable Analyzer",
            font=('Arial', 12),
            bootstyle=SECONDARY
        )
        subtitle_label.pack(side=LEFT, padx=(20, 0), pady=(5, 0))
        
        # 主题切换
        theme_frame = ttk_bs.Frame(header_frame)
        theme_frame.pack(side=RIGHT)
        
        ttk_bs.Label(theme_frame, text="主题:", font=('Microsoft YaHei UI', 10)).pack(side=LEFT, padx=(0, 5))
        
        self.theme_var = tk.StringVar(value='superhero')
        theme_combo = ttk_bs.Combobox(
            theme_frame,
            textvariable=self.theme_var,
            values=['superhero', 'darkly', 'cosmo', 'flatly', 'litera', 'cyborg'],
            width=10,
            state='readonly'
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
            text="📂 选择文件",
            command=self.open_file,
            bootstyle=SUCCESS,
            width=15
        )
        select_btn.pack(side=LEFT, padx=(0, 10))
        
        # 清空按钮
        clear_btn = ttk_bs.Button(
            button_frame,
            text="🗑️ 清空",
            command=self.clear_data,
            bootstyle=WARNING,
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
        
    def create_results_section(self):
        """创建结果显示区域"""
        results_frame = ttk_bs.Frame(self.main_frame)
        results_frame.pack(fill=BOTH, expand=True)
        
        # 左侧：统计结果
        left_frame = ttk_bs.LabelFrame(
            results_frame,
            text="📊 统计结果",
            padding=10,
            bootstyle=PRIMARY
        )
        left_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 10))
        
        # 创建带滚动条的文本框
        text_frame = ttk_bs.Frame(left_frame)
        text_frame.pack(fill=BOTH, expand=True)
        
        self.result_text = tk.Text(
            text_frame,
            font=('Consolas', 12),
            wrap=tk.WORD,
            padx=10,
            pady=10
        )
        
        # 滚动条
        scrollbar = ttk_bs.Scrollbar(text_frame, orient=VERTICAL)
        self.result_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.result_text.yview)
        
        self.result_text.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        # 右侧：控制面板
        right_frame = ttk_bs.LabelFrame(
            results_frame,
            text="🎛️ 控制面板",
            padding=15,
            bootstyle=SUCCESS
        )
        right_frame.pack(side=RIGHT, fill=Y)
        
        # 统计按钮
        self.analyze_btn = ttk_bs.Button(
            right_frame,
            text="📈 开始统计",
            command=self.count_tibetan,
            bootstyle=SUCCESS,
            width=20
        )
        self.analyze_btn.pack(pady=(0, 15))
        
        # 进度条
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk_bs.Progressbar(
            right_frame,
            variable=self.progress_var,
            bootstyle=INFO,
            length=200
        )
        self.progress_bar.pack(pady=(0, 15))
        
        # 统计信息
        stats_frame = ttk_bs.LabelFrame(
            right_frame,
            text="📋 统计信息",
            padding=10,
            bootstyle=INFO
        )
        stats_frame.pack(fill=X, pady=(0, 15))
        
        self.stats_labels = {}
        stats_items = [
            ('总字符数', 'total_chars'),
            ('音节数量', 'syllable_count'),
            ('唯一音节', 'unique_syllables'),
            ('处理时间', 'process_time')
        ]
        
        for i, (label, key) in enumerate(stats_items):
            ttk_bs.Label(
                stats_frame,
                text=f"{label}:",
                font=('Microsoft YaHei UI', 10)
            ).grid(row=i, column=0, sticky=W, pady=2)
            
            self.stats_labels[key] = ttk_bs.Label(
                stats_frame,
                text="0",
                font=('Microsoft YaHei UI', 10, 'bold'),
                bootstyle=PRIMARY
            )
            self.stats_labels[key].grid(row=i, column=1, sticky=E, pady=2, padx=(10, 0))
        
        # 保存按钮
        save_btn = ttk_bs.Button(
            right_frame,
            text="💾 保存结果",
            command=self.save_file,
            bootstyle=INFO,
            width=20
        )
        save_btn.pack(pady=(0, 15))
        
        # 退出按钮
        exit_btn = ttk_bs.Button(
            right_frame,
            text="❌ 退出",
            command=self.window.destroy,
            bootstyle=DANGER,
            width=20
        )
        exit_btn.pack()
        
    def create_control_section(self):
        """创建控制区域"""
        pass  # 已在results_section中创建
        
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
            text="v1.0 | 基于哈希表的音节统计",
            font=('Microsoft YaHei UI', 9),
            bootstyle=INFO
        )
        version_label.pack(side=RIGHT)

    def Insert_elem(self, tibetan, id):
        """插入元素到散列表"""
        fin = False
        for word in self.words_count[id]:
            if word[0] == tibetan:
                word[1] += 1
                fin = True
                break
        if not fin:
            self.words_count[id].append([tibetan, 1])

    def count_tibetan(self):
        """统计藏文音节"""
        if not self.essay:
            messagebox.showwarning('警告', '请先选择文件！')
            return
            
        # 清空之前的结果
        self.words_count = [[] for i in range(18785)]
        self.result_text.delete('1.0', 'end')
        
        # 开始计时
        time_start = time.time()
        
        # 更新状态
        self.update_status("正在分析藏文音节...")
        self.analyze_btn.config(state='disabled')
        
        # 处理文本
        s = ''
        total_chars = len(self.essay)
        processed_chars = 0
        
        for i, ch in enumerate(self.essay):
            # 更新进度
            if i % 1000 == 0:
                progress = (i / total_chars) * 100
                self.progress_var.set(progress)
                self.window.update()
            
            # 如果是藏字构字符，添加进s的尾部
            if ('\u0F00' <= ch <= '\u0FDA' and ch not in split_char):
                s += ch
                continue
            # 当前ch为非藏字构字字符
            else:
                if s != '':  # s不为空，存储的就是一个藏文音节
                    # 计算s的Hash值
                    id = 0
                    for pos, char in enumerate(s):
                        if char in id_m:
                            id += (id_m[char]) ** 3 - pos ** 2
                    id = id % 18785
                    # 将s插入散列表
                    self.Insert_elem(s, id)
                    s = ''
                processed_chars += 1
        
        # 处理最后一个音节
        if s != '':
            id = 0
            for pos, char in enumerate(s):
                if char in id_m:
                    id += (id_m[char]) ** 3 - pos ** 2
            id = id % 18785
            self.Insert_elem(s, id)
        
        # 完成处理
        time_end = time.time()
        process_time = time_end - time_start
        
        # 统计结果
        total_syllables = 0
        unique_syllables = 0
        
        # 收集所有音节并按频率排序
        all_syllables = []
        for words in self.words_count:
            for word in words:
                all_syllables.append(word)
                total_syllables += word[1]
                unique_syllables += 1
        
        # 按频率降序排序
        all_syllables.sort(key=lambda x: x[1], reverse=True)
        
        # 显示结果
        self.result_text.insert('1.0', f"{'='*60}\n")
        self.result_text.insert('end', f"藏文音节统计分析结果\n")
        self.result_text.insert('end', f"{'='*60}\n\n")
        self.result_text.insert('end', f"处理时间: {process_time:.3f} 秒\n")
        self.result_text.insert('end', f"总字符数: {total_chars:,}\n")
        self.result_text.insert('end', f"音节总数: {total_syllables:,}\n")
        self.result_text.insert('end', f"唯一音节: {unique_syllables:,}\n\n")
        self.result_text.insert('end', f"{'音节':<20} {'频次':<10} {'占比':<10}\n")
        self.result_text.insert('end', f"{'-'*40}\n")
        
        for word in all_syllables:
            percentage = (word[1] / total_syllables) * 100
            self.result_text.insert('end', f"{word[0]:<20} {word[1]:<10} {percentage:.2f}%\n")
        
        # 更新统计信息
        self.stats_labels['total_chars'].config(text=f"{total_chars:,}")
        self.stats_labels['syllable_count'].config(text=f"{total_syllables:,}")
        self.stats_labels['unique_syllables'].config(text=f"{unique_syllables:,}")
        self.stats_labels['process_time'].config(text=f"{process_time:.3f}s")
        
        # 重置状态
        self.progress_var.set(100)
        self.analyze_btn.config(state='normal')
        self.update_status(f"分析完成 | 找到 {unique_syllables} 个唯一音节")

    def open_file(self):
        """打开文件或文件夹"""
        self.result_text.delete('1.0', 'end')
        
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
        
        for i, file_path in enumerate(files):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.essay += content + '\n'
                    file_count += 1
                    total_size += len(content)
                
                # 更新进度
                progress = ((i + 1) / len(files)) * 100
                self.progress_var.set(progress)
                self.window.update()
                    
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
            if len(self.essay) < 10000:
                result_info += "文件内容预览:\n" + "-"*30 + "\n"
                result_info += self.essay[:3000]
                if len(self.essay) > 3000:
                    result_info += "\n\n... (内容过长，已截断)\n"
            else:
                result_info += "由于内容较多，暂不显示预览\n"
            
            result_info += "\n点击'开始统计'按钮进行音节分析"
            
            self.result_text.insert('1.0', result_info)
            self.update_status(f"已加载 {file_count} 个文件，共 {total_size:,} 个字符")
            
            # 如果有失败的文件，显示警告
            if failed_files:
                messagebox.showwarning(
                    '部分文件加载失败',
                    f'成功加载 {file_count} 个文件\n失败 {len(failed_files)} 个文件\n\n详细信息请查看结果区域'
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
        self.words_count = [[] for i in range(18785)]
        self.file_path_var.set('')
        self.file_info_label.config(text="未选择文件")
        self.result_text.delete('1.0', 'end')
        self.progress_var.set(0)
        
        # 重置统计信息
        for label in self.stats_labels.values():
            label.config(text="0")
        
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

# 保持向后兼容的全局函数
def Insert_elem(Tibetan, id):
    fin = False
    for word in words_count[id]:
        if (word[0] == Tibetan):
            word[1] += 1
            fin = True
    if (fin == False): 
        words_count[id].append([Tibetan, 1])

def Count_Tibetan():
    global essay
    timeA = time.time()
    text1.delete('1.0', 'end')
    s = ''
    for i, ch in enumerate(essay):
        if ('\u0F00' <= ch <= '\u0FDA' and ch not in split_char):
            s += ch
            continue
        else:
            if(s!=''):
                id = 0
                for pos, char in enumerate(s):
                    id += (id_m[char]) ** 3 - pos ** 2
                id = id % 18785
                Insert_elem(s, id)
                s = ''

    timeB = time.time()
    text1.insert('insert', f'用时：{timeB - timeA}秒\n')
    for words in words_count:
        for word in words:
            text1.insert('insert', f'{word[0]} : {word[1]:>8}\n')

def open_file():
    global essay
    window.update()
    text1.delete('1.0', 'end')
    files = filedialog.askopenfilename(title=u'选择文件夹', initialdir=(
        os.path.expanduser('./')),
                                       multiple=True)
    text.insert('insert', f'文件地址：{files}')

    for file_path in files:
        if file_path is not None:
            try:
                with open(file=file_path, mode='r', encoding='utf-8') as f:
                    essay = f.read()
                    if (len(essay) < 12000):
                        text1.insert('insert', f'{essay}\n')
                    else:
                        text1.insert('insert', '文本已加载，由于文本数量过多，暂不显示在组件内')

            except Exception as e:
                print(str(e))
                messagebox.askokcancel(title='警告', message='文件加载异常，请重新加载文件')
                text1.insert('insert', f'加载文件异常：{str(e)}，请重新加载文件')

def save_file():
    global file_path
    text_str = text1.get('2.0', 'end')
    file_path = filedialog.asksaveasfilename(title=u'保存文件')
    print('保存文件：', file_path)
    if file_path is not None:
        with open(file=file_path, mode='w', encoding='utf-8') as f:
            f.write(text_str)
        result = messagebox.askokcancel(title='提示', message='文件已保存')
        if (result):
            print('保存完成')
        else:
            print('保存失败')

if __name__ == '__main__':
    # 使用新的现代化界面
    app = TibetanSyllableAnalyzer()
    app.run()