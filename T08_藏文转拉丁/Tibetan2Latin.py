# -*- coding: UTF-8 -*-
# 创建者：Pemawangchuk
# 版本：2.1
# 日期：2025-08-12
# 描述：藏文拉丁互转工具（优化版）

import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
import tkinter.font as tkFont
import os
import re
import sys
import ttkbootstrap as ttk
from PIL import Image, ImageTk
from Preprocessing import Preprocessing  # 假设已正确实现

# 添加公共模块路径
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'common'))

# 全局变量
essay = ''  # 源文本
target = ''  # 目标文本
la2Tibetan = {}  # 拉丁到藏文映射字典
tibetan2La = {}  # 藏文到拉丁映射字典
vowPos = {}  # 元音位置字典

# 黏着词后缀列表
adhering = ['འུའི', 'འི', 'འོ', 'འང']

# 元音列表
vowel = ['\u0F72', '\u0F74', '\u0F7A', '\u0F7C']
la_vowel = ['i', 'u', 'e', 'o', 'a']

# 结束符号
end = ['།', '༏', '༐', '༑']

# 分隔符
split_char = [
    'ༀ', '༁', '༂', '༃', '༄', '༆', '༇', '༈', '༉', '༊', '་', '༌',
    '༒', '༓', '༔', '༕', '༖', '༗', '༘', '༙', '༚', '༛', '༜', '༝', '༞',
    '༟', '༠', '༡', '༢', '༣', '༤', '༥', '༦', '༧', '༨', '༩', '༪',
    '༫', '༬', '༭', '༮', '༯', '༰', '༱', '༲', '༳', '༴', '༵', '༶', '༷', '༸',
    '༺', '༻', '༼', '༽', '༾', '༿', '྾', '྿', '࿀', '࿁', '࿂', '࿃', '࿄', '࿅',
    '࿆', '࿇', '࿈', '࿉', '࿊', '࿋', '࿌', '࿎', '࿏', '࿐', '࿑', '࿒', '࿓', '࿔',
    '\u0FD5', '\u0FD6', '\u0FD7', '\u0FD8', '࿙', '࿚', ' '
]

