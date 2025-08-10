# -*- coding: utf-8 -*-
# 创建者：Pemawangchuk
# 版本：1.0
# 日期：2025-04-06
# 描述：藏文基本集转换扩充集
import sys
import os
import tkinter as tk
from tkinter import filedialog, messagebox, Frame, ttk
import tkinter.font as tkFont
from ttkbootstrap import Style

# ===== 功能函数保持不变 =====
def b2e_trans_f(data_list, b2e_dict):
    """将藏文基本集转换为扩展集"""
    out_list = []
    for line_data in data_list:
        len_line = len(line_data)
        i = 0
        str_out = ''
        while i < len_line - 1:
            if 0x0FC0 >= ord(line_data[i + 1]) >= 0x0F70:
                count = 1
                str_order = '0' + str(hex(ord(line_data[i]))).upper().replace('0X', '')
                while 0x0FC0 >= ord(line_data[i + count]) >= 0x0F70:
                    str_order += '0' + str(hex(ord(line_data[i + count]))).upper().replace('0X', '')
                    count += 1
                try:
                    str_out += chr(int('0x' + b2e_dict[str_order], base=16))
                except KeyError:
                    str_out += '<None>'
                i += count
            else:
                str_out += line_data[i]
                i += 1
        out_list.append(str_out)
    return out_list

def e2b_trans_f(data_list, e2b_dict):
    """将藏文扩展集转换为基本集"""
    out_list = []
    for line_data in data_list:
        len_line = len(line_data)
        i = 0
        str_out = ''
        while i < len_line:
            if 0xF300 <= ord(line_data[i]) <= 0xF8FF:
                str_order = str(hex(ord(line_data[i]))).upper().replace('0X', '')
                try:
                    str_b = e2b_dict[str_order]
                    x = 0
                    len__ = len(str_b)
                    while x + 4 <= len__:
                        str_out += chr(int('0x' + str(str_b[x:x + 4]), base=16))
                        x += 4
                except KeyError:
                    str_out += '<None>'
                i += 1
            else:
                str_out += line_data[i]
                i += 1
        out_list.append(str_out)
    return out_list

