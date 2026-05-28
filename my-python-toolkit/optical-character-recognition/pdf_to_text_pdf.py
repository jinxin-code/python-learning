#!/usr/bin/env python3
import os
import sys
import shutil
import subprocess
import argparse
import time

# 导入PDF处理相关库
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def check_environment():
    """检查运行环境，验证所有依赖是否已安装"""
    print("=" * 50)
    print("正在检查运行环境...")
    print("=" * 50)
    
    missing_deps = []
    
    # 检查Python版本
    print(f"\n[1/4] Python版本: {sys.version.split()[0]}")
    
    # 检查Python包
    print("\n[2/4] 检查Python包...")
    python_packages = {
        'pdf2image': 'pdf2image',
        'pytesseract': 'pytesseract',
        'PIL': 'Pillow',
        'reportlab': 'reportlab'
    }
    
    for module_name, package_name in python_packages.items():
        try:
            module = __import__(module_name)
            print(f"  ✓ {package_name} (版本: {getattr(module, '__version__', '未知')})")
        except ImportError as e:
            print(f"  ✗ {package_name} (未安装) - 错误: {str(e)[:50]}")
            missing_deps.append(package_name)
    
    # 检查系统工具
    print("\n[3/4] 检查系统工具...")
    
    # 检查Poppler
    if shutil.which('pdftoppm'):
        print("  ✓ Poppler (pdftoppm)")
    else:
        print("  ✗ Poppler (未安装) - 需要通过 brew install poppler 安装")
        missing_deps.append('poppler')
    
    # 检查Tesseract
    if shutil.which('tesseract'):
        try:
            result = subprocess.run(['tesseract', '--version'], capture_output=True, text=True, timeout=5)
            version = result.stdout.split('\n')[0] if result.stdout else "未知版本"
        except:
            version = "未知版本"
        print(f"  ✓ Tesseract ({version})")
    else:
        print("  ✗ Tesseract (未安装) - 需要通过 brew install tesseract 安装")
        missing_deps.append('tesseract')
    
    # 检查Tesseract中文语言包
    print("\n[4/4] 检查Tesseract语言包...")
    try:
        result = subprocess.run(['tesseract', '--list-langs'], capture_output=True, text=True, timeout=5)
        tesseract_data = result.stdout
    except:
        tesseract_data = ""
    
    if 'chi_sim' in tesseract_data:
        print("  ✓ 简体中文语言包 (chi_sim)")
    else:
        print("  ✗ 简体中文语言包 (chi_sim) - 需要通过 brew install tesseract-lang 安装")
        missing_deps.append('tesseract-lang')
    
    print("\n" + "=" * 50)
    
    if missing_deps:
        print("缺少以下依赖:")
        for dep in missing_deps:
            print(f"  - {dep}")
        print("\n请先安装缺失的依赖后再运行程序")
        return False
    else:
        print("✓ 所有依赖已安装，可以正常运行！")
        print("=" * 50)
        return True


def pdf_to_images(pdf_path):
    """将PDF文件转换为图片列表"""
    print(f"正在将PDF转换为图片: {pdf_path}")
    images = convert_from_path(pdf_path)
    print(f"转换完成，共 {len(images)} 页")
    return images


def ocr_image(image):
    """对图片进行OCR识别，返回文字和识别数据"""
    print("正在进行OCR识别...")
    try:
        # 尝试使用Output.DICT（新版API）
        data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT, lang='chi_sim+eng')
    except AttributeError:
        # 旧版API回退
        data = pytesseract.image_to_data(image, lang='chi_sim+eng', output_type='dict')
    
    text = pytesseract.image_to_string(image, lang='chi_sim+eng')
    return text, data


def get_chinese_font():
    """获取系统中可用的中文字体"""
    font_paths = [
        '/System/Library/Fonts/PingFang.ttc',
        '/System/Library/Fonts/STHeiti Light.ttc',
        '/System/Library/Fonts/Songti.ttc',
        '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
        '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
    ]
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            font_name = os.path.splitext(os.path.basename(font_path))[0]
            try:
                pdfmetrics.registerFont(TTFont(font_name, font_path))
                return font_name
            except:
                continue
    
    return "Helvetica"

