#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
图片转 Base64 转换工具

此脚本用于将指定目录中的图片文件转换为 Base64 编码，并保存为文本文件。
支持的图片格式：JPG、JPEG、PNG、GIF、BMP、WEBP、TIFF、ICO

作者：SpaceCoder
日期：2023
"""

import os
import sys
import base64
import argparse
import time
import shutil
from pathlib import Path
from typing import List, Tuple, Optional
import imghdr  # 用于验证图片文件


# 支持的图片格式
SUPPORTED_FORMATS = {
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', 
    '.webp', '.tiff', '.tif', '.ico'
}


def is_valid_image(file_path: str) -> bool:
    """
    检查文件是否为有效的图片文件
    
    Args:
        file_path: 文件路径
        
    Returns:
        bool: 如果是有效的图片文件则返回 True，否则返回 False
    """
    # 首先检查扩展名
    suffix = Path(file_path).suffix.lower()
    if suffix not in SUPPORTED_FORMATS:
        return False
    
    # 然后使用 imghdr 验证文件内容
    try:
        img_type = imghdr.what(file_path)
        return img_type is not None
    except Exception:
        return False


def get_free_space(directory: str) -> int:
    """
    获取指定目录所在磁盘的可用空间（字节）
    
    Args:
        directory: 目录路径
        
    Returns:
        int: 可用空间（字节）
    """
    try:
        total, used, free = shutil.disk_usage(directory)
        return free
    except Exception as e:
        print(f"警告：无法获取磁盘空间信息: {str(e)}")
        return 0


def convert_to_base64(file_path: str) -> Optional[str]:
    """
    将图片文件转换为 Base64 编码字符串
    
    Args:
        file_path: 图片文件路径
        
    Returns:
        Optional[str]: Base64 编码字符串，如果转换失败则返回 None
    """
    try:
        with open(file_path, 'rb') as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except PermissionError:
        print(f"错误：没有权限读取文件 {file_path}")
        return None
    except Exception as e:
        print(f"错误：处理文件 {file_path} 时出错: {str(e)}")
        return None


def save_base64_to_file(base64_str: str, output_path: str) -> bool:
    """
    将 Base64 编码字符串保存到文件
    
    Args:
        base64_str: Base64 编码字符串
        output_path: 输出文件路径
        
    Returns:
        bool: 如果保存成功则返回 True，否则返回 False
    """
    try:
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(base64_str)
        return True
    except PermissionError:
        print(f"错误：没有权限写入文件 {output_path}")
        return False
    except OSError as e:
        if e.errno == 28:  # 磁盘空间不足
            print(f"错误：磁盘空间不足，无法保存文件 {output_path}")
        else:
            print(f"错误：保存文件 {output_path} 时出错: {str(e)}")
        return False
    except Exception as e:
        print(f"错误：保存文件 {output_path} 时出错: {str(e)}")
        return False


def remove_file(file_path: str) -> bool:
    """
    删除文件
    
    Args:
        file_path: 文件路径
        
    Returns:
        bool: 如果删除成功则返回 True，否则返回 False
    """
    try:
        os.remove(file_path)
        return True
    except PermissionError:
        print(f"错误：没有权限删除文件 {file_path}")
        return False
    except Exception as e:
        print(f"错误：删除文件 {file_path} 时出错: {str(e)}")
        return False


def find_image_files(directory: str, recursive: bool = True) -> List[str]:
    """
    查找指定目录中的所有图片文件
    
    Args:
        directory: 目录路径
        recursive: 是否递归处理子目录
        
    Returns:
        List[str]: 图片文件路径列表
    """
    image_files = []
    
    if recursive:
        # 递归处理
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                if Path(file_path).suffix.lower() in SUPPORTED_FORMATS:
                    image_files.append(file_path)
    else:
        # 只处理当前目录
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            if os.path.isfile(file_path) and Path(file_path).suffix.lower() in SUPPORTED_FORMATS:
                image_files.append(file_path)
    
    return image_files


def format_time(seconds: float) -> str:
    """
    将秒数格式化为时分秒
    
    Args:
        seconds: 秒数
        
    Returns:
        str: 格式化后的时间字符串
    """
    if seconds < 60:
        return f"{seconds:.1f}秒"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        seconds = seconds % 60
        return f"{minutes}分{seconds:.1f}秒"
    else:
        hours = int(seconds / 3600)
        minutes = int((seconds % 3600) / 60)
        seconds = seconds % 60
        return f"{hours}小时{minutes}分{seconds:.1f}秒"


def draw_progress_bar(progress: float, width: int = 50) -> str:
    """
    绘制进度条
    
    Args:
        progress: 进度（0.0 到 1.0）
        width: 进度条宽度
        
    Returns:
        str: 进度条字符串
    """
    filled_width = int(width * progress)
    bar = '█' * filled_width + '░' * (width - filled_width)
    return f"[{bar}] {progress * 100:.1f}%"


def process_images(image_files: List[str], output_dir: Optional[str] = None) -> Tuple[int, int]:
    """
    处理图片文件列表
    
    Args:
        image_files: 图片文件路径列表
        output_dir: 输出目录，如果为 None 则与原图片位于同一目录
        
    Returns:
        Tuple[int, int]: 成功处理的文件数量和失败的文件数量
    """
    total_files = len(image_files)
    processed_files = 0
    failed_files = 0
    start_time = time.time()
    
    for file_path in image_files:
        processed_files += 1
        
        # 显示当前处理的文件
        file_name = os.path.basename(file_path)
        print(f"\n正在处理: {file_path} ({processed_files}/{total_files})")
        
        # 验证图片文件
        if not is_valid_image(file_path):
            print(f"跳过：{file_path} 不是有效的图片文件")
            failed_files += 1
            continue
        
        # 检查磁盘空间
        if get_free_space(os.path.dirname(file_path)) < os.path.getsize(file_path) * 2:
            print(f"错误：磁盘空间不足，无法处理文件 {file_path}")
            failed_files += 1
            continue
        
        # 转换为 Base64
        base64_str = convert_to_base64(file_path)
        if base64_str is None:
            failed_files += 1
            continue
        
        # 确定输出路径
        if output_dir:
            # 使用指定的输出目录
            rel_path = os.path.relpath(file_path, os.path.dirname(file_path))
            output_path = os.path.join(output_dir, os.path.splitext(rel_path)[0] + '.txt')
        else:
            # 与原图片位于同一目录
            output_path = os.path.splitext(file_path)[0] + '.txt'
        
        # 保存 Base64 字符串
        if save_base64_to_file(base64_str, output_path):
            # 删除原始图片文件
            if remove_file(file_path):
                print(f"成功：{file_path} -> {output_path}")
            else:
                print(f"部分成功：已保存 {output_path}，但无法删除原始文件")
                failed_files += 1
        else:
            failed_files += 1
        
        # 计算进度和估计剩余时间
        elapsed_time = time.time() - start_time
        progress = processed_files / total_files
        
        if processed_files > 1:  # 至少处理一个文件后才能估计时间
            avg_time_per_file = elapsed_time / processed_files
            remaining_files = total_files - processed_files
            estimated_time = avg_time_per_file * remaining_files
            
            # 显示进度条和估计时间
            progress_bar = draw_progress_bar(progress)
            print(f"{progress_bar} 已用时: {format_time(elapsed_time)} 预计剩余: {format_time(estimated_time)}")
    
    return processed_files - failed_files, failed_files


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='将图片文件转换为 Base64 编码并保存为文本文件')
    parser.add_argument('directory', help='要扫描的目录路径')
    parser.add_argument('--no-recursive', action='store_true', help='不递归处理子目录')
    parser.add_argument('--output-dir', '-o', help='输出目录路径（默认与原图片位于同一目录）')
    
    args = parser.parse_args()
    
    # 检查目录是否存在
    if not os.path.isdir(args.directory):
        print(f"错误：目录 '{args.directory}' 不存在")
        return 1
    
    # 检查输出目录
    if args.output_dir and not os.path.exists(args.output_dir):
        try:
            os.makedirs(args.output_dir, exist_ok=True)
            print(f"已创建输出目录: {args.output_dir}")
        except Exception as e:
            print(f"错误：无法创建输出目录 '{args.output_dir}': {str(e)}")
            return 1
    
    print(f"开始扫描目录: {args.directory}" + (" (不包含子目录)" if args.no_recursive else ""))
    
    # 查找图片文件
    image_files = find_image_files(args.directory, not args.no_recursive)
    
    if not image_files:
        print("未找到任何图片文件")
        return 0
    
    print(f"找到 {len(image_files)} 个图片文件")
    
    # 处理图片文件
    success_count, failed_count = process_images(image_files, args.output_dir)
    
    # 显示处理结果
    print("\n处理完成！")
    print(f"成功处理: {success_count} 个文件")
    if failed_count > 0:
        print(f"处理失败: {failed_count} 个文件")
    
    return 0 if failed_count == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
