#!/usr/bin/env python3
"""
纯文字版PDF生成器
将影印版PDF转换为只有文字的PDF文件（无图片背景）
"""
import os
import sys
import shutil
import subprocess
import argparse
import time

from pdf2image import convert_from_path
import pytesseract
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch


def check_environment():
    """检查运行环境"""
    print("=" * 50)
    print("正在检查运行环境...")
    print("=" * 50)
    
    missing_deps = []
    
    print(f"\n[1/2] Python版本: {sys.version.split()[0]}")
    
    print("\n[2/2] 检查系统工具...")
    if shutil.which('pdftoppm'):
        print("  ✓ Poppler")
    else:
        print("  ✗ Poppler - 需要 brew install poppler")
        missing_deps.append('poppler')
    
    if shutil.which('tesseract'):
        print("  ✓ Tesseract")
    else:
        print("  ✗ Tesseract - 需要 brew install tesseract")
        missing_deps.append('tesseract')
    
    try:
        from pdf2image import convert_from_path
        print("  ✓ pdf2image")
    except ImportError:
        print("  ✗ pdf2image")
        missing_deps.append('pdf2image')
    
    try:
        import pytesseract
        print("  ✓ pytesseract")
    except ImportError:
        print("  ✗ pytesseract")
        missing_deps.append('pytesseract')
    
    try:
        from reportlab.pdfgen import canvas
        print("  ✓ reportlab")
    except ImportError:
        print("  ✗ reportlab")
        missing_deps.append('reportlab')
    
    print("\n" + "=" * 50)
    if missing_deps:
        print("缺少以下依赖:")
        for dep in missing_deps:
            print(f"  - {dep}")
        return False
    else:
        print("✓ 所有依赖已安装")
        print("=" * 50)
        return True


def extract_text_from_pdf(pdf_path):
    """从PDF提取文字"""
    print(f"\n正在提取文字: {os.path.basename(pdf_path)}")
    images = convert_from_path(pdf_path)
    print(f"共 {len(images)} 页")
    
    all_text = []
    for i, image in enumerate(images):
        print(f"  提取第 {i+1} 页...")
        try:
            text = pytesseract.image_to_string(image, lang='chi_sim+eng')
            all_text.append(text)
        except Exception as e:
            print(f"    警告: 提取失败 - {e}")
            all_text.append("")
    
    return all_text


def create_text_only_pdf(text_pages, output_path):
    """创建纯文字PDF"""
    print(f"\n正在生成纯文字PDF...")
    
    c = canvas.Canvas(output_path, pagesize=letter)
    page_width, page_height = letter
    
    # 设置字体和大小
    margin = 0.75 * inch
    font_size = 10
    line_height = font_size * 1.5
    
    for page_num, text in enumerate(text_pages):
        print(f"  处理第 {page_num+1} 页...")
        
        # 分割文字为行
        lines = text.split('\n')
        
        # 计算每页能容纳的行数
        max_lines_per_page = int((page_height - 2 * margin) / line_height)
        
        current_line = 0
        while current_line < len(lines):
            # 设置起始位置
            y = page_height - margin
            c.setFont("Helvetica", font_size)
            
            # 逐行写入
            for i in range(min(max_lines_per_page, len(lines) - current_line)):
                line = lines[current_line + i].strip()
                if line:  # 跳过空行
                    c.drawString(margin, y, line[:120])  # 限制每行字符数
                y -= line_height
            
            current_line += max_lines_per_page
            c.showPage()
    
    c.save()
    print(f"纯文字PDF已保存: {output_path}")


def main():
    if not check_environment():
        sys.exit(1)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    source_dir = os.path.join(script_dir, 'source_PDF')
    output_dir = os.path.join(script_dir, 'output_PDF')
    
    parser = argparse.ArgumentParser(description='将影印版PDF转换为纯文字版PDF')
    parser.add_argument('input_pdf', help='输入的影印版PDF文件')
    parser.add_argument('-o', '--output', help='输出的纯文字PDF文件')
    
    args = parser.parse_args()
    
    # 处理输入路径
    input_pdf = args.input_pdf
    if not os.path.isabs(input_pdf):
        source_file = os.path.join(source_dir, input_pdf)
        if os.path.exists(source_file):
            input_pdf = source_file
        elif not os.path.exists(input_pdf):
            print(f"错误: 文件不存在: {input_pdf}")
            return
    
    # 处理输出路径
    if args.output:
        output_pdf = args.output
        if not os.path.isabs(output_pdf):
            output_pdf = os.path.join(output_dir, output_pdf)
    else:
        base_name = os.path.splitext(os.path.basename(input_pdf))[0]
        output_pdf = os.path.join(output_dir, f"{base_name}_纯文字版.pdf")
    
    os.makedirs(os.path.dirname(output_pdf), exist_ok=True)
    
    start_time = time.time()
    
    try:
        text_pages = extract_text_from_pdf(input_pdf)
        create_text_only_pdf(text_pages, output_pdf)
        
        elapsed = time.time() - start_time
        print(f"\n转换完成！耗时: {int(elapsed//60)}分{int(elapsed%60)}秒")
        
    except Exception as e:
        print(f"转换失败: {e}")


if __name__ == "__main__":
    main()