def create_text_pdf(images, output_path):
    """创建包含可搜索文字的PDF"""
    print(f"正在创建文字版PDF: {output_path}")
    
    # 获取中文字体
    chinese_font = get_chinese_font()
    print(f"  使用字体: {chinese_font}")
    
    c = canvas.Canvas(output_path, pagesize=letter)
    
    for i, image in enumerate(images):
        print(f"处理第 {i+1} 页...")
        
        try:
            img_width, img_height = image.size
            page_width, page_height = letter
            
            scale = min(page_width / img_width, page_height / img_height)
            scaled_width = img_width * scale
            scaled_height = img_height * scale
            
            x = (page_width - scaled_width) / 2
            y = (page_height - scaled_height) / 2
            
            c.drawInlineImage(image, x, y, width=scaled_width, height=scaled_height)
            
            _, data = ocr_image(image)
            
            c.saveState()
            c.setFillColorRGB(0, 0, 0, 0)
            
            n_boxes = len(data['text'])
            for j in range(n_boxes):
                conf = int(data['conf'][j]) if data['conf'][j] else 0
                text = data['text'][j] if data['text'][j] else ""
                
                if conf > 60 and text.strip() and text != "undefined":
                    left = data['left'][j] * scale + x
                    top = page_height - (data['top'][j] * scale + y) - data['height'][j] * scale
                    height = data['height'][j] * scale
                    
                    if height > 0 and left >= 0 and top >= 0:
                        c.setFont(chinese_font, height * 0.8)
                        c.drawString(left, top, text)
            
            c.restoreState()
        except Exception as e:
            print(f"  警告: 处理第 {i+1} 页时出现错误: {e}")
        
        c.showPage()
    
    c.save()
    print(f"文字版PDF已保存至: {output_path}")


def main():
    # 首先检查运行环境
    if not check_environment():
        sys.exit(1)
    
    # 获取脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    source_dir = os.path.join(script_dir, 'source_PDF')
    output_dir = os.path.join(script_dir, 'output_PDF')
    
    parser = argparse.ArgumentParser(description='将影印版PDF转换为文字版PDF')
    parser.add_argument('input_pdf', nargs='?', help='输入的影印版PDF文件路径（可选，默认从source_PDF文件夹读取）')
    parser.add_argument('-o', '--output', help='输出的文字版PDF文件路径（可选，默认保存到output_PDF文件夹）')
    parser.add_argument('-l', '--list', action='store_true', help='列出source_PDF文件夹中的所有PDF文件')
    
    args = parser.parse_args()
    
    # 列出文件模式
    if args.list:
        if not os.path.exists(source_dir):
            print(f"源文件目录不存在: {source_dir}")
            return
        
        pdf_files = [f for f in os.listdir(source_dir) if f.lower().endswith('.pdf')]
        if not pdf_files:
            print("source_PDF文件夹中没有PDF文件")
        else:
            print(f"\nsource_PDF文件夹中的PDF文件 ({len(pdf_files)}个):\n")
            for i, f in enumerate(pdf_files, 1):
                print(f"  {i}. {f}")
            print()
        return
    
    # 如果没有提供输入文件，退出
    if not args.input_pdf:
        print("错误: 请提供输入PDF文件路径")
        print("用法: python3 pdf_to_text_pdf.py input.pdf [-o output.pdf]")
        print("      python3 pdf_to_text_pdf.py -l  # 列出source_PDF中的文件")
        return
    
    # 处理输入路径
    input_pdf = args.input_pdf
    if not os.path.isabs(input_pdf):
        # 如果是相对路径，检查是否在source_PDF中
        source_file = os.path.join(source_dir, input_pdf)
        if os.path.exists(source_file):
            input_pdf = source_file
        else:
            # 尝试在当前目录查找
            if not os.path.exists(input_pdf):
                print(f"错误: 文件不存在: {input_pdf}")
                print(f"提示: 请将文件放到{source_dir}文件夹中，或使用绝对路径")
                return
    
    if not os.path.exists(input_pdf):
        print(f"错误: 文件不存在: {input_pdf}")
        return
    
    # 处理输出路径
    if args.output:
        output_pdf = args.output
        if not os.path.isabs(output_pdf):
            output_pdf = os.path.join(output_dir, output_pdf) if not os.path.dirname(output_pdf) else output_pdf
    else:
        base_name = os.path.splitext(os.path.basename(input_pdf))[0]
        output_pdf = os.path.join(output_dir, f"{base_name}_text.pdf")
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_pdf), exist_ok=True)
    
    try:
        # 记录开始时间
        start_time = time.time()
        
        print("\n" + "=" * 50)
        print(f"开始转换: {os.path.basename(input_pdf)}")
        print("=" * 50)
        
        # Step 1: PDF转图片
        images = pdf_to_images(input_pdf)
        num_pages = len(images)
        
        # 估算剩余时间（基于每页约3-5秒）
        estimated_time = num_pages * 4  # 假设每页平均4秒
        print(f"\n预计剩余时间: {estimated_time // 60}分{estimated_time % 60}秒")
        
        # Step 2: 创建文字PDF
        create_text_pdf(images, output_pdf)
        
        # 计算实际耗时
        end_time = time.time()
        elapsed_time = end_time - start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        
        print("\n" + "=" * 50)
        print(f"转换完成！")
        print(f"总页数: {num_pages}")
        print(f"耗时: {minutes}分{seconds}秒")
        print(f"输出文件: {output_pdf}")
        print("=" * 50)
    except Exception as e:
        print(f"转换过程中发生错误: {e}")


if __name__ == "__main__":
    main()
