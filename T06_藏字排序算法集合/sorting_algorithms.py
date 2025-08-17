# -*- coding: utf-8 -*-
import time
import sys
import os

# 获取项目根目录路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

try:
    from common.Comparator import cmp
except ImportError:
    print("警告：未找到Comparator模块，使用模拟函数")
    def cmp(a, b): return a < b

class Insertion:
    """插入排序实现"""
    def sort(self, arr, reverse=False, progress_callback=None):
        start_time = time.time()
        n = len(arr)
        if n <= 1:
            if progress_callback:
                progress_callback(100)
            return time.time() - start_time

        for i in range(1, n):
            key = arr[i]
            j = i - 1
            # 根据升序/降序选择比较方式
            while j >= 0 and (cmp(key, arr[j]) if not reverse else cmp(arr[j], key)):
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
            
            if progress_callback:
                progress = int((i + 1) / n * 100)
                progress_callback(progress)
        
        if progress_callback:
            progress_callback(100)
            
        return time.time() - start_time

import math

class Heap_sort:
    """堆排序实现"""
    def sort(self, arr, reverse=False, progress_callback=None):
        start_time = time.time()
        n = len(arr)
        if n <= 1:
            if progress_callback: progress_callback(100)
            return time.time() - start_time

        # 1. 构建堆
        for i in range(n // 2 - 1, -1, -1):
            self._heapify(arr, n, i, reverse)

        # 2. 逐个提取元素
        for i in range(n - 1, 0, -1):
            arr[0], arr[i] = arr[i], arr[0]
            self._heapify(arr, i, 0, reverse)
            if progress_callback:
                progress = int((n - i) / n * 100)
                progress_callback(progress)
        
        if progress_callback: progress_callback(100)
        return time.time() - start_time

    def _heapify(self, arr, n, i, reverse):
        extreme = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and (cmp(arr[extreme], arr[left]) if not reverse else cmp(arr[left], arr[extreme])):
            extreme = left

        if right < n and (cmp(arr[extreme], arr[right]) if not reverse else cmp(arr[right], arr[extreme])):
            extreme = right

        if extreme != i:
            arr[i], arr[extreme] = arr[extreme], arr[i]
            self._heapify(arr, n, extreme, reverse)

class Merge_sort:
    """归并排序实现"""
    def sort(self, arr, reverse=False, progress_callback=None):
        start_time = time.time()
        n = len(arr)
        if n <= 1:
            if progress_callback: progress_callback(100)
            return time.time() - start_time
        
        self._merge_sort_recursive(arr, 0, n - 1, reverse)
        
        # 归并排序的递归特性使得精确的线性进度更新变得复杂，此处模拟进度。
        if progress_callback:
            for i in range(0, 101, 10):
                progress_callback(i)
                time.sleep(0.02)
        
        return time.time() - start_time

    def _merge_sort_recursive(self, arr, left, right, reverse):
        if left < right:
            mid = (left + right) // 2
            self._merge_sort_recursive(arr, left, mid, reverse)
            self._merge_sort_recursive(arr, mid + 1, right, reverse)
            self._merge(arr, left, mid, right, reverse)

    def _merge(self, arr, left, mid, right, reverse):
        L = arr[left : mid + 1]
        R = arr[mid + 1 : right + 1]
        i = j = 0
        k = left
        while i < len(L) and j < len(R):
            if cmp(L[i], R[j]) if not reverse else cmp(R[j], L[i]):
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

class Quick_sort:
    """快速排序实现 (迭代版本)"""
    def sort(self, arr, reverse=False, progress_callback=None):
        start_time = time.time()
        n = len(arr)
        if n <= 1:
            if progress_callback: progress_callback(100)
            return time.time() - start_time

        stack = [(0, n - 1)]
        # 快速排序的平均复杂度为 O(n log n)，以此为基准估算进度
        total_size_for_progress = n * math.log2(n) if n > 1 else 1
        completed_operations = 0

        while stack:
            low, high = stack.pop()
            if low < high:
                pi = self._partition(arr, low, high, reverse)
                
                if progress_callback:
                    completed_operations += (high - low)
                    if total_size_for_progress > 0:
                        progress = int(completed_operations / total_size_for_progress * 100)
                        progress_callback(min(progress, 99)) # 避免过早达到100%

                if pi - 1 > low:
                    stack.append((low, pi - 1))
                if pi + 1 < high:
                    stack.append((pi + 1, high))
        
        if progress_callback: progress_callback(100)
        return time.time() - start_time

    def _partition(self, arr, low, high, reverse):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if cmp(arr[j], pivot) if not reverse else cmp(pivot, arr[j]):
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1
