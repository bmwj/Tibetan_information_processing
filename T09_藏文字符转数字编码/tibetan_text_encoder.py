# -*- coding: UTF-8 -*-
# 创建者：Pemawangchuk
# 版本：1.0
# 日期：2025-04-06
# 描述：藏文字符转换数字编码工具
"""
tibetan_text_encoder.py - 藏文字符转换数字编码
This script converts Tibetan characters to numeric encoding.
"""
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext, Frame
import tkinter.font as tkFont
import os
from ttkbootstrap import Style
import re
import sys
import os
# 获取项目根目录路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)  # 将项目根目录添加到Python路径
# 导入common目录下的模块
from common.TibetanSyllableSegmenter import Split_component

''' 
    在编码中，
     ① '་' 转为 空格
     ② 结束符转为 ' . '（因为结束符和之前的藏文音节中没有分隔符'་'，所以需要手动添加空格
'''

essay = ''
target = ''
end = ['།', '༏', '༐' ,'༑', '༎']
adhering =  ['འུའི', 'འི', 'འོ', 'འང']
split_char = [
                  'ༀ', '༁', '༂', '༃', '༄', '༆', '༇', '༈', '༉', '༊', '་', '༌',
                  '༒', '༓', '༔', '༕', '༖', '༗', '༘', '༙', '༚', '༛', '༜', '༝', '༞',
                  '༟', '༠', '༡', '༢', '༣', '༤', '༥', '༦', '༧', '༨', '༩', '༪',
                  '༫', '༬', '༭', '༮', '༯', '༰', '༱', '༲', '༳', '༴', '༵', '༶', '༷', '༸',
                  '༺', '༻', '༼', '༽', '༾', '༿', '྾', '྿', '࿀', '࿁', '࿂', '࿃', '࿄', '࿅',
                  '࿆', '࿇', '࿈', '࿉', '࿊', '࿋', '࿌', '࿎', '࿏', '࿐', '࿑', '࿒', '࿓', '࿔',
                  '\u0FD5', '\u0FD6', '\u0FD7', '\u0FD8', '࿙', '࿚'
              ]

tibtBase_num = {}
tibtFront_num = {}
tibtVowelrear_num = {}
num_tibtBase = {}
num_tibtFront = {}
num_tibtVowelrer = {}

def open_file():
    global essay
    filePaths = []
    essay = ''

    text1.delete('1.0', 'end')
    text2.delete('1.0', 'end')
    # 设置打开的默认位置
    files = filedialog.askopenfilename(title=u'选择文件夹', initialdir=(
        os.path.expanduser('./')),
                                       multiple=True)
    var = window.splitlist(files)
    for f in var: filePaths.append(f)
    print(f'打开文件：{filePaths}')

    for file_path in filePaths:
        if file_path is not None:
            try:
                with open(file=file_path, mode='r+', encoding='utf-8') as f:
                    essay = f.read()
                    # print(len(word))
                    if (len(essay) < 50000):
                        text1.insert('insert', f'{essay}\n')
                    else:
                        text1.insert('insert', '文本已加载，由于文本数量过多，暂不显示在组件内')

            except Exception as e:
                print(str(e))
                messagebox.askokcancel(title='警告', message='文件加载异常，请重新加载文件')
                text1.insert('insert', f'加载文件异常：{str(e)}，请重新加载文件')

def save_file():
    global file_path
    text_str = text2.get('1.0', 'end')
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

def clear_content():
    """清空文本框内容"""
    result = messagebox.askyesno(title='确认清空', message='确定要清空所有文本内容吗？')
    if result:
        text1.delete('1.0', 'end')
        text2.delete('1.0', 'end')
        global essay, target
        essay = ''
        target = ''
        print('内容已清空')

def is_mainly_tibetan(text):
    """判断文本是否主要包含藏文字符"""
    if not text.strip():
        return False
    
    tibetan_count = 0
    digit_count = 0
    total_chars = 0
    
    for char in text:
        if char.strip():  # 忽略空白字符
            total_chars += 1
            if '\u0F00' <= char <= '\u0FDA':  # 藏文Unicode范围
                tibetan_count += 1
            elif char.isdigit() or char in ['*', '_']:  # 数字编码字符
                digit_count += 1
    
    if total_chars == 0:
        return False
    
    # 如果藏文字符占比超过30%，认为是藏文文本
    tibetan_ratio = tibetan_count / total_chars
    return tibetan_ratio > 0.3

