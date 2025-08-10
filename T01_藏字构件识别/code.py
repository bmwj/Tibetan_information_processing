# coding:utf-8
# 创建者：Pemawangchuk
# 版本：1.0
# 日期：2025-01-04
# 功能：藏文音节分类
import xlwt
from collections import Counter

# 所有的分类类别
CLASS_NAMES = [
    '辅音字母', '基字+元音', '基字+后加字', '上加字+基字', '基字+下加字',
    '前加字+基字+后加字', '前加字+基字+元音', '前加字+上加字+基字', '前加字+基字+下加字',
    '上加字+基字+元音', '上加字+基字+下加字', '基字+下加字+再下加字', '上加字+基字+后加字',
    '基字+下加字+元音', '基字+下加字+后加字', '基字+元音+后加字', '基字+后加字+再后加字',
    '前加字+上加字+基字+元音', '前加字+基字+下加字+元音', '前加字+基字+元音+后加字',
    '前加字+上加字+基字+下加字', '前加字+上加字+基字+后加字', '前加字+基字+下加字+后加字',
    '前加字+基字+后加字+再后加字', '上加字+基字+下加字+元音', '上加字+基字+元音+后加字',
    '上加字+基字+下加字+后加字', '上加字+基字+后加字+再后加字', '基字+元音+后加字+再后加字',
    '基字+下加字+元音+后加字', '基字+下加字+后加字+再后加字', '基字+下加字+再下加字+元音',
    '基字+下加字+再下加字+后加字', '前加字+上加字+基字+下加字+元音',
    '前加字+上加字+基字+下加字+后加字', '前加字+上加字+基字+元音+后加字',
    '前加字+上加字+基字+后加字+再后加字', '前加字+基字+下加字+元音+后加字',
    '前加字+基字+下加字+后加字+再后加字', '前加字+基字+元音+后加字+再后加字',
    '上加字+基字+下加字+元音+后加字', '上加字+基字+下加字+后加字+再后加字',
    '上加字+基字+元音+后加字+再后加字', '基字+下加字+元音+后加字+再后加字',
    '基字+下加字+再下加字+元音+后加字', '基字+下加字+再下加字+后加字+再后加字',
    '前加字+上加字+基字+下加字+元音+后加字', '前加字+基字+下加字+元音+后加字+再后加字',
    '前加字+上加字+基字+元音+后加字+再后加字', '前加字+上加字+基字+下加字+后加字+再后加字',
    '上加字+基字+下加字+元音+后加字+再后加字', '基字+下加字+再下加字+元音+后加字+再后加字',
    '前加字+上加字+基字+下加字+元音+后加字+再后加字'
]

# 藏文字母和组合
CONSONANTS = ['\u0F40', '\u0F41', '\u0F42', '\u0F44', '\u0F45', '\u0F46', '\u0F47', '\u0F49',
              '\u0F4F', '\u0F50', '\u0F51', '\u0F53', '\u0F54', '\u0F55', '\u0F56', '\u0F58',
              '\u0F59', '\u0F5A', '\u0F5B', '\u0F5D', '\u0F5E', '\u0F5F', '\u0F60', '\u0F61',
              '\u0F62', '\u0F63', '\u0F64', '\u0F66', '\u0F67', '\u0F68']
VOWELS = ['\u0F72', '\u0F74', '\u0F7A', '\u0F7C']
UP_BASE_2 = ['རྐ', 'རྒ', 'རྔ', 'རྗ', 'རྙ', 'རྟ', 'རྡ', 'རྣ', 'རྦ', 'རྨ', 'རྩ', 'རྫ', 'ལྐ', 'ལྒ', 'ལྔ',
             'ལྕ', 'ལྗ', 'ལྟ', 'ལྡ', 'ལྤ', 'ལྦ', 'ལྷ', 'སྐ', 'སྒ', 'སྔ', 'སྙ', 'སྟ', 'སྡ', 'སྣ', 'སྤ',
             'སྦ', 'སྨ', 'སྩ']
BASE_DOWN_2 = ['ཀྱ', 'ཁྱ', 'གྱ', 'པྱ', 'ཕྱ', 'བྱ', 'མྱ', 'ཀྲ', 'ཁྲ', 'གྲ', 'ཏྲ', 'ཐྲ', 'དྲ', 'པྲ', 'ཕྲ',
               'བྲ', 'སྲ', 'ཧྲ', 'ཀླ', 'གླ', 'བླ', 'ཟླ', 'རླ', 'སླ', 'ཀྭ', 'ཁྭ', 'གྭ', 'ཉྭ', 'དྭ', 'ཚྭ',
               'ཞྭ', 'ཟྭ', 'རྭ', 'ལྭ', 'ཤྭ', 'ཧྭ']
