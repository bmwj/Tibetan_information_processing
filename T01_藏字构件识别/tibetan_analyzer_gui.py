#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
藏文构件识别与分析工具 - GUI版本 (优化版)
重构代码结构，消除重复，美化界面
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
import time
from PIL import Image, ImageTk, ImageFilter, ImageEnhance, ImageDraw

# 获取项目根目录路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# 导入藏文分析函数
from T01_藏字构件识别.tibetan_analyzer import cut


class UIConstants:
    """UI常量配置类"""
    # 界面颜色主题 - 现代化配色方案
    COLORS = {
        "primary": "#2C3E50",       # 深蓝灰色
        "secondary": "#34495E",     # 中蓝灰色
        "accent": "#3498DB",        # 蓝色
        "success": "#27AE60",       # 绿色
        "warning": "#F39C12",       # 橙色
        "error": "#E74C3C",         # 红色
        "background": "#ECF0F1",    # 浅灰背景
        "card_bg": "#FFFFFF",       # 卡片背景
        "text": "#2C3E50",          # 深色文本
        "text_light": "#FFFFFF",    # 白色文本
        "text_muted": "#7F8C8D",    # 灰色文本
        "border": "#BDC3C7",        # 边框颜色
        "hover": "#E8F4FD",         # 悬停颜色
        "selected": "#D5DBDB",      # 选中颜色
    }
    
    # 字体配置
    FONT_SIZES = {
        "title": 24,
        "heading": 16,
        "text": 12,
        "button": 11,
        "status": 10
    }
    
    # 组件尺寸
    SIZES = {
        "button_width": 100,
        "button_height": 35,
        "padding": 10,
        "margin": 10,
        "border_radius": 8
    }
    
    # 占位提示文本
    PLACEHOLDER_TEXT = "请输入藏文字符进行分析..."
    
    # 藏文字符检测
    TIBETAN_CHARS = ['ཀ','ཁ','ག','ང','ཅ','ཆ','ཇ','ཉ','ཏ','ཐ','ད','ན','པ','ཕ','བ','མ','ཙ','ཚ','ཛ','ཝ','ཞ','ཟ','འ','ཡ','ར','ལ','ཤ','ས','ཧ','ཨ']


class ModernButton(tk.Canvas):
    """现代风格按钮组件"""
    
    def __init__(self, master, text, command=None, width=120, height=50, 
                 bg_color=None, hover_color=None, text_color=None, 
                 font=None, corner_radius=8, **kwargs):
        
        # 使用默认颜色配置
        self.bg_color = bg_color or UIConstants.COLORS["accent"]
        self.hover_color = hover_color or UIConstants.COLORS["primary"]
        self.text_color = text_color or UIConstants.COLORS["text_light"]
        self.corner_radius = corner_radius
        self.command = command
        self.text = text
        self.font = font or ("Arial", UIConstants.FONT_SIZES["button"])
        
        super().__init__(master, width=width, height=height, 
                         bg=UIConstants.COLORS["background"], 
                         highlightthickness=0, **kwargs)
        
        self._setup_events()
        self.draw_button(self.bg_color)
        
    def _setup_events(self):
        """设置事件绑定"""
        events = {
            "<Enter>": self._on_enter,
            "<Leave>": self._on_leave,
            "<Button-1>": self._on_click,
            "<ButtonRelease-1>": self._on_release,
            "<Configure>": self._on_configure
        }
        for event, handler in events.items():
            self.bind(event, handler)
    
    def draw_button(self, color):
        """绘制按钮"""
        self.delete("all")
        width = self.winfo_reqwidth() or self["width"]
        height = self.winfo_reqheight() or self["height"]
        
        # 创建圆角矩形
        self._create_rounded_rect(0, 0, width, height, 
                                 self.corner_radius, fill=color, outline="")
        
        # 添加文本
        self.create_text(width/2, height/2, text=self.text, 
                        fill=self.text_color, font=self.font)
    
    def _create_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        """创建圆角矩形"""
        points = [
            x1+radius, y1, x2-radius, y1, x2, y1, x2, y1+radius,
            x2, y2-radius, x2, y2, x2-radius, y2, x1+radius, y2,
            x1, y2, x1, y2-radius, x1, y1+radius, x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)
    
    def _on_enter(self, event):
        self.draw_button(self.hover_color)
    
    def _on_leave(self, event):
        self.draw_button(self.bg_color)
    
    def _on_click(self, event):
        self.draw_button(self.bg_color)
    
    def _on_release(self, event):
        self.draw_button(self.hover_color)
        if self.command:
            self.command()
    
    def _on_configure(self, event):
        self.draw_button(self.bg_color)


