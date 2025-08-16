# -*- coding: UTF-8 -*-
# 构件分析模块 - 包含藏文构件分析的核心逻辑

from data_structures import *

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


def int2uni(num):
    """数字转Unicode"""
    return ('\\u{:0>4x}'.format(num)).encode().decode('unicode_escape')


class ComponentAnalyzer:
    """藏文构件分析器"""
    
    def __init__(self):
        self.words_18785 = []
        self.tib_count = 0
        self.init_components()
        
    def init_components(self):
        """初始化构件"""
        self.creCom = Create_18785Com()
        self.creCom.Create(self.words_18785)
        
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
            base_char[int2uni(ord(word[3]) - 80)] += 1
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
            
    def analyze_text(self, text, update_callback=None):
        """分析文本中的藏文构件
        
        Args:
            text: 要分析的文本
            update_callback: 更新进度的回调函数，接收参数(current, total, progress_percent)
        
        Returns:
            tuple: (处理时间, 总字符数, 藏文音节数)
        """
        # 重置计数器
        reset_counters()
        self.tib_count = 0
        
        # 开始计时
        import time
        start_time = time.time()
        
        total_chars = len(text)
        one_fifth = max(1, total_chars // 100)  # 更频繁的更新
        
        s = ''
        for i, ch in enumerate(text):
            # 更新进度
            if update_callback and i % one_fifth == 0:
                progress = (i / total_chars) * 100
                update_callback(i, total_chars, progress)

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
        
        return process_time, total_chars, self.tib_count
        
    def get_statistics_results(self):
        """获取统计结果
        
        Returns:
            dict: 包含各类构件统计结果的字典
        """
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
        
        results = {}
        for type_name, char_dict in component_types:
            # 按频次排序
            sorted_items = sorted(char_dict.items(), key=lambda x: x[1], reverse=True)
            results[type_name] = sorted_items
            
        return results