AFTER_REAFTER_2 = ['ནད', 'རད', 'ལད', 'གས', 'ངས', 'བས', 'མས']
UP_BASE_DOWN_3 = ['རྐྱ', 'རྒྱ', 'རྨྱ', 'སྐྱ', 'སྒྱ', 'སྤྱ', 'སྦྱ', 'སྨྱ', 'སྐྲ', 'སྒྲ', 'སྣྲ', 'སྤྲ', 'སྦྲ', 'སྨྲ', 'རྩྭ']
BASE_AFTER_REAFTER_3 = ['བགས', 'མབས', 'གགས', 'བངས', 'དངས', 'གངs', 'འངས', 'གམས', 'མམས', 'བབས', 'མངས', 'གབས', 'བམs', 'འམས']
BASE_UNDER_REUNDER_3 = ['གྲྭ', 'ཕྱྭ']

# 构件位置映射
POS_MAPPING = {
    '辅音字母': [3],
    '基字+元音': [3, 6],
    '基字+后加字': [3, 7],
    '上加字+基字': [2, 3],
    '基字+下加字': [3, 4],
    '前加字+基字+后加字': [1, 3, 7],
    '前加字+基字+元音': [1, 3, 6],
    '前加字+上加字+基字': [1, 2, 3],
    '前加字+基字+下加字': [1, 3, 4],
    '上加字+基字+元音': [2, 3, 6],
    '上加字+基字+下加字': [2, 3, 4],
    '基字+下加字+再下加字': [3, 4, 5],
    '上加字+基字+后加字': [2, 3, 7],
    '基字+下加字+元音': [3, 4, 6],
    '基字+下加字+后加字': [3, 4, 7],
    '基字+元音+后加字': [3, 6, 7],
    '基字+后加字+再后加字': [3, 7, 8],
    '前加字+上加字+基字+元音': [1, 2, 3, 6],
    '前加字+基字+下加字+元音': [1, 3, 4, 6],
    '前加字+基字+元音+后加字': [1, 3, 6, 7],
    '前加字+上加字+基字+下加字': [1, 2, 3, 4],
    '前加字+上加字+基字+后加字': [1, 2, 3, 7],
    '前加字+基字+下加字+后加字': [1, 3, 4, 7],
    '前加字+基字+后加字+再后加字': [1, 3, 7, 8],
    '上加字+基字+下加字+元音': [2, 3, 4, 6],
    '上加字+基字+元音+后加字': [2, 3, 6, 7],
    '上加字+基字+下加字+后加字': [2, 3, 4, 7],
    '上加字+基字+后加字+再后加字': [2, 3, 7, 8],
    '基字+元音+后加字+再后加字': [3, 6, 7, 8],
    '基字+下加字+元音+后加字': [3, 4, 6, 7],
    '基字+下加字+后加字+再后加字': [3, 4, 7, 8],
    '基字+下加字+再下加字+元音': [3, 4, 5, 6],
    '基字+下加字+再下加字+后加字': [3, 4, 5, 7],
    '前加字+上加字+基字+下加字+元音': [1, 2, 3, 4, 6],
    '前加字+上加字+基字+下加字+后加字': [1, 2, 3, 4, 7],
    '前加字+上加字+基字+元音+后加字': [1, 2, 3, 6, 7],
    '前加字+上加字+基字+后加字+再后加字': [1, 2, 3, 7, 8],
    '前加字+基字+下加字+元音+后加字': [1, 3, 4, 6, 7],
    '前加字+基字+下加字+后加字+再后加字': [1, 3, 4, 7, 8],
    '前加字+基字+元音+后加字+再后加字': [1, 3, 6, 7, 8],
    '上加字+基字+下加字+元音+后加字': [2, 3, 4, 6, 7],
    '上加字+基字+下加字+后加字+再后加字': [2, 3, 4, 7, 8],
    '上加字+基字+元音+后加字+再后加字': [2, 3, 6, 7, 8],
    '基字+下加字+元音+后加字+再后加字': [3, 4, 6, 7, 8],
    '基字+下加字+再下加字+元音+后加字': [3, 4, 5, 6, 7],
    '基字+下加字+再下加字+后加字+再后加字': [3, 4, 5, 7, 8],
    '前加字+上加字+基字+下加字+元音+后加字': [1, 2, 3, 4, 6, 7],
    '前加字+基字+下加字+元音+后加字+再后加字': [1, 3, 4, 6, 7, 8],
    '前加字+上加字+基字+元音+后加字+再后加字': [1, 2, 3, 6, 7, 8],
    '前加字+上加字+基字+下加字+后加字+再后加字': [1, 2, 3, 4, 7, 8],
    '上加字+基字+下加字+元音+后加字+再后加字': [2, 3, 4, 6, 7, 8],
    '基字+下加字+再下加字+元音+后加字+再后加字': [3, 4, 5, 6, 7, 8],
    '前加字+上加字+基字+下加字+元音+后加字+再后加字': [1, 2, 3, 4, 6, 7, 8]
}

