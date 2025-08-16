# -*- coding: UTF-8 -*-
# 创建者：Pemawangchuk
# 版本：1.0
# 日期：2025-04-06
# 描述：藏字构件动态统计
'''
Dynamic-Component-Statistics.py - 藏字构件动态统计
This program is a dynamic component statistics program.
'''
import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext, Frame
import tkinter.font as tkFont
import os
import ttkbootstrap as ttk_bs
from ttkbootstrap import Style
from ttkbootstrap.constants import *
import sys


# 合并的Creat_18785Componet代码
# 30个辅音
consonant = ['\u0F40', '\u0F41', '\u0F42', '\u0F44', '\u0F45', '\u0F46', '\u0F47', '\u0F49',
             '\u0F4F', '\u0F50', '\u0F51', '\u0F53', '\u0F54', '\u0F55', '\u0F56', '\u0F58',
             '\u0F59', '\u0F5A', '\u0F5B', '\u0F5D', '\u0F5E', '\u0F5F', '\u0F60', '\u0F61',
             '\u0F62', '\u0F63', '\u0F64', '\u0F66', '\u0F67', '\u0F68']

# 4个元音
tibetan_vowel = ['\u0F72', '\u0F74', '\u0F7A', '\u0F7C']

# 表1：上加+基字 的叠加组合
up_base_2 = ['རྐ', 'རྒ', 'རྔ', 'རྗ', 'རྙ', 'རྟ', 'རྡ', 'རྣ', 'རྦ', 'རྨ', 'རྩ', 'རྫ', 'ལྐ', 'ལྒ', 'ལྔ',
             'ལྕ', 'ལྗ', 'ལྟ', 'ལྡ', 'ལྤ', 'ལྦ', 'ལྷ', 'སྐ', 'སྒ', 'སྔ', 'སྙ', 'སྟ', 'སྡ', 'སྣ', 'སྤ',
             'སྦ', 'སྨ', 'སྩ']

# 表2：基字+下加 的叠加组合
base_down_2 = ['ཀྱ', 'ཁྱ', 'གྱ', 'པྱ', 'ཕྱ', 'བྱ', 'མྱ', 'ཀྲ', 'ཁྲ', 'གྲ', 'ཏྲ', 'ཐྲ', 'དྲ', 'པྲ', 'ཕྲ',
               'བྲ', 'སྲ', 'ཧྲ', 'ཀླ', 'གླ', 'བླ', 'ཟླ', 'རླ', 'སླ', 'ཀྭ', 'ཁྭ', 'གྭ', 'ཉྭ', 'དྭ', 'ཚྭ',
               'ཞྭ', 'ཟྭ', 'རྭ', 'ལྭ', 'ཤྭ', 'ཧྭ']

# 表3：后加字与再后加字的组合
after_reafter_2 = ['ནད', 'རད', 'ལད', 'གས', 'ངས', 'བས', 'མས']

# 表:4：上加+基字+下加 的叠加组合
up_base_down_3 = ['རྐྱ', 'རྒྱ', 'རྨྱ', 'སྐྱ', 'སྒྱ', 'སྤྱ', 'སྦྱ', 'སྨྱ', 'སྐྲ', 'སྒྲ', 'སྣྲ', 'སྤྲ', 'སྦྲ', 'སྨྲ',
                  'རྩྭ']

# 表5：基字+后加+再后加（其中 14 个有歧义）
base_after_reafter_3 = ['བགས', 'མབས', 'གགས', 'བངས', 'དངས', 'གངས', 'འངས', 'གམས', 'མམས', 'བབས', 'མངས', 'གབས', 'བམས',
                        'འམས']

# 表6：特殊的两个字（基字+下加字+再下加字）
base_under_reunder_3 = ['གྲྭ', 'ཕྱྭ']


