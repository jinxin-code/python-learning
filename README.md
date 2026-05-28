# Python Learning

一个包含三个 Python Web 框架学习项目的仓库，对比学习 Flask、FastAPI 和 Django。

## 项目列表

### 1. python-flask-learning
Flask 框架学习项目

**特点：**
- 工厂模式应用结构
- Flask-Caching 缓存
- Flask-WTF 表单验证
- Jinja2 模板引擎

**启动方式：**
```bash
cd python-flask-learning
pip install -r requirements.txt
python run.py
```

**访问地址：** http://localhost:5000

---

### 2. python-fastapi-learning
FastAPI 框架学习项目

**特点：**
- Pydantic 数据验证
- 自动生成 API 文档（Swagger/ReDoc）
- 依赖注入
- 异步支持

**启动方式：**
```bash
cd python-fastapi-learning
pip install -r requirements.txt
python main.py
```

**访问地址：**
- API：http://localhost:8000
- Swagger 文档：http://localhost:8000/docs
- ReDoc 文档：http://localhost:8000/redoc

---

### 3. python-django-learning
Django 框架学习项目

**特点：**
- Django ORM 数据库操作
- CBV（基于类的视图）
- Django Admin 后台管理
- 表单验证

**启动方式：**
```bash
cd python-django-learning
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

**访问地址：** http://localhost:8000
**后台管理：** http://localhost:8000/admin

---

### 4. my-python-toolkit/optical-character-recognition
OCR PDF 文字识别工具

**功能特点：**
- 将扫描版PDF转换为可搜索文字版PDF
- 支持中英文混合识别
- 自动检测系统中文字体（苹方、黑体、宋体等），确保中文正确显示
- 两种输出模式：保留原图背景 / 纯文字输出
- 自动环境检查，提示缺失依赖及安装命令

**技术栈：**
- Poppler（PDF渲染引擎）
- Tesseract OCR引擎
- pdf2image、pytesseract、Pillow、reportlab

**启动方式：**
```bash
cd my-python-toolkit/optical-character-recognition
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**使用方法：**
```bash
# 列出可用文件
python3 pdf_to_text_pdf.py -l

# 模式A：保留原图版（添加透明文字层）
python3 pdf_to_text_pdf.py input.pdf

# 模式B：纯文字版（无图片背景）
python3 pdf_to_text_only.py input.pdf
```

---

## 技术对比

| 特性 | Flask | FastAPI | Django |
|------|-------|---------|--------|
| 框架类型 | 微框架 | 现代 API 框架 | 全功能框架 |
| 数据验证 | Flask-WTF | Pydantic | Django Forms/ORM |
| 模板引擎 | Jinja2 | 不内置 | Django Templates |
| 数据库 | SQLAlchemy（需安装） | ORM（需安装） | 内置 ORM |
| API 文档 | 需额外配置 | 自动生成 | 需 DRF |
| 学习曲线 | 低 | 中 | 高 |
| 适用场景 | 小型应用、API | 高性能 API | 大型 Web 应用 |

---

# Python Learning

A repository containing three Python web framework learning projects for comparing Flask, FastAPI, and Django.

## Project List

### 1. python-flask-learning
Flask Framework Learning Project

**Features:**
- Factory pattern application structure
- Flask-Caching
- Flask-WTF form validation
- Jinja2 template engine

**Quick Start:**
```bash
cd python-flask-learning
pip install -r requirements.txt
python run.py
```

**Access:** http://localhost:5000

---

### 2. python-fastapi-learning
FastAPI Framework Learning Project

**Features:**
- Pydantic data validation
- Auto-generated API documentation (Swagger/ReDoc)
- Dependency injection
- Async support

**Quick Start:**
```bash
cd python-fastapi-learning
pip install -r requirements.txt
python main.py
```

**Access:**
- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs
- ReDoc Docs: http://localhost:8000/redoc

---

### 3. python-django-learning
Django Framework Learning Project

**Features:**
- Django ORM database operations
- CBV (Class-Based Views)
- Django Admin backend
- Form validation

**Quick Start:**
```bash
cd python-django-learning
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

**Access:** http://localhost:8000
**Admin:** http://localhost:8000/admin

---

### 4. my-python-toolkit/optical-character-recognition
OCR PDF Text Recognition Tool

**Features:**
- Convert scanned PDFs to searchable text PDFs
- Support mixed Chinese-English recognition
- Auto-detect system Chinese fonts (PingFang, STHeiti, Songti, etc.) for proper Chinese display
- Two output modes: preserve original image / text-only output
- Auto environment check with installation instructions

**Tech Stack:**
- Poppler (PDF rendering engine)
- Tesseract OCR engine
- pdf2image, pytesseract, Pillow, reportlab

**Quick Start:**
```bash
cd my-python-toolkit/optical-character-recognition
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Usage:**
```bash
# List available files
python3 pdf_to_text_pdf.py -l

# Mode A: Preserve original image (add transparent text layer)
python3 pdf_to_text_pdf.py input.pdf

# Mode B: Text-only (no image background)
python3 pdf_to_text_only.py input.pdf
```

---

## Technology Comparison

| Feature | Flask | FastAPI | Django |
|---------|-------|---------|--------|
| Framework Type | Micro Framework | Modern API Framework | Full-Stack Framework |
| Data Validation | Flask-WTF | Pydantic | Django Forms/ORM |
| Template Engine | Jinja2 | Not Built-in | Django Templates |
| Database | SQLAlchemy (required) | ORM (required) | Built-in ORM |
| API Documentation | Requires extra config | Auto-generated | Requires DRF |
| Learning Curve | Low | Medium | High |
| Use Case | Small apps, APIs | High-performance APIs | Large web applications |

---

## Project Structure

```
python-learning/
├── python-flask-learning/     # Flask learning project
│   ├── app/                   # Application code
│   │   ├── models/            # Data models
│   │   ├── services/          # Service layer
│   │   └── templates/         # Template files
│   ├── tests/                 # Test files
│   └── ...
│
├── python-fastapi-learning/   # FastAPI learning project
│   ├── app/                   # Application code
│   │   ├── models/            # Pydantic models
│   │   └── services/          # Service layer
│   ├── tests/                 # Test files
│   └── ...
│
├── python-django-learning/    # Django learning project
│   ├── myproject/             # Project configuration
│   ├── users/                 # User app
│   ├── templates/             # Template files
│   └── ...
│
├── my-python-toolkit/         # Python toolkits
│   └── optical-character-recognition/  # OCR PDF tool
│       ├── source_PDF/        # Input PDF files
│       ├── output_PDF/        # Output PDF files
│       └── ...
│
└── README.md                  # This file
```

## License

MIT License