def parse_syllable(syllable, index, words_18785):
    """解析藏文音节并分配构件到指定位置"""
    length = len(syllable)
    if length not in range(1, 8):
        print(f"音节 {syllable} 长度异常，需额外处理")
        return

    # 根据音节长度选择处理函数
    parsers = {
        1: parse_one_char,
        2: parse_two_chars,
        3: parse_three_chars,
        4: parse_four_chars,
        5: parse_five_chars,
        6: parse_six_chars,
        7: parse_seven_chars
    }
    parsers[length](syllable, index, words_18785)

def parse_one_char(syllable, index, words_18785):
    words_18785[index][3] = syllable[0]
    words_18785[index][-1] = '辅音字母'

def parse_two_chars(syllable, index, words_18785):
    if syllable in UP_BASE_2:
        words_18785[index][2:4] = list(syllable)
        words_18785[index][-1] = '上加字+基字'
    elif syllable in BASE_DOWN_2:
        words_18785[index][3:5] = list(syllable)
        words_18785[index][-1] = '基字+下加字'
    elif syllable[-1] in VOWELS:
        words_18785[index][3], words_18785[index][6] = syllable[0], syllable[1]
        words_18785[index][-1] = '基字+元音'
    else:
        words_18785[index][3], words_18785[index][7] = syllable[0], syllable[1]
        words_18785[index][-1] = '基字+后加字'

def parse_three_chars(syllable, index, words_18785):
    if syllable in BASE_UNDER_REUNDER_3:
        words_18785[index][3:6] = list(syllable)
        words_18785[index][-1] = '基字+下加字+再下加字'
        return
    if syllable in BASE_AFTER_REAFTER_3:
        words_18785[index][3], words_18785[index][7:9] = syllable[0], list(syllable[1:])
        words_18785[index][-1] = '基字+后加字+再后加字'
        return
    if syllable in UP_BASE_DOWN_3:
        words_18785[index][2:5] = list(syllable)
        words_18785[index][-1] = '上加字+基字+下加字'
        return

    for vow in VOWELS:
        ppos = syllable.find(vow)
        if ppos == 1:
            words_18785[index][3], words_18785[index][6], words_18785[index][7] = syllable[0], vow, syllable[2]
            words_18785[index][-1] = '基字+元音+后加字'
            return
        elif ppos == 2:
            if syllable[:2] in UP_BASE_2:
                words_18785[index][2:4], words_18785[index][6] = list(syllable[:2]), vow
                words_18785[index][-1] = '上加字+基字+元音'
                return
            elif syllable[:2] in BASE_DOWN_2:
                words_18785[index][3:5], words_18785[index][6] = list(syllable[:2]), vow
                words_18785[index][-1] = '基字+下加字+元音'
                return
            else:
                words_18785[index][1], words_18785[index][3], words_18785[index][6] = syllable[0], syllable[1], vow
                words_18785[index][-1] = '前加字+基字+元音'
                return

    for up_base in UP_BASE_2:
        ppos = syllable.find(up_base)
        if ppos == 1:
            words_18785[index][1:4] = list(syllable)
            words_18785[index][-1] = '前加字+上加字+基字'
            return
        elif ppos == 0:
            words_18785[index][2:4], words_18785[index][7] = list(syllable[:2]), syllable[2]
            words_18785[index][-1] = '上加字+基字+后加字'
            return

    for base_down in BASE_DOWN_2:
        ppos = syllable.find(base_down)
        if ppos == 1:
            words_18785[index][1], words_18785[index][3:5] = syllable[0], list(syllable[1:])
            words_18785[index][-1] = '前加字+基字+下加字'
            return
        elif ppos == 0:
            words_18785[index][3:5], words_18785[index][7] = list(syllable[:2]), syllable[2]
            words_18785[index][-1] = '基字+下加字+后加字'
            return

    for after_reafter in AFTER_REAFTER_2:
        if syllable[1:] == after_reafter:
            words_18785[index][3], words_18785[index][7:9] = syllable[0], list(syllable[1:])
            words_18785[index][-1] = '基字+后加字+再后加字'
            return

    words_18785[index][1], words_18785[index][3], words_18785[index][7] = syllable
    words_18785[index][-1] = '前加字+基字+后加字'

