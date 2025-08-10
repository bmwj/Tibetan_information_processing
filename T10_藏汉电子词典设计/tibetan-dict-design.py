# -*- coding: UTF-8 -*-
# 创建者：Pemawangchuk
# 版本：1.0
# 日期：2025-04-06
# 描述：藏汉电子词典设计
"""
tibetan_dict_design.py - 藏汉电子词典设计
This script designs a Tibetan-Chinese electronic dictionary.
"""
import tkinter as tk
from tkinter import *
import tkinter.font as tkFont
from tkinter import messagebox, ttk
import ttkbootstrap as ttk_bs
from ttkbootstrap import Style
from ttkbootstrap.constants import *
block_di = {
    'ཀ': 0, 'ཁ': 1, 'ག': 2, 'ང': 3, 'ཅ': 4, 'ཆ': 5, 'ཇ': 6, 'ཉ': 7, 'ཏ': 8, 'ཐ': 9, 'ད': 10, 'ན': 11,
    'པ': 12, 'ཕ': 13, 'བ': 14, 'མ': 15, 'ཙ': 16, 'ཚ': 17, 'ཛ': 18, 'ཝ': 19, 'ཞ': 20, 'ཟ': 21, 'འ': 22,
    'ཡ': 23, 'ར': 24, 'ལ': 25, 'ཤ': 26, 'ས': 27, 'ཧ': 28, 'ཨ': 29, 'ཊ': 30
}

class Create_blocks:
    """藏文词典块处理类"""
    
    def __init__(self):
        pass
    
    def int2uni(self, num):
        """将整数转换为Unicode字符"""
        return chr(num)
    
    def int2uni(self, num):
        """将整数转换为Unicode字符"""
        return chr(num)
    
    def Create(self, filename, dictionary_info):
        """
        从文件创建词典块
        :param filename: 词典文件名
        :param dictionary_info: 存储词典信息的列表
        """
        try:
            # 尝试多种编码方式读取文件
            encodings = ['utf-16', 'utf-8', 'utf-16-le', 'utf-16-be', 'gbk']
            lines = []
            
            for encoding in encodings:
                try:
                    with open(filename, 'r', encoding=encoding) as file:
                        lines = file.readlines()
                        print(f"成功使用 {encoding} 编码读取文件")
                        break
                except (UnicodeDecodeError, UnicodeError):
                    continue
            
            if not lines:
                raise FileNotFoundError("无法以任何编码方式读取文件")
                
            # 处理读取的行
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                    
                # 分割藏文词和中文释义
                parts = line.split('\t')
                if len(parts) >= 2:
                    tibetan_word = parts[0].strip()
                    chinese_meaning = parts[1].strip()
                    
                    if tibetan_word:
                        first_char = tibetan_word[0]
                        
                        # 处理特殊字符范围
                        if '\u0F90' <= first_char <= '\u0FB8':
                            first_char = self.int2uni(ord(first_char) - 80)
                        
                        if first_char in block_di:
                            block_id = block_di[first_char]
                            dictionary_info[block_id].append([tibetan_word, chinese_meaning])
                        
        except FileNotFoundError:
            print(f"词典文件 '{filename}' 未找到，使用示例数据")
            # 创建更丰富的示例数据
            sample_data = [
                ['ཀ་བ', '柱子；支柱'],
                ['ཀ་ལེན', '承担；负责'],
                ['ཁ་བ', '雪；雪花'],
                ['ཁ་སང', '昨天'],
                ['ཁྱེད', '您；你们'],
                ['གཅིག', '一；一个'],
                ['གཉིས', '二；两个'],
                ['གསུམ', '三；三个'],
                ['ང་', '我'],
                ['ངེད', '我们'],
                ['ཅིག', '一个（量词）'],
                ['ཆུ', '水'],
                ['ཆུ་ཚོད', '时间；钟点'],
                ['ཇ', '茶'],
                ['ཇ་ཁང', '茶馆'],
                ['ཉི་མ', '太阳；日子'],
                ['ཉིན', '白天'],
                ['ཏ་ལ', '马'],
                ['ཏིང་འཛིན', '禅定'],
                ['ཐང་ཀ', '唐卡'],
                ['ཐུགས', '心；意'],
                ['དགེ་བ', '善；功德'],
                ['དཔེ་ཆ', '书；书籍'],
                ['ནམ་མཁའ', '天空'],
                ['ནང་པ', '佛教徒'],
                ['པད་མ', '莲花'],
                ['ཕ་མ', '父母'],
                ['བཀྲ་ཤིས', '吉祥'],
                ['བླ་མ', '上师；喇嘛'],
                ['མི', '人'],
                ['མེ', '火'],
                ['ཙན་དན', '檀香'],
                ['ཚ་བ', '热'],
                ['ཛམ་བུ', '赡部洲'],
                ['ཝ་ལེ', '好的'],
                ['ཞི་བ', '寂静；和平'],
                ['ཟས', '食物'],
                ['འཇིག་རྟེན', '世界'],
                ['ཡི་གེ', '文字；字母'],
                ['རི', '山'],
                ['རླུང', '风'],
                ['ལ་དྭགས', '拉达克'],
                ['ལྷ', '神；天'],
                ['ཤེས་རབ', '智慧'],
                ['སངས་རྒྱས', '佛陀'],
                ['སེམས', '心；意识'],
                ['ཧ་ལས', '惊讶'],
                ['ཨ་མ', '母亲'],
                ['ཨ་ཕ', '父亲']
            ]
            
            for tibetan_word, chinese_meaning in sample_data:
                if tibetan_word:
                    first_char = tibetan_word[0]
                    if first_char in block_di:
                        block_id = block_di[first_char]
                        dictionary_info[block_id].append([tibetan_word, chinese_meaning])
        
        except Exception as e:
            print(f"读取词典文件时发生错误: {e}")
            # 使用基本示例数据
            basic_data = [
                ['ཀ་བ', '柱子'],
                ['ཁ་བ', '雪'],
                ['གཅིག', '一'],
                ['ང་', '我'],
                ['ཆུ', '水']
            ]
            for tibetan_word, chinese_meaning in basic_data:
                if tibetan_word and tibetan_word[0] in block_di:
                    block_id = block_di[tibetan_word[0]]
                    dictionary_info[block_id].append([tibetan_word, chinese_meaning])