class FontManager:
    """字体管理器"""
    
    def __init__(self):
        self.available_fonts = []
        self.font_paths = {}
        self.current_font_name = None
        self._load_fonts()
    
    def _load_fonts(self):
        """加载藏文字体"""
        font_dir = os.path.join(project_root, "T01_藏字构件识别", "fontfile")
        default_font_file = "吞弥恰俊——尼赤乌坚体.ttf"
        default_font_path = os.path.join(font_dir, default_font_file)
        
        # 加载字体文件
        if os.path.exists(font_dir):
            for file_name in os.listdir(font_dir):
                if file_name.lower().endswith(('.ttf', '.otf')):
                    font_path = os.path.join(font_dir, file_name)
                    font_name = os.path.splitext(file_name)[0]
                    self.available_fonts.append(font_name)
                    self.font_paths[font_name] = font_path
        
        # 检查系统字体
        if not self.available_fonts:
            self._load_system_fonts()
        
        # 设置默认字体
        if os.path.exists(default_font_path):
            default_font_name = os.path.splitext(default_font_file)[0]
            self.current_font_name = default_font_name
            if default_font_name not in self.available_fonts:
                self.available_fonts.insert(0, default_font_name)
                self.font_paths[default_font_name] = default_font_path
        elif self.available_fonts:
            self.current_font_name = self.available_fonts[0]
        else:
            self.current_font_name = "Arial"
            self.available_fonts = ["Arial"]
            self.font_paths["Arial"] = "Arial"
    
    def _load_system_fonts(self):
        """加载系统藏文字体"""
        system_fonts = font.families()
        keywords = ["Tibetan", "藏文", "Jomolhari", "DDC Uchen", "Qomolangma"]
        
        for font_name in system_fonts:
            for keyword in keywords:
                if keyword.lower() in font_name.lower():
                    self.available_fonts.append(font_name)
                    self.font_paths[font_name] = font_name
                    break
    
    def get_font_path(self, font_name=None):
        """获取字体路径"""
        font_name = font_name or self.current_font_name
        return self.font_paths.get(font_name, font_name)
    
    def create_font(self, size, weight="normal"):
        """创建字体对象"""
        font_path = self.get_font_path()
        return (font_path, size, weight)


class StyleManager:
    """样式管理器"""
    
    def __init__(self, font_manager):
        self.font_manager = font_manager
        self.style = ttk.Style()
        self._configure_styles()
    
    def _configure_styles(self):
        """配置TTK样式"""
        colors = UIConstants.COLORS
        
        # 基础样式
        self.style.configure("TFrame", background=colors["background"])
        self.style.configure("Card.TFrame", background=colors["card_bg"], relief="flat")
        
        # 标签样式
        self.style.configure("TLabel", background=colors["background"], 
                           foreground=colors["text"])
        self.style.configure("Card.TLabel", background=colors["card_bg"], 
                           foreground=colors["text"])
        self.style.configure("Title.TLabel", 
                           font=self.font_manager.create_font(UIConstants.FONT_SIZES["title"], "bold"),
                           foreground=colors["primary"],
                           padding=(0, 5, 0, 5))#垂直内边距
        
        # 按钮样式
        self.style.configure("TButton", 
                           background=colors["accent"], 
                           foreground=colors["text_light"],
                           font=self.font_manager.create_font(UIConstants.FONT_SIZES["button"]),
                           padding=(15, 8), relief="flat", borderwidth=0)
        
        self.style.map("TButton",
                      background=[("active", colors["primary"]), 
                                ("pressed", colors["primary"])],
                      foreground=[("active", colors["text_light"])])
        
        # 表格样式
        self.style.configure("Treeview",
                           font=self.font_manager.create_font(UIConstants.FONT_SIZES["text"]),
                           rowheight=28, background="white", 
                           fieldbackground="white", borderwidth=0)
        
        self.style.configure("Treeview.Heading",
                           font=self.font_manager.create_font(UIConstants.FONT_SIZES["text"], "bold"),
                           background=colors["secondary"],
                           foreground="black")
        
        self.style.map("Treeview",
                      background=[("selected", colors["selected"])])
        
        # 其他组件样式
        self._configure_other_styles()
    
    def _configure_other_styles(self):
        """配置其他组件样式"""
        colors = UIConstants.COLORS
        
        # 选项卡样式
        self.style.configure("TNotebook", background=colors["background"], borderwidth=0)
        self.style.configure("TNotebook.Tab", 
                           background=colors["secondary"], 
                           foreground=colors["text_light"], padding=(20, 10))
        self.style.map("TNotebook.Tab",
                      background=[("selected", colors["primary"])],
                      foreground=[("selected", colors["text_light"])])
        
        # # 进度条样式 - 现代化美化
        # self.style.configure("TProgressbar", 
        #                    background=colors["accent"],
        #                    troughcolor=colors["background"],
        #                    borderwidth=0, thickness=12)
        
        # 自定义进度条样式 - 现代化渐变效果
        self.style.configure("Custom.Horizontal.TProgressbar",
                           background=colors["success"],
                           troughcolor="#F5F5F5",  # 更柔和的背景色
                           borderwidth=0,
                           lightcolor="#2ECC71",  # 亮绿色
                           darkcolor="#27AE60",   # 深绿色
                           thickness=10,          # 增加厚度
                           relief="flat")
        
        # # 动画进度条样式 - 带有光泽效果
        # self.style.configure("Animated.Horizontal.TProgressbar",
        #                    background="#4CAF50",
        #                    troughcolor="#E8F5E8",
        #                    borderwidth=1,
        #                    lightcolor="#66BB6A",
        #                    darkcolor="#388E3C",
        #                    thickness=28,
        #                    relief="raised")
        
        # 输入框样式
        self.style.configure("TEntry", 
                           font=self.font_manager.create_font(UIConstants.FONT_SIZES["text"]),
                           fieldbackground="white", borderwidth=1)
    
    def refresh_styles(self):
        """刷新样式"""
        self._configure_styles()