def parse_four_chars(syllable, index, words_18785):
    for vow in VOWELS:
        ppos = syllable.find(vow)
        if ppos == 3:
            if syllable[:3] in BASE_UNDER_REUNDER_3:
                words_18785[index][3:6], words_18785[index][6] = list(syllable[:3]), vow
                words_18785[index][-1] = '基字+下加字+再下加字+元音'
                return
            elif syllable[:2] in UP_BASE_2:
                words_18785[index][2:5], words_18785[index][6] = list(syllable[:3]), vow
                words_18785[index][-1] = '上加字+基字+下加字+元音'
                return
            elif syllable[1:3] in UP_BASE_2:
                words_18785[index][1:4], words_18785[index][6] = list(syllable[:3]), vow
                words_18785[index][-1] = '前加字+上加字+基字+元音'
                return
            elif syllable[1:3] in BASE_DOWN_2:
                words_18785[index][1], words_18785[index][3:5], words_18785[index][6] = syllable[0], list(syllable[1:3]), vow
                words_18785[index][-1] = '前加字+基字+下加字+元音'
                return
        elif ppos == 2:
            if syllable[:2] in UP_BASE_2:
                words_18785[index][2:4], words_18785[index][6], words_18785[index][7] = list(syllable[:2]), vow, syllable[3]
                words_18785[index][-1] = '上加字+基字+元音+后加字'
                return
            elif syllable[:2] in BASE_DOWN_2:
                words_18785[index][3:5], words_18785[index][6], words_18785[index][7] = list(syllable[:2]), vow, syllable[3]
                words_18785[index][-1] = '基字+下加字+元音+后加字'
                return
            else:
                words_18785[index][1], words_18785[index][3], words_18785[index][6], words_18785[index][7] = syllable[0], syllable[1], vow, syllable[3]
                words_18785[index][-1] = '前加字+基字+元音+后加字'
                return
        elif ppos == 1:
            words_18785[index][3], words_18785[index][6:9] = syllable[0], list(syllable[1:])
            words_18785[index][-1] = '基字+元音+后加字+再后加字'
            return

    for base_under_reunder in BASE_UNDER_REUNDER_3:
        if syllable.startswith(base_under_reunder):
            words_18785[index][3:6], words_18785[index][7] = list(syllable[:3]), syllable[3]
            words_18785[index][-1] = '基字+下加字+再下加字+后加字'
            return

    for up_base_down in UP_BASE_DOWN_3:
        ppos = syllable.find(up_base_down)
        if ppos == 1:
            words_18785[index][1:5] = list(syllable)
            words_18785[index][-1] = '前加字+上加字+基字+下加字'
            return
        elif ppos == 0:
            words_18785[index][2:5], words_18785[index][7] = list(syllable[:3]), syllable[3]
            words_18785[index][-1] = '上加字+基字+下加字+后加字'
            return

    for up_base in UP_BASE_2:
        ppos = syllable.find(up_base)
        if ppos == 1:
            words_18785[index][1:4], words_18785[index][7] = list(syllable[:3]), syllable[3]
            words_18785[index][-1] = '前加字+上加字+基字+后加字'
            return
        elif ppos == 0:
            words_18785[index][2:4], words_18785[index][7:9] = list(syllable[:2]), list(syllable[2:])
            words_18785[index][-1] = '上加字+基字+后加字+再后加字'
            return

    for base_down in BASE_DOWN_2:
        ppos = syllable.find(base_down)
        if ppos == 1:
            words_18785[index][1], words_18785[index][3:5], words_18785[index][7] = syllable[0], list(syllable[1:3]), syllable[3]
            words_18785[index][-1] = '前加字+基字+下加字+后加字'
            return
        elif ppos == 0:
            if syllable[2:] in AFTER_REAFTER_2:
                words_18785[index][3:5], words_18785[index][7:9] = list(syllable[:2]), list(syllable[2:])
                words_18785[index][-1] = '基字+下加字+后加字+再后加字'
                return

    if syllable[2:] in AFTER_REAFTER_2:
        words_18785[index][1], words_18785[index][3], words_18785[index][7:9] = syllable[0], syllable[1], list(syllable[2:])
        words_18785[index][-1] = '前加字+基字+后加字+再后加字'