# ===== GUI =====
class TibetanConverter:
    """藏文编码转换器GUI界面（美化版）"""
    def __init__(self):
        self.b2e_dict = dict()
        self.e2b_dict = dict()
        self.txt_data = list()
        self.txt_trans_data = list()
        self.mode = True
        self.is_converting = False
        self.theme = "flatly"

        # Color schemes for light and dark modes
        self.themes = {
            "flatly": {
                "C_BG": "#f5f7fa", "C_CARD": "#ffffff", "C_ACCENT": "#4a6fa5",
                "C_SUCCESS": "#2ecc71", "C_ERROR": "#e74c3c", "C_WARN": "#f39c12",
                "C_TEXT": "#333333", "C_STATUS_BG": "#e8edf2"
            },
            "darkly": {
                "C_BG": "#2c3e50", "C_CARD": "#34495e", "C_ACCENT": "#3498db",
                "C_SUCCESS": "#2ecc71", "C_ERROR": "#e74c3c", "C_WARN": "#f1c40f",
                "C_TEXT": "#ecf0f1", "C_STATUS_BG": "#2e4053"
            }
        }
        self.set_theme("flatly")

        # Fonts
        self.F_TITLE = ("微软雅黑", 20, "bold")
        self.F_LABEL = ("微软雅黑", 14, "bold")
        self.F_BTN = ("微软雅黑", 12, "bold")
        self.F_STATUS = ("微软雅黑", 10)

        self.style = Style(theme=self.theme)
        self.window = self.style.master
        self.window.title("藏文编码转换系统")
        self.window.geometry("1200x950+400+100")
        self.window.minsize(900, 700)
        self.window.configure(bg=self.C_BG)
        self.window.resizable(True, True)
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(1, weight=1)

        try:
            self.window.iconbitmap("tibetan_converter.ico")  # Provide a valid .ico file
        except:
            pass  # Silently ignore if icon is missing

        self._create_widgets()
        self.window.mainloop()

    def set_theme(self, theme_name):
        self.theme = theme_name
        theme_colors = self.themes[theme_name]
        for key, value in theme_colors.items():
            setattr(self, key, value)

    def toggle_theme(self):
        new_theme = "darkly" if self.theme == "flatly" else "flatly"
        self.set_theme(new_theme)
        self.style = Style(theme=new_theme)
        self.window.configure(bg=self.C_BG)
        self._refresh_widgets()

    # ---------- 组件 ----------
    def _create_widgets(self):
        # Status bar (moved to top to initialize status_label early)
        status = Frame(self.window, bg=self.C_STATUS_BG, height=30)
        status.pack_propagate(False)
        self.status_label = tk.Label(status, text="✅ 系统准备就绪", font=self.F_STATUS, fg=self.C_ACCENT, bg=self.C_STATUS_BG)
        self.status_label.pack(side="left", padx=15)
        Frame(status, width=2, bg=self.C_ACCENT).pack(side="left", fill="y", padx=5)
        tk.Label(status, text="版本 1.0.0", font=self.F_STATUS, fg="#666", bg=self.C_STATUS_BG).pack(side="right", padx=15)
        status.pack(fill="x", side="bottom")

        # Title bar
        title_bar = Frame(self.window, bg=self.C_ACCENT, height=70)
        title_bar.pack_propagate(False)
        tk.Label(
            title_bar,
            text="⛰️ 藏文编码转换系统 ⛰️",
            font=self.F_TITLE,
            fg="white",
            bg=self.C_ACCENT,
        ).pack(pady=15)
        title_bar.pack(fill="x")

        # Separator
        Frame(self.window, height=3, bg=self.C_ACCENT).pack(fill="x")

        # Main container
        main = Frame(self.window, bg=self.C_BG, padx=20, pady=15)
        main.pack(fill="both", expand=True)

        # Load conversion table card
        load_card = self._card(main, height=70)
        self.btn_load = self._button(load_card, "📁 加载对照表", self.data_order_load, width=30)
        self.btn_load.pack(expand=True)
        load_card.pack(fill="x", pady=(0, 15))

        # Conversion area
        convert_frame = self._card(main)
        convert_frame.pack(fill="both", expand=True, pady=(0, 15))

        # Basic set
        left_frame = self._text_block(convert_frame, "📝 藏文基本集", "Microsoft Himalaya", 22)
        left_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        self.text0 = self._text_widget(left_frame, "基本集")

        # Middle buttons
        mid = Frame(convert_frame, bg=self.C_CARD)
        mid.pack(side="left", fill="y", padx=10)
        self.btn_b2e = self._button(mid, "基本集 >> 扩充集", self.b2e_trans, bg=self.C_SUCCESS)
        self.btn_b2e.pack(pady=20)
        self.btn_e2b = self._button(mid, "基本集 << 扩充集", self.e2b_trans, bg=self.C_ACCENT)
        self.btn_e2b.pack(pady=20)

        # Extended set
        right_frame = self._text_block(convert_frame, "📄 藏文扩展集", "珠穆朗玛—乌金苏通体", 14)
        right_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        self.text1 = self._text_widget(right_frame, "扩展集")

        # Bottom buttons
        bottom_card = self._card(main)
        bottom_card.pack(fill="x")
        for txt, cmd, color in [
            ("📂 打开文件", self.open_file, self.C_ACCENT),
            ("💾 保存结果", self.save_data, self.C_ACCENT),
            ("🗑️ 清空文本", self.clear_text, self.C_ACCENT),
            ("🌙 切换主题", self.toggle_theme, self.C_ACCENT),
            ("❌ 退出程序", self.quit_app, self.C_ERROR)
        ]:
            self._button(bottom_card, txt, cmd, bg=color).pack(side="left", expand=True, padx=15, pady=10)

        # Keyboard shortcuts
        self.window.bind("<Control-o>", lambda e: self.open_file())
        self.window.bind("<Control-s>", lambda e: self.save_data())
        self.window.bind("<Control-q>", lambda e: self.quit_app())

    def _refresh_widgets(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        self._create_widgets()

    # ---------- 工具 ----------
    def _card(self, parent, height=None):
        card = Frame(parent, bg=self.C_CARD, relief="flat", bd=0)
        if height:
            card.pack_propagate(False)
            card.configure(height=height)
        return card

    def _button(self, parent, text, command, width=16, bg=None):
        btn = ttk.Button(
            parent,
            text=text,
            command=command,
            width=width,
            style="primary.TButton" if bg == self.C_ACCENT else "success.TButton" if bg == self.C_SUCCESS else "danger.TButton",
            cursor="hand2",
        )
        tooltip_text = {
            "📁 加载对照表": "加载包含基本集与扩展集映射的制表符分隔文件",
            "基本集 ➤ 扩充集": "将藏文基本集转换为扩展集",
            "扩充集 ➤ 基本集": "将藏文扩展集转换为基本集",
            "📂 打开文件": "打开藏文文本文件进行转换",
            "💾 保存结果": "将转换后的文本保存到文件",
            "🗑️ 清空文本": "清空输入和输出文本区域",
            "🌙 切换主题": "在亮色和暗色主题间切换",
            "❌ 退出程序": "退出应用程序"
        }.get(text, "")
        btn.bind("<Enter>", lambda e: self._show_tooltip(btn, tooltip_text))
        btn.bind("<Leave>", lambda e: self._hide_tooltip())
        return btn

    def _text_block(self, parent, title, font_family, font_size):
        block = self._card(parent)
        header = Frame(block, bg=self.C_ACCENT, height=35)
        tk.Label(header, text=title, font=self.F_LABEL, bg=self.C_ACCENT, fg="white").pack(
            side="left", padx=10, pady=5
        )
        header.pack(fill="x")
        return block

    def _text_widget(self, parent, block_type):
        frame = Frame(parent, bg=self.C_CARD, padx=5, pady=5)
        font_family = "Microsoft Himalaya" if "基本集" in block_type else "珠穆朗玛—乌金苏通体"
        font_size = 22 if "基本集" in block_type else 14
        available_fonts = tkFont.families()
        if font_family not in available_fonts:
            font_family = "Arial"
            self._status(f"⚠️ 字体 {font_family} 不可用，使用 Arial", self.C_WARN)
        txt = tk.Text(
            frame,
            width=35,
            height=18,
            wrap="word",
            font=(tkFont.Font(family=font_family, size=font_size)),
            padx=10,
            pady=10,
            bd=1,
            relief="solid",
            bg="#ffffff" if self.theme == "flatly" else "#2c3e50",
            fg=self.C_TEXT,
            insertbackground=self.C_ACCENT,
            selectbackground="#d6e6f2" if self.theme == "flatly" else "#3498db",
        )
        scroll = ttk.Scrollbar(frame, command=txt.yview, style="Vertical.TScrollbar")
        txt.configure(yscrollcommand=scroll.set)
        txt.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        frame.pack(fill="both", expand=True)
        return txt

    def _show_tooltip(self, widget, text):
        if not text:
            return
        x, y, _, _ = widget.bbox("insert")
        x += widget.winfo_rootx() + 25
        y += widget.winfo_rooty() + 20
        self.tooltip = tk.Toplevel(widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip, text=text, background="#ffffe0", relief="solid", borderwidth=1, font=("微软雅黑", 10))
        label.pack()

    def _hide_tooltip(self):
        if hasattr(self, "tooltip"):
            self.tooltip.destroy()

    def _status(self, text, color=None):
        self.status_label.config(text=text, fg=color or self.C_ACCENT, bg=self.C_STATUS_BG)
        self.window.update_idletasks()

    # ---------- 业务 ----------
    def data_order_load(self):
        self.b2e_dict.clear()
        self.e2b_dict.clear()
        path = filedialog.askopenfilename(title="选择藏文扩充集与基本集的对照表")
        if path and path.endswith(".txt"):
            try:
                self._status("正在加载对照表...", self.C_ACCENT)
                with open(path, encoding="utf-8") as f:
                    for line in f:
                        if "\t" in line:
                            b, e = line.strip().split("\t")
                            self.b2e_dict.update({e: b})
                            self.e2b_dict.update({b: e})
                self._status(f"✅ 已加载：{os.path.basename(path)}", self.C_SUCCESS)
                messagebox.showinfo("成功", "对照表加载成功")
            except Exception as e:
                self._status(f"❌ 加载失败：{e}", self.C_ERROR)
                messagebox.showerror("错误", f"文件加载失败：{e}")
        else:
            self._status("⚠️ 未选择有效对照表", self.C_WARN)

    def open_file(self):
        self.txt_data.clear()
        self.text0.delete("1.0", "end")
        self.text1.delete("1.0", "end")
        path = filedialog.askopenfilename(title="选择藏文文本文件")
        if path and path.endswith(".txt"):
            try:
                self.mode = "_trans" not in os.path.basename(path)
                with open(path, encoding="utf-8") as f:
                    self.txt_data = f.readlines()
                tgt = self.text0 if self.mode else self.text1
                for line in self.txt_data:
                    tgt.insert("end", line)
                self._status(f"✅ 已加载：{os.path.basename(path)} | 模式：{'基本集' if self.mode else '扩展集'}", self.C_SUCCESS)
                messagebox.showinfo("成功", f"文件加载成功")
            except Exception as e:
                self._status(f"❌ 加载失败：{e}", self.C_ERROR)
                messagebox.showerror("错误", f"文件加载失败：{e}")
        else:
            self._status("⚠️ 未选择有效文本文件", self.C_WARN)

    def b2e_trans(self):
        if self.is_converting or not (self.txt_data and self.b2e_dict):
            messagebox.showwarning("警告", "请先加载文本文件和对照表")
            return
        if not self.mode:
            messagebox.showinfo("提示", "当前已是扩展集模式")
            return
        self.is_converting = True
        self.btn_b2e.config(state="disabled")
        progress = ttk.Progressbar(self.window, mode="indeterminate", style="info.Horizontal.TProgressbar")
        progress.pack(fill="x", padx=20, pady=5)
        progress.start()
        try:
            self._status("正在转换：基本集 → 扩展集...", self.C_ACCENT)
            self.text1.delete("1.0", "end")
            self.txt_trans_data = b2e_trans_f(self.txt_data, self.b2e_dict)
            for line in self.txt_trans_data:
                self.text1.insert("end", line + "\n")
            self._status("✅ 转换完成：基本集 → 扩展集", self.C_SUCCESS)
        except Exception as e:
            self._status(f"❌ 转换失败：{e}", self.C_ERROR)
            messagebox.showerror("错误", f"转换失败：{e}")
        finally:
            progress.stop()
            progress.destroy()
            self.btn_b2e.config(state="normal")
            self.is_converting = False

    def e2b_trans(self):
        if self.is_converting or not (self.txt_data and self.e2b_dict):
            messagebox.showwarning("警告", "请先加载文本文件和对照表")
            return
        if self.mode:
            messagebox.showinfo("提示", "当前已是基本集模式")
            return
        self.is_converting = True
        self.btn_e2b.config(state="disabled")
        progress = ttk.Progressbar(self.window, mode="indeterminate", style="info.Horizontal.TProgressbar")
        progress.pack(fill="x", padx=20, pady=5)
        progress.start()
        try:
            self._status("正在转换：扩展集 → 基本集...", self.C_ACCENT)
            self.text0.delete("1.0", "end")
            self.txt_trans_data = e2b_trans_f(self.txt_data, self.e2b_dict)
            for line in self.txt_trans_data:
                self.text0.insert("end", line + "\n")
            self._status("✅ 转换完成：扩展集 → 基本集", self.C_SUCCESS)
        except Exception as e:
            self._status(f"❌ 转换失败：{e}", self.C_ERROR)
            messagebox.showerror("错误", f"转换失败：{e}")
        finally:
            progress.stop()
            progress.destroy()
            self.btn_e2b.config(state="normal")
            self.is_converting = False

    def save_data(self):
        if not self.txt_trans_data:
            messagebox.showwarning("警告", "没有可保存的转换结果")
            return
        folder = filedialog.askdirectory(title="选择保存位置")
        if folder:
            try:
                name = "experiment_trans.txt" if self.mode else "experiment_data.txt"
                full = os.path.join(folder, name)
                with open(full, "w", encoding="utf-8") as f:
                    for line in self.txt_trans_data:
                        f.write(line + "\n")
                self._status(f"✅ 文件已保存：{name}", self.C_SUCCESS)
                messagebox.showinfo("成功", f"文件已保存至：\n{full}")
            except Exception as e:
                self._status(f"❌ 保存失败：{e}", self.C_ERROR)
                messagebox.showerror("错误", f"保存失败：{e}")

    def clear_text(self):
        self.text0.delete("1.0", "end")
        self.text1.delete("1.0", "end")
        self.txt_data.clear()
        self.txt_trans_data.clear()
        self._status("✅ 文本已清空", self.C_SUCCESS)

    def quit_app(self):
        if messagebox.askyesno("确认", "确定要退出程序吗？"):
            self.window.quit()
            sys.exit()

if __name__ == "__main__":
    TibetanConverter()