class TibetanTextValidator:
    """藏文文本验证器"""
    
    @staticmethod
    def contains_tibetan(text):
        """检查文本是否包含藏文字符"""
        # Unicode范围检查
        for char in text:
            if 0x0F00 <= ord(char) <= 0x0FFF:
                return True
        
        # 常见藏文字符检查
        if text and not text.isascii():
            for tibetan_char in UIConstants.TIBETAN_CHARS:
                if tibetan_char in text:
                    return True
        
        return False
    
    @staticmethod
    def is_placeholder(text):
        """检查是否为占位符文本"""
        return not text or text.strip() == UIConstants.PLACEHOLDER_TEXT


class AnimationManager:
    """动画管理器"""
    
    def __init__(self, canvas, font_manager):
        self.canvas = canvas
        self.font_manager = font_manager
        self.animation_in_progress = False
        self.animation_items = []
        self.animation_speed = 10
    
    def cancel_animation(self):
        """取消当前动画"""
        self.animation_in_progress = False
        self.animation_items = []
    
    def create_fade_in_animation(self, x, y, text, font_size, callback=None):
        """创建淡入动画"""
        steps = 10
        font_path = self.font_manager.get_font_path()
        
        def animate_step(step=0):
            if step >= steps:
                text_item = self.canvas.create_text(
                    x, y, text=text,
                    font=(font_path, font_size, "bold"),
                    fill=UIConstants.COLORS["primary"]
                )
                if callback:
                    callback()
                return
            
            if step > 0:
                self.canvas.delete(f"fade_text_{step-1}")
            
            text_item = self.canvas.create_text(
                x, y, text=text,
                font=(font_path, font_size, "bold"),
                fill=UIConstants.COLORS["primary"],
                tags=f"fade_text_{step}"
            )
            
            self.canvas.after(self.animation_speed, 
                            lambda: animate_step(step + 1))
        
        animate_step()