class TibetanLatinConverter:
    """藏文拉丁转换器核心类"""
    
    @staticmethod
    def tibetan_to_latin_traverse():
        """
        藏文转拉丁：
        1. 按分隔符分离藏文
        2. 查看是否是黏着词
           2.1 后缀是 ['འུའི', 'འི', 'འོ', 'འང'] 的分离后缀，拆成两个藏文音节，中间以 _ 相连
           2.2 不是黏着词，直接转为拉丁
        3. 先查元音表找元音位置
           3.1 找不到，说明传入的藏字有误（可能是没考虑到的黏着词，或者分隔有误），报异常
           3.2 隐式元音位置可能 > 传入的藏文长度，此时要判断一下，把隐式元音对应的符号 '.' 放在最后
        4. 查藏-拉表，从大字符串到小字符串查找
           4.1 查找到，查看当前生成的 Latin 与前一位生成的 Latin 是否能构成在表中的 Latin，如果构成需在中间加入 '-' 符号
           4.2 如果没查找到，可能是带圈辅音（下加字，再下加字）的编码问题，转为辅音对应的编码再查表
        5. 重复上述步骤直到结束
        """
        global target, essay
        essay = text1.get('1.0', 'end-1c')
        target = ''
        
        try:
            # 检查输入是否为空
            if not essay.strip():
                messagebox.showwarning("警告", "请先输入或加载藏文文本")
                return

            # 检查输入是否为藏文
            is_tibetan = any('\u0F00' <= char <= '\u0FFF' for char in essay)
            if not is_tibetan:
                messagebox.showwarning("输入错误", "源文本中未检测到藏文，无法进行藏文转拉丁操作。")
                return
                
            # 预处理文本
            essay = essay.replace('་', ' ')
            essay = essay.replace('༎', ' .. ')
            for E in end:
                essay = essay.replace(E, ' . ')
            
            s = ''
            for i, ch in enumerate(essay):
                # 如果是藏字且不是分隔符，与之前的字符构成字符串
                if '\u0F00' <= ch <= '\u0FDA' and ch not in split_char:
                    s += ch
                    continue
                # 藏字已构成，转写拉丁
                elif s != '':
                    # 当前字符不是藏文字符，但加入到目标文件中
                    target += ch
                    # 先判断是否是黏着词（如果后缀是 ['འུའི', 'འི', 'འོ', 'འང'] 的，拆开变为两个词）
                    # 查看是否在18785的表中，不在再判断后缀
                    if vowPos.get(s, -1) == -1:
                        for adhere in adhering:
                            if s.endswith(adhere):
                                # 找到拆分位置，分别转为 latin
                                sep = s.rfind(adhere)
                                TibetanLatinConverter.tibetan_to_latin(s[:sep])
                                target += '_'
                                TibetanLatinConverter.tibetan_to_latin(s[sep:])
                                target += ' '
                                break
                        else:
                            # 如果不是黏着词，尝试直接转换
                            try:
                                TibetanLatinConverter.tibetan_to_latin(s)
                                target += ' '
                            except Exception as e:
                                print(f"转换错误 '{s}': {str(e)}")
                                target += s + ' '
                    else:
                        try:
                            TibetanLatinConverter.tibetan_to_latin(s)
                            target += ' '
                        except Exception as e:
                            print(f"转换错误 '{s}': {str(e)}")
                            target += s + ' '
                    s = ''
                else:
                    target += ch
            
            # 处理最后一个音节
            if s:
                try:
                    TibetanLatinConverter.tibetan_to_latin(s)
                    target += ' '
                except Exception as e:
                    print(f"转换错误 '{s}': {str(e)}")
                    target += s + ' '
            
            text2.delete('1.0', 'end')
            text2.insert('insert', target)
            app.status_var.set("转换完成")
            
        except Exception as e:
            messagebox.showerror("错误", f"转换过程中出错: {str(e)}")
            app.status_var.set(f"转换失败: {str(e)}")

    @staticmethod
    def tibetan_to_latin(tibetan):
        """转换单个藏文音节为拉丁文"""
        global target
        
        # 先找到元音位置（之前已预处理）
        vowpos = vowPos.get(tibetan, False)

        # 如果在元的音位找不到元音，说明是隐式，在转换表中，我们新增了一个 '.' -> 'a' 的转换方式
        # 有可能隐式元音应该添加到最后，有可能需要添加在中间
        if vowpos is False:
            vowpos = 0  # 默认在第一个位置添加隐式元音
        
        if vowpos >= len(tibetan):
            tibetan += '*'
        elif tibetan[vowpos] not in vowel:
            tibetan = tibetan[:vowpos] + '*' + tibetan[vowpos:]

        begin = 0  # 控制每次匹配都是从当前未匹配的第一个字符开始
        while begin < len(tibetan):
            fin = False
            for key, value in tibetan2La.items():
                # 从左到右先匹配最大能够转写的字符串
                pos = tibetan.find(key, begin)
                if pos != -1 and tibetan[begin:begin+len(key)] == key:  # 如果找到，先转写，然后把下次查找的起始点设为当前点
                    # 有重复的例如 གཡ 和 གྱ ，都是 gy，后者区分为 g-y
                    if len(target) >= 1 and target[-1] + value in la2Tibetan:
                        target = target + '-' + value
                    else:
                        target += value
                    begin += len(key)
                    fin = True
                    break

            if fin is False and begin < len(tibetan) and '\u0F90' <= tibetan[begin] <= '\u0FBC':
                ch = chr(ord(tibetan[begin]) - 80)
                if ch in tibetan2La:
                    value = tibetan2La[ch]
                    if len(target) >= 1 and target[-1] + value in la2Tibetan:  # 有重复的例如 གཡ 和 གྱ ，都是 gy，后者区分为 g-y
                        target = target + '-' + value
                    else:
                        target += value
                    begin += 1
                    fin = True
            
            # 如果无法匹配，跳过当前字符
            if not fin:
                if begin < len(tibetan):
                    # 无法转换的字符，直接添加
                    target += tibetan[begin]
                begin += 1

    @staticmethod
    def latin_to_tibetan_traverse():
        """
        拉丁转藏文：
        1. 按照空格拆分 Latin，放入列表中
        2. 遍历列表中的每个 Latin
           2.1 将当前 Latin 以 '_' 、'-'对应 Latin字母进行分隔  ['ab_c-dif'] -> ['ab'、'c'、'dif']
           2.2 遍历当前 Latin 生成的列表，以元音分隔对每一个元素使用最大匹配算法转成藏文文本
        3. 对产生的藏文文本进行后处理（对应之前藏->拉的方式，将其中一些转换还原）
        """
        global target, essay
        essay = text1.get('1.0', 'end-1c')
        target = ''
        
        try:
            # 检查输入是否为空
            if not essay.strip():
                messagebox.showwarning("警告", "请先输入或加载拉丁文本")
                return

            # 检查输入是否为拉丁文
            is_latin = any('a' <= char.lower() <= 'z' for char in essay)
            if not is_latin:
                messagebox.showwarning("输入错误", "源文本中未检测到拉丁字母，无法进行拉丁转藏文操作。")
                return
                
            latin = essay.strip().split(' ')
            for la in latin:
                sec = re.split('[_ -]', la)
                for s in sec:
                    found_vowel = False
                    for vol in la_vowel:
                        pos = s.find(vol)
                        if pos != -1:
                            try:
                                TibetanLatinConverter.latin_to_tibetan(s[:pos])
                                if vol in la2Tibetan:
                                    target += la2Tibetan[vol]
                                TibetanLatinConverter.latin_to_tibetan(s[pos+1:])
                                found_vowel = True
                                break
                            except Exception as e:
                                print(f"转换错误 '{s}': {str(e)}")
                    
                    # 如果没有找到元音，尝试直接转换
                    if not found_vowel and s:
                        try:
                            TibetanLatinConverter.latin_to_tibetan(s)
                        except Exception as e:
                            print(f"转换错误 '{s}': {str(e)}")
                            target += s
                target += ' '

            # 后处理
            target = target.replace('*', '')  # 隐式元音转为空
            target = target.replace('.', '།')
            target = target.replace('  ', ' ')  # 在藏文转拉丁时，因为原本的文本就有空格，我们将分隔符又转为空格，所以会有多的空格被转为 '་'，我们先将多余的空格去除
            target = target.replace(' ', '་')
            target = target.replace('་།', '། ')  # 单垂符之前是单独作为 ' . ' 转换为拉丁的，但在藏文中是直接与句子最后一个藏文音节相连，中间没有 '་'，我们需要转换回去

            text2.delete('1.0', 'end')
            text2.insert('insert', target)
            app.status_var.set("转换完成")
            
        except Exception as e:
            messagebox.showerror("错误", f"转换过程中出错: {str(e)}")
            app.status_var.set(f"转换失败: {str(e)}")

    @staticmethod
    def latin_to_tibetan(s):
        """转换单个拉丁文为藏文音节"""
        global target
        begin = 0  # 控制每次匹配都是从当前未匹配的第一个字符开始
        
        # 处理非字母字符
        for ch in s:
            if not ch.isalpha():
                target += ch
                begin += 1  # 如果非藏文则不匹配
            else:
                break

        # 先匹配最大字符串，如果匹配不到就删除最后一个字符串，直到匹配上为止
        while begin < len(s):
            matched = False
            for i in range(len(s[begin:]), 0, -1):
                if la2Tibetan.get(s[begin:begin+i], -1) != -1:
                    target += la2Tibetan[s[begin:begin+i]]
                    begin += i
                    matched = True
                    break
            
            # 如果无法匹配，跳过当前字符
            if not matched:
                if begin < len(s):
                    # 无法转换的字符，直接添加
                    target += s[begin]
                begin += 1

