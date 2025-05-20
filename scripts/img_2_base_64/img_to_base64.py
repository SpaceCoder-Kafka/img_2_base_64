#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import base64
import argparse
from pathlib import Path
from typing import Dict, Set
import sys

# 支持的图片格式
SUPPORTED_FORMATS: Set[str] = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}

def is_image_file(file_path: str) -> bool:
    """检查文件是否为支持的图片格式"""
    return Path(file_path).suffix.lower() in SUPPORTED_FORMATS

def convert_to_base64(file_path: str) -> str:
    """将图片文件转换为 Base64 编码字符串"""
    try:
        with open(file_path, 'rb') as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        print(f"错误：处理文件 {file_path} 时出错: {str(e)}")
        return ""

def scan_directory(directory: str) -> Dict[str, str]:
    """扫描目录并转换所有图片文件为 Base64"""
    base64_dict = {}
    total_files = sum(1 for root, _, files in os.walk(directory) 
                     for f in files if is_image_file(f))
    processed_files = 0

    for root, _, files in os.walk(directory):
        for file in files:
            if is_image_file(file):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, directory)
                # 统一使用正斜杠作为路径分隔符
                relative_path = relative_path.replace('\\', '/')
                
                print(f"正在处理: {relative_path} ({processed_files + 1}/{total_files})")
                base64_str = convert_to_base64(file_path)
                if base64_str:
                    base64_dict[relative_path] = base64_str
                processed_files += 1
                
                # 显示进度
                progress = (processed_files / total_files) * 100
                sys.stdout.write(f"\r进度: {progress:.1f}%")
                sys.stdout.flush()

    print("\n处理完成！")
    return base64_dict

def generate_dart_file(base64_dict: Dict[str, str], output_file: str):
    """生成 Dart 文件"""
    try:
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("// 此文件由 Python 脚本自动生成，请勿手动修改\n\n")
            f.write("const Map<String, String> base64Images = {\n")
            
            # 按字母顺序排序键，使输出更有序
            for key in sorted(base64_dict.keys()):
                # 用三引号包裹，避免转义和换行问题
                f.write(f"  '{key}': '''{base64_dict[key]}''',\n")
            
            f.write("};\n")
        print(f"成功生成 Dart 文件: {output_file}")
    except Exception as e:
        print(f"错误：生成 Dart 文件时出错: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='将图片文件转换为 Base64 编码并生成 Dart 文件')
    parser.add_argument('directory', help='要扫描的图片目录路径')
    parser.add_argument('--output', '-o', default='base64_images.dart',
                      help='输出的 Dart 文件名 (默认: base64_images.dart)')
    
    args = parser.parse_args()
    
    if not os.path.isdir(args.directory):
        print(f"错误：目录 '{args.directory}' 不存在")
        return
    
    print(f"开始扫描目录: {args.directory}")
    base64_dict = scan_directory(args.directory)
    
    if not base64_dict:
        print("警告：未找到任何图片文件")
        return
    
    # 使用绝对路径处理输出文件
    output_path = os.path.abspath(args.output)
    generate_dart_file(base64_dict, output_path)

if __name__ == '__main__':
    main() 