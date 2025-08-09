
import time
import os
from tqdm import tqdm
# =================== SplitComponent.py ===================
# 30个辅音
consonant = ['\u0F40', '\u0F41', '\u0F42', '\u0F44', '\u0F45', '\u0F46', '\u0F47', '\u0F49',
             '\u0F4F', '\u0F50', '\u0F51', '\u0F53', '\u0F54', '\u0F55', '\u0F56', '\u0F58',
             '\u0F59', '\u0F5A', '\u0F5B', '\u0F5D', '\u0F5E', '\u0F5F', '\u0F60', '\u0F61',
             '\u0F62', '\u0F63', '\u0F64', '\u0F66', '\u0F67', '\u0F68']
# 4个元音
vowel = ['\u0F72', '\u0F74', '\u0F7A', '\u0F7C']
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

class Split_component(object):
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

    # 当音节为两个字符的时候，传入此音节在 words_18785 中的位置。以此类推
    def Two_chars(self, Tibetan):
        word = ['' for _ in range(10)]
        fin = False
        pos = [-1, -1]
        word[0] = Tibetan
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
        for vow in vowel:
            if (Tibetan[-1] == vow):
                pos[1] = 6
                word[-1] = '基字+元音'
                fin = True
                break
        if (fin == False):
            pos[1] = 7
            word[-1] = '基字+后加字'
            fin = True

        # 如果不能分类，报错
        if(fin==False): print(word)
        assert fin
        for i, char_cur in enumerate(pos):
            word[char_cur] = Tibetan[i]

        return word

    # 当音节为三个字符的时候，传入此音节在 words_18785 中的位置
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

        for vow in vowel:
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

        assert fin
        for i, char_cur in enumerate(pos):
            word[char_cur] = Tibetan[i]

        return word

    def Four_chars(self, Tibetan):
        word = ['' for _ in range(10)]
        fin = False
        word[0] = Tibetan
        pos = [-1 for i in range(4)]

        for vow in vowel:
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

        assert fin
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
            for vow in vowel:
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

        if (fin == False): print(word)
        assert fin
        for i, char_cur in enumerate(pos):
            word[char_cur] = Tibetan[i]

        return word

    def Six_chars(self, Tibetan):
        word = ['' for _ in range(10)]
        fin = False
        word[0] = Tibetan
        pos = [-1 for i in range(6)]

        for vow in vowel:
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
        assert fin
        for i, char_cur in enumerate(pos):
            word[char_cur] = Tibetan[i]

        return word

    def Seven_chars(self, Tibetan):
        word = ['' for _ in range(10)]
        fin = False
        word[0] = Tibetan
        pos = [-1 for i in range(7)]
        for vow in vowel:
            if (Tibetan.find(vow) == 4):
                pos[0], pos[1], pos[2], pos[3], pos[4], pos[5], pos[6] = 1, 2, 3, 4, 6, 7, 8
                word[-1] = '前加字+上加字+基字+下加字+元音+后加字+再后加字'
                fin = True
                break

        assert fin
        for i, char_cur in enumerate(pos):
            word[char_cur] = Tibetan[i]

        return word
# =================== Cmp.py ===================
def cmp(a, b):
    for i in range(1, 9):
        if (a[i] == b[i]): continue
        return a[i] < b[i]
    return True

def Adjust_heap(unsorted, l, r, reverse):
    root = l
    child = root * 2 + 1
    while (child <= r):
        if (child + 1 <= r and cmp(unsorted[child + 1], unsorted[child]) == reverse):
            child += 1
        if (cmp(unsorted[child] , unsorted[root]) == reverse):
            unsorted[root], unsorted[child] = unsorted[child], unsorted[root]
            root = child
            child = root * 2 + 1
        else:
            break

def Heap_sort(unsorted, reverse=False, show_progress=True):
    leaf = len(unsorted) // 2 - 1
    if show_progress:
        for st in tqdm(range(leaf, -1, -1), desc="建堆", unit="步"):
            Adjust_heap(unsorted, st, len(unsorted) - 1, reverse)
        for ed in tqdm(range(len(unsorted) - 1, 0, -1), desc="堆排序", unit="步"):
            unsorted[0], unsorted[ed] = unsorted[ed], unsorted[0]
            Adjust_heap(unsorted, 0, ed - 1, reverse)
    else:
        for st in range(leaf, -1, -1):
            Adjust_heap(unsorted, st, len(unsorted) - 1, reverse)
        for ed in range(len(unsorted) - 1, 0, -1):
            unsorted[0], unsorted[ed] = unsorted[ed], unsorted[0]
            Adjust_heap(unsorted, 0, ed - 1, reverse)
    return unsorted

def load_tibet_file(file_path):
    split_com = Split_component()
    word_18785_ns = []
    with open(file_path, mode='r', encoding='utf-8') as f:
        lines = f.readlines()
        for Tibetan in tqdm([line.strip('\n') for line in lines], desc="解析字符", unit="行"):
            if not Tibetan:
                continue
            word = split_com.Split(Tibetan)[:-1]
            for i in range(1, 9):
                if (word[i] != ''):
                    word[i] = ord(word[i])
                else:
                    word[i] = 0
            word[1], word[3] = word[3], word[1]
            for i in range(1, 9):
                if (0x0F90<=word[i]<=0x0FB8):
                    word[i] = word[i] - 80
            word_18785_ns.append(word)
    return word_18785_ns

def save_result(words, save_path):
    with open(save_path, 'w', encoding='utf-8') as f:
        for word in tqdm(words, desc=f"写入{os.path.basename(save_path)}", unit="行"):
            f.write(word[0] + '\n')

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="藏文堆排序，无GUI，带进度条")
    parser.add_argument('--file', type=str, required=True, help='待排序的txt文件路径')
    parser.add_argument('--reverse', action='store_true', help='降序排序（默认升序）')
    parser.add_argument('--output', type=str, default='sorted_tibet.txt', help='排序结果保存路径')
    args = parser.parse_args()

    print(f"加载文件：{args.file}")
    word_18785_ns = load_tibet_file(args.file)
    print(f"共加载 {len(word_18785_ns)} 行")

    print("开始排序...")
    t1 = time.time()
    Heap_sort(word_18785_ns, reverse=args.reverse, show_progress=True)
    t2 = time.time()
    print(f"排序完成，用时 {t2-t1:.2f} 秒")

    print(f"保存排序结果到 {args.output}")
    save_result(word_18785_ns, args.output)
    print("全部完成！")

    # 执行时示例：
    # python Heap_Sort.py --file T4_demo/tibet.txt --reverse --output sorted_desc.txt