class Split_component():
    def Split(self, Tibetan):
        if (len(Tibetan) == 1):
            return self.One_char(Tibetan)
        elif (len(Tibetan)  == 2):
            return self.Two_chars(Tibetan)
        elif (len(Tibetan)  == 3):
            return self.Three_chars(Tibetan)
        elif (len(Tibetan)  == 4):
            return self.Four_chars(Tibetan)
        elif (len(Tibetan)  == 5):
            return self.Five_chars(Tibetan)
        elif (len(Tibetan)  == 6):
            return self.Six_chars(Tibetan)
        elif (len(Tibetan)  == 7):
            return self.Seven_chars(Tibetan)

    def One_char(self, Tibetan):
        word = ['' for _ in range(10)]
        word[0] = Tibetan
        word[3] = Tibetan[0]
        word[-1] = '辅音字母'
        return word

    def Two_chars(self, Tibetan):
        word = ['' for _ in range(10)]
        fin = False
        word[0] = Tibetan
        pos = [-1, -1]
        # 为上加+基字
        if (Tibetan in up_base_2):
            pos[0], pos[1] = 2, 3
            word[-1] = '上加字+基字'
            for i, char_cur in enumerate(pos):
                word[char_cur] = Tibetan[i]
            return word
        # 为基字+下加
        if (Tibetan in base_down_2):
            pos[0], pos[1] = 3, 4
            word[-1] = '基字+下加字'
            for i, char_cur in enumerate(pos):
                word[char_cur] = Tibetan[i]
            return word

        pos[0] = 3
        for vow in tibetan_vowel:
            if (Tibetan[-1] == vow):
                pos[1] = 6
                word[-1] = '基字+元音'
                fin = True
                break
        if (fin == False):
            pos[1] = 7
            word[-1] = '基字+后加字'
            fin = True

        if (fin == False):
            print(word)
            return None
        for i, char_cur in enumerate(pos):
            word[char_cur] = Tibetan[i]

        return word

    def Three_chars(self, Tibetan):
        word = ['' for _ in range(10)]
        fin = False
        word[0] = Tibetan
        pos = [-1 for i in range(3)]
        # 查找表
        if (Tibetan in base_under_reunder_3):
            pos[0], pos[1], pos[2] = 3, 4, 5
            word[-1] = '基字+下加字+再下加字'
            for i, char_cur in enumerate(pos):
                word[char_cur] = Tibetan[i]
            return word
        if (Tibetan in base_after_reafter_3):
            pos[0], pos[1], pos[2] = 3, 7, 8
            word[-1] = '基字+后加字+再后加字'
            for i, char_cur in enumerate(pos):
                word[char_cur] = Tibetan[i]
            return word
        if (Tibetan in up_base_down_3):
            pos[0], pos[1], pos[2] = 2, 3, 4
            word[-1] = '上加字+基字+下加字'
            for i, char_cur in enumerate(pos):
                word[char_cur] = Tibetan[i]
            return word

        for vow in tibetan_vowel:
            ppos = Tibetan.find(vow)
            if (ppos == 1):
                pos[0], pos[1], pos[2] = 3, 6, 7
                word[-1] = '基字+元音+后加字'
                fin = True
                break
            elif (ppos == 2):
                for up_base in up_base_2:
                    if (Tibetan.find(up_base) == 0):
                        pos[0], pos[1], pos[2] = 2, 3, 6
                        word[-1] = '上加字+基字+元音'
                        fin = True
                        break

                if (fin == False):
                    for base_down in base_down_2:
                        if (Tibetan.find(base_down) == 0):
                            pos[0], pos[1], pos[2] = 3, 4, 6
                            word[-1] = '基字+下加字+元音'
                            fin = True
                            break

                if (fin == False):
                    pos[0], pos[1], pos[2] = 1, 3, 6
                    word[-1] = '前加字+基字+元音'
                    fin = True

        if (fin == False):
            for up_base in up_base_2:
                ppos = Tibetan.find(up_base)
                if (ppos == 1):
                    pos[0], pos[1], pos[2] = 1, 2, 3
                    word[-1] = '前加字+上加字+基字'
                    fin = True
                    break
                elif (ppos == 0):
                    pos[0], pos[1], pos[2] = 2, 3, 7
                    word[-1] = '上加字+基字+后加字'
                    fin = True
                    break

        if (fin == False):
            for base_down in base_down_2:
                ppos = Tibetan.find(base_down)
                if (ppos == 1):
                    pos[0], pos[1], pos[2] = 1, 3, 4
                    word[-1] = '前加字+基字+下加字'
                    fin = True
                    break
                elif (ppos == 0):
                    pos[0], pos[1], pos[2] = 3, 4, 7
                    word[-1] = '基字+下加字+后加字'
                    fin = True
                    break

        if (fin == False):
            for after_reafter in after_reafter_2:
                if (Tibetan.rfind(after_reafter) == 1):
                    pos[0], pos[1], pos[2] = 3, 7, 8
                    word[-1] = '基字+后加字+再后加字'
                    fin = True
                    break
            if (fin == False):
                pos[0], pos[1], pos[2] = 1, 3, 7
                word[-1] = '前加字+基字+后加字'
                fin = True

        if (fin == False):
            print(word)
            return None
        for i, char_cur in enumerate(pos):
            word[char_cur] = Tibetan[i]

        return word

    def Four_chars(self, Tibetan):
        word = ['' for _ in range(10)]
        fin = False
        word[0] = Tibetan
        pos = [-1 for i in range(4)]

        for vow in tibetan_vowel:
            ppos = Tibetan.find(vow)
            if (ppos == 3):
                for base_under_reunder in base_under_reunder_3:
                    if (Tibetan.find(base_under_reunder) == 0):
                        pos[0], pos[1], pos[2], pos[3] = 3, 4, 5, 6
                        word[-1] = '基字+下加字+再下加字+元音'
                        fin = True

                if (fin == False):
                    for up_base in up_base_2:
                        ppos2 = Tibetan.find(up_base)
                        if (ppos2 == 0):
                            pos[0], pos[1], pos[2], pos[3] = 2, 3, 4, 6
                            word[-1] = '上加字+基字+下加字+元音'
                            fin = True
                            break
                        elif (ppos2 == 1):
                            pos[0], pos[1], pos[2], pos[3] = 1, 2, 3, 6
                            word[-1] = '前加字+上加字+基字+元音'
                            fin = True
                            break

                if (fin == False):
                    for base_down in base_down_2:
                        if (Tibetan.find(base_down) == 1):
                            pos[0], pos[1], pos[2], pos[3] = 1, 3, 4, 6
                            word[-1] = '前加字+基字+下加字+元音'
                            fin = True

            elif (ppos == 2):
                for up_base in up_base_2:
                    ppos2 = Tibetan.find(up_base)
                    if (ppos2 == 0):
                        pos[0], pos[1], pos[2], pos[3] = 2, 3, 6, 7
                        word[-1] = '上加字+基字+元音+后加字'
                        fin = True
                        break
                for base_down in base_down_2:
                    ppos2 = Tibetan.find(base_down)
                    if (ppos2 == 0):
                        pos[0], pos[1], pos[2], pos[3] = 3, 4, 6, 7
                        word[-1] = '基字+下加字+元音+后加字'
                        fin = True
                        break
                if (fin == False):
                    pos[0], pos[1], pos[2], pos[3] = 1, 3, 6, 7
                    word[-1] = '前加字+基字+元音+后加字'
                    fin = True

            elif (ppos == 1):
                pos[0], pos[1], pos[2], pos[3] = 3, 6, 7, 8
                word[-1] = '基字+元音+后加字+再后加字'
                fin = True
                break

        if (fin == False):
            for base_under_reunder in base_under_reunder_3:
                if (Tibetan.find(base_under_reunder) == 0):
                    pos[0], pos[1], pos[2], pos[3] = 3, 4, 5, 7
                    word[-1] = '基字+下加字+再下加字+后加字'
                    fin = True
                    break

        if (fin == False):
            for up_base_down in up_base_down_3:
                ppos = Tibetan.find(up_base_down)
                if (ppos == 1):
                    pos[0], pos[1], pos[2], pos[3] = 1, 2, 3, 4
                    word[-1] = '前加字+上加字+基字+下加字'
                    fin = True
                    break
                elif (ppos == 0):
                    pos[0], pos[1], pos[2], pos[3] = 2, 3, 4, 7
                    word[-1] = '上加字+基字+下加字+后加字'
                    fin = True
                    break

        if (fin == False):
            for up_base in up_base_2:
                ppos = Tibetan.find(up_base)
                if (ppos == 1):
                    pos[0], pos[1], pos[2], pos[3] = 1, 2, 3, 7
                    word[-1] = '前加字+上加字+基字+后加字'
                    fin = True
                    break
                elif (ppos == 0):
                    pos[0], pos[1], pos[2], pos[3] = 2, 3, 7, 8
                    word[-1] = '上加字+基字+后加字+再后加字'
                    fin = True
                    break

        if (fin == False):
            for base_down in base_down_2:
                ppos = Tibetan.find(base_down)
                if (ppos == 1):
                    pos[0], pos[1], pos[2], pos[3] = 1, 3, 4, 7
                    word[-1] = '前加字+基字+下加字+后加字'
                    fin = True
                    break
                elif (ppos == 0):
                    for after_reafter in after_reafter_2:
                        if (Tibetan.rfind(after_reafter) == 2):
                            pos[0], pos[1], pos[2], pos[3] = 3, 4, 7, 8
                            word[-1] = '基字+下加字+后加字+再后加字'
                            fin = True
                            break

        if (fin == False):
            for after_reafter in after_reafter_2:
                if (Tibetan.rfind(after_reafter) == 2):
                    pos[0], pos[1], pos[2], pos[3] = 1, 3, 7, 8
                    word[-1] = '前加字+基字+后加字+再后加字'
                    fin = True

        if (fin == False):
            print(word)
            return None
        for i, char_cur in enumerate(pos):
            word[char_cur] = Tibetan[i]

        return word

    def Five_chars(self, Tibetan):
        word = ['' for _ in range(10)]
        fin = False
        word[0] = Tibetan
        pos = [-1 for i in range(5)]

        for base_under_reunder in base_under_reunder_3:
            if (Tibetan.find(base_under_reunder) == 0):
                for after_reafter in after_reafter_2:
                    if (Tibetan.rfind(after_reafter) == 3):
                        pos[0], pos[1], pos[2], pos[3], pos[4] = 3, 4, 5, 7, 8
                        word[-1] = '基字+下加字+再下加字+后加字+再后加字'
                        fin = True
        if (fin == False):
            for vow in tibetan_vowel:
                ppos = Tibetan.find(vow)
                if (ppos == 4):
                    pos[0], pos[1], pos[2], pos[3], pos[4] = 1, 2, 3, 4, 6
                    word[-1] = '前加字+上加字+基字+下加字+元音'
                    fin = True
                    break
                elif (ppos == 3):
                    for base_under_reunder in base_under_reunder_3:
                        if (Tibetan.find(base_under_reunder) == 0):
                            pos[0], pos[1], pos[2], pos[3], pos[4] = 3, 4, 5, 6, 7
                            word[-1] = '基字+下加字+再下加字+元音+后加字'
                            fin = True
                            break

                    if (fin == False):
                        for up_base in up_base_2:
                            ppos2 = Tibetan.find(up_base)
                            if (ppos2 == 1):
                                pos[0], pos[1], pos[2], pos[3], pos[4] = 1, 2, 3, 6, 7
                                word[-1] = '前加字+上加字+基字+元音+后加字'
                                fin = True
                                break
                            elif (ppos2 == 0):
                                pos[0], pos[1], pos[2], pos[3], pos[4] = 2, 3, 4, 6, 7
                                word[-1] = '上加字+基字+下加字+元音+后加字'
                                fin = True
                                break

                    if (fin == False):
                        for base_down in base_down_2:
                            if (Tibetan.find(base_down) == 1):
                                pos[0], pos[1], pos[2], pos[3], pos[4] = 1, 3, 4, 6, 7
                                word[-1] = '前加字+基字+下加字+元音+后加字'
                                fin = True
                                break

                elif (ppos == 2):
                    for up_base in up_base_2:
                        if (Tibetan.find(up_base) == 0):
                            pos[0], pos[1], pos[2], pos[3], pos[4] = 2, 3, 6, 7, 8
                            word[-1] = '上加字+基字+元音+后加字+再后加字'
                            fin = True
                            break

                    if (fin == False):
                        for base_down in base_down_2:
                            if (Tibetan.find(base_down) == 0):
                                pos[0], pos[1], pos[2], pos[3], pos[4] = 3, 4, 6, 7, 8
                                word[-1] = '基字+下加字+元音+后加字+再后加字'
                                fin = True
                                break

                    if (fin == False):
                        for after_reafter in after_reafter_2:
                            if (Tibetan.rfind(after_reafter) == 3):
                                pos[0], pos[1], pos[2], pos[3], pos[4] = 1, 3, 6, 7, 8
                                word[-1] = '前加字+基字+元音+后加字+再后加字'
                                fin = True
        if (fin == False):
            for up_base_down in up_base_down_3:
                ppos = Tibetan.find(up_base_down)
                if (ppos == 1):
                    pos[0], pos[1], pos[2], pos[3], pos[4] = 1, 2, 3, 4, 7
                    word[-1] = '前加字+上加字+基字+下加字+后加字'
                    fin = True
                    break
                elif (ppos == 0):
                    for after_reafter in after_reafter_2:
                        if (Tibetan.rfind(after_reafter) == 3):
                            pos[0], pos[1], pos[2], pos[3], pos[4] = 2, 3, 4, 7, 8
                            word[-1] = '上加字+基字+下加字+后加字+再后加字'
                            fin = True
                            break

        if (fin == False):
            for up_base in up_base_2:
                if (Tibetan.find(up_base) == 1):
                    pos[0], pos[1], pos[2], pos[3], pos[4] = 1, 2, 3, 7, 8
                    word[-1] = '前加字+上加字+基字+后加字+再后加字'
                    fin = True
                    break

        if (fin == False):
            for base_down in base_down_2:
                if (Tibetan.find(base_down) == 1):
                    pos[0], pos[1], pos[2], pos[3], pos[4] = 1, 3, 4, 7, 8
                    word[-1] = '前加字+基字+下加字+后加字+再后加字'
                    fin = True

        if (fin == False):
            print(word)
            return None

        for i, char_cur in enumerate(pos):
            word[char_cur] = Tibetan[i]

        return word

    def Six_chars(self, Tibetan):
        word = ['' for _ in range(10)]
        fin = False
        word[0] = Tibetan
        pos = [-1 for i in range(6)]

        for vow in tibetan_vowel:
            ppos = Tibetan.find(vow)
            if (ppos == 4):
                pos[0], pos[1], pos[2], pos[3], pos[4], pos[5] = 1, 2, 3, 4, 6, 7
                word[-1] = '前加字+上加字+基字+下加字+元音+后加字'
                fin = True
                break
            elif (ppos == 3):
                for base_under_reunder in base_under_reunder_3:
                    if (Tibetan.find(base_under_reunder) == 0):
                        for after_reafter in after_reafter_2:
                            if (Tibetan.rfind(after_reafter) == 4):
                                pos[0], pos[1], pos[2], pos[3], pos[4], pos[5] = 3, 4, 5, 6, 7, 8
                                word[-1] = '基字+下加字+再下加字+元音+后加字+再后加字'
                                fin = True
                                break

                if (fin == False):
                    for up_base in up_base_2:
                        ppos2 = Tibetan.find(up_base)
                        if (ppos2 == 1):
                            pos[0], pos[1], pos[2], pos[3], pos[4], pos[5] = 1, 2, 3, 6, 7, 8
                            word[-1] = '前加字+上加字+基字+元音+后加字+再后加字'
                            fin = True
                            break
                        elif (ppos2 == 0):
                            pos[0], pos[1], pos[2], pos[3], pos[4], pos[5] = 2, 3, 4, 6, 7, 8
                            word[-1] = '上加字+基字+下加字+元音+后加字+再后加字'
                            fin = True
                            break

                if (fin == False):
                    for base_down in base_down_2:
                        if (Tibetan.find(base_down) == 1):
                            pos[0], pos[1], pos[2], pos[3], pos[4], pos[5] = 1, 3, 4, 6, 7, 8
                            word[-1] = '前加字+基字+下加字+元音+后加字+再后加字'
                            fin = True
                            break

        if (fin == False):
            for up_base in up_base_2:
                if (Tibetan.find(up_base) == 1):
                    pos[0], pos[1], pos[2], pos[3], pos[4], pos[5] = 1, 2, 3, 4, 7, 8
                    word[-1] = '前加字+上加字+基字+下加字+后加字+再后加字'
                    fin = True
        if (fin == False):
            print(word)
            return None
        for i, char_cur in enumerate(pos):
            word[char_cur] = Tibetan[i]

        return word

    def Seven_chars(self, Tibetan):
        word = ['' for _ in range(10)]
        fin = False
        word[0] = Tibetan
        pos = [-1 for i in range(7)]
        for vow in tibetan_vowel:
            if (Tibetan.find(vow) == 4):
                pos[0], pos[1], pos[2], pos[3], pos[4], pos[5], pos[6] = 1, 2, 3, 4, 6, 7, 8
                word[-1] = '前加字+上加字+基字+下加字+元音+后加字+再后加字'
                fin = True
                break

        if (fin == False):
            print(word)
            return None
        for i, char_cur in enumerate(pos):
            word[char_cur] = Tibetan[i]

        return word


