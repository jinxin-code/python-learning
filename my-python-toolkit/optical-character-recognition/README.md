# 影印版PDF转文字版PDF

这是一个使用OCR技术将影印版PDF转换为可搜索文字版PDF的Python工具。

## 功能特点

- 将扫描版PDF转换为可搜索文字版PDF
- 支持中英文混合识别
- **两种输出模式**：
  - `pdf_to_text_pdf.py`：保留原图背景，添加透明文字层（可搜索）
  - `pdf_to_text_only.py`：纯文字输出，无图片背景
- **自动环境检查**：运行前自动检测所有依赖是否已安装，提示缺失项及安装命令

## 系统要求

- Python 3.7+
- Poppler（PDF渲染引擎）
- Tesseract OCR引擎
- Tesseract中文语言包

## 依赖说明

本程序依赖分为两类：**Python包**和**系统工具**。

### 系统工具（必须通过系统包管理器安装）

| 依赖 | 说明 | 安装方式 |
|------|------|----------|
| **Poppler** | PDF渲染引擎，用于将PDF页面转换为图片。<br>这是C/C++编写的系统库，不是Python包。 | macOS: `brew install poppler`<br>Ubuntu: `apt-get install poppler-utils` |
| **Tesseract** | OCR识别引擎，负责从图片中提取文字。<br>这是C/C++编写的系统程序，不是Python包。 | macOS: `brew install tesseract`<br>Ubuntu: `apt-get install tesseract-ocr` |
| **Tesseract中文语言包** | 中文OCR识别支持。如果PDF仅包含英文，可不安装。 | macOS: `brew install tesseract-lang`<br>Ubuntu: `apt-get install tesseract-ocr-chi-sim` |

> **为什么系统工具必须通过brew/apt安装？**
>
> Poppler和Tesseract都是C/C++编写的系统级程序，而`pdf2image`和`pytesseract`只是它们的Python封装。系统级工具无法通过pip安装，必须使用系统包管理器（brew/apt）全局安装。

### Python包（通过pip3安装）

| 包名 | 说明 | 用途 |
|------|------|------|
| **pdf2image** | 将PDF转换为PIL图片对象 | 调用Poppler进行PDF渲染 |
| **pytesseract** | Tesseract OCR的Python封装 | 调用Tesseract进行文字识别 |
| **Pillow** | Python图像处理库 | 处理和管理图片数据 |
| **reportlab** | PDF生成库 | 创建包含透明文字层的PDF |

## 安装依赖

### 步骤1：安装系统工具（必须）

#### macOS

```bash
brew install poppler
brew install tesseract
brew install tesseract-lang  # 如果PDF包含中文，需要此语言包
```

#### Ubuntu/Debian

```bash
sudo apt-get install poppler-utils tesseract-ocr tesseract-ocr-chi-sim
```

### 步骤2：创建Python虚拟环境（推荐）

由于Python 3.11+使用了PEP 668限制，不允许直接pip安装到系统Python。需要创建虚拟环境：

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装Python依赖
pip install -r requirements.txt
```

> **提示**：激活虚拟环境后，终端前面会显示`(venv)`标识。以后每次使用程序前，需要先运行`source venv/bin/activate`。

### Ubuntu/Debian

```bash
# 安装系统依赖
sudo apt-get install poppler-utils tesseract-ocr tesseract-ocr-chi-sim

# 创建虚拟环境并安装
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 使用方法

### 目录结构

```
optical-character-recognition/
├── pdf_to_text_pdf.py       # 保留原图版（添加透明文字层）
├── pdf_to_text_only.py      # 纯文字版（无图片背景）
├── source_PDF/              # 存放源PDF文件
├── output_PDF/              # 存放输出文件
├── venv/                    # Python虚拟环境（安装后生成）
├── requirements.txt
└── README.md
```

### 基本命令

```bash
# 1. 激活虚拟环境（每次使用前都需要）
source venv/bin/activate

# 2. 列出source_PDF中的文件
python3 pdf_to_text_pdf.py -l

# 3. 模式A：保留原图版（添加透明文字层）
python3 pdf_to_text_pdf.py 源文件.pdf
python3 pdf_to_text_pdf.py 源文件.pdf -o 输出文件.pdf

# 4. 模式B：纯文字版（无图片背景）
python3 pdf_to_text_only.py 源文件.pdf
python3 pdf_to_text_only.py 源文件.pdf -o 输出文件.pdf
```

### 两种模式对比

| 特性 | 模式A: pdf_to_text_pdf.py | 模式B: pdf_to_text_only.py |
|------|---------------------------|-----------------------------|
| 图片背景 | ✓ 保留 | ✗ 移除 |
| 视觉效果 | 与原图一致 | 纯文字排版 |
| 文字可搜索 | ✓ | ✓ |
| 文件大小 | 较大（包含图片） | 较小（仅文字） |
| 排版还原 | 精确 | 基础 |

### 命令行选项

- `input_pdf`: 输入的PDF文件（可选，默认从source_PDF文件夹读取）
- `-o, --output`: 输出的PDF文件路径（可选，默认保存到output_PDF文件夹）
- `-l, --list`: 列出source_PDF文件夹中的所有PDF文件（仅模式A支持）

### 使用示例

```bash
# 列出可用文件
python3 pdf_to_text_pdf.py -l

# 模式A：保留原图版（适合需要保留原始格式的场景）
python3 pdf_to_text_pdf.py input.pdf
python3 pdf_to_text_pdf.py input.pdf -o output.pdf

# 模式B：纯文字版（适合只需要文字内容的场景）
python3 pdf_to_text_only.py input.pdf
python3 pdf_to_text_only.py input.pdf -o output.pdf
```

### 自动环境检查

程序运行时会自动检查以下依赖：

- **Python版本**：显示当前Python版本
- **Python包**：pdf2image、pytesseract、Pillow、reportlab
- **系统工具**：Poppler (pdftoppm)、Tesseract OCR引擎
- **语言包**：Tesseract中文语言包 (chi_sim)

如果检测到任何缺失的依赖，程序会显示具体的安装命令（使用brew或apt-get）。

### 环境检查示例输出

```
==================================================
正在检查运行环境...
==================================================

[1/4] Python版本: 3.9.0

[2/4] 检查Python包...
  ✓ pdf2image
  ✓ pytesseract
  ✓ Pillow
  ✓ reportlab

[3/4] 检查系统工具...
  ✓ Poppler (pdftoppm)
  ✓ Tesseract (tesseract 5.3.0)

[4/4] 检查Tesseract语言包...
  ✓ 简体中文语言包 (chi_sim)

==================================================
✓ 所有依赖已安装，可以正常运行！
==================================================
```

## 工作原理

1. **PDF转图片**：使用`pdf2image`将PDF每一页转换为图片
2. **OCR识别**：使用Tesseract对图片进行文字识别
3. **生成文字PDF**：使用`reportlab`创建新的PDF，保留原图并添加透明文字层

## 注意事项

- 首次运行前，程序会自动检查环境并提示缺失的依赖
- OCR识别准确率取决于原始PDF的清晰度
- 处理大文件可能需要较长时间

## 文件说明

- `pdf_to_text_pdf.py` - 主程序文件
- `requirements.txt` - Python依赖库清单
