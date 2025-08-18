#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
藏文构件识别与分析工具 - 核心功能模块
提供藏文字符分析的核心功能
"""
import os
import csv
import logging
from typing import Dict, List, Optional, Tuple, Any

# 藏文Unicode范围常量
TIBETAN_NORMAL_RANGE = (0x0F40, 0x0F6D)  # 除叠字、元音外的普通字
TIBETAN_STACK_RANGE = (0x0F8D, 0x0FBD)   # 叠字范围

# 藏文分隔符
TIBETAN_DELIMITERS = ['་', '།', '།།']  # 藏文分隔符：音节点、句号、双句号

def cut(tibetan: str) -> Dict[str, Optional[str]]:
    """
    分析藏文字符的构件组成
    
    参数:
    tibetan -- 要分析的藏文字符
    
    返回:
    包含藏文构件分析结果的字典
    """
    # 初始化结果字典
    tibetan_att = {
        '原字': tibetan, 
        '类型': '藏文字符',
        '前加字': None, 
        '上加字': None, 
        '基字': None, 
        '下加字': None,
        '再下加字': None, 
        '元音': None, 
        '后加字': None, 
        '再后加字': None
    }
    
    # 检查是否为分隔符
    if tibetan in TIBETAN_DELIMITERS:
        tibetan_att['类型'] = '分隔符'
        return tibetan_att
    
    # 检查是否包含分隔符
    for delimiter in TIBETAN_DELIMITERS:
        if delimiter in tibetan:
            tibetan_att['类型'] = '包含分隔符'
            return tibetan_att
    
    # 正常藏文字符分析
    tibetan_len = len(tibetan)
    
    # 判断叠字，元音
    tibetan_pile = []
    first = True
    i = 0
    
    while i < tibetan_len:
        char_code = ord(tibetan[i])
        
        # 除叠字、元音外的普通字
        if TIBETAN_NORMAL_RANGE[0] <= char_code < TIBETAN_NORMAL_RANGE[1]:
            if not first:
                tibetan_att['后加字'] = tibetan[i]
                i += 1
                if i < tibetan_len:
                    tibetan_att['再后加字'] = tibetan[i]
                break
        
        # 叠字
        elif TIBETAN_STACK_RANGE[0] <= char_code < TIBETAN_STACK_RANGE[1]:
            if first:  # 遇到第一个叠字
                if i == 2:
                    tibetan_att['前加字'] = tibetan[0]
                tibetan_pile.append(tibetan[i - 1])
                first = False
                tibetan_pile.append(tibetan[i])
            else:  # 除第一个叠字之外其他叠字
                tibetan_pile.append(tibetan[i])
        
        # 元音
        else:
            tibetan_att['元音'] = tibetan[i]
            if first:  # 元音无叠字
                tibetan_att['基字'] = tibetan[i - 1]
                if i == 2:
                    tibetan_att['前加字'] = tibetan[0]
            first = False
            
            # 元音有无叠字都要处理
            i += 1
            if i < tibetan_len:
                tibetan_att['后加字'] = tibetan[i]
            else:
                break
            
            i += 1
            if i < tibetan_len:
                tibetan_att['再后加字'] = tibetan[i]
            else:
                break
        
        i += 1
    
    # 判断叠字
    if tibetan_pile:
        _process_tibetan_pile(tibetan_pile, tibetan_att)
    
    # 判断无叠字无元音(长度5，6，7一定有元音，叠字)
    elif first:
        _process_no_stack_no_vowel(tibetan, tibetan_len, tibetan_att)
    
    return tibetan_att


def _process_tibetan_pile(tibetan_pile: List[str], tibetan_att: Dict[str, Optional[str]]) -> None:
    """
    处理藏文叠字
    
    参数:
    tibetan_pile -- 叠字列表
    tibetan_att -- 藏文属性字典，将被修改
    """
    if len(tibetan_pile) == 2:
        if tibetan_pile[1] in ['ྱ', 'ྲ', 'ྭ', 'ླ']:
            tibetan_att['基字'], tibetan_att['下加字'] = tibetan_pile[0], tibetan_pile[1]
        else:
            tibetan_att['上加字'], tibetan_att['基字'] = tibetan_pile[0], tibetan_pile[1]
    else:
        if ''.join(tibetan_pile) in ['ཕྱྭ', 'གྲྭ']:
            tibetan_att['基字'], tibetan_att['下加字'], tibetan_att['再下加字'] = \
                tibetan_pile[0], tibetan_pile[1], tibetan_pile[2]
        else:
            tibetan_att['上加字'], tibetan_att['基字'], tibetan_att['下加字'] = \
                tibetan_pile[0], tibetan_pile[1], tibetan_pile[2]


def _process_no_stack_no_vowel(tibetan: str, tibetan_len: int, tibetan_att: Dict[str, Optional[str]]) -> None:
    """
    处理无叠字无元音的情况
    
    参数:
    tibetan -- 藏文字符串
    tibetan_len -- 藏文字符串长度
    tibetan_att -- 藏文属性字典，将被修改
    """
    if tibetan_len == 4:
        tibetan_att['前加字'], tibetan_att['基字'], tibetan_att['后加字'], tibetan_att['再后加字'] = \
            tibetan[0], tibetan[1], tibetan[2], tibetan[3]
    elif tibetan_len == 3:
        if ord(tibetan[0]) < 0x0F40:  # 前加字
            tibetan_att['前加字'], tibetan_att['基字'], tibetan_att['后加字'] = \
                tibetan[0], tibetan[1], tibetan[2]
        else:
            tibetan_att['基字'], tibetan_att['后加字'], tibetan_att['再后加字'] = \
                tibetan[0], tibetan[1], tibetan[2]
    elif tibetan_len == 2:
        tibetan_att['基字'], tibetan_att['后加字'] = tibetan[0], tibetan[1]
    elif tibetan_len == 1:
        tibetan_att['基字'] = tibetan[0]


def save_to_csv(results: List[Dict[str, Optional[str]]], output_path: str, encoding: str = 'utf-8') -> None:
    """
    将分析结果保存到CSV文件
    
    参数:
    results -- 分析结果列表
    output_path -- 输出文件路径
    encoding -- 文件编码，默认为utf-8
    """
    # 确保输出目录存在
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # 写入CSV文件
    header = ['原字', '类型', '前加字', '上加字', '基字', '下加字', '再下加字', '元音', '后加字', '再后加字']
    
    with open(output_path, 'w', newline='', encoding=encoding) as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(results)


def analyze_file(file_path: str, encoding: str = 'utf-8') -> List[Dict[str, Optional[str]]]:
    """
    分析藏文文件
    
    参数:
    file_path -- 文件路径
    encoding -- 文件编码，默认为utf-8
    
    返回:
    分析结果列表
    """
    results = []
    
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                    
                result = cut(line)
                results.append(result)
                
    except UnicodeError:
        # 如果指定编码失败，尝试其他编码
        logging.warning(f"使用 {encoding} 编码读取失败，尝试其他编码")
        for enc in ['utf-8', 'utf-16', 'utf-16-le', 'utf-16-be', 'gb18030']:
            if enc == encoding:
                continue
                
            try:
                results = []
                with open(file_path, 'r', encoding=enc) as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                            
                        result = cut(line)
                        results.append(result)
                        
                logging.info(f"成功使用 {enc} 编码读取文件")
                break
            except UnicodeError:
                continue
                
    return results


if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # 示例用法
    test_str = "བཀྲ་ཤིས་བདེ་ལེགས།"
    result = cut(test_str)
    print(f"分析结果: {result}")