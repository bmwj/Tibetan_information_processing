# -*- coding: UTF-8 -*-
# 工具函数模块 - 包含辅助函数和工具方法

def format_results(results, process_time, total_chars, tib_count):
    """格式化统计结果
    
    Args:
        results: 统计结果字典
        process_time: 处理时间
        total_chars: 总字符数
        tib_count: 藏文音节数
        
    Returns:
        str: 格式化后的结果文本
    """
    output = f"{'='*60}\n"
    output += f"藏字构件动态统计分析结果\n"
    output += f"{'='*60}\n\n"
    output += f"处理时间: {process_time:.3f} 秒\n"
    output += f"总字符数: {total_chars:,}\n"
    output += f"藏文音节: {tib_count:,}\n\n"
    
    # 显示各类构件统计
    for type_name, sorted_items in results.items():
        output += f"【{type_name}】统计结果:\n"
        output += f"{'-'*50}\n"
        
        for char, count in sorted_items:
            if count > 0:  # 只显示有统计的字符
                percentage = (count / tib_count * 100) if tib_count > 0 else 0
                output += f"{char:<10} {count:>8} ({percentage:.2f}%)\n"
        
        output += '\n'
    
    return output

def create_icon():
    """创建应用程序图标
    
    如果需要创建图标文件，可以使用此函数
    """
    try:
        import base64
        from PIL import Image, ImageDraw
        import io
        
        # 创建一个200x200的图像
        img = Image.new('RGBA', (200, 200), color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # 绘制一个简单的图标
        draw.rectangle([(40, 40), (160, 160)], fill=(45, 55, 72))
        draw.ellipse([(60, 60), (140, 140)], fill=(52, 152, 219))
        draw.rectangle([(85, 40), (115, 160)], fill=(230, 126, 34))
        
        # 保存图标
        img.save('T11_藏字构件动态统计/icon.png')
        return True
    except:
        return False