# -*- coding: utf-8 -*-
# 创建者：Pemawangchuk
# 版本：1.0
# 日期：2025-01-09
# 功能：藏文归并排序算法实现
"""
Merge_Sort.py - 藏文归并排序实现
This script implements a merge sort algorithm for Tibetan words.
"""
import time
import os
import math
from tqdm import tqdm
import sys
import os
# 获取项目根目录路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)  # 将项目根目录添加到Python路径
# 导入common目录下的模块
from common.Cmp import cmp
from common.SplitComponent import Split_component


constant_unconverted = [0x0F90, 0x0F91, 0x0F92, 0x0F94, 0x0F95, 0x0F96, 0x0F97, 0x0F99, 0x0F9F, 0x0FA0,
                    0x0FA1, 0x0FA3, 0x0FA4, 0x0FA5,0x0FA6, 0x0FA8, 0x0FA9, 0x0FAA, 0x0FAB, 0x0FAE,
                    0x0FAF, 0x0FB0, 0x0FB3, 0x0FB4, 0x0FB6, 0x0FB7, 0x0FB8, 0x0FBA, 0x0FBB, 0x0FBC]

class Merge():
    def Merge_sort(self, unsorted, l, mid, r, reverse=False, progress_bar=None):
        """归并排序的合并操作"""
        n1 = mid - l + 1
        n2 = r - mid
        L_list = [[] for i in range(n1)]
        R_list = [[] for i in range(n2)]
        for i in range(n1):
            L_list[i] = unsorted[l + i]
        for j in range(n2):
            R_list[j] = unsorted[mid + 1 + j]
        i, j = 0, 0
        k = l
        while i < n1 and j < n2:
            if cmp(R_list[j], L_list[i]) == reverse:
                unsorted[k] = L_list[i]
                i += 1
            else:
                unsorted[k] = R_list[j]
                j += 1
            k += 1
        while i < n1:
            unsorted[k] = L_list[i]
            i += 1
            k += 1
        while j < n2:
            unsorted[k] = R_list[j]
            j += 1
            k += 1

    def MergeTraverse(self, unsorted, l, r, reverse=False, progress_bar=None):
        """归并排序的递归遍历"""
        timA = time.time()
        
        # 只在第一次调用时初始化进度条相关变量
        if progress_bar is not None and not hasattr(self, 'initialized_progress'):
            self.initialized_progress = True
            self.total_operations = 0
            self.completed_operations = 0
            
            # 计算总的归并操作次数
            n = len(unsorted)
            # 归并排序的比较次数约为 n*log(n)
            self.total_operations = int(n * math.log2(n)) if n > 1 else 1
            
            # 设置进度条为百分比显示
            progress_bar.total = 100
            progress_bar.n = 0
            progress_bar.refresh()
        
        if (l < r):
            mid = int((l + (r - 1)) // 2)
            self.MergeTraverse(unsorted, l, mid, reverse, progress_bar)
            self.MergeTraverse(unsorted, mid + 1, r, reverse, progress_bar)
            self.Merge_sort(unsorted, l, mid, r, reverse)
            
            # 更新已完成操作数和进度条
            if progress_bar is not None and hasattr(self, 'total_operations'):
                # 每次归并操作增加的操作数与归并的元素数量相关
                self.completed_operations += (r - l + 1)
                
                # 计算百分比进度，确保不超过100%
                progress_percent = min(int(self.completed_operations * 100 / self.total_operations), 100)
                
                # 只有百分比变化时才更新进度条
                if progress_percent > progress_bar.n:
                    progress_bar.update(progress_percent - progress_bar.n)
                    
        timB = time.time()
        return timB - timA

def load_file(file_path):
    """加载文件并处理藏文数据"""
    split_com = Split_component()
    word_18785_ns = []
    
    # 尝试不同的编码方式
    encodings = ['utf-8', 'utf-16', 'utf-16-le', 'utf-16-be', 'gb18030']
    
    for encoding in encodings:
        try:
            with open(file=file_path, mode='r', encoding=encoding) as f:
                # 读取文件的前几行来确认编码是否正确
                try:
                    lines = []
                    for _ in range(5):
                        line = f.readline().strip('\n')
                        if line:
                            lines.append(line)
                    if not lines:
                        continue  # 如果没有读到内容，尝试下一种编码
                    
                    # 如果能够成功读取，则使用此编码
                    print(f"使用 {encoding} 编码读取文件")
                    break
                except:
                    continue
        except:
            continue
    else:
        # 如果所有编码都失败
        print("无法确定文件编码，请检查文件格式")
        return None
    
    try:
        # 重新打开文件并读取全部内容
        with open(file=file_path, mode='r', encoding=encoding) as f:
            # 获取文件总行数
            all_lines = f.readlines()
            total_lines = len(all_lines)
            
            # 创建进度条显示文件读取进度
            print(f"正在读取文件，共 {total_lines} 行...")
            with tqdm(total=total_lines, desc="读取文件", unit="行") as pbar:
                for i, line in enumerate(all_lines):
                    Tibetan = line.strip('\n')
                    if not Tibetan:
                        print(f"警告：第{i+1}行为空")
                        pbar.update(1)
                        continue
                        
                    try:
                        word = split_com.Split(Tibetan)[:-1]
                        for j in range(1, 9):
                            if (word[j] != ''):
                                word[j] = ord(word[j])
                            else:
                                word[j] = 0
                        word[1], word[3] = word[3], word[1]
                        for j in range(1, 9):
                            if (0x0F90 <= word[j] <= 0x0FB8):
                                word[j] = word[j] - 80
                        word_18785_ns.append(word)
                    except Exception as e:
                        print(f"处理第{i+1}行时出错: {str(e)}")
                    
                    pbar.update(1)
                    
        print(f"文件加载完成，共读取{len(word_18785_ns)}个藏文词条")
        return word_18785_ns
    except Exception as e:
        print(f"文件加载异常：{str(e)}，请检查文件路径和格式")
        return None

def save_file(file_path, words):
    """保存排序后的结果到文件"""
    try:
        with open(file=file_path, mode='w', encoding='utf-8') as f:
            for word in words:
                f.write(f"{word[0]}\n")
        print(f"文件已保存至：{file_path}")
        return True
    except Exception as e:
        print(f"保存文件异常：{str(e)}")
        return False

def main():
    import argparse
    parser = argparse.ArgumentParser(description="藏文归并排序命令行工具")
    parser.add_argument('input', help='输入文件路径')
    parser.add_argument('output', help='输出文件路径')
    parser.add_argument('--reverse', choices=['true', 'false'], default='false', help='是否逆序排序 (true/false)')
    parser.add_argument('--preview', action='store_true', help='显示排序结果前10个词条')
    args = parser.parse_args()

    # 检查输入文件是否存在
    if not os.path.exists(args.input):
        print(f"错误：输入文件 '{args.input}' 不存在")
        return
    
    # 加载文件
    words = load_file(args.input)
    if words is None or len(words) == 0:
        print("文件加载失败或没有有效数据")
        return
    
    # 将字符串参数转换为布尔值
    reverse_flag = args.reverse.lower() == 'true'
    
    # 创建排序进度条
    print(f"开始排序，共 {len(words)} 个词条...")
    with tqdm(total=100, desc="排序进度", unit="%") as pbar:
        merge = Merge()
        sort_time = merge.MergeTraverse(words, 0, len(words)-1, reverse=reverse_flag, progress_bar=pbar)
    
    print(f"归并排序完成，用时{sort_time:.2f}秒")
    
    # 如果指定了预览参数，显示排序结果的前10个
    if args.preview:
        print("\n排序结果前10个词条:")
        for i in range(min(10, len(words))):
            print(words[i][0])
    
    # 保存结果
    save_file(args.output, words)
    print(f"排序结果已保存至: {args.output}")

if __name__ == '__main__':
    main()


# 执行命令
# python T4_demo/Merge_Sort.py input.txt output.txt --reverse true --preview
# 必选参数：input（输入文件路径）和 output（输出文件路径）
# 可选参数：--reverse（是否逆序排序）和 --preview（是否显示排序结果前10个词条）