def parse_five_chars(syllable, index, words_18785):
    for base_under_reunder in BASE_UNDER_REUNDER_3:
        if syllable.startswith(base_under_reunder) and syllable[3:] in AFTER_REAFTER_2:
            words_18785[index][3:6], words_18785[index][7:9] = list(syllable[:3]), list(syllable[3:])
            words_18785[index][-1] = '基字+下加字+再下加字+后加字+再后加字'
            return

    for vow in VOWELS:
        ppos = syllable.find(vow)
        if ppos == 4:
            words_18785[index][1:5], words_18785[index][6] = list(syllable[:4]), vow
            words_18785[index][-1] = '前加字+上加字+基字+下加字+元音'
            return
        elif ppos == 3:
            if syllable[:3] in BASE_UNDER_REUNDER_3:
                words_18785[index][3:6], words_18785[index][6], words_18785[index][7] = list(syllable[:3]), vow, syllable[4]
                words_18785[index][-1] = '基字+下加字+再下加字+元音+后加字'
                return
            elif syllable[1:3] in UP_BASE_2:
                words_18785[index][1:4], words_18785[index][6], words_18785[index][7] = list(syllable[:3]), vow, syllable[4]
                words_18785[index][-1] = '前加字+上加字+基字+元音+后加字'
                return
            elif syllable[:2] in UP_BASE_2:
                words_18785[index][2:5], words_18785[index][6], words_18785[index][7] = list(syllable[:3]), vow, syllable[4]
                words_18785[index][-1] = '上加字+基字+下加字+元音+后加字'
                return
            elif syllable[1:3] in BASE_DOWN_2:
                words_18785[index][1], words_18785[index][3:5], words_18785[index][6], words_18785[index][7] = syllable[0], list(syllable[1:3]), vow, syllable[4]
                words_18785[index][-1] = '前加字+基字+下加字+元音+后加字'
                return
        elif ppos == 2:
            if syllable[:2] in UP_BASE_2:
                words_18785[index][2:4], words_18785[index][6:9] = list(syllable[:2]), list(syllable[2:])
                words_18785[index][-1] = '上加字+基字+元音+后加字+再后加字'
                return
            elif syllable[:2] in BASE_DOWN_2:
                words_18785[index][3:5], words_18785[index][6:9] = list(syllable[:2]), list(syllable[2:])
                words_18785[index][-1] = '基字+下加字+元音+后加字+再后加字'
                return
            elif syllable[3:] in AFTER_REAFTER_2:
                words_18785[index][1], words_18785[index][3], words_18785[index][6:9] = syllable[0], syllable[1], list(syllable[2:])
                words_18785[index][-1] = '前加字+基字+元音+后加字+再后加字'
                return

    for up_base_down in UP_BASE_DOWN_3:
        ppos = syllable.find(up_base_down)
        if ppos == 1:
            words_18785[index][1:5], words_18785[index][7] = list(syllable[:4]), syllable[4]
            words_18785[index][-1] = '前加字+上加字+基字+下加字+后加字'
            return
        elif ppos == 0 and syllable[3:] in AFTER_REAFTER_2:
            words_18785[index][2:5], words_18785[index][7:9] = list(syllable[:3]), list(syllable[3:])
            words_18785[index][-1] = '上加字+基字+下加字+后加字+再后加字'
            return

    for up_base in UP_BASE_2:
        if syllable[1:3] == up_base:
            words_18785[index][1:4], words_18785[index][7:9] = list(syllable[:3]), list(syllable[3:])
            words_18785[index][-1] = '前加字+上加字+基字+后加字+再后加字'
            return

    for base_down in BASE_DOWN_2:
        if syllable[1:3] == base_down:
            words_18785[index][1], words_18785[index][3:5], words_18785[index][7:9] = syllable[0], list(syllable[1:3]), list(syllable[3:])
            words_18785[index][-1] = '前加字+基字+下加字+后加字+再后加字'