# ==================== 主应用程序类 ====================

class TibetanDictionaryApp:
    """藏汉电子词典主应用程序"""
    
    def __init__(self):
        # 初始化词典数据
        self.dictionary_info = [[] for i in range(31)]
        self.create_blocks = Create_blocks()
        self.create_blocks.Create('藏汉词典.txt', self.dictionary_info)
        
        # 创建GUI
        self.setup_gui()
        
    def setup_gui(self):
        """设置GUI界面"""
        # 使用现代主题
        self.style = Style(theme='superhero')  # 深色主题，也可以选择 'cosmo', 'flatly', 'darkly' 等
        self.window = self.style.master
        
        # 窗口基本设置
        self.window.title('🏔️ 藏汉电子词典')
        self.window.geometry('1000x700+400+200')
        self.window.minsize(800, 600)
        
        # 设置窗口图标（如果有的话）
        try:
            self.window.iconbitmap('icon.ico')
        except:
            pass
            
        # 创建主容器
        self.create_main_container()
        
        # 创建各个组件
        self.create_header()
        self.create_search_section()
        self.create_results_section()
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
            text="藏汉电子词典",
            font=('Microsoft YaHei UI', 24, 'bold'),
            bootstyle=PRIMARY
        )
        title_label.pack(side=LEFT)
        
        # 副标题
        subtitle_label = ttk_bs.Label(
            header_frame,
            text="Tibetan-Chinese Electronic Dictionary",
            font=('Arial', 12),
            bootstyle=SECONDARY
        )
        subtitle_label.pack(side=LEFT, padx=(20, 0), pady=(5, 0))
        
        # 主题切换按钮
        theme_frame = ttk_bs.Frame(header_frame)
        theme_frame.pack(side=RIGHT)
        
        ttk_bs.Label(theme_frame, text="主题:", font=('Microsoft YaHei UI', 10)).pack(side=LEFT, padx=(0, 5))
        
        self.theme_var = tk.StringVar(value='superhero')
        theme_combo = ttk_bs.Combobox(
            theme_frame,
            textvariable=self.theme_var,
            values=['superhero', 'darkly', 'cosmo', 'flatly', 'litera', 'cyborg', 'vapor'],
            width=10,
            state='readonly'
        )
        theme_combo.pack(side=LEFT)
        theme_combo.bind('<<ComboboxSelected>>', self.change_theme)
        
    def create_search_section(self):
        """创建搜索区域"""
        search_frame = ttk_bs.LabelFrame(
            self.main_frame,
            text="🔍 词汇查询",
            padding=15,
            bootstyle=INFO
        )
        search_frame.pack(fill=X, pady=(0, 20))
        
        # 搜索输入区域
        input_frame = ttk_bs.Frame(search_frame)
        input_frame.pack(fill=X, pady=(0, 10))
        
        # 输入提示
        ttk_bs.Label(
            input_frame,
            text="请输入藏文词汇:",
            font=('Microsoft YaHei UI', 12)
        ).pack(anchor=W, pady=(0, 5))
        
        # 搜索输入框和按钮的容器
        search_input_frame = ttk_bs.Frame(input_frame)
        search_input_frame.pack(fill=X)
        
        # 搜索输入框
        self.search_var = tk.StringVar()
        self.search_entry = ttk_bs.Entry(
            search_input_frame,
            textvariable=self.search_var,
            font=('Qomolangma-Dunhuang.ttf', 16),
            width=40
        )
        self.search_entry.pack(side=LEFT, fill=X, expand=True, padx=(0, 10))
        self.search_entry.bind('<Return>', lambda e: self.search_info())
        
        # 搜索按钮
        search_btn = ttk_bs.Button(
            search_input_frame,
            text="🔍 查找",
            command=self.search_info,
            bootstyle=SUCCESS,
            width=12
        )
        search_btn.pack(side=LEFT, padx=(0, 5))
        
        # 清空按钮
        clear_btn = ttk_bs.Button(
            search_input_frame,
            text="🗑️ 清空",
            command=self.clear_search,
            bootstyle=WARNING,
            width=12
        )
        clear_btn.pack(side=LEFT, padx=(0, 5))
        
        # 退出按钮
        exit_btn = ttk_bs.Button(
            search_input_frame,
            text="❌ 退出",
            command=self.window.destroy,
            bootstyle=DANGER,
            width=12
        )
        exit_btn.pack(side=LEFT)
        
    def create_results_section(self):
        """创建结果显示区域"""
        results_frame = ttk_bs.Frame(self.main_frame)
        results_frame.pack(fill=BOTH, expand=True)
        
        # 左侧：搜索结果列表
        left_frame = ttk_bs.LabelFrame(
            results_frame,
            text="📋 搜索结果",
            padding=10,
            bootstyle=PRIMARY
        )
        left_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 10))
        
        # 创建带滚动条的列表框
        list_frame = ttk_bs.Frame(left_frame)
        list_frame.pack(fill=BOTH, expand=True)
        
        self.results_listbox = tk.Listbox(
            list_frame,
            font=('Qomolangma-Dunhuang.ttf', 14),
            selectmode=SINGLE,
            activestyle='dotbox'
        )
        
        # 滚动条
        scrollbar_list = ttk_bs.Scrollbar(list_frame, orient=VERTICAL)
        self.results_listbox.config(yscrollcommand=scrollbar_list.set)
        scrollbar_list.config(command=self.results_listbox.yview)
        
        self.results_listbox.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar_list.pack(side=RIGHT, fill=Y)
        
        self.results_listbox.bind('<<ListboxSelect>>', self.display_info)
        
        # 右侧：详细信息显示
        right_frame = ttk_bs.LabelFrame(
            results_frame,
            text="📖 详细释义",
            padding=10,
            bootstyle=SUCCESS
        )
        right_frame.pack(side=RIGHT, fill=BOTH, expand=True)
        
        # 创建带滚动条的文本框
        text_frame = ttk_bs.Frame(right_frame)
        text_frame.pack(fill=BOTH, expand=True)
        
        self.detail_text = tk.Text(
            text_frame,
            font=('Qomolangma-Dunhuang.ttf', 14),
            wrap=WORD,
            state=DISABLED,
            padx=10,
            pady=10
        )
        
        # 滚动条
        scrollbar_text = ttk_bs.Scrollbar(text_frame, orient=VERTICAL)
        self.detail_text.config(yscrollcommand=scrollbar_text.set)
        scrollbar_text.config(command=self.detail_text.yview)
        
        self.detail_text.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar_text.pack(side=RIGHT, fill=Y)
        
    def create_status_bar(self):
        """创建状态栏"""
        self.status_frame = ttk_bs.Frame(self.main_frame)
        self.status_frame.pack(fill=X, pady=(10, 0))
        
        # 状态标签
        self.status_label = ttk_bs.Label(
            self.status_frame,
            text="就绪 | 词典已加载",
            font=('Microsoft YaHei UI', 9),
            bootstyle=SECONDARY
        )
        self.status_label.pack(side=LEFT)
        
        # 统计信息
        total_words = sum(len(block) for block in self.dictionary_info)
        stats_label = ttk_bs.Label(
            self.status_frame,
            text=f"总词条数: {total_words}",
            font=('Microsoft YaHei UI', 9),
            bootstyle=INFO
        )
        stats_label.pack(side=RIGHT)
        
    def search_info(self):
        """搜索功能"""
        self.results_listbox.delete(0, END)
        self.update_detail_text("")
        
        search_str = self.search_var.get().strip()
        if not search_str:
            self.update_status("请输入要查询的藏文词汇")
            return
            
        try:
            if search_str[0] not in block_di:
                messagebox.showwarning('警告', '输入的字符不是有效的藏文辅音字符，请重新输入')
                self.search_entry.focus()
                return
                
            block_id = block_di[search_str[0]]
        except Exception as e:
            messagebox.showerror('错误', f'输入信息有误：{str(e)}')
            self.search_entry.focus()
            return
        
        num = 0
        found = False
        
        for info in self.dictionary_info[block_id]:
            if info[0].find(search_str) == 0:  # 以搜索字符串开头
                self.results_listbox.insert(END, info[0])
                num += 1
                found = True
            if num >= 100:  # 最多显示20条数据
                break
                
        if found:
            self.update_status(f"找到 {num} 个匹配结果")
            # 自动选择第一个结果
            if self.results_listbox.size() > 0:
                self.results_listbox.selection_set(0)
                self.results_listbox.event_generate('<<ListboxSelect>>')
        else:
            self.update_status("未找到匹配的词条")
            self.update_detail_text("未查找到对应词条信息\n\n请检查输入的藏文词汇是否正确。")
            
    def display_info(self, event):
        """显示选中词条的详细信息"""
        try:
            selection = self.results_listbox.curselection()
            if not selection:
                return
                
            selected_word = self.results_listbox.get(selection[0])
            first_char = selected_word[0]
            
            # 处理特殊字符
            if '\u0F90' <= first_char <= '\u0FB8':
                first_char = self.create_blocks.int2uni(ord(first_char) - 80)
                
            # 查找详细信息
            for info in self.dictionary_info[block_di[first_char]]:
                if info[0] == selected_word:
                    detail_text = f"藏文: {info[0]}\n\n中文释义:\n{info[1]}"
                    self.update_detail_text(detail_text)
                    self.update_status(f"显示词条: {selected_word}")
                    break
        except Exception as e:
            self.update_status(f"显示错误: {str(e)}")
            
    def update_detail_text(self, text):
        """更新详细信息文本框"""
        self.detail_text.config(state=NORMAL)
        self.detail_text.delete('1.0', END)
        self.detail_text.insert('1.0', text)
        self.detail_text.config(state=DISABLED)
        
    def update_status(self, message):
        """更新状态栏"""
        self.status_label.config(text=message)
        
    def clear_search(self):
        """清空搜索"""
        self.search_var.set("")
        self.results_listbox.delete(0, END)
        self.update_detail_text("")
        self.update_status("已清空搜索结果")
        self.search_entry.focus()
        
    def change_theme(self, event=None):
        """切换主题"""
        new_theme = self.theme_var.get()
        self.style.theme_use(new_theme)
        self.update_status(f"已切换到 {new_theme} 主题")
        
    def run(self):
        """运行应用程序"""
        self.window.mainloop()

# ==================== 主程序入口 ====================

if __name__ == '__main__':
    app = TibetanDictionaryApp()
    app.run()