def is_mainly_numeric_code(text):
    """判断文本是否主要包含数字编码"""
    if not text.strip():
        return False
    
    digit_count = 0
    total_chars = 0
    
    for char in text:
        if char.strip():  # 忽略空白字符
            total_chars += 1
            if char.isdigit() or char in ['*', '_']:  # 数字编码字符
                digit_count += 1
    
    if total_chars == 0:
        return False
    
    # 如果数字编码字符占比超过50%，认为是数字编码文本
    digit_ratio = digit_count / total_chars
    return digit_ratio > 0.5

# 根据传入的编码表位置path，生成对应的 tibt_num 和 num_tibt 表
def Data_process(path, tibt_num, num_tibt):
    with open(path, mode='r', encoding='utf-8') as f:
        All = []
        while(True):
            temp = f.readline().strip().split('\t')
            if(temp[0]!=''): All.append(temp)
            else: break
        All.reverse()
        for temp in All:
            tibt_num[temp[0]] = temp[1]
            num_tibt[temp[1]] = temp[0]

def Tibetan2Num_Traverse():
    global target, essay
    
    # 检查文本内容类型
    if not essay.strip():
        messagebox.showwarning("提示", "请先打开文件或输入内容")
        return
    
    if is_mainly_numeric_code(essay):
        messagebox.showwarning("内容类型错误", "文件内容为数字编码，请使用'数字解码'功能")
        return
    
    target = ''
    essay = essay.replace('་', ' ')
    for E in end: essay = essay.replace(E, ' . ')
    # print(essay)
    s = ''
    for i, ch in enumerate(essay):
        # 如果是藏字且不是分隔符，与之前的字符构成字符串
        if ('\u0F00' <= ch <= '\u0FDA' and ch not in split_char):
            s += ch
            continue
        # 当前字符 ch 不是藏字，我们首先将当前字符加入到字符串中，然后对 s 进行编码
        elif s != '':
            # print(f'拆分后的藏字为：{s}')
            # 先判断是否是黏着词（如果后缀是  ['འུའི', 'འི', 'འོ', 'འང'] 的，拆开变为两个词）
            is_adhere = False
            for adhere in adhering:
                if s.endswith(adhere):
                    # 找到拆分位置，分别转为数字编码
                    sep = s.rfind(adhere)
                    Tibetan2Num1(s[:sep])
                    target += '_'
                    Tibetan2Num1(s[sep:])
                    is_adhere = True
                    break
            if(is_adhere==False):
                Tibetan2Num1(s)
            s = ''
            target += ch
        # 当前遇到多个非藏字相连，要将当前 ch 放入目标文件中
        else:
            target += ch

    text2.insert('insert', target)

def Tibetan2Num1(Tibetan):
    # word：[ 1前、2上、3基、4下、5再下、6元、7后、8再后 ]
    global target
    Component = Split_component()
    word = Component.Split(Tibetan)

    front = word[1]
    base = word[2] + word[3] + word[4] + word[5]
    vowel_rear = word[6] + word[7] + word[8]

    # 如果当前音节没有对应的构建，使用 '*' 进行占位
    if front!='': Tibetan2Num2(front, tibtFront_num)
    else: target+='*'
    if base!='': Tibetan2Num2(base, tibtBase_num)
    else: target+='***'
    if vowel_rear!='': Tibetan2Num2(vowel_rear, tibtVowelrear_num)
    else: target += '**'

def Tibetan2Num2(compo, di):
    global target

    aim = di.get(compo, False)
    if(aim!=False): target += aim
    else: target += compo