def parse_six_chars(syllable, index, words_18785):
    for vow in VOWELS:
        ppos = syllable.find(vow)
        if ppos == 4:
            words_18785[index][1:5], words_18785[index][6], words_18785[index][7] = list(syllable[:4]), vow, syllable[5]
            words_18785[index][-1] = '前加字+上加字+基字+下加字+元音+后加字'
            return
        elif ppos == 3:
            if syllable[:3] in BASE_UNDER_REUNDER_3 and syllable[4:] in AFTER_REAFTER_2:
                words_18785[index][3:6], words_18785[index][6:9] = list(syllable[:3]), list(syllable[3:])
                words_18785[index][-1] = '基字+下加字+再下加字+元音+后加字+再后加字'
                return
            elif syllable[1:3] in UP_BASE_2:
                words_18785[index][1:4], words_18785[index][6:9] = list(syllable[:3]), list(syllable[3:])
                words_18785[index][-1] = '前加字+上加字+基字+元音+后加字+再后加字'
                return
            elif syllable[:2] in UP_BASE_2:
                words_18785[index][2:5], words_18785[index][6:9] = list(syllable[:3]), list(syllable[3:])
                words_18785[index][-1] = '上加字+基字+下加字+元音+后加字+再后加字'
                return
            elif syllable[1:3] in BASE_DOWN_2:
                words_18785[index][1], words_18785[index][3:5], words_18785[index][6:9] = syllable[0], list(syllable[1:3]), list(syllable[3:])
                words_18785[index][-1] = '前加字+基字+下加字+元音+后加字+再后加字'
                return

    if syllable[1:4] in UP_BASE_DOWN_3:
        words_18785[index][1:5], words_18785[index][7:9] = list(syllable[:4]), list(syllable[4:])
        words_18785[index][-1] = '前加字+上加字+基字+下加字+后加字+再后加字'

def parse_seven_chars(syllable, index, words_18785):
    for vow in VOWELS:
        if syllable.find(vow) == 4:
            words_18785[index][1:5], words_18785[index][6:9] = list(syllable[:4]), list(syllable[4:])
            words_18785[index][-1] = '前加字+上加字+基字+下加字+元音+后加字+再后加字'
            return

def main():
    words_18785 = []
    # 读取藏文音节
    try:
        with open('./全藏字.txt', 'r', encoding='utf-8') as f:
            for line in f:
                syllable = line.strip()
                if syllable:
                    words_18785.append([syllable] + [''] * 8 + ['未知结构'])
    except FileNotFoundError:
        print("错误：未找到文件 '全藏字.txt'")
        return
    except Exception as e:
        print(f"读取文件时发生错误：{e}")
        return

    # 解析音节
    for i, word in enumerate(words_18785):
        parse_syllable(word[0], i, words_18785)

    # 统计类别
    class_counts = Counter(word[-1] for word in words_18785)
    total_chars = sum(class_counts.values())
    valid_classes = [c for c in CLASS_NAMES if c in class_counts]

    # 按类别名长度排序并打印
    sorted_counts = sorted(
        [(name, class_counts[name]) for name in valid_classes],
        key=lambda x: len(x[0])
    )
    for i, (name, count) in enumerate(sorted_counts, 1):
        print(f"{i}. {name} = {count}")

    print(f"总类别个数为：{len(valid_classes)}，总输出的字符个数为：{total_chars}")
    print(f"总音节数：{len(words_18785)}")

    # 保存到 Excel
    try:
        excel = xlwt.Workbook(encoding='utf-8')
        sheet = excel.add_sheet('字符结构', cell_overwrite_ok=True)
        columns = ('藏字', '前加字', '上加字', '基字', '下加字', '再下加字', '元音', '后加字', '再后加字', '类别名')
        for i, col in enumerate(columns):
            sheet.write(0, i, col)

        for i, word in enumerate(words_18785, 1):
            for j, value in enumerate(word):
                sheet.write(i, j, value)

        excel.save('./Classified.xls')
        print("已成功保存到 Classified.xls")
    except Exception as e:
        print(f"保存 Excel 文件时发生错误：{e}")

if __name__ == '__main__':
    main()