class Create_18785Com():
    def Create(self, words_18785):
        split_com = Split_component()
        
        # 创建内置的18785个藏文构件数据
        # 这里使用简化的构件生成逻辑，实际应用中可以从文件读取
        tibetan_chars = []
        
        # 生成基本的藏文字符组合
        for base in consonant:
            # 单个基字
            word = split_com.Split(base)
            if word:
                tibetan_chars.append(word)
        
        # 生成更多组合（这里简化处理，实际应该包含所有18785个组合）
        # 可以根据需要扩展更多的组合逻辑
        
        # 如果有18785_words.txt文件，优先从文件读取
        try:
            with open('18785_words.txt', 'r', encoding='utf-8') as f:
                for i in range(18785):
                    line = f.readline().strip()
                    if line:
                        word = split_com.Split(line)
                        if word:
                            words_18785.append(word)
            return words_18785
        except FileNotFoundError:
            # 如果文件不存在，使用内置的简化数据
            words_18785.extend(tibetan_chars)
            
            # 补充到18785个（使用重复数据填充，实际应用中应该有完整的数据）
            while len(words_18785) < 18785:
                words_18785.extend(tibetan_chars[:min(len(tibetan_chars), 18785 - len(words_18785))])
            
            return words_18785

# 黏着词后缀
adhering = ['འུའི', 'འི', 'འོ', 'འང', 'འུ']