def Num2Tibetan_Traverse():
    global target, essay
    
    # 检查文本内容类型
    if not essay.strip():
        messagebox.showwarning("提示", "请先打开文件或输入内容")
        return
    
    if is_mainly_tibetan(essay):
        messagebox.showwarning("内容类型错误", "文件内容为藏文，请使用'藏文编码'功能")
        return
    
    # 利用正则：将数字编码中 '数字编码 数字编码' 中的空格替换为分隔符
    essay = re.sub(r'(?<=([0-9]|\*))(\s{1})(?=([0-9]|\*))', '་', essay)
    target = ''
    s = ''
    for i, ch in enumerate(essay):
        # 如果是藏字且不是分隔符，与之前的字符构成字符串
        if (ch.isdigit() or ch=='*' or ch=='_'):
            s += ch
            continue
        # 当前字符 ch 不是藏字，我们首先将当前字符加入到字符串中，然后对 s 进行编码
        elif s != '':
            # 在黏着词前还有原本文本中的数字，一般来说数字会出现在藏文音节前，所以我们可以进行截断
            # need_nums 代表我们正确的编码位数，用 s的长度-need_nums = 需要截去的长度
            need_nums = 0
            cut = False
            if(len(s) > 13):
                if('_' in s): need_nums = 13
                else: need_nums = 6
            elif(6<len(s)<13):
                cut = True
                need_nums = 6
            if(cut):
                other_nums = len(s) - need_nums
                target += s[:other_nums]
                s = s[other_nums:]

            # 先判断是否是黏着词，黏着词的数字编码应该是 13(6+1+6) 位，藏文的普通音节应该是 6 位
            if (len(s) == 13):
                Num2Tibetan(s[:6])
                Num2Tibetan(s[7:])
                # target += '་'
            elif (len(s) == 6):
                Num2Tibetan(s)
                # target += '་'
            else:
                target += s
            s = ''
            target += ch
        # 当前遇到多个非藏字相连，要将当前 ch 放入目标文件中
        else: target += ch

    target = target.replace(' . ', '།')
    # 在新闻中还会有一部分 དང་། 的情况，所以这部分是被替换为了 ' །'，我们需要替换回'་།'
    target = target.replace(' །', '་།')

    text2.insert('insert', target)

def Num2Tibetan(co_str):
    global target

    front = co_str[0]
    base = co_str[1:4]
    vowel_rear = co_str[4:]

    if front.isdigit():
        target += num_tibtFront[front]

    if base[0].isdigit():
        target += num_tibtBase[base]
    elif '\u0F00' <= base[0] <= '\u0FDA':
        target += base

    if vowel_rear[0].isdigit():
        target += num_tibtVowelrer[vowel_rear]
    elif '\u0F00' <= vowel_rear[0] <= '\u0FDA':
        target += vowel_rear