class TibetanLatinGUI:
    """藏文拉丁转换工具GUI界面"""
    
    def __init__(self, root):
        """初始化GUI界面"""
        self.root = root
        self.root.title("藏文拉丁互转工具")
        self.root.geometry("900x600+400+200")  # 调整窗口大小和位置
        
        # 加载映射字典
        process = Preprocessing(tibetan2La, la2Tibetan, vowPos)
        
        # 创建界面
        self.create_ui()
    
    def create_ui(self):
        """创建用户界面"""
        # Define custom font
        custom_font = ("Arial", 12)  # Default fallback font
        try:
            font_name = "吞弥恰俊——尼赤乌坚体"

            temp_font = tkFont.Font(family=font_name, size=14)
            actual_family = temp_font.actual()["family"]
            
            if font_name in actual_family:
                custom_font = (font_name, 14)
                print(f"成功加载字体: '{font_name}'")
            else:
               
                font_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fontfile", f"{font_name}.ttf")
                if os.path.exists(font_path):
                    custom_font = (font_name, 14)
                    print(f"警告: 字体 '{font_name}' 未在系统中注册。尝试从路径 '{font_path}' 加载，可能无法生效。")
                else:
                     print(f"警告: 字体 '{font_name}' 未安装，且在本地路径也未找到。将使用默认字体。")
        except Exception as e:
            print(f"警告: 加载自定义字体时出错: {e}。将使用默认字体。")

        # 创建主框架
        main_frame = tk.Frame(self.root, bg="#f5f5f5")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # 创建标题
        title_frame = tk.Frame(main_frame, bg="#4a86e8", height=60)
        title_frame.pack(fill=tk.X, pady=(0, 15))
        
        # 创建标题标签
        title_label = tk.Label(
            title_frame, 
            text="藏文拉丁互转工具-Tibetan-Latin Conversion Tool", 
            font=("Arial", 22, "bold"),
            fg="white",
            bg="#4a86e8",
            padx=20,
            pady=10
        )
        title_label.pack(side=tk.LEFT)
        
        
        # 创建左侧内容区域
        content_frame = tk.Frame(main_frame, bg="#f5f5f5")
        content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 源文件区域
        source_frame = ttk.LabelFrame(content_frame, text="源文件", padding=10)
        source_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        global text1
        text1 = scrolledtext.ScrolledText(
            source_frame, 
            width=50, 
            height=10,
            font=custom_font,
            wrap=tk.WORD,
            bg="#ffffff",
            relief=tk.SOLID,
            borderwidth=1
        )
        text1.pack(fill=tk.BOTH, expand=True)
        
        # 目标文件区域
        target_frame = ttk.LabelFrame(content_frame, text="目标文件", padding=10)
        target_frame.pack(fill=tk.BOTH, expand=True)
        
        global text2
        text2 = scrolledtext.ScrolledText(
            target_frame, 
            width=50, 
            height=10,
            font=custom_font,
            wrap=tk.WORD,
            bg="#ffffff",
            relief=tk.SOLID,
            borderwidth=1
        )
        text2.pack(fill=tk.BOTH, expand=True)
        
        # 创建右侧按钮区域
        button_frame = tk.Frame(main_frame, bg="#f5f5f5", width=150)
        button_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(20, 0))
        
        # 创建按钮
        button_style = ttk.Style()
        button_style.configure('TButton', font=('Arial', 10, 'bold'), padding=5)

        open_btn = ttk.Button(
            button_frame, text="📂 打开文件", command=self.open_file, style='TButton'
        )
        open_btn.pack(pady=8, fill=tk.X, expand=False)

        open_folder_btn = ttk.Button(
            button_frame, text="📁 打开文件夹", command=self.open_folder, style='TButton'
        )
        open_folder_btn.pack(pady=8, fill=tk.X, expand=False)

        convert_to_latin_btn = ttk.Button(
            button_frame, text="➡️ 藏文转拉丁", command=TibetanLatinConverter.tibetan_to_latin_traverse, style='TButton'
        )
        convert_to_latin_btn.pack(pady=8, fill=tk.X, expand=False)

        convert_to_tibetan_btn = ttk.Button(
            button_frame, text="⬅️ 拉丁转藏文", command=TibetanLatinConverter.latin_to_tibetan_traverse, style='TButton'
        )
        convert_to_tibetan_btn.pack(pady=8, fill=tk.X, expand=False)
        
        save_btn = ttk.Button(
            button_frame, text="💾 保存结果", command=self.save_file, style='TButton'
        )
        save_btn.pack(pady=8, fill=tk.X, expand=False)

        clear_btn = ttk.Button(
            button_frame, text="🗑️ 清空", command=self.clear_text, style='TButton'
        )
        clear_btn.pack(pady=8, fill=tk.X, expand=False)

        exit_btn = ttk.Button(
            button_frame, text="❌ 退出", command=self.root.destroy, style='TButton'
        )
        exit_btn.pack(pady=8, fill=tk.X, expand=False)
        
        # 添加状态栏
        status_frame = tk.Frame(self.root, bg="#3498db", height=30, name="status_frame")
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_var = tk.StringVar()
        self.status_var.set("就绪")
        
        status_label = tk.Label(
            status_frame, 
            textvariable=self.status_var,
            anchor=tk.W,
            bg="#3498db",
            fg="white",
            font=("Arial", 10),
            padx=15,
            pady=5
        )
        status_label.pack(side=tk.LEFT, fill=tk.X)
    
    def open_file(self):
        """打开文件"""
        global essay
        filePaths = []
        essay = ''

        self.root.update()
        text1.delete('1.0', 'end')
        text2.delete('1.0', 'end')
        
        # 设置打开的默认位置
        files = filedialog.askopenfilename(
            title='选择文件',
            initialdir=(os.path.expanduser('./')),
            multiple=True,
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        
        var = self.root.splitlist(files)
        for f in var:
            filePaths.append(f)
        
        if not filePaths:
            return
            
        self.status_var.set(f"已选择 {len(filePaths)} 个文件")

        for file_path in filePaths:
            if file_path is not None:
                try:
                    with open(file=file_path, mode='r', encoding='utf-8') as f:
                        word = f.read()
                        if len(word) < 50000:
                            text1.insert('insert', f'{word}\n')
                        else:
                            text1.insert('insert', '文本已加载，由于文本数量过多，暂不显示在组件内\n')
                        essay = essay + ''.join(word)
                    
                    self.status_var.set(f"已加载文件: {os.path.basename(file_path)}")

                except Exception as e:
                    messagebox.showerror("错误", f"文件加载异常: {str(e)}")
                    text1.insert('insert', f'加载文件异常：{str(e)}，请重新加载文件\n')
                    self.status_var.set("加载文件失败")

    def open_folder(self):
        """打开文件夹进行批量处理"""
        global essay
        essay = ''
        
        self.root.update()
        text1.delete('1.0', 'end')
        text2.delete('1.0', 'end')
        
        dir_path = filedialog.askdirectory(
            title='选择文件夹',
            initialdir=(os.path.expanduser('./'))
        )
        
        if not dir_path:
            return
            
        file_paths = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.endswith('.txt')]
        
        if not file_paths:
            messagebox.showinfo("提示", "所选文件夹中没有找到 .txt 文件。")
            self.status_var.set("未找到 .txt 文件")
            return
            
        self.status_var.set(f"已选择文件夹，找到 {len(file_paths)} 个 .txt 文件")
        
        for file_path in file_paths:
            try:
                with open(file=file_path, mode='r', encoding='utf-8') as f:
                    word = f.read()
                    # Add a separator to distinguish file content
                    text1.insert('insert', f'--- {os.path.basename(file_path)} ---\n')
                    if len(word) < 50000:
                        text1.insert('insert', f'{word}\n\n')
                    else:
                        text1.insert('insert', '文本已加载，由于文本数量过多，暂不显示在组件内\n\n')
                    essay = essay + ''.join(word)
                
                self.status_var.set(f"已加载文件: {os.path.basename(file_path)}")

            except Exception as e:
                messagebox.showerror("错误", f"文件加载异常: {str(e)}")
                text1.insert('insert', f'加载文件 {os.path.basename(file_path)} 异常：{str(e)}，请重新加载文件\n')
                self.status_var.set("加载文件失败")
        
        self.status_var.set(f"批量加载完成，共 {len(file_paths)} 个文件。")
    
    def save_file(self):
        """保存文件"""
        text_str = text2.get('1.0', 'end')
        if not text_str.strip():
            messagebox.showwarning("警告", "没有可保存的内容")
            return
            
        file_path = filedialog.asksaveasfilename(
            title='保存文件',
            defaultextension=".txt",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        
        if not file_path:
            return
            
        try:
            with open(file=file_path, mode='w', encoding='utf-8') as f:
                f.write(text_str)
            
            messagebox.showinfo("成功", "文件保存成功")
            self.status_var.set(f"已保存至: {os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror("错误", f"保存文件失败: {str(e)}")
            self.status_var.set("保存文件失败")
    
    def clear_text(self):
        """清空文本框"""
        text1.delete('1.0', 'end')
        text2.delete('1.0', 'end')
        global essay, target
        essay = ''
        target = ''
        self.status_var.set("已清空")
    

def main():
    """主函数"""
    root = ttk.Window(themename="lumen")
    global app
    app = TibetanLatinGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()