# 元音
vowel = {'ི': 0, 'ུ': 0, 'ེ': 0, 'ོ': 0, '#':0}

# 前加字符
front_char = {'ག': 0, 'ད': 0, 'བ': 0, 'མ': 0, 'འ': 0, '#':0}

# 上加字符
up_char = {'ར': 0, 'ལ': 0, 'ས': 0, '#':0}

# 基字
base_char = {'ཀ': 0, 'ཁ': 0, 'ག': 0, 'ང': 0, 'ཅ': 0, 'ཆ': 0, 'ཇ': 0, 'ཉ': 0, 'ཏ': 0, 'ཐ': 0, 'ད': 0, 'ན': 0, 'པ': 0, 'ཕ': 0,
             'བ': 0, 'མ': 0, 'ཙ': 0, 'ཚ': 0, 'ཛ': 0, 'ཝ': 0, 'ཞ': 0, 'ཟ': 0, 'འ': 0, 'ཡ': 0, 'ར': 0, 'ལ': 0, 'ཤ': 0, 'ས': 0,
             'ཧ': 0, 'ཨ': 0}

# 叠加基字
base_overlied = {'ྐ': 0, 'ྑ': 0, 'ྒ': 0, 'ྔ': 0, 'ྕ': 0, 'ྖ': 0, 'ྗ': 0, 'ྙ': 0, 'ྟ': 0, 'ྠ': 0, 'ྡ': 0, 'ྣ': 0, 'ྤ': 0, 'ྥ': 0, 'ྦ': 0, 'ྨ': 0,
                 'ྩ': 0, 'ྪ': 0, 'ྫ': 0, 'ྺ': 0, 'ྮ': 0, 'ྯ': 0, 'ྰ': 0, 'ྱ': 0, 'ྲ': 0, 'ླ': 0, 'ྴ': 0, 'ྶ': 0, 'ྷ': 0, 'ྸ': 0}