if __name__ == '__main__':
    # 制数字编码表
    Data_process('./Table/TibtFront.txt', tibtFront_num, num_tibtFront)
    Data_process('./Table/TibtBase.txt', tibtBase_num, num_tibtBase)
    Data_process('./Table/TibetVowelrear.txt', tibtVowelrear_num, num_tibtVowelrer)

    # 使用 ttkbootstrap 的 'darkly' 深色主题
    style = Style(theme='darkly')
    window = style.master
    window.title('藏文数字编码转换工具 (darkly版)')
    window.geometry('1000x650+400+200')
    
    # 设置窗口最小尺寸
    window.minsize(900, 600)
    
    # 主标题
    title_label = ttk.Label(window, text='藏文数字编码转换工具', 
                          font=('Microsoft YaHei UI', 20, 'bold'), 
                          anchor='center')
    title_label.pack(fill='x', pady=(20, 10))

    # 主容器
    main_container = ttk.Frame(window, padding=20)
    main_container.pack(fill='both', expand=True)
    main_container.columnconfigure(0, weight=3)
    main_container.columnconfigure(1, weight=1)
    main_container.rowconfigure(0, weight=1)

    # 左侧文本区域
    text_frame = ttk.Frame(main_container)
    text_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 15))
    text_frame.rowconfigure(1, weight=1)
    text_frame.rowconfigure(4, weight=1)
    text_frame.columnconfigure(0, weight=1)

    # 源文件区域
    source_label = ttk.Label(text_frame, text='📄 源文件内容', 
                           font=('Microsoft YaHei UI', 12, 'bold'))
    source_label.grid(row=0, column=0, sticky='w', pady=(0, 5))

    text1 = scrolledtext.ScrolledText(text_frame, width=55, height=10,
                                     font=('珠穆朗玛—乌金苏通体', 14),
                                     relief='solid', bd=1,
                                     wrap='word',
                                     bg="#2a2a2a", fg="white",
                                     insertbackground="white")
    text1.grid(row=1, column=0, sticky='nsew')

    # 分隔线
    separator = ttk.Separator(text_frame, orient='horizontal')
    separator.grid(row=2, column=0, sticky='ew', pady=15)

    # 目标文件区域
    target_label = ttk.Label(text_frame, text='🎯 编码或者解码后的结果', 
                           font=('Microsoft YaHei UI', 12, 'bold'))
    target_label.grid(row=3, column=0, sticky='w', pady=(0, 5))

    text2 = scrolledtext.ScrolledText(text_frame, width=55, height=10,
                                     font=('珠穆朗玛—乌金苏通体', 14),
                                     relief='solid', bd=1,
                                     wrap='word',
                                     bg="#2a2a2a", fg="white",
                                     insertbackground="white")
    text2.grid(row=4, column=0, sticky='nsew')

    # 右侧按钮区域
    button_frame = ttk.Frame(main_container)
    button_frame.grid(row=0, column=1, sticky='nsew')
    
    # 主题切换功能
    themes = style.theme_names()
    current_theme_index = themes.index(style.theme.name)

    def switch_theme():
        global current_theme_index
        current_theme_index = (current_theme_index + 1) % len(themes)
        new_theme = themes[current_theme_index]
        try:
            style.theme_use(new_theme)
            is_dark = style.theme.type == 'dark'
            
            # 更新窗口标题和状态栏
            window.title(f'藏文数字编码转换工具 ({new_theme}版)')
            status_label.config(text=f'就绪 | 藏文数字编码转换工具 v1.2 ({new_theme}版)')
            
            # 更新文本框颜色
            bg_color = "#2a2a2a" if is_dark else "white"
            fg_color = "white" if is_dark else "black"
            text1.config(bg=bg_color, fg=fg_color, insertbackground=fg_color)
            text2.config(bg=bg_color, fg=fg_color, insertbackground=fg_color)

        except Exception as e:
            print(f"Error switching theme: {e}")
            messagebox.showerror("主题切换失败", f"无法切换到主题: {new_theme}")
    
    # 使用 ttk.Button 来自动适应主题
    style.configure('TButton', font=('Microsoft YaHei UI', 11, 'bold'))
    
    # 按钮垂直居中
    button_frame.rowconfigure(0, weight=1)
    button_frame.rowconfigure(8, weight=1) # 增加一行以适应新按钮
    button_frame.columnconfigure(0, weight=1)

    # 打开文件按钮
    bt1 = ttk.Button(button_frame, text='📁 打开文件', 
                   command=open_file, style='primary.TButton')
    bt1.grid(row=1, column=0, sticky='ew', pady=10, ipady=8)
    
    # 编码按钮
    bt2 = ttk.Button(button_frame, text='🔢 藏文编码', 
                   command=Tibetan2Num_Traverse, style='danger.TButton')
    bt2.grid(row=2, column=0, sticky='ew', pady=10, ipady=8)
    
    # 解码按钮
    bt5 = ttk.Button(button_frame, text='📝 数字解码', 
                   command=Num2Tibetan_Traverse, style='warning.TButton')
    bt5.grid(row=3, column=0, sticky='ew', pady=10, ipady=8)
    
    # 保存按钮
    bt3 = ttk.Button(button_frame, text='💾 保存文件', 
                   command=save_file, style='success.TButton')
    bt3.grid(row=4, column=0, sticky='ew', pady=10, ipady=8)
    
    # 清空内容按钮
    bt_clear = ttk.Button(button_frame, text='🗑️ 清空内容',
                          command=clear_content, style='warning.TButton')
    bt_clear.grid(row=5, column=0, sticky='ew', pady=10, ipady=8)

    # 主题切换按钮
    bt_theme = ttk.Button(button_frame, text='🎨 切换主题',
                          command=switch_theme, style='info.TButton')
    bt_theme.grid(row=6, column=0, sticky='ew', pady=10, ipady=8)

    # 退出按钮
    bt4 = ttk.Button(button_frame, text='❌ 退出程序', 
                   command=window.destroy, style='secondary.TButton')
    bt4.grid(row=7, column=0, sticky='ew', pady=10, ipady=8)
    
    # 状态栏
    status_frame = ttk.Frame(window, padding=(10, 5))
    status_frame.pack(fill='x', side='bottom')
    
    status_label = ttk.Label(status_frame, text='就绪 | 藏文数字编码转换工具 v1.2 (darkly版)', 
                           font=('Microsoft YaHei UI', 9))
    status_label.pack(side='left')

    window.mainloop()