class TibetanAnalyzerApp:
    """藏文构件识别与分析工具主应用"""
    
    def __init__(self, root):
        self.root = root
        self._setup_window()
        self._initialize_managers()
        self._initialize_variables()
        self._create_ui()
        self._setup_bindings()
    
    def _setup_window(self):
        """设置窗口属性"""
        self.root.title("藏文构件识别与分析工具")
        self.root.geometry("1400x900")
        self.root.configure(bg=UIConstants.COLORS["background"])
        self.root.minsize(1200, 800)
    
    def _initialize_managers(self):
        """初始化管理器"""
        self.font_manager = FontManager()
        self.style_manager = StyleManager(self.font_manager)
        self.validator = TibetanTextValidator()
    
    def _initialize_variables(self):
        """初始化变量"""
        self.current_input_panel = "file"
        self.current_result_panel = "table"
        self.current_tibetan = ""
        self.analysis_results = []
        self.current_visual_index = 0
        
        # 状态变量
        self.status_var = tk.StringVar(value="就绪")
        self.progress_var = tk.DoubleVar()
        self.font_var = tk.StringVar(value=self.font_manager.current_font_name)
    
    def _create_ui(self):
        """创建用户界面"""
        self._create_main_frame()
        self._create_title_bar()
        self._create_content_area()
        self._create_status_bar()
    
    def _create_main_frame(self):
        """创建主框架"""
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, 
                           padx=UIConstants.SIZES["padding"], 
                           pady=UIConstants.SIZES["padding"])
    
    def _create_title_bar(self):
        """创建标题栏"""
        title_card = ttk.Frame(self.main_frame, style="Card.TFrame")
        title_card.pack(fill=tk.X, pady=(0, UIConstants.SIZES["margin"]), ipady=10)
        
        # 装饰线
        decoration = tk.Canvas(title_card, height=2, 
                             bg=UIConstants.COLORS["accent"], 
                             highlightthickness=0)
        decoration.pack(fill=tk.X, side=tk.TOP)
        
        # 标题内容
        title_content = ttk.Frame(title_card, style="Card.TFrame")
        title_content.pack(fill=tk.X, padx=20, pady=10)
        
        # 标题文本
        title_label = ttk.Label(title_content, 
                              text="藏文构件识别与分析工具-བོད་ཡིག་གི་ལྷུ་ལག་ངོས་འཛིན་དང་དབྱེ་ཞིབ་ཡོ་བྱད།", 
                              style="Title.TLabel",
                              )
        title_label.pack(side=tk.LEFT)
    
    def _create_content_area(self):
        """创建内容区域"""
        self.paned_window = ttk.PanedWindow(self.main_frame, orient=tk.VERTICAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # 创建输入和结果区域
        self._create_input_area()
        self._create_result_area()
        
        # 设置分割比例
        self.paned_window.add(self.input_card, weight=20)
        self.paned_window.add(self.result_card, weight=60)
    
    def _create_input_area(self):
        """创建输入区域"""
        self.input_card = ttk.Frame(self.paned_window, style="Card.TFrame")
        
        # 输入区域主框架
        main_input_frame = ttk.Frame(self.input_card, style="Card.TFrame")
        main_input_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # 左侧输入区域
        input_area_frame = ttk.Frame(main_input_frame, style="Card.TFrame")
        input_area_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # 右侧按钮区域
        self._create_input_buttons(main_input_frame)
        
        # 输入面板容器
        self._create_input_panels(input_area_frame)
    
    def _create_input_buttons(self, parent):
        """创建输入区域按钮"""
        button_frame = ttk.Frame(parent, style="Card.TFrame")
        button_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        
        buttons = [
            ("📃 文件输入", lambda: self._show_input_panel("file"), UIConstants.COLORS["accent"]),
            ("⌨️ 直接输入", lambda: self._show_input_panel("direct"), UIConstants.COLORS["accent"]),
            ("📊 开始分析", self._analyze_current, UIConstants.COLORS["success"]),
        ]
        
        for text, command, color in buttons:
            btn = ModernButton(button_frame, text=text, command=command,
                             width=UIConstants.SIZES["button_width"],
                             height=UIConstants.SIZES["button_height"],
                             bg_color=color,
                             font=self.font_manager.create_font(UIConstants.FONT_SIZES["button"]))
            btn.pack(pady=8)
    
    def _create_input_panels(self, parent):
        """创建输入面板"""
        self.input_panel_container = ttk.Frame(parent, style="Card.TFrame")
        self.input_panel_container.pack(fill=tk.BOTH, expand=True)
        
        # 文件输入面板
        self._create_file_input_panel()
        
        # 直接输入面板
        self._create_direct_input_panel()
        
        # 默认显示文件输入面板
        self._show_input_panel("file")
    
    def _create_file_input_panel(self):
        """创建文件输入面板"""
        self.file_input_panel = ttk.Frame(self.input_panel_container, style="Card.TFrame")
        
        # 文件路径选择
        file_path_frame = ttk.Frame(self.file_input_panel, style="Card.TFrame")
        file_path_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.file_path_var = tk.StringVar()
        file_entry = ttk.Entry(file_path_frame, textvariable=self.file_path_var, width=50)
        file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        browse_btn = ModernButton(file_path_frame, text="📁 浏览...", 
                                command=self._browse_file,
                                width=80, height=35,
                                bg_color=UIConstants.COLORS["secondary"])
        browse_btn.pack(side=tk.RIGHT)
        
        # 编码选择
        self._create_encoding_selector(self.file_input_panel)
    
    def _create_encoding_selector(self, parent):
        """创建编码选择器"""
        encoding_frame = ttk.Frame(parent, style="Card.TFrame")
        encoding_frame.pack(fill=tk.X)
        
        ttk.Label(encoding_frame, text="文件编码:", style="Card.TLabel").pack(anchor=tk.W, pady=(0, 5))
        
        encoding_options = ttk.Frame(encoding_frame, style="Card.TFrame")
        encoding_options.pack(fill=tk.X)
        
        self.encoding_var = tk.StringVar(value="utf-8")
        encodings = ["utf-8", "utf-16", "utf-16-le", "utf-16-be", "gb18030"]
        
        for i, enc in enumerate(encodings):
            rb = ttk.Radiobutton(encoding_options, text=enc, 
                               variable=self.encoding_var, value=enc)
            rb.grid(row=0, column=i, padx=15, pady=5, sticky="w")
    
    def _create_direct_input_panel(self):
        """创建直接输入面板"""
        self.direct_input_panel = ttk.Frame(self.input_panel_container, style="Card.TFrame")
        
        text_container = ttk.Frame(self.direct_input_panel, style="Card.TFrame")
        text_container.pack(fill=tk.BOTH, expand=True)
        
        self.input_text = ScrolledText(text_container, 
                                     height=4,
                                     font=self.font_manager.create_font(UIConstants.FONT_SIZES["text"]),
                                     wrap=tk.WORD, background="white",
                                     borderwidth=1, relief=tk.SOLID)
        self.input_text.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # 设置占位符
        self._setup_placeholder()
    
    def _setup_placeholder(self):
        """设置占位符文本"""
        self.input_text.insert("1.0", UIConstants.PLACEHOLDER_TEXT)
        self.input_text.configure(foreground=UIConstants.COLORS["text_muted"])
        
        # 绑定事件
        self.input_text.bind("<FocusIn>", self._on_text_focus_in)
        self.input_text.bind("<FocusOut>", self._on_text_focus_out)
        self.input_text.bind("<KeyPress>", self._on_text_key_press)
    
    def _create_result_area(self):
        """创建结果区域"""
        self.result_card = ttk.Frame(self.paned_window, style="Card.TFrame")
        
        # 结果区域主框架
        main_result_frame = ttk.Frame(self.result_card, style="Card.TFrame")
        main_result_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # 左侧结果显示区域 - 增加宽度比例
        result_display_frame = ttk.Frame(main_result_frame, style="Card.TFrame")
        result_display_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))
        
        # 右侧按钮区域
        self._create_result_buttons(main_result_frame)
        
        # 结果面板容器
        self._create_result_panels(result_display_frame)
    
    def _create_result_buttons(self, parent):
        """创建结果区域按钮"""
        button_frame = ttk.Frame(parent, style="Card.TFrame")
        button_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(15, 0))
        
        buttons = [
            ("🗳️ 表格视图", lambda: self._show_result_panel("table"), UIConstants.COLORS["accent"]),
            ("📊 可视化视图", lambda: self._show_result_panel("visual"), UIConstants.COLORS["accent"]),
            ("💻 详细信息", lambda: self._show_result_panel("detail"), UIConstants.COLORS["accent"]),
            ("📖 导出CSV", self._export_csv, UIConstants.COLORS["secondary"]),
            ("📖 导出JSON", self._export_json, UIConstants.COLORS["secondary"]),
            ("🗑️ 清除内容", self._clear_all, UIConstants.COLORS["warning"]),
            ("❌ 退出程序", self.root.quit, UIConstants.COLORS["error"]),
        ]
        
        for text, command, color in buttons:
            btn = ModernButton(button_frame, text=text, command=command,
                             width=UIConstants.SIZES["button_width"],
                             height=UIConstants.SIZES["button_height"],
                             bg_color=color,
                             font=self.font_manager.create_font(UIConstants.FONT_SIZES["button"]))
            btn.pack(pady=6)
    
    def _create_result_panels(self, parent):
        """创建结果面板"""
        self.result_panel_container = ttk.Frame(parent, style="Card.TFrame")
        self.result_panel_container.pack(fill=tk.BOTH, expand=True)
        
        # 创建各个结果面板
        self._create_table_panel()
        self._create_visual_panel()
        self._create_detail_panel()
        
        # 默认显示表格视图
        self._show_result_panel("table")
    
    def _create_table_panel(self):
        """创建表格面板"""
        self.table_panel = ttk.Frame(self.result_panel_container, style="Card.TFrame")
        
        table_container = ttk.Frame(self.table_panel, style="Card.TFrame")
        table_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建表格
        columns = ('原字', '类型', '前加字', '上加字', '基字', '下加字', '再下加字', '元音', '后加字', '再后加字')
        self.result_table = ttk.Treeview(table_container, columns=columns, 
                                       show='headings', height=20)
        
        # 设置列
        for col in columns:
            self.result_table.heading(col, text=col)
            self.result_table.column(col, width=90, anchor=tk.CENTER)
        
        # 添加滚动条
        y_scrollbar = ttk.Scrollbar(table_container, orient=tk.VERTICAL, 
                                  command=self.result_table.yview)
        self.result_table.configure(yscroll=y_scrollbar.set)
        
        x_scrollbar = ttk.Scrollbar(table_container, orient=tk.HORIZONTAL, 
                                  command=self.result_table.xview)
        self.result_table.configure(xscroll=x_scrollbar.set)
        
        # 布局组件
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.result_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    def _create_visual_panel(self):
        """创建可视化面板"""
        self.visual_panel = ttk.Frame(self.result_panel_container, style="Card.TFrame")
        
        visual_container = ttk.Frame(self.visual_panel, style="Card.TFrame")
        visual_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 导航按钮容器
        nav_container = ttk.Frame(visual_container, style="Card.TFrame")
        nav_container.pack(fill=tk.X, side=tk.BOTTOM, pady=10)
        
        # 导航按钮
        self.prev_button = ModernButton(nav_container, text="◀ 上一个", 
                                      command=self._show_prev_visual,
                                      width=100, height=30,
                                      bg_color=UIConstants.COLORS["secondary"])
        self.prev_button.pack(side=tk.LEFT, padx=20)
        
        # 索引显示
        self.visual_index_var = tk.StringVar(value="0/0")
        index_label = ttk.Label(nav_container, textvariable=self.visual_index_var,
                              font=self.font_manager.create_font(UIConstants.FONT_SIZES["text"]),
                              style="Card.TLabel")
        index_label.pack(side=tk.LEFT, expand=True)
        
        self.next_button = ModernButton(nav_container, text="下一个 ▶", 
                                      command=self._show_next_visual,
                                      width=100, height=30,
                                      bg_color=UIConstants.COLORS["secondary"])
        self.next_button.pack(side=tk.RIGHT, padx=20)
        
        # 可视化画布
        self.visual_canvas = tk.Canvas(visual_container, bg="white", 
                                     highlightthickness=1, 
                                     highlightbackground=UIConstants.COLORS["border"])
        self.visual_canvas.pack(fill=tk.BOTH, expand=True)
        
        # 初始化动画管理器
        self.animation_manager = AnimationManager(self.visual_canvas, self.font_manager)
    
    def _create_detail_panel(self):
        """创建详细信息面板"""
        self.detail_panel = ttk.Frame(self.result_panel_container, style="Card.TFrame")
        
        detail_container = ttk.Frame(self.detail_panel, style="Card.TFrame")
        detail_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.detail_text = ScrolledText(detail_container, 
                                      height=25,
                                      font=self.font_manager.create_font(UIConstants.FONT_SIZES["text"]),
                                      wrap=tk.WORD, background="white",
                                      borderwidth=1, relief=tk.SOLID)
        self.detail_text.pack(fill=tk.BOTH, expand=True)
    
    def _create_status_bar(self):
        """创建状态栏"""
        # 创建一个完全独立的状态栏，确保它不会被其他组件影响
        status_frame = tk.Frame(self.root, bg=UIConstants.COLORS["card_bg"], height=60)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM, 
                        padx=UIConstants.SIZES["padding"], 
                        pady=(0, UIConstants.SIZES["padding"]))
        status_frame.pack_propagate(False)  # 防止高度被压缩
        
        # 添加醒目的顶部边框
        border = tk.Frame(status_frame, height=3, bg=UIConstants.COLORS["accent"])
        border.pack(fill=tk.X, side=tk.TOP)
        
        # 内容容器 - 使用tk.Frame而不是ttk.Frame以确保更好的控制
        status_content = tk.Frame(status_frame, bg=UIConstants.COLORS["card_bg"])
        status_content.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # 状态标签 - 使用tk.Label
        status_label = tk.Label(status_content, 
                              textvariable=self.status_var,
                              font=self.font_manager.create_font(UIConstants.FONT_SIZES["status"], "bold"),
                              bg=UIConstants.COLORS["card_bg"],
                              fg=UIConstants.COLORS["text"])
        status_label.pack(side=tk.LEFT, anchor=tk.W)
        
        # 右侧进度信息 - 使用tk.Frame
        progress_frame = tk.Frame(status_content, bg=UIConstants.COLORS["card_bg"])
        progress_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 进度条标签
        progress_label = tk.Label(progress_frame, 
                                text="进度:",
                                font=self.font_manager.create_font(UIConstants.FONT_SIZES["status"], "bold"),
                                bg=UIConstants.COLORS["card_bg"],
                                fg=UIConstants.COLORS["text"])
        progress_label.pack(side=tk.LEFT, padx=(0, 5))
        
        # 进度条 - 使用ttk.Progressbar但确保它有足够的空间
        self.progress_bar = ttk.Progressbar(progress_frame, 
                                          variable=self.progress_var,
                                          length=250, 
                                          mode='determinate',
                                          style="Custom.Horizontal.TProgressbar")
        self.progress_bar.pack(side=tk.LEFT, pady=5)
        
        # 进度百分比标签
        self.progress_percent_var = tk.StringVar(value="0%")
        progress_percent_label = tk.Label(progress_frame, 
                                        textvariable=self.progress_percent_var,
                                        font=self.font_manager.create_font(UIConstants.FONT_SIZES["status"], "bold"),
                                        bg=UIConstants.COLORS["card_bg"],
                                        fg=UIConstants.COLORS["text"])
        progress_percent_label.pack(side=tk.LEFT, padx=(5, 0))
    
    def _setup_bindings(self):
        """设置事件绑定"""
        self.root.bind("<Configure>", self._on_window_resize)
    
    # 事件处理方法
    def _on_font_change(self, event):
        """字体更改事件"""
        selected_font = self.font_var.get()
        self.font_manager.current_font_name = selected_font
        self.style_manager.refresh_styles()
        
        # 更新文本组件字体
        text_font = self.font_manager.create_font(UIConstants.FONT_SIZES["text"])
        self.input_text.configure(font=text_font)
        self.detail_text.configure(font=text_font)
        
        # 刷新可视化视图
        if self.analysis_results:
            self._update_visual_view()
        
        self.status_var.set(f"字体已更改为: {selected_font}")
    
    def _on_window_resize(self, event):
        """窗口大小调整事件"""
        if event.widget == self.root:
            self.root.update_idletasks()
            total_height = self.root.winfo_height()
            if total_height > 100:
                self.paned_window.sashpos(0, int(total_height * 0.25))
    
    def _on_text_focus_in(self, event):
        """文本框获得焦点"""
        current_text = self.input_text.get("1.0", tk.END).strip()
        if current_text == UIConstants.PLACEHOLDER_TEXT:
            self.input_text.delete("1.0", tk.END)
            self.input_text.configure(foreground=UIConstants.COLORS["text"])
    
    def _on_text_focus_out(self, event):
        """文本框失去焦点"""
        current_text = self.input_text.get("1.0", tk.END).strip()
        if not current_text:
            self.input_text.insert("1.0", UIConstants.PLACEHOLDER_TEXT)
            self.input_text.configure(foreground=UIConstants.COLORS["text_muted"])
    
    def _on_text_key_press(self, event):
        """按键事件"""
        current_text = self.input_text.get("1.0", tk.END).strip()
        if current_text == UIConstants.PLACEHOLDER_TEXT:
            self.input_text.delete("1.0", tk.END)
            self.input_text.configure(foreground=UIConstants.COLORS["text"])
    
    # 界面控制方法
    def _show_input_panel(self, panel_type):
        """显示输入面板"""
        self.file_input_panel.pack_forget()
        self.direct_input_panel.pack_forget()
        
        if panel_type == "file":
            self.file_input_panel.pack(fill=tk.BOTH, expand=True)
            self.current_input_panel = "file"
        else:
            self.direct_input_panel.pack(fill=tk.BOTH, expand=True)
            self.current_input_panel = "direct"
    
    def _show_result_panel(self, panel_type):
        """显示结果面板"""
        self.table_panel.pack_forget()
        self.visual_panel.pack_forget()
        self.detail_panel.pack_forget()
        
        if panel_type == "table":
            self.table_panel.pack(fill=tk.BOTH, expand=True)
            self.current_result_panel = "table"
        elif panel_type == "visual":
            self.visual_panel.pack(fill=tk.BOTH, expand=True)
            self.current_result_panel = "visual"
            self._update_visual_view()
        else:
            self.detail_panel.pack(fill=tk.BOTH, expand=True)
            self.current_result_panel = "detail"
            self._update_detail_view()
    
    # 核心功能方法
    def _browse_file(self):
        """浏览文件"""
        file_path = filedialog.askopenfilename(
            title="选择藏文文件",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        if file_path:
            self.file_path_var.set(file_path)
    
    def _analyze_current(self):
        """分析当前输入"""
        if self.current_input_panel == "file":
            self._analyze_file()
        else:
            self._analyze_text()
    
    def _analyze_file(self):
        """分析文件"""
        file_path = self.file_path_var.get()
        if not file_path:
            messagebox.showerror("错误", "请选择文件")
            return
        
        if not os.path.exists(file_path):
            messagebox.showerror("错误", f"文件不存在: {file_path}")
            return
        
        # 验证文件内容
        try:
            encoding = self.encoding_var.get()
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read(100)
            if not self.validator.contains_tibetan(content):
                messagebox.showerror("错误", "文件不包含藏文字符")
                return
        except Exception as e:
            messagebox.showerror("错误", f"读取文件失败: {str(e)}")
            return
        
        # 在后台线程中处理
        threading.Thread(target=self._process_file, 
                        args=(file_path, encoding), daemon=True).start()
    
    def _analyze_text(self):
        """分析文本输入"""
        text = self.input_text.get("1.0", tk.END).strip()
        
        if self.validator.is_placeholder(text):
            messagebox.showerror("错误", "请输入藏文文本")
            return
        
        if not self.validator.contains_tibetan(text):
            messagebox.showerror("错误", "请输入藏文字符")
            return
        
        self._process_text(text)
    
    def _process_file(self, file_path, encoding):
        """处理文件分析"""
        try:
            self.status_var.set(f"正在分析文件: {os.path.basename(file_path)}...")
            self.progress_var.set(0)
            
            self.analysis_results = []
            
            with open(file_path, 'r', encoding=encoding) as f:
                lines = f.readlines()
            
            total_lines = len(lines)
            
            for i, line in enumerate(lines):
                line = line.strip()
                if not line:
                    continue
                
                result = cut(line)
                if isinstance(result, list):
                    self.analysis_results.extend(result)
                else:
                    self.analysis_results.append(result)
                
                progress = (i + 1) / total_lines * 100
                progress = (i + 1) / total_lines * 100
                self.progress_var.set(progress)
                self.progress_percent_var.set(f"{int(progress)}%")
                
                if i % 10 == 0:
                    self.status_var.set(f"已分析 {i+1}/{total_lines} 行...")
                    self.root.update_idletasks()
            
            self.root.after(0, self._update_results_ui)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("错误", f"分析文件时出错: {str(e)}"))
            self.status_var.set("分析失败")
    
    def _process_text(self, text):
        """处理文本分析"""
        self.status_var.set("正在分析输入文本...")
        self.progress_var.set(0)
        
        self.analysis_results = []
        lines = text.split('\n')
        total_lines = len(lines)
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            try:
                result = cut(line)
                if isinstance(result, list):
                    self.analysis_results.extend(result)
                else:
                    self.analysis_results.append(result)
            except Exception as e:
                print(f"分析行 '{line}' 时出错: {e}")
                # 创建基本结果结构
                basic_result = {
                    '原字': line, '类型': '未知', '前加字': '', '上加字': '',
                    '基字': line, '下加字': '', '再下加字': '', '元音': '',
                    '后加字': '', '再后加字': ''
                }
                self.analysis_results.append(basic_result)
            
            progress = (i + 1) / total_lines * 100
            progress = (i + 1) / total_lines * 100
            self.progress_var.set(progress)
            self.progress_percent_var.set(f"{int(progress)}%")
        
        self._update_results_ui()
    
    def _update_results_ui(self):
        """更新结果UI"""
        self._update_table_view()
        self.current_visual_index = 0
        
        if self.analysis_results:
            self.current_tibetan = self.analysis_results[0]['原字']
        
        self.status_var.set(f"分析完成，共 {len(self.analysis_results)} 个结果")
        self.progress_var.set(100)
        self._show_result_panel("table")
    
    def _update_table_view(self):
        """更新表格视图"""
        # 清空表格
        for item in self.result_table.get_children():
            self.result_table.delete(item)
        
        # 添加数据
        for result in self.analysis_results:
            values = [result.get('原字', ''), result.get('类型', '藏文字符')]
            for key in ('前加字', '上加字', '基字', '下加字', '再下加字', '元音', '后加字', '再后加字'):
                values.append(result.get(key, ''))
            self.result_table.insert('', tk.END, values=values)
    
    def _update_visual_view(self):
        """更新可视化视图"""
        if not self.analysis_results:
            self._show_empty_visual()
            return
        
        # 更新导航状态
        total_results = len(self.analysis_results)
        self.visual_index_var.set(f"{self.current_visual_index + 1}/{total_results}")
        
        if total_results > 1:
            self.prev_button.configure(state=tk.NORMAL)
            self.next_button.configure(state=tk.NORMAL)
        else:
            self.prev_button.configure(state=tk.DISABLED)
            self.next_button.configure(state=tk.DISABLED)
        
        # 显示当前结果
        self._draw_current_result()
    
    def _show_empty_visual(self):
        """显示空的可视化视图"""
        self.visual_canvas.delete("all")
        canvas_width = self.visual_canvas.winfo_width() or 800
        canvas_height = self.visual_canvas.winfo_height() or 600
        
        self.visual_canvas.create_text(
            canvas_width // 2, canvas_height // 2,
            text="请输入藏文字符进行分析",
            font=self.font_manager.create_font(20),
            fill=UIConstants.COLORS["text_muted"]
        )
        
        self.prev_button.configure(state=tk.DISABLED)
        self.next_button.configure(state=tk.DISABLED)
        self.visual_index_var.set("0/0")
    
    def _draw_current_result(self):
        """绘制当前结果"""
        if self.current_visual_index >= len(self.analysis_results):
            self.current_visual_index = 0
        
        result = self.analysis_results[self.current_visual_index]
        self.visual_canvas.delete("all")
        
        canvas_width = self.visual_canvas.winfo_width() or 800
        canvas_height = self.visual_canvas.winfo_height() or 400
        
        # 绘制背景
        self.visual_canvas.create_rectangle(
            0, 0, canvas_width, canvas_height,
            fill=UIConstants.COLORS["card_bg"], outline=""
        )
        
        center_x = canvas_width // 2
        center_y = canvas_height // 2
        
        # 绘制原字
        font_path = self.font_manager.get_font_path()
        self.visual_canvas.create_text(
            center_x, center_y - 100,
            text=result['原字'],
            font=(font_path, 48, "bold"),
            fill=UIConstants.COLORS["primary"]
        )
        
        # 绘制构件信息
        self._draw_components(result, center_x, center_y, canvas_width)
    
    def _draw_components(self, result, center_x, center_y, canvas_width):
        """绘制构件信息"""
        components = []
        for key in ('前加字', '上加字', '基字', '下加字', '再下加字', '元音', '后加字', '再后加字'):
            if result.get(key):
                components.append((key, result[key]))
        
        if not components:
            return
        
        # 计算布局
        total_components = len(components)
        component_spacing = min(120, (canvas_width - 200) // max(total_components, 1))
        total_width = total_components * component_spacing
        start_x = center_x - total_width // 2 + component_spacing // 2
        
        component_y = center_y + 50
        
        # 绘制构件
        for i, (key, value) in enumerate(components):
            x = start_x + i * component_spacing
            
            # 绘制构件背景
            self.visual_canvas.create_oval(
                x - 30, component_y - 30,
                x + 30, component_y + 30,
                fill=UIConstants.COLORS["hover"],
                outline=UIConstants.COLORS["accent"],
                width=2
            )
            
            # 绘制构件文字
            font_path = self.font_manager.get_font_path()
            self.visual_canvas.create_text(
                x, component_y,
                text=value,
                font=(font_path, 18, "bold"),
                fill=UIConstants.COLORS["primary"]
            )
            
            # 绘制标签
            self.visual_canvas.create_text(
                x, component_y + 50,
                text=key,
                font=(font_path, 12),
                fill=UIConstants.COLORS["text_muted"]
            )
            
            # 绘制连接线
            self.visual_canvas.create_line(
                center_x, center_y - 60,
                x, component_y - 30,
                fill=UIConstants.COLORS["border"],
                width=2, smooth=True
            )
    
    def _update_detail_view(self):
        """更新详细信息视图"""
        self.detail_text.delete("1.0", tk.END)
        
        if not self.analysis_results:
            return
        
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
        font_path = self.font_manager.get_font_path()
        self.detail_text.tag_configure("heading", 
                                     font=(font_path, 16, "bold"), 
                                     foreground=UIConstants.COLORS["primary"])
        self.detail_text.tag_configure("bold", 
                                     font=(font_path, 14, "bold"))
    
    # 导航方法
    def _show_prev_visual(self):
        """显示上一个可视化结果"""
        if not self.analysis_results or len(self.analysis_results) <= 1:
            return
        
        self.current_visual_index = (self.current_visual_index - 1) % len(self.analysis_results)
        self._update_visual_view()
    
    def _show_next_visual(self):
        """显示下一个可视化结果"""
        if not self.analysis_results or len(self.analysis_results) <= 1:
            return
        
        self.current_visual_index = (self.current_visual_index + 1) % len(self.analysis_results)
        self._update_visual_view()
    
    # 导出方法
    def _export_csv(self):
        """导出CSV文件"""
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
                fieldnames = ['原字', '类型', '前加字', '上加字', '基字', '下加字', '再下加字', '元音', '后加字', '再后加字']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.analysis_results)
            
            messagebox.showinfo("成功", f"结果已导出到 {file_path}")
            
        except Exception as e:
            messagebox.showerror("错误", f"导出CSV时出错: {str(e)}")
    
    def _export_json(self):
        """导出JSON文件"""
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
    
    def _clear_all(self):
        """清除所有内容"""
        # 清除输入
        self.file_path_var.set("")
        self.input_text.delete("1.0", tk.END)
        self.input_text.insert("1.0", UIConstants.PLACEHOLDER_TEXT)
        self.input_text.configure(foreground=UIConstants.COLORS["text_muted"])
        # 清除结果
        for item in self.result_table.get_children():
            self.result_table.delete(item)
        
        self.detail_text.delete("1.0", tk.END)
        self.visual_canvas.delete("all")
        
        # 重置数据
        self.analysis_results = []
        self.current_tibetan = ""
        self.current_visual_index = 0
        
        self._show_empty_visual()
        self.status_var.set("已清除所有内容")
        self.progress_var.set(0)