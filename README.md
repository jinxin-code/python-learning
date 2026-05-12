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

## 项目结构

```
python-learning/
├── python-flask-learning/     # Flask 学习项目
│   ├── app/                   # 应用代码
│   │   ├── models/            # 数据模型
│   │   ├── services/          # 服务层
│   │   └── templates/         # 模板文件
│   ├── tests/                 # 测试文件
│   └── ...
│
├── python-fastapi-learning/   # FastAPI 学习项目
│   ├── app/                   # 应用代码
│   │   ├── models/            # Pydantic 模型
│   │   └── services/          # 服务层
│   ├── tests/                 # 测试文件
│   └── ...
│
├── python-django-learning/    # Django 学习项目
│   ├── myproject/             # 项目配置
│   ├── users/                 # 用户应用
│   ├── templates/             # 模板文件
│   └── ...
│
└── README.md                  # 本文件
```

## 许可证

MIT License