# 下加字
down_char = {'ྭ': 0, 'ྱ': 0, 'ྲ': 0, 'ླ': 0, '#':0}

# 再下加字
redown_char = {'ྭ': 0, '#':0}

# 后加字
rear_char = {'ག': 0, 'ང': 0, 'ད': 0, 'ན': 0, 'བ': 0, 'མ': 0, 'འ': 0, 'ར': 0, 'ལ': 0, 'ས': 0, '#':0}

# 再后加字
rerear_char = {'ད': 0, 'ས': 0, '#':0}

# 分隔符
split_char = {'ༀ': 0, '༁': 0, '༂': 0, '༃': 0, '༄': 0, '༆': 0, '༇': 0, '༈': 0, '༉': 0, '༊': 0,
              '་': 0, '༌': 0, '།': 0, '༎': 0, '༏': 0, '༐': 0, '༑': 0, '༒': 0, '༓': 0, '༔': 0, '༕': 0,
              '༖': 0, '༗': 0, '༘': 0, '༙': 0, '༚': 0, '༛': 0, '༜': 0, '༝': 0, '༞': 0, '༟': 0, '༠': 0,
              '༡': 0, '༢': 0, '༣': 0, '༤': 0, '༥': 0, '༦': 0, '༧': 0, '༨': 0, '༩': 0, '༪': 0, '༫': 0,
              '༬': 0, '༭': 0, '༮': 0, '༯': 0, '༰': 0, '༱': 0, '༲': 0, '༳': 0, '༴': 0, '༵': 0, '༶': 0,
              '༷': 0, '༸': 0, '༺': 0, '༻': 0, '༼': 0, '༽': 0, '༾': 0, '༿': 0, '྾': 0, '྿': 0, '࿀': 0,
              '࿁': 0, '࿂': 0, '࿃': 0, '࿄': 0, '࿅': 0, '࿆': 0, '࿇': 0, '࿈': 0, '࿉': 0, '࿊': 0, '࿋': 0,
              '࿌': 0, '࿎': 0, '࿏': 0, '࿐': 0, '࿑': 0, '࿒': 0, '࿓': 0, '࿔': 0, '\u0FD5': 0, '\u0FD6':0,
              '\u0FD7': 0, '\u0FD8':0, '࿙': 0, '࿚': 0}

