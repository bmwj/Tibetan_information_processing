#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
藏文构件识别与分析工具 - GUI版本
支持文件选择和直接输入两种模式，界面美观炫酷
"""
import os
import sys
import csv
import json
from typing import Dict, List, Optional, Tuple, Any
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font, TclError
from tkinter.scrolledtext import ScrolledText
import threading
import math
from PIL import Image, ImageTk, ImageFilter, ImageEnhance, ImageDraw
# 获取项目根目录路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)  # 将项目根目录添加到Python路径
# 导入common目录下的模块
# 导入藏文分析函数
from T01_藏字构件识别.tibetan_analyzer import cut


class ModernButton(tk.Canvas):
    """现代风格按钮"""
    def __init__(self, master, text, command=None, width=120, height=40, 
                 bg_color="#6B4226", hover_color="#8A6642", text_color="white", 
                 font=None, corner_radius=10, **kwargs):
        # 直接使用默认背景色，不尝试从master获取
        bg = "#F8F3E6"  # 默认使用与应用背景相同的颜色
            
        super().__init__(master, width=width, height=height, 
                         bg=bg, highlightthickness=0, **kwargs)
        
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.corner_radius = corner_radius
        self.command = command
        self.text = text
        self.font = font or ("Arial", 12)
        self.width = width
        self.height = height
        
        # 绘制按钮
        self.draw_button(self.bg_color)
        
        # 绑定事件
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)
        self.bind("<ButtonRelease-1>", self.on_release)
        self.bind("<Configure>", self.on_configure)
        
    def draw_button(self, color):
        """绘制按钮"""
        self.delete("all")
        
        # 获取当前宽度和高度
        width = self.winfo_reqwidth()
        height = self.winfo_reqheight()
        
        # 确保使用实际尺寸而不是请求尺寸
        if width <= 1:
            width = self["width"]
        if height <= 1:
            height = self["height"]
        
        # 创建圆角矩形
        self.create_rounded_rect(0, 0, width, height, 
                                self.corner_radius, fill=color, outline="")
        
        # 添加文本
        self.create_text(width/2, height/2, 
                        text=self.text, fill=self.text_color, font=self.font)
        
    def create_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        """创建圆角矩形"""
        points = [
            x1+radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1, y2,
            x1, y2-radius,
            x1, y1+radius,
            x1, y1
        ]
        return self.create_polygon(points, **kwargs, smooth=True)
        
    def on_enter(self, event):
        """鼠标进入事件"""
        self.draw_button(self.hover_color)
        
    def on_leave(self, event):
        """鼠标离开事件"""
        self.draw_button(self.bg_color)
        
    def on_click(self, event):
        """鼠标点击事件"""
        self.draw_button(self.bg_color)
        
    def on_release(self, event):
        """鼠标释放事件"""
        self.draw_button(self.hover_color)
        if self.command:
            self.command()
            
    def on_configure(self, event):
        """大小变化事件"""
        # 当按钮大小变化时重绘
        self.draw_button(self.bg_color)


class TibetanAnalyzerApp:
    """藏文构件识别与分析工具GUI应用"""
    
    # 界面颜色主题 - 更加精美的配色方案
    COLORS = {
        "primary": "#6B4226",       # 深棕色
        "secondary": "#A67C52",     # 浅棕色
        "accent": "#4682B4",        # 浅蓝色（钢蓝色）
        "background": "#F8F3E6",    # 米色背景
        "card_bg": "#FFFFFF",       # 卡片背景
        "text": "#3E2723",          # 深棕文本
        "text_light": "#FFFFFF",    # 白色文本
        "button": "#5F9EA0",        # 浅蓝色按钮（凫绿色）
        "button_hover": "#4682B4",  # 浅蓝色按钮悬停（钢蓝色）
        "success": "#2E8B57",       # 海绿色
        "error": "#8B0000",         # 深红色
        "border": "#D2B48C",        # 边框颜色
        "highlight": "#87CEEB",     # 高亮颜色（天蓝色）
    }
    
    def __init__(self, root):
        """初始化应用"""
        self.root = root
        self.root.title("藏文构件识别与分析工具")
        self.root.geometry("1280x800")  # 增加窗口大小
        self.root.configure(bg=self.COLORS["background"])
        
        # 设置应用图标
        # self.root.iconphoto(True, tk.PhotoImage(file="icon.png"))
        
        # 初始化变量
        self.current_input_panel = "file"
        self.current_result_panel = "table"
        self.current_tibetan = ""
        self.analysis_results = []
        self.current_visual_index = 0  # 当前可视化视图显示的结果索引
        
        # 加载藏文字体
        self.load_tibetan_fonts()
        
        # 创建自定义样式
        self.create_custom_styles()
        
        # 创建主框架
        self.create_main_frame()
        
        # 创建标题栏 (10% 高度)
        self.create_title_bar()
        
        # 创建主内容区域，分为输入区域 (25% 高度) 和结果区域 (65% 高度)
        self.create_content_area()
        
        # 创建状态栏
        self.create_status_bar()
        
        # 设置初始状态
        self.status_var.set("就绪")
        
        # 初始化数据
        self.current_tibetan = ""
        self.analysis_results = []
        
        # 设置初始状态
        self.status_var.set("就绪")
        
        # 绑定窗口大小变化事件
        self.root.bind("<Configure>", self.on_window_resize)
        
    def load_tibetan_fonts(self):
        """加载藏文字体"""
        self.available_fonts = []
        self.tibetan_font = None
        self.font_paths = {}  # 存储字体名称到路径的映射
        
        # 从fontfile目录加载藏文字体
        font_dir = os.path.join(project_root, "T01_藏字构件识别", "fontfile")
        
        # 指定默认字体文件
        default_font_file = "吞弥恰俊——尼赤乌坚体.ttf"
        default_font_path = os.path.join(font_dir, default_font_file)
        
        if os.path.exists(font_dir):
            # 遍历字体目录
            for file_name in os.listdir(font_dir):
                if file_name.lower().endswith(('.ttf', '.otf')):
                    font_path = os.path.join(font_dir, file_name)
                    font_name = os.path.splitext(file_name)[0]
                    self.available_fonts.append(font_name)
                    self.font_paths[font_name] = font_path
        
        # 如果没有找到藏文字体，检查系统中的藏文字体
        if not self.available_fonts:
            system_fonts = font.families()
            tibetan_font_keywords = ["Tibetan", "藏文", "Jomolhari", "DDC Uchen", "Qomolangma"]
            
            for font_name in system_fonts:
                for keyword in tibetan_font_keywords:
                    if keyword.lower() in font_name.lower():
                        self.available_fonts.append(font_name)
                        break
        
        # 设置默认字体
        if os.path.exists(default_font_path):
            # 使用指定的默认字体
            default_font_name = os.path.splitext(default_font_file)[0]
            self.tibetan_font = default_font_path  # 直接使用字体文件路径
            # 确保默认字体在可用字体列表中
            if default_font_name not in self.available_fonts:
                self.available_fonts.insert(0, default_font_name)
                self.font_paths[default_font_name] = default_font_path
        elif self.available_fonts:
            # 如果默认字体不存在，使用第一个可用字体
            first_font = self.available_fonts[0]
            self.tibetan_font = self.font_paths.get(first_font, first_font)
        else:
            # 如果没有找到藏文字体，使用默认字体
            self.tibetan_font = "TkDefaultFont"
            
        # 创建字体对象
        self.title_font = (self.tibetan_font, 28, "bold")
        self.heading_font = (self.tibetan_font, 18, "bold")
        self.text_font = (self.tibetan_font, 14)
        self.button_font = (self.tibetan_font, 12, "bold")
        self.status_font = (self.tibetan_font, 10)
        
    def create_custom_styles(self):
        """创建自定义样式"""
        style = ttk.Style()
        
        # 配置基本样式
        style.configure("TFrame", background=self.COLORS["background"])
        style.configure("Card.TFrame", background=self.COLORS["card_bg"], relief="flat")
        
        style.configure("TLabel", background=self.COLORS["background"], foreground=self.COLORS["text"])
        style.configure("Card.TLabel", background=self.COLORS["card_bg"], foreground=self.COLORS["text"])
        style.configure("Title.TLabel", font=self.title_font, foreground=self.COLORS["primary"])
        
        style.configure("TLabelframe", background=self.COLORS["background"], foreground=self.COLORS["text"])
        style.configure("TLabelframe.Label", background=self.COLORS["background"], foreground=self.COLORS["text"], font=self.heading_font)
        
        style.configure("Card.TLabelframe", background=self.COLORS["card_bg"], foreground=self.COLORS["text"])
        style.configure("Card.TLabelframe.Label", background=self.COLORS["background"], foreground=self.COLORS["primary"], font=self.heading_font)
        
        # 配置按钮样式
        style.configure("TButton", 
                      background=self.COLORS["button"], 
                      foreground=self.COLORS["text_light"],
                      font=self.button_font,
                      padding=(15, 10),
                      relief="flat",
                      borderwidth=0)
        
        style.map("TButton",
                background=[("active", self.COLORS["button_hover"]), ("pressed", self.COLORS["button_hover"])],
                foreground=[("active", self.COLORS["text_light"])])
        
        # 配置选项卡样式
        style.configure("TNotebook", background=self.COLORS["background"], borderwidth=0)
        style.configure("TNotebook.Tab", background=self.COLORS["secondary"], foreground=self.COLORS["text_light"], padding=(20, 10))
        style.map("TNotebook.Tab",
                background=[("selected", self.COLORS["primary"])],
                foreground=[("selected", self.COLORS["text_light"])])
        
        # 配置进度条样式
        style.configure("TProgressbar", 
                      background=self.COLORS["accent"],
                      troughcolor=self.COLORS["background"],
                      borderwidth=0,
                      thickness=12)
        
        # 配置单选按钮样式
        style.configure("TRadiobutton", 
                      background=self.COLORS["card_bg"],
                      foreground=self.COLORS["text"],
                      font=self.text_font)
        
        # 配置输入框样式
        style.configure("TEntry", 
                      font=self.text_font,
                      fieldbackground="white",
                      borderwidth=1)
        
    def create_main_frame(self):
        """创建主框架"""
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
    def create_title_bar(self):
        """创建标题栏 - 高度占10%"""
        # 创建标题背景卡片
        title_card = ttk.Frame(self.main_frame, style="Card.TFrame")
        title_card.pack(fill=tk.X, pady=5, ipady=5)
        
        # 添加装饰线条
        decoration = tk.Canvas(title_card, height=3, bg=self.COLORS["accent"], highlightthickness=0)
        decoration.pack(fill=tk.X, side=tk.TOP)
        
        # 标题内容框架
        title_content = ttk.Frame(title_card, style="Card.TFrame")
        title_content.pack(fill=tk.X, padx=20, pady=5)
        
        # 标题文本
        title_label = ttk.Label(title_content, 
                              text="藏文构件识别与分析工具", 
                              font=self.title_font,
                              foreground=self.COLORS["primary"],
                              style="Card.TLabel")
        title_label.pack(side=tk.LEFT, pady=2)
        
        # 添加字体选择下拉框
        font_frame = ttk.Frame(title_content, style="Card.TFrame")
        font_frame.pack(side=tk.RIGHT, pady=2)
        
        ttk.Label(font_frame, text="藏文字体:", font=self.text_font, style="Card.TLabel").pack(side=tk.LEFT, padx=5)
        
        self.font_var = tk.StringVar(value=self.tibetan_font)
        # 设置字体选择器的默认值
        default_display_name = "吞弥恰俊——尼赤乌坚体" if "吞弥恰俊——尼赤乌坚体" in self.available_fonts else (self.available_fonts[0] if self.available_fonts else "TkDefaultFont")
        
        self.font_var = tk.StringVar(value=default_display_name)
        font_combo = ttk.Combobox(font_frame, 
                                textvariable=self.font_var, 
                                values=self.available_fonts,
                                state="readonly",
                                width=20,
                                font=self.text_font)
        font_combo.pack(side=tk.LEFT)
        font_combo.bind("<<ComboboxSelected>>", self.change_font)
        
    def create_content_area(self):
        """创建主内容区域，使用PanedWindow分割输入和结果区域"""
        # 创建垂直分割窗口
        self.paned_window = ttk.PanedWindow(self.main_frame, orient=tk.VERTICAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # 创建输入区域卡片
        self.input_card = ttk.Frame(self.paned_window, style="Card.TFrame")
        input_header = ttk.Frame(self.input_card, style="Card.TFrame")
        input_header.pack(fill=tk.X, padx=15, pady=(15, 5))
        
        # 输入区域标题和按钮区域
        input_header_left = ttk.Frame(input_header, style="Card.TFrame")
        input_header_left.pack(side=tk.LEFT, fill=tk.Y)
                
        # 创建结果区域卡片
        self.result_card = ttk.Frame(self.paned_window, style="Card.TFrame")
        result_header = ttk.Frame(self.result_card, style="Card.TFrame")
        result_header.pack(fill=tk.X, padx=15, pady=(15, 5))
        
        # 结果区域标题和按钮区域
        result_header_left = ttk.Frame(result_header, style="Card.TFrame")
        result_header_left.pack(side=tk.LEFT, fill=tk.Y)
        
        ttk.Label(result_header_left, text="分析结果", font=self.heading_font, foreground=self.COLORS["primary"], style="Card.TLabel").pack(side=tk.LEFT)
        
        # 添加到分割窗口，调整比例为20:75（输入:结果）
        self.paned_window.add(self.input_card, weight=20)  # 输入区域占20%
        self.paned_window.add(self.result_card, weight=75)  # 结果区域占75%
        
        # 设置初始位置
        self.root.update_idletasks()  # 确保窗口已经绘制
        total_height = self.root.winfo_height()
        if total_height > 0:
            self.paned_window.sashpos(0, int(total_height * 0.20))
        
        # 填充输入区域内容
        self.create_input_content()
        
        # 填充结果区域内容
        self.create_result_content()
        
    def create_input_content(self):
        """创建输入区域内容 - 主区域和右侧按钮区域"""
        # 创建主框架，包含输入区域和按钮区域
        main_input_frame = ttk.Frame(self.input_card, style="Card.TFrame")
        main_input_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(5, 15))
        
        # 左侧输入区域
        input_area_frame = ttk.Frame(main_input_frame, style="Card.TFrame")
        input_area_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))
        
        # 右侧按钮区域 - 纵向排列
        button_area_frame = ttk.Frame(main_input_frame, style="Card.TFrame")
        button_area_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(8, 0))
        
        # 创建文件输入和直接输入按钮
        file_input_button = ModernButton(button_area_frame, text="文件输入", 
                                      command=lambda: self.show_input_panel("file"),
                                      width=120, height=35, bg_color=self.COLORS["button"],
                                      hover_color=self.COLORS["button_hover"], 
                                      text_color=self.COLORS["text_light"],
                                      font=self.button_font)
        file_input_button.pack(pady=8)
        
        direct_input_button = ModernButton(button_area_frame, text="直接输入", 
                                        command=lambda: self.show_input_panel("direct"),
                                        width=120, height=35, bg_color=self.COLORS["button"],
                                        hover_color=self.COLORS["button_hover"], 
                                        text_color=self.COLORS["text_light"],
                                        font=self.button_font)
        direct_input_button.pack(pady=8)
        
        # 分析按钮 - 使用更明显的颜色
        analyze_button = ModernButton(button_area_frame, text="构件识别", 
                                   command=self.analyze_current,
                                   width=120, height=35, bg_color=self.COLORS["accent"],
                                   hover_color=self.COLORS["button_hover"], 
                                   text_color=self.COLORS["text_light"],
                                   font=self.button_font)
        analyze_button.pack(pady=8)
        
        # 创建输入面板容器
        self.input_panel_container = ttk.Frame(input_area_frame, style="Card.TFrame")
        self.input_panel_container.pack(fill=tk.BOTH, expand=True)
        
        # 创建文件输入面板
        self.file_input_panel = ttk.Frame(self.input_panel_container, style="Card.TFrame")
        
        # 文件路径（删除标签）
        file_path_frame = ttk.Frame(self.file_input_panel, style="Card.TFrame")
        file_path_frame.pack(fill=tk.X, pady=(0, 15))
        
        file_input_frame = ttk.Frame(file_path_frame, style="Card.TFrame")
        file_input_frame.pack(fill=tk.X)
        
        self.file_path_var = tk.StringVar()
        file_entry = ttk.Entry(file_input_frame, textvariable=self.file_path_var, font=self.text_font, width=40)
        file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        # 创建现代风格的浏览按钮
        browse_button = ModernButton(file_input_frame, text="浏览...", command=self.browse_file, 
                                  width=80, height=30, bg_color=self.COLORS["button"], 
                                  hover_color=self.COLORS["button_hover"], 
                                  text_color=self.COLORS["text_light"],
                                  font=self.button_font)
        browse_button.pack(side=tk.RIGHT)
        
        # 文件编码
        encoding_frame = ttk.Frame(self.file_input_panel, style="Card.TFrame")
        encoding_frame.pack(fill=tk.X)
        
        ttk.Label(encoding_frame, text="文件编码:", font=self.text_font, style="Card.TLabel").pack(anchor=tk.W, pady=(0, 5))
        
        encoding_options = ttk.Frame(encoding_frame, style="Card.TFrame")
        encoding_options.pack(fill=tk.X)
        
        self.encoding_var = tk.StringVar(value="utf-8")
        encodings = ["utf-8", "utf-16", "utf-16-le", "utf-16-be", "gb18030"]
        
        for i, enc in enumerate(encodings):
            rb = ttk.Radiobutton(encoding_options, text=enc, variable=self.encoding_var, value=enc)
            rb.grid(row=0, column=i, padx=15, pady=5)
        
        # 创建直接输入面板
        self.direct_input_panel = ttk.Frame(self.input_panel_container, style="Card.TFrame")
        
        # 创建带有边框的文本输入框（不显示标签）
        text_container = ttk.Frame(self.direct_input_panel, style="Card.TFrame")
        text_container.pack(fill=tk.BOTH, expand=True)
        
        self.input_text = ScrolledText(text_container, 
                                    height=4,
                                    font=self.text_font,
                                    wrap=tk.WORD,
                                    background="white",
                                    borderwidth=1,
                                    relief=tk.SOLID)
        self.input_text.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
        # 添加半透明的藏文提示文本
        self.input_text.insert("1.0", "请输入藏文字符......")
        self.input_text.configure(foreground="lightgray")
        
        # 绑定焦点事件来处理提示文本
        self.input_text.bind("<FocusIn>", self.on_text_focus_in)
        self.input_text.bind("<FocusOut>", self.on_text_focus_out)
        self.input_text.bind("<KeyPress>", self.on_text_key_press)
        
        # 默认显示文件输入面板
        self.current_input_panel = "file"
        self.show_input_panel("file")
        
    def show_input_panel(self, panel_type):
        """显示指定的输入面板"""
        # 隐藏所有面板
        self.file_input_panel.pack_forget()
        self.direct_input_panel.pack_forget()
        
        # 显示指定面板
        if panel_type == "file":
            self.file_input_panel.pack(fill=tk.BOTH, expand=True)
            self.current_input_panel = "file"
        else:
            self.direct_input_panel.pack(fill=tk.BOTH, expand=True)
            self.current_input_panel = "direct"
            
    def analyze_current(self):
        """根据当前输入面板分析内容"""
        # 检查输入是否为藏文字符
        if self.current_input_panel == "file":
            file_path = self.file_path_var.get()
            if not file_path:
                messagebox.showerror("错误", "请选择文件")
                return
                
            # 尝试读取文件的前几个字符来判断是否为藏文
            try:
                encoding = self.encoding_var.get()
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read(100)  # 读取前100个字符
                if not self.contains_tibetan(content):
                    messagebox.showerror("错误", "文件不包含藏文字符，请选择包含藏文的文件")
                    return
            except Exception as e:
                # 如果读取失败，继续尝试分析，因为可能是编码问题
                pass
                
            self.analyze_file()
        else:
            text = self.input_text.get("1.0", tk.END).strip()
            
            # 检查是否为提示文本或空文本
            if not text or text == "ཀ་ཁ་ག་ང་ཅ་ཆ་ཇ་ཉ་ཏ་ཐ་ད་ན་པ་ཕ་བ་མ་ཙ་ཚ་ཛ་ཝ་ཞ་ཟ་འ་ཡ་ར་ལ་ཤ་ས་ཧ་ཨ།":
                messagebox.showerror("错误", "请输入藏文文本")
                return
                
            # 检查是否包含藏文字符（放宽检查条件）
            if not self.contains_tibetan(text):
                messagebox.showerror("错误", f"请输入藏文字符。当前输入：{repr(text)}")
                return
                
            self.analyze_text()
            
        # 显示结果区域
        self.show_result_panel("table")
        
    def contains_tibetan(self, text):
        """判断文本是否包含藏文字符"""
        # 藏文Unicode范围：0x0F00-0x0FFF
        # 同时检查常见的藏文字符范围
        for char in text:
            char_code = ord(char)
            # 藏文基本范围
            if 0x0F00 <= char_code <= 0x0FFF:
                return True
            # 藏文扩展范围A
            if 0x0F00 <= char_code <= 0x0FD4:
                return True
        
        # 如果没有找到藏文字符，但文本不为空且不是纯ASCII，也认为可能是藏文
        # 这是为了处理一些特殊编码情况
        if text and not text.isascii():
            # 检查是否包含一些常见的藏文字符
            tibetan_chars = ['ཀ', 'ཁ', 'ག', 'ང', 'ཅ', 'ཆ', 'ཇ', 'ཉ', 'ཏ', 'ཐ', 'ད', 'ན', 'པ', 'ཕ', 'བ', 'མ', 'ཙ', 'ཚ', 'ཛ', 'ཝ', 'ཞ', 'ཟ', 'འ', 'ཡ', 'ར', 'ལ', 'ཤ', 'ས', 'ཧ', 'ཨ']
            for tibetan_char in tibetan_chars:
                if tibetan_char in text:
                    return True
        
        return False
            
    def clear_input(self):
        """清空当前输入"""
        if self.current_input_panel == "file":
            self.file_path_var.set("")
        else:
            self.input_text.delete("1.0", tk.END)
            
    def clear_all(self):
        """清除所有内容（输入和分析结果）"""
        # 清除输入
        self.file_path_var.set("")
        self.input_text.delete("1.0", tk.END)
        
        # 恢复提示文本
        self.input_text.insert("1.0", "བསྒྲིགས")
        self.input_text.configure(foreground="lightgray")
        
        # 清除分析结果
        for item in self.result_table.get_children():
            self.result_table.delete(item)
            
        self.detail_text.delete("1.0", tk.END)
        
        # 清除可视化视图
        self.visual_canvas.delete("all")
        
        # 重置数据和索引
        self.analysis_results = []
        self.current_tibetan = ""
        self.current_visual_index = 0
        
        # 更新可视化视图以显示提示信息
        self.update_visual_view()
        
        # 更新状态
        self.status_var.set("已清除所有内容")
        self.progress_var.set(0)
        
    def create_result_content(self):
        """创建结果区域内容 - 主区域和右侧按钮区域"""
        # 创建主框架，包含结果显示区域和按钮区域
        main_result_frame = ttk.Frame(self.result_card, style="Card.TFrame")
        main_result_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(5, 15))
        
        # 左侧结果显示区域
        result_display_frame = ttk.Frame(main_result_frame, style="Card.TFrame")
        result_display_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))
        
        # 右侧按钮区域 - 纵向排列
        result_button_frame = ttk.Frame(main_result_frame, style="Card.TFrame")
        result_button_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(15, 0))
        
        # 创建视图切换按钮
        table_view_button = ModernButton(result_button_frame, text="表格视图", 
                                      command=lambda: self.show_result_panel("table"),
                                      width=120, height=35, bg_color=self.COLORS["button"],
                                      hover_color=self.COLORS["button_hover"], 
                                      text_color=self.COLORS["text_light"],
                                      font=self.button_font)
        table_view_button.pack(pady=8)
        
        visual_view_button = ModernButton(result_button_frame, text="可视化视图", 
                                       command=lambda: self.show_result_panel("visual"),
                                       width=120, height=35, bg_color=self.COLORS["button"],
                                       hover_color=self.COLORS["button_hover"], 
                                       text_color=self.COLORS["text_light"],
                                       font=self.button_font)
        visual_view_button.pack(pady=8)
        
        detail_view_button = ModernButton(result_button_frame, text="详细信息", 
                                       command=lambda: self.show_result_panel("detail"),
                                       width=120, height=35, bg_color=self.COLORS["button"],
                                       hover_color=self.COLORS["button_hover"], 
                                       text_color=self.COLORS["text_light"],
                                       font=self.button_font)
        detail_view_button.pack(pady=8)
        
        # 导出按钮
        export_csv_button = ModernButton(result_button_frame, text="导出为CSV", 
                                      command=self.export_csv, 
                                      width=120, height=35, bg_color=self.COLORS["button"], 
                                      hover_color=self.COLORS["button_hover"], 
                                      text_color=self.COLORS["text_light"],
                                      font=self.button_font)
        export_csv_button.pack(pady=8)
        
        export_json_button = ModernButton(result_button_frame, text="导出为JSON", 
                                       command=self.export_json, 
                                       width=120, height=35, bg_color=self.COLORS["button"], 
                                       hover_color=self.COLORS["button_hover"], 
                                       text_color=self.COLORS["text_light"],
                                       font=self.button_font)
        export_json_button.pack(pady=8)
        
        # 清空内容按钮
        clear_button = ModernButton(result_button_frame, text="清除内容", 
                                 command=self.clear_all,
                                 width=120, height=35, bg_color=self.COLORS["button"],
                                 hover_color=self.COLORS["button_hover"], 
                                 text_color=self.COLORS["text_light"],
                                 font=self.button_font)
        clear_button.pack(pady=8)
        
        # 程序退出按钮
        exit_button = ModernButton(result_button_frame, text="程序退出", 
                                command=self.root.quit,
                                width=120, height=35, bg_color=self.COLORS["error"],
                                hover_color="#A52A2A",  # 深红色悬停
                                text_color=self.COLORS["text_light"],
                                font=self.button_font)
        exit_button.pack(pady=8)
        
        # 创建结果面板容器
        self.result_panel_container = ttk.Frame(result_display_frame, style="Card.TFrame")
        self.result_panel_container.pack(fill=tk.BOTH, expand=True)
        
        # 创建表格视图面板
        self.table_panel = ttk.Frame(self.result_panel_container, style="Card.TFrame")
        
        # 创建表格容器
        table_container = ttk.Frame(self.table_panel, style="Card.TFrame")
        table_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建表格
        columns = ('原字', '类型', '前加字', '上加字', '基字', '下加字', '再下加字', '元音', '后加字', '再后加字')
        self.result_table = ttk.Treeview(table_container, columns=columns, show='headings', height=15)
        
        # 设置列标题
        for col in columns:
            self.result_table.heading(col, text=col)
            self.result_table.column(col, width=80, anchor=tk.CENTER)
        
        # 添加滚动条
        y_scrollbar = ttk.Scrollbar(table_container, orient=tk.VERTICAL, command=self.result_table.yview)
        self.result_table.configure(yscroll=y_scrollbar.set)
        
        x_scrollbar = ttk.Scrollbar(table_container, orient=tk.HORIZONTAL, command=self.result_table.xview)
        self.result_table.configure(xscroll=x_scrollbar.set)
        
        # 放置组件
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.result_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 创建可视化视图面板
        self.visual_panel = ttk.Frame(self.result_panel_container, style="Card.TFrame")
        
        # 创建可视化容器
        visual_container = ttk.Frame(self.visual_panel, style="Card.TFrame")
        visual_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建导航按钮容器
        nav_container = ttk.Frame(visual_container, style="Card.TFrame")
        nav_container.pack(fill=tk.X, side=tk.BOTTOM, pady=5)
        
        # 创建左右导航按钮
        self.prev_button = ModernButton(nav_container, text="◀ 上一个", 
                                     command=self.show_prev_visual,
                                     width=100, height=30, bg_color=self.COLORS["button"],
                                     hover_color=self.COLORS["button_hover"], 
                                     text_color=self.COLORS["text_light"],
                                     font=self.button_font)
        self.prev_button.pack(side=tk.LEFT, padx=20)
        
        # 创建索引显示标签
        self.visual_index_var = tk.StringVar(value="1/1")
        self.visual_index_label = ttk.Label(nav_container, 
                                         textvariable=self.visual_index_var,
                                         font=self.text_font,
                                         style="Card.TLabel")
        self.visual_index_label.pack(side=tk.LEFT, expand=True)
        
        self.next_button = ModernButton(nav_container, text="下一个 ▶", 
                                     command=self.show_next_visual,
                                     width=100, height=30, bg_color=self.COLORS["button"],
                                     hover_color=self.COLORS["button_hover"], 
                                     text_color=self.COLORS["text_light"],
                                     font=self.button_font)
        self.next_button.pack(side=tk.RIGHT, padx=20)
        
        # 创建可视化画布
        self.visual_canvas = tk.Canvas(visual_container, bg="white", highlightthickness=1, highlightbackground=self.COLORS["border"])
        self.visual_canvas.pack(fill=tk.BOTH, expand=True)
        
        # 绑定鼠标事件用于左右滑动
        self.visual_canvas.bind("<ButtonPress-1>", self.on_canvas_press)
        self.visual_canvas.bind("<ButtonRelease-1>", self.on_canvas_release)
        self.visual_canvas.bind("<B1-Motion>", self.on_canvas_motion)
        
        # 创建详细信息面板
        self.detail_panel = ttk.Frame(self.result_panel_container, style="Card.TFrame")
        
        # 创建详细信息容器
        detail_container = ttk.Frame(self.detail_panel, style="Card.TFrame")
        detail_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.detail_text = ScrolledText(detail_container, 
                                     height=20,
                                     font=self.text_font,
                                     wrap=tk.WORD,
                                     background="white",
                                     borderwidth=1,
                                     relief=tk.SOLID)
        self.detail_text.pack(fill=tk.BOTH, expand=True)
        
        # 默认显示表格视图
        self.current_result_panel = "table"
        self.show_result_panel("table")
        
    def show_result_panel(self, panel_type):
        """显示指定的结果面板"""
        # 隐藏所有面板
        self.table_panel.pack_forget()
        self.visual_panel.pack_forget()
        self.detail_panel.pack_forget()
        
        # 显示指定面板
        if panel_type == "table":
            self.table_panel.pack(fill=tk.BOTH, expand=True)
            self.current_result_panel = "table"
        elif panel_type == "visual":
            self.visual_panel.pack(fill=tk.BOTH, expand=True)
            self.current_result_panel = "visual"
        else:
            self.detail_panel.pack(fill=tk.BOTH, expand=True)
            self.current_result_panel = "detail"
        
    def create_status_bar(self):
        """创建状态栏"""
        # 创建状态栏卡片
        status_card = ttk.Frame(self.root, style="Card.TFrame")
        status_card.pack(fill=tk.X, side=tk.BOTTOM, padx=20, pady=10)
        
        status_content = ttk.Frame(status_card, style="Card.TFrame")
        status_content.pack(fill=tk.X, padx=15, pady=10)
        
        self.status_var = tk.StringVar()
        status_label = ttk.Label(status_content, 
                              textvariable=self.status_var,
                              font=self.status_font,
                              style="Card.TLabel")
        status_label.pack(side=tk.LEFT)
        
        # 添加进度条
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(status_content, 
                                         variable=self.progress_var,
                                         length=300,
                                         mode='determinate',
                                         style="TProgressbar")
        self.progress_bar.pack(side=tk.RIGHT)
        
    def browse_file(self):
        """浏览文件"""
        file_path = filedialog.askopenfilename(
            title="选择藏文文件",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        if file_path:
            self.file_path_var.set(file_path)
            
    def on_window_resize(self, event):
        """窗口大小变化时调整各部分比例"""
        # 只处理来自根窗口的事件
        if event.widget == self.root:
            # 确保窗口已经绘制
            self.root.update_idletasks()
            
            # 获取窗口高度
            total_height = self.root.winfo_height()
            
            # 调整分割窗口的位置
            if total_height > 100:  # 确保窗口高度足够
                self.paned_window.sashpos(0, int(total_height * 0.20))
    
    def on_text_focus_in(self, event):
        """文本框获得焦点时清除提示文本"""
        if self.input_text.get("1.0", tk.END).strip() == "请输入藏文字符......":
            self.input_text.delete("1.0", tk.END)
            self.input_text.configure(foreground="black")
    
    def on_text_focus_out(self, event):
        """文本框失去焦点时恢复提示文本"""
        if not self.input_text.get("1.0", tk.END).strip():
            self.input_text.insert("1.0", "请输入藏文字符......")
            self.input_text.configure(foreground="lightgray")
    
    def on_text_key_press(self, event):
        """按键时清除提示文本"""
        if self.input_text.get("1.0", tk.END).strip() == "请输入藏文字符......":
            self.input_text.delete("1.0", tk.END)
            self.input_text.configure(foreground="black")

    def change_font(self, event):
        """更改藏文字体"""
        selected_font_name = self.font_var.get()
        
        # 获取字体路径或使用字体名称
        if selected_font_name in self.font_paths:
            self.tibetan_font = self.font_paths[selected_font_name]
        else:
            self.tibetan_font = selected_font_name
        
        # 更新字体
        self.title_font = (self.tibetan_font, 28, "bold")
        self.heading_font = (self.tibetan_font, 18, "bold")
        self.text_font = (self.tibetan_font, 14)
        self.button_font = (self.tibetan_font, 12, "bold")
        self.status_font = (self.tibetan_font, 10)
        
        # 更新输入文本框字体
        self.input_text.configure(font=self.text_font)
        self.detail_text.configure(font=self.text_font)
        
        # 刷新显示
        if self.analysis_results:
            self.update_visual_view()
            
    def analyze_file(self):
        """分析文件"""
        file_path = self.file_path_var.get()
        encoding = self.encoding_var.get()
        
        if not file_path:
            messagebox.showerror("错误", "请选择文件")
            return
            
        if not os.path.exists(file_path):
            messagebox.showerror("错误", f"文件不存在: {file_path}")
            return
            
        # 在单独的线程中处理文件
        threading.Thread(target=self._process_file, args=(file_path, encoding)).start()
        
    def _process_file(self, file_path, encoding):
        """在后台线程中处理文件"""
        try:
            self.status_var.set(f"正在分析文件: {os.path.basename(file_path)}...")
            self.progress_var.set(0)
            self.root.update_idletasks()
            
            # 清空之前的结果
            self.analysis_results = []
            
            # 读取文件
            with open(file_path, 'r', encoding=encoding) as f:
                lines = f.readlines()
                
            total_lines = len(lines)
            
            for i, line in enumerate(lines):
                line = line.strip()
                if not line:
                    continue
                    
                # 分析每个藏文字符
                result = cut(line)
                self.analysis_results.append(result)
                
                # 更新进度
                progress = (i + 1) / total_lines * 100
                self.progress_var.set(progress)
                
                if i % 10 == 0:  # 每10行更新一次UI
                    self.status_var.set(f"已分析 {i+1}/{total_lines} 行...")
                    self.root.update_idletasks()
            
            # 在主线程中更新UI
            self.root.after(0, self._update_results_ui)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("错误", f"分析文件时出错: {str(e)}"))
            self.status_var.set("分析失败")
            
    def analyze_text(self):
        """分析输入文本"""
        text = self.input_text.get("1.0", tk.END).strip()
        
        # 检查是否为提示文本
        if not text or text == "ཀ་ཁ་ག་ང་ཅ་ཆ་ཇ་ཉ་ཏ་ཐ་ད་ན་པ་ཕ་བ་མ་ཙ་ཚ་ཛ་ཝ་ཞ་ཟ་འ་ཡ་ར་ལ་ཤ་ས་ཧ་ཨ།":
            messagebox.showerror("错误", "请输入藏文文本")
            return
        
        # 检查是否包含藏文字符
        if not self.contains_tibetan(text):
            messagebox.showerror("错误", f"请输入藏文字符。当前输入：{repr(text)}")
            return
            
        # 清空之前的结果
        self.analysis_results = []
        
        # 分析每行文本
        lines = text.split('\n')
        total_lines = len(lines)
        
        self.status_var.set("正在分析输入文本...")
        self.progress_var.set(0)
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
                
            # 分析藏文字符
            try:
                result = cut(line)
                if isinstance(result, list):
                    self.analysis_results.extend(result)
                else:
                    self.analysis_results.append(result)
            except Exception as e:
                print(f"分析行 '{line}' 时出错: {e}")
                # 创建一个基本的结果结构
                basic_result = {
                    '原字': line,
                    '类型': '未知',
                    '前加字': '',
                    '上加字': '',
                    '基字': line,
                    '下加字': '',
                    '再下加字': '',
                    '元音': '',
                    '后加字': '',
                    '再后加字': ''
                }
                self.analysis_results.append(basic_result)
            
            # 更新进度
            progress = (i + 1) / total_lines * 100
            self.progress_var.set(progress)
            
        # 更新UI
        self._update_results_ui()
        
    def _update_results_ui(self):
        """更新结果UI"""
        # 更新表格
        self.update_table_view()
        
        # 重置可视化索引
        self.current_visual_index = 0
        
        # 更新可视化视图
        if self.analysis_results:
            self.current_tibetan = self.analysis_results[0]['原字']
            self.update_visual_view()
            
        # 更新详细信息
        self.update_detail_view()
        
        # 更新状态
        self.status_var.set(f"分析完成，共 {len(self.analysis_results)} 个结果")
        self.progress_var.set(100)
        
        # 切换到表格视图
        self.show_result_panel("table")
        
    def update_table_view(self):
        """更新表格视图"""
        # 清空表格
        for item in self.result_table.get_children():
            self.result_table.delete(item)
            
        # 添加新数据
        for result in self.analysis_results:
            values = [result.get('原字', ''), result.get('类型', '藏文字符')]
            
            for key in ('前加字', '上加字', '基字', '下加字', '再下加字', '元音', '后加字', '再后加字'):
                values.append(result.get(key, ''))
                
            self.result_table.insert('', tk.END, values=values)
            
    def on_canvas_press(self, event):
        """鼠标按下事件"""
        self.canvas_drag_start_x = event.x
        
    def on_canvas_release(self, event):
        """鼠标释放事件"""
        # 计算拖动距离
        if hasattr(self, 'canvas_drag_start_x'):
            drag_distance = event.x - self.canvas_drag_start_x
            
            # 如果拖动距离足够大，切换到上一个或下一个
            if drag_distance > 100 and len(self.analysis_results) > 1:  # 向右拖动，显示上一个
                self.show_prev_visual()
            elif drag_distance < -100 and len(self.analysis_results) > 1:  # 向左拖动，显示下一个
                self.show_next_visual()
                
    def on_canvas_motion(self, event):
        """鼠标移动事件"""
        # 可以添加拖动过程中的视觉反馈
        pass
        
    def show_prev_visual(self):
        """显示上一个可视化结果"""
        if not self.analysis_results or len(self.analysis_results) <= 1:
            return
            
        self.current_visual_index = (self.current_visual_index - 1) % len(self.analysis_results)
        self.update_visual_view()
        
    def show_next_visual(self):
        """显示下一个可视化结果"""
        if not self.analysis_results or len(self.analysis_results) <= 1:
            return
            
        self.current_visual_index = (self.current_visual_index + 1) % len(self.analysis_results)
        self.update_visual_view()
        
    def update_visual_view(self):
        """更新可视化视图 - 更加美观的可视化效果，始终居中显示"""
        # 清空画布
        self.visual_canvas.delete("all")
        
        if not self.analysis_results:
            # 如果没有分析结果，显示提示信息
            canvas_width = self.visual_canvas.winfo_width()
            canvas_height = self.visual_canvas.winfo_height()
            
            # 如果画布尚未渲染，使用默认尺寸
            if canvas_width <= 1:
                canvas_width = 800
            if canvas_height <= 1:
                canvas_height = 600
                
            # 绘制提示信息
            self.visual_canvas.create_text(
                canvas_width // 2, canvas_height // 2,
                text="请输入藏文字符进行分析",
                font=(self.tibetan_font, 20),
                fill=self.COLORS["secondary"]
            )
            
            # 更新导航按钮状态
            self.prev_button.configure(state=tk.DISABLED)
            self.next_button.configure(state=tk.DISABLED)
            self.visual_index_var.set("0/0")
            return
            
        # 更新导航按钮状态
        total_results = len(self.analysis_results)
        if total_results > 1:
            self.prev_button.configure(state=tk.NORMAL)
            self.next_button.configure(state=tk.NORMAL)
        else:
            self.prev_button.configure(state=tk.DISABLED)
            self.next_button.configure(state=tk.DISABLED)
            
        # 更新索引显示
        # 检查索引是否有效
        if self.current_visual_index >= len(self.analysis_results):
            self.current_visual_index = 0
            
        # 如果仍然没有结果，显示提示
        if not self.analysis_results:
            # 绘制提示信息
            self.visual_canvas.create_text(
                canvas_width // 2, canvas_height // 2,
                text="请输入藏文字符进行分析",
                font=(self.tibetan_font, 20),
                fill=self.COLORS["secondary"]
            )
            
            # 更新导航按钮状态
            self.prev_button.configure(state=tk.DISABLED)
            self.next_button.configure(state=tk.DISABLED)
            self.visual_index_var.set("0/0")
            return
            
        # 更新索引显示
        self.visual_index_var.set(f"{self.current_visual_index + 1}/{total_results}")
            
        # 获取当前索引的结果进行可视化
        result = self.analysis_results[self.current_visual_index]
        
        # 画布尺寸
        canvas_width = self.visual_canvas.winfo_width()
        canvas_height = self.visual_canvas.winfo_height()
        
        # 如果画布尚未渲染，使用默认尺寸
        if canvas_width <= 1:
            canvas_width = 800
        if canvas_height <= 1:
            canvas_height = 500
            
        # 中心点
        center_x = canvas_width // 2
        center_y = canvas_height // 2
        
        # 绘制背景
        self.visual_canvas.create_rectangle(
            0, 0, canvas_width, canvas_height,
            fill=self.COLORS["card_bg"],
            outline=""
        )
        
        # 检查是否为分隔符
        # 检查是否为分隔符
        if result.get('类型') in ['分隔符', '包含分隔符']:
            # 计算分隔符文本的实际尺寸
            temp_text = self.visual_canvas.create_text(
                0, 0, text=result['原字'], 
                font=(self.tibetan_font, 100, "bold")
            )
            text_bbox = self.visual_canvas.bbox(temp_text)
            self.visual_canvas.delete(temp_text)
            
            # 根据文本尺寸动态调整圆形背景大小
            if text_bbox:
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]
                # 计算需要的半径，确保文字完全包含在圆内
                radius = max(text_width, text_height) // 2 + 40
                radius = max(radius, 100)  # 最小半径100
            else:
                radius = 150
            
            # 绘制装饰性背景
            self.visual_canvas.create_oval(
                center_x - radius, center_y - radius,
                center_x + radius, center_y + radius,
                fill=self.COLORS["background"],
                outline=self.COLORS["accent"],
                width=3
            )
            
            # 添加光晕效果
            for i in range(3):
                size = radius - i * 10
                if size > 0:
                    self.visual_canvas.create_oval(
                        center_x - size, center_y - size,
                        center_x + size, center_y + size,
                        outline=self.COLORS["accent"],
                        width=1,
                        fill=""
                    )
            
            # 绘制分隔符（调整大小）
            self.visual_canvas.create_text(
                center_x, center_y,
                text=result['原字'],
                font=(self.tibetan_font, 100, "bold"),
                fill=self.COLORS["accent"]
            )
            
            # 添加分隔符说明
            self.visual_canvas.create_text(
                center_x, center_y + radius + 30,
                text=f"类型: {result.get('类型', '分隔符')}",
                font=(self.tibetan_font, 24),
                fill=self.COLORS["primary"]
            )
            return
        
        # 绘制装饰性背景
        radius = min(canvas_width, canvas_height) // 3
        self.visual_canvas.create_oval(
            center_x - radius, center_y - radius,
            center_x + radius, center_y + radius,
            fill=self.COLORS["background"],
            outline=self.COLORS["accent"],
            width=2
        )
        
        # 绘制原字背景 - 使用圆角矩形
        # 计算原字文本的实际尺寸
        temp_text = self.visual_canvas.create_text(
            0, 0, text=result['原字'], 
            font=(self.tibetan_font, 60, "bold")
        )
        text_bbox = self.visual_canvas.bbox(temp_text)
        self.visual_canvas.delete(temp_text)
        
        # 根据文本尺寸动态调整背景框大小
        if text_bbox:
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            # 添加适当的内边距
            rect_width = max(text_width + 60, 200)  # 最小宽度200
            rect_height = max(text_height + 40, 80)   # 最小高度80
        else:
            rect_width = 300
            rect_height = 100
        
        # 绘制原字背景 - 使用圆角矩形
        bg_y_top = center_y - 130 - rect_height//2
        bg_y_bottom = center_y - 130 + rect_height//2
        
        self.create_rounded_rectangle(
            self.visual_canvas,
            center_x - rect_width//2, bg_y_top,
            center_x + rect_width//2, bg_y_bottom,
            20,  # 圆角半径
            fill=self.COLORS["primary"],
            outline=self.COLORS["accent"],
            width=2
        )
        
        # 绘制原字（缩小）
        self.visual_canvas.create_text(
            center_x, center_y - 130,
            text=result['原字'],
            font=(self.tibetan_font, 60, "bold"),
            fill=self.COLORS["text_light"]
        )
        
        # 绘制构件连接图
        component_font_size = 22
        component_y = center_y + 60
        
        # 计算所有非空构件
        components = []
        for key in ('前加字', '上加字', '基字', '下加字', '再下加字', '元音', '后加字', '再后加字'):
            if result.get(key):
                components.append((key, result[key]))
                
        # 计算总宽度和每个组件的间距
        total_components = len(components)
        if total_components == 0:
            return
            
        # 动态计算组件间距，确保不会超出画布
        component_spacing = min(120, (canvas_width - 200) // max(total_components, 1))
        total_width = total_components * component_spacing
        start_x = center_x - total_width // 2 + component_spacing // 2
        
        # 绘制连接线背景
        self.visual_canvas.create_line(
            center_x, center_y - 80,
            center_x, center_y,
            fill=self.COLORS["accent"],
            width=3
        )
        
        # 绘制构件和连接线
        for i, (key, value) in enumerate(components):
            x = start_x + i * component_spacing
            
            # 绘制构件背景 - 使用渐变效果
            bg_radius = 40
            for r in range(bg_radius, bg_radius-10, -2):
                alpha = int(255 * (1 - (bg_radius - r) / 10))
                color = self.COLORS["accent"]
                self.visual_canvas.create_oval(
                    x - r, component_y - r,
                    x + r, component_y + r,
                    outline=color,
                    width=1
                )
            
            # 绘制构件背景
            self.visual_canvas.create_oval(
                x - bg_radius + 10, component_y - bg_radius + 10,
                x + bg_radius - 10, component_y + bg_radius - 10,
                fill=self.COLORS["background"],
                outline=self.COLORS["accent"],
                width=2
            )
            
            # 绘制构件
            self.visual_canvas.create_text(
                x, component_y,
                text=value,
                font=(self.tibetan_font, component_font_size),
                fill=self.COLORS["primary"]
            )
            
            # 绘制标签背景 - 使用圆角矩形
            label_width = len(key) * 12 + 20
            self.create_rounded_rectangle(
                self.visual_canvas,
                x - label_width//2, component_y + 60,
                x + label_width//2, component_y + 90,
                10,  # 圆角半径
                fill=self.COLORS["secondary"],
                outline=self.COLORS["accent"],
                width=1
            )
            
            # 绘制标签
            self.visual_canvas.create_text(
                x, component_y + 75,
                text=key,
                font=(self.tibetan_font, 14),
                fill=self.COLORS["text_light"]
            )
            
            # 绘制连接线 - 使用贝塞尔曲线效果
            self.visual_canvas.create_line(
                center_x, center_y,
                center_x, center_y + 20,
                x, component_y - bg_radius,
                smooth=True,
                fill=self.COLORS["accent"],
                width=2,
                splinesteps=36
            )
        
        # 绑定窗口大小变化事件，确保可视化视图始终居中显示
        self.visual_canvas.bind("<Configure>", lambda e: self.update_visual_view() if self.current_result_panel == "visual" else None)
    
    def create_rounded_rectangle(self, canvas, x1, y1, x2, y2, radius, **kwargs):
        """在画布上创建圆角矩形"""
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
        ]
        return canvas.create_polygon(points, smooth=True, **kwargs)
            
    def update_detail_view(self):
        """更新详细信息视图"""
        # 清空文本
        self.detail_text.delete("1.0", tk.END)
        
        if not self.analysis_results:
            return
            
        # 添加详细信息
        for i, result in enumerate(self.analysis_results):
            self.detail_text.insert(tk.END, f"藏文字符 #{i+1}:\n", "heading")
            self.detail_text.insert(tk.END, f"原字: {result['原字']}\n", "bold")
            
            if '类型' in result:
                self.detail_text.insert(tk.END, f"类型: {result['类型']}\n", "bold")
            
            for key in ('前加字', '上加字', '基字', '下加字', '再下加字', '元音', '后加字', '再后加字'):
                value = result.get(key)
                if value:
                    self.detail_text.insert(tk.END, f"{key}: {value}\n")
                    
            self.detail_text.insert(tk.END, "\n")
            
        # 配置文本标签
        self.detail_text.tag_configure("heading", font=(self.tibetan_font, 16, "bold"), foreground=self.COLORS["primary"])
        self.detail_text.tag_configure("bold", font=(self.tibetan_font, 14, "bold"))
            
    def export_csv(self):
        """导出为CSV文件"""
        if not self.analysis_results:
            messagebox.showerror("错误", "没有可导出的结果")
            return
            
        file_path = filedialog.asksaveasfilename(
            title="导出CSV文件",
            defaultextension=".csv",
            filetypes=[("CSV文件", "*.csv"), ("所有文件", "*.*")]
        )
        
        if not file_path:
            return
            
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=[
                    '原字', '类型', '前加字', '上加字', '基字', '下加字', '再下加字', '元音', '后加字', '再后加字'
                ])
                writer.writeheader()
                writer.writerows(self.analysis_results)
                
            messagebox.showinfo("成功", f"结果已导出到 {file_path}")
            
        except Exception as e:
            messagebox.showerror("错误", f"导出CSV时出错: {str(e)}")
            
    def export_json(self):
        """导出为JSON文件"""
        if not self.analysis_results:
            messagebox.showerror("错误", "没有可导出的结果")
            return
            
        file_path = filedialog.asksaveasfilename(
            title="导出JSON文件",
            defaultextension=".json",
            filetypes=[("JSON文件", "*.json"), ("所有文件", "*.*")]
        )
        
        if not file_path:
            return
            
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.analysis_results, f, ensure_ascii=False, indent=2)
                
            messagebox.showinfo("成功", f"结果已导出到 {file_path}")
            
        except Exception as e:
            messagebox.showerror("错误", f"导出JSON时出错: {str(e)}")


def main():
    """主函数"""
    root = tk.Tk()
    app = TibetanAnalyzerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
