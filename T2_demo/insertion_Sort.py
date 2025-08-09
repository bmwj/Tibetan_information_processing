import time
import xlrd
from tqdm import tqdm

file_path = 'Classified.xls'
data = xlrd.open_workbook(file_path, encoding_override='utf-8')
table = data.sheets()[0]

# 带圈的辅音需要转化为不带圈进行对比
constant_unconverted = [
    0x0F90, 0x0F91, 0x0F92, 0x0F94, 0x0F95, 0x0F96, 0x0F97, 0x0F99, 0x0F9F, 0x0FA0,
    0x0FA1, 0x0FA3, 0x0FA4, 0x0FA5, 0x0FA6, 0x0FA8, 0x0FA9, 0x0FAA, 0x0FAB, 0x0FAE,
    0x0FAF, 0x0FB0, 0x0FB3, 0x0FB4, 0x0FB6, 0x0FB7, 0x0FB8, 0x0FBA, 0x0FBB, 0x0FBC
]

def import_excelTable(table):
    # 书写顺序：前1，上2，基3，下4，再下5，元6，后7，再后8
    # 排序顺序：基1，上2，前3，下4，再下5，元音6，后7，再后8
    word_18785_ns = []
    for i in tqdm(range(1, table.nrows), desc="读取Excel", unit="行"):
        word = table.row_values(i)
        for j in range(1, 9):
            if word[j] != '':
                word[j] = ord(word[j])
            else:
                word[j] = 0
        word[1], word[3] = word[3], word[1]
        for j in range(1, 9):
            if word[j] in constant_unconverted:
                word[j] = word[j] - 80
        word_18785_ns.append(word)
    return word_18785_ns

def cmp(a, b):
    for i in range(1, 9):
        if a[i] == b[i]:
            continue
        return a[i] < b[i]
    return False

def insertion_sort_asc(arr):
    """
    升序插入排序
    """
    for i in tqdm(range(1, len(arr)), desc="升序插入排序", unit="项"):
        key = arr[i]
        j = i - 1
        while j >= 0 and cmp(arr[j], key):
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

def insertion_sort_desc(arr):
    """
    降序插入排序
    """
    for i in tqdm(range(1, len(arr)), desc="降序插入排序", unit="项"):
        key = arr[i]
        j = i - 1
        while j >= 0 and not cmp(arr[j], key):
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

if __name__ == '__main__':
    # 排序顺序：基1，上2，前3，下4，再下5，元音6，后7，再后8
    word_18785_ns = import_excelTable(table)
    word_asc = word_18785_ns.copy()
    word_desc = word_18785_ns.copy()

    print("正在进行升序排序...")
    timeA = time.time()
    insertion_sort_asc(word_asc)
    timeB = time.time()

    print("正在进行降序排序...")
    timeC = time.time()
    insertion_sort_desc(word_desc)
    timeD = time.time()

    print(f'升序排序用时: {timeB-timeA:.4f}s')
    print(f'降序排序用时: {timeD-timeC:.4f}s')

    # 保存升序结果
    asc_path = 'sorted_sequence_Tibet_asc.txt'
    with open(asc_path, 'w', encoding='utf-8') as f:
        for word in tqdm(word_asc, desc="写入升序文件", unit="行"):
            f.write(word[0])
            f.write('\n')

    # 保存降序结果
    desc_path = 'sorted_sequence_Tibet_desc.txt'
    with open(desc_path, 'w', encoding='utf-8') as f:
        for word in tqdm(word_desc, desc="写入降序文件", unit="行"):
            f.write(word[0])
            f.write('\n')