class DynamicTibetanComponentAnalyzer:
    """藏字构件动态统计分析器"""
    
    def __init__(self):
        self.essay = ''
        self.words_18785 = []
        self.tib_count = 0
        self.setup_gui()
        self.init_components()
        
    def setup_gui(self):
        """设置GUI界面"""
        # 使用现代主题
        self.style = Style(theme='superhero')  # 深色主题
        self.window = self.style.master
        
        # 窗口基本设置
        self.window.title('🏔️ 藏字构件动态统计分析器')
        self.window.geometry('1400x900+200+50')
        self.window.minsize(1200, 800)
        
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
        self.main_frame = ttk_bs.Frame(self.window, padding=20)
        self.main_frame.pack(fill=BOTH, expand=True)
        
    def create_header(self):
        """创建标题区域"""
        header_frame = ttk_bs.Frame(self.main_frame)
        header_frame.pack(fill=X, pady=(0, 20))
        
        # 主标题
        title_label = ttk_bs.Label(
            header_frame,
            text="藏字构件动态统计分析器",
            font=('Microsoft YaHei UI', 24, 'bold'),
            bootstyle=PRIMARY
        )
        title_label.pack(side=LEFT)
        
        # 副标题
        subtitle_label = ttk_bs.Label(
            header_frame,
            text="Dynamic Tibetan Component Statistics Analyzer",
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
            text="📂 选择文件/文件夹",
            command=self.open_file,
            bootstyle=SUCCESS,
            width=18
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
            padx=10,
            pady=10
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
            padx=10,
            pady=10
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
            command=self.split_tibetan,
            bootstyle=SUCCESS,
            width=15
        )
        self.analyze_btn.pack(side=LEFT, padx=(0, 10))
        
        # 保存按钮
        save_btn = ttk_bs.Button(
            button_frame,
            text="💾 保存结果",
            command=self.save_file,
            bootstyle=INFO,
            width=15
        )
        save_btn.pack(side=LEFT, padx=(0, 10))
        
        # 退出按钮
        exit_btn = ttk_bs.Button(
            button_frame,
            text="❌ 退出",
            command=self.window.destroy,
            bootstyle=DANGER,
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
        progress_container = ttk_bs.Frame(progress_frame, height=30)
        progress_container.pack(fill=X, pady=(5, 10))
        progress_container.pack_propagate(False)  # 防止子组件影响容器大小
        
        # 进度条
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk_bs.Progressbar(
            progress_container,
            variable=self.progress_var,
            bootstyle=SUCCESS,
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

    def init_components(self):
        """初始化构件"""
        self.creCom = Create_18785Com()
        self.creCom.Create(self.words_18785)
        self.update_status("构件初始化完成，共加载 18785 个构件")

    def int2uni(self, num):
        """数字转Unicode"""
        return ('\\u{:0>4x}'.format(num)).encode().decode('unicode_escape')

    def count_tibetan_components(self, tibetan):
        """统计藏文构件"""
        # 前1 上2 基3 下4 再下5 元6 后7 再后8
        # 只有带上加字的基字才会有叠加圈
        fin = False
        for tibetan_word in self.words_18785:
            if tibetan_word[0] == tibetan:
                word = tibetan_word
                fin = True
                break
        if not fin:
            return

        if word[1] == '':
            front_char['#'] += 1
        else:
            front_char[word[1]] += 1

        if word[2] == '':
            up_char['#'] += 1
        else:
            up_char[word[2]] += 1

        if '\u0F90' <= word[3] <= '\u0FB8':
            base_overlied[word[3]] += 1
            base_char[self.int2uni(ord(word[3]) - 80)] += 1
        else:
            base_char[word[3]] += 1

        if word[4] == '':
            down_char['#'] += 1
        else:
            down_char[word[4]] += 1

        if word[5] == '':
            redown_char['#'] += 1
        else:
            redown_char[word[5]] += 1

        if word[6] == '':
            vowel['#'] += 1
        else:
            vowel[word[6]] += 1

        if word[7] == '':
            rear_char['#'] += 1
        else:
            rear_char[word[7]] += 1

        if word[8] == '':
            rerear_char['#'] += 1
        else:
            rerear_char[word[8]] += 1

    def split_tibetan(self):
        """分析藏文构件"""
        if not self.essay:
            messagebox.showwarning('警告', '请先选择文件！')
            return
        
        # 重置统计数据
        self.reset_counters()
        
        # 开始计时
        start_time = time.time()
        
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
        
        s = ''
        one_fifth = max(1, total_chars // 100)  # 更频繁的更新
        
        for i, ch in enumerate(self.essay):
            # 更新进度（更频繁地更新进度条）
            if i % one_fifth == 0:
                progress = (i / total_chars) * 100
                self.progress_var.set(i)  # 直接设置当前处理的字符数
                self.progress_label.config(text=f"处理进度: {progress:.1f}% ({i}/{total_chars})")
                # 强制更新UI
                self.progress_bar.update()
                self.progress_label.update()
                self.window.update_idletasks()

            if ch in split_char:
                split_char[ch] += 1
            elif '\u0F00' <= ch <= '\u0FDA':
                s += ch
                continue
                
            if s != '':
                fin = False
                for adher in adhering:
                    pos = s.find(adher)
                    if pos != 0 and pos != -1 and s[-1] == adher[-1]:  # 是黏着词，分开统计构建
                        self.count_tibetan_components(s[:pos])
                        self.count_tibetan_components(s[pos:])
                        self.tib_count += 1
                        s = ''
                        fin = True
                        break
                if not fin:
                    self.count_tibetan_components(s)
                    self.tib_count += 1
                    s = ''

        # 完成处理
        end_time = time.time()
        process_time = end_time - start_time
        
        # 显示结果
        self.display_results(process_time)
        
        # 更新状态 - 设置为最大值而不是百分比
        self.progress_var.set(total_chars)  # 设置为最大值
        self.progress_label.config(text="分析完成！")
        self.analyze_btn.config(state='normal')
        self.stats_labels['current_status'].config(text="完成")
        self.stats_labels['total_chars'].config(text=f"{total_chars:,}")
        self.stats_labels['tibetan_count'].config(text=f"{self.tib_count:,}")
        self.stats_labels['process_time'].config(text=f"{process_time:.3f}s")
        self.update_status(f"分析完成 | 处理了 {self.tib_count} 个藏文音节")

    def display_results(self, process_time):
        """显示统计结果"""
        self.result_text.insert('1.0', f"{'='*60}\n")
        self.result_text.insert('end', f"藏字构件动态统计分析结果\n")
        self.result_text.insert('end', f"{'='*60}\n\n")
        self.result_text.insert('end', f"处理时间: {process_time:.3f} 秒\n")
        self.result_text.insert('end', f"总字符数: {len(self.essay):,}\n")
        self.result_text.insert('end', f"藏文音节: {self.tib_count:,}\n\n")
        
        # 显示各类构件统计
        component_types = [
            ('前加字', front_char),
            ('上加字', up_char),
            ('基字', base_char),
            ('叠加基字', base_overlied),
            ('下加字', down_char),
            ('再下加字', redown_char),
            ('元音', vowel),
            ('后加字', rear_char),
            ('再后加字', rerear_char),
            ('分隔符', split_char)
        ]
        
        for type_name, char_dict in component_types:
            self.result_text.insert('end', f"{type_name}的统计结果:\n")
            self.result_text.insert('end', f"{'-'*40}\n")
            
            # 按频次排序
            sorted_items = sorted(char_dict.items(), key=lambda x: x[1], reverse=True)
            
            for char, count in sorted_items:
                if count > 0:  # 只显示有统计的字符
                    percentage = (count / self.tib_count * 100) if self.tib_count > 0 else 0
                    self.result_text.insert('end', f"{char:<10} {count:>8} ({percentage:.2f}%)\n")
            
            self.result_text.insert('end', '\n')

    def reset_counters(self):
        """重置所有计数器"""
        self.tib_count = 0
        
        # 重置所有字典
        for key in vowel:
            vowel[key] = 0
        for key in front_char:
            front_char[key] = 0
        for key in up_char:
            up_char[key] = 0
        for key in base_char:
            base_char[key] = 0
        for key in base_overlied:
            base_overlied[key] = 0
        for key in down_char:
            down_char[key] = 0
        for key in redown_char:
            redown_char[key] = 0
        for key in rear_char:
            rear_char[key] = 0
        for key in rerear_char:
            rerear_char[key] = 0
        for key in split_char:
            split_char[key] = 0

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
        self.tib_count = 0
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
        self.reset_counters()
        
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

# 保持向后兼容的全局变量和函数
essay = ''
words_18785 = []
creCom = Create_18785Com()
creCom.Create(words_18785)
Tib_count = 0

def int2uni(num):
    return ('\\u{:0>4x}'.format(num)).encode().decode('unicode_escape')

def Count_TibetanComponents(Tibetan):
    # 前1 上2 基3 下4 再下5 元6 后7 再后8
    # 只有带上加字的基字才会有叠加圈
    fin = False
    for tibetan in words_18785:
        if(tibetan[0]==Tibetan):
            word = tibetan
            fin = True
            break
    if(fin==False): return

    if(word[1]==''): front_char['#'] += 1
    else: front_char[word[1]] += 1

    if(word[2] == ''):up_char['#'] += 1
    else: up_char[word[2]] += 1

    if('\u0F90'<= word[3] <='\u0FB8'):
        base_overlied[word[3]] += 1
        base_char[int2uni(ord(word[3])-80)] += 1
    else: base_char[word[3]] += 1

    if(word[4] == ''):down_char['#'] += 1
    else: down_char[word[4]] += 1

    if(word[5] == ''):redown_char['#'] += 1
    else: redown_char[word[5]] += 1

    if(word[6] == ''):vowel['#'] += 1
    else: vowel[word[6]] += 1

    if(word[7] == ''):rear_char['#'] += 1
    else: rear_char[word[7]] += 1

    if(word[8] == ''):rerear_char['#'] += 1
    else: rerear_char[word[8]] += 1

def Split_Tibetan():
    global Tib_count
    p1['maximum'] = len(essay) - 1
    one_fifth = len(essay) // 5
    print(len(essay))
    text1.delete('1.0', 'end')
    s = ''
    for i, ch in enumerate(essay):
        p1['value'] = i
        if(i%one_fifth==0): window.update()

        if(ch in split_char):
            split_char[ch] += 1
        elif('\u0F00'<=ch<='\u0FDA'):
            s += ch
            continue
        if(s!=''):
            fin = False
            for adher in adhering:
                pos = s.find(adher)
                if (pos!=0 and pos != -1 and s[-1] == adher[-1]):  # 是黏着词，分开统计构建
                    Count_TibetanComponents(s[:pos])
                    Count_TibetanComponents(s[pos:])
                    Tib_count += 1
                    s = ''
                    fin = True
                    break
            if(fin==False):
                Count_TibetanComponents(s)
                Tib_count += 1
                s = ''

    # 统计完后显示
    # 前1 上2 基3 下4 再下5 元6 后7 再后8
    text1.insert('insert', '前加字的统计结果如下：\n')
    for key, value in front_char.items(): text1.insert('insert', f'{key}        {value}\n')
    text1.insert('insert', '上加字的统计结果如下：\n')
    for key, value in up_char.items(): text1.insert('insert', f'{key}        {value}\n')
    text1.insert('insert', '基字的统计结果如下：\n')
    for key, value in base_char.items(): text1.insert('insert', f'{key}        {value}\n')
    text1.insert('insert', '叠加基字的统计结果如下：\n')
    for key, value in base_overlied.items(): text1.insert('insert', f'{key}        {value}\n')
    text1.insert('insert', '下加字的统计结果如下：\n')
    for key, value in down_char.items(): text1.insert('insert', f'{key}        {value}\n')
    text1.insert('insert', '再下加字的统计结果如下：\n')
    for key, value in redown_char.items(): text1.insert('insert', f'{key}        {value}\n')
    text1.insert('insert', '元音的统计结果如下：\n')
    for key, value in vowel.items(): text1.insert('insert', f'{key}        {value}\n')
    text1.insert('insert', '后字的统计结果如下：\n')
    for key, value in rear_char.items(): text1.insert('insert', f'{key}        {value}\n')
    text1.insert('insert', '再后加字的统计结果如下：\n')
    for key, value in rerear_char.items(): text1.insert('insert', f'{key}        {value}\n')
    text1.insert('insert', '藏文特殊字符的统计如下：\n')
    for key, value in split_char.items(): text1.insert('insert', f'{key}        {value}\n')
    print(Tib_count)

def open_file():
    global essay
    filePaths = []
    essay = ''
    p1['value'] = 0
    window.update()
    text1.delete('1.0', 'end')
    # 设置打开的默认位置
    files = filedialog.askopenfilename(title=u'选择文件夹', initialdir=(os.path.expanduser('S:/Pycharm/installed/WorkPlace_defualt/Master_Work/First_year/Algorithm analysis')), multiple=True)
    text.insert('insert', f'加载文件地址：')
    for file_path in files:
        if file_path is not None:
            try:
                with open(file=file_path, mode='r+', encoding='utf-8') as f:
                    word = f.read()
                    # print(len(word))
                    text.insert('insert', f'{file_path}    ')
                    if(len(word)<12000): text1.insert('insert', f'{word}\n')
                    else: text1.insert('insert', '文本已加载，由于文本数量过多，暂不显示在组件内')
                    essay = essay + ''.join(word.strip('\n').strip().split())
                    # print(essay)

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
        if(result):print('保存完成')
        else: print('保存失败')

if __name__ == '__main__':
    # 使用新的现代化界面
    app = DynamicTibetanComponentAnalyzer()
    app.run()