# Python Django Learning

一个使用 Django 构建的用户管理系统学习项目。

## 项目特点

- 使用 **Django** 框架构建完整的 Web 应用
- 使用 **Django ORM** 进行数据库操作
- 使用 **Bootstrap 5** 进行前端样式设计
- 支持从外部 API 同步数据
- 完整的用户 CRUD 操作

## 技术栈

- Python 3.10+
- Django 5.0+
- Bootstrap 5.3+
- requests 库（HTTP 请求）

## 项目结构

```
python-django-learning/
├── myproject/                 # Django 项目配置
│   ├── __init__.py
│   ├── settings.py            # 项目配置
│   ├── urls.py                # 根 URL 配置
│   └── wsgi.py                # WSGI 配置
├── users/                     # 用户管理应用
│   ├── __init__.py
│   ├── admin.py               # 管理员后台配置
│   ├── apps.py                # 应用配置
│   ├── forms.py               # 表单定义
│   ├── models.py              # 数据模型
│   ├── services/              # 服务层
│   │   └── api_service.py     # API 服务封装
│   ├── urls.py                # 应用 URL 配置
│   └── views.py               # 视图函数
├── templates/                 # 模板文件
│   ├── base.html              # 基础模板
│   └── users/                 # 用户相关模板
│       ├── add.html           # 添加用户
│       ├── confirm_delete.html # 删除确认
│       ├── detail.html        # 用户详情
│       ├── edit.html          # 编辑用户
│       └── index.html         # 用户列表
├── manage.py                  # Django 管理命令
├── requirements.txt           # 依赖列表
├── .gitignore                # Git 忽略文件
└── README.md                 # 项目说明文档
```

## 快速开始

### 1. 安装依赖

```bash
# 进入项目目录
cd python-django-learning

# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 数据库迁移

```bash
# 创建数据库迁移文件
python manage.py makemigrations

# 应用数据库迁移
python manage.py migrate
```

### 3. 运行应用

```bash
# 启动开发服务器
python manage.py runserver

# 访问地址
# http://localhost:8000
```

### 4. 创建管理员账户（可选）

```bash
python manage.py createsuperuser

# 访问后台管理
# http://localhost:8000/admin
```

## 功能特性

### 用户管理

| 功能 | 描述 |
|------|------|
| 用户列表 | 显示所有用户，支持搜索和筛选 |
| 用户详情 | 查看单个用户的详细信息 |
| 添加用户 | 创建新用户 |
| 编辑用户 | 修改用户信息 |
| 删除用户 | 删除用户（带确认） |
| 同步用户 | 从外部 API 同步用户数据 |

### 搜索和筛选

- **搜索**: 根据姓名或用户名搜索用户
- **排序**: 支持按用户名或邮箱排序
- **分页**: 每页显示 10 条记录

## API 接口

项目支持从外部 API 同步数据：

```bash
# 同步用户数据
curl http://localhost:8000/users/sync/
```

## 配置说明

### 环境变量

| 环境变量 | 说明 | 默认值 |
|----------|------|--------|
| SECRET_KEY | Django 安全密钥 | django-insecure-dev-key |
| DEBUG | 调试模式 | True |
| ALLOWED_HOSTS | 允许的主机 | localhost,127.0.0.1 |
| API_BASE_URL | 外部 API 地址 | https://jsonplaceholder.typicode.com/users |

### settings.py 配置项

```python
# 数据库配置（SQLite）
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 注册的应用
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'users',
]
```

## 学习要点

本项目展示了以下 Django 核心概念：

1. **项目结构**: Django 项目和应用的组织方式
2. **模型定义**: 使用 Django ORM 定义数据模型
3. **视图函数**: 基于类的视图（CBV）和函数式视图
4. **URL 配置**: URL 路由的定义和命名空间
5. **表单处理**: Django 表单的定义和验证
6. **模板系统**: 模板继承和上下文变量
7. **数据库迁移**: Django 的迁移系统
8. **消息闪现**: 用户操作反馈
9. **服务层**: 业务逻辑的封装

## 开发命令

```bash
# 启动开发服务器
python manage.py runserver

# 创建新应用
python manage.py startapp myapp

# 创建迁移文件
python manage.py makemigrations

# 应用迁移
python manage.py migrate

# 运行测试
python manage.py test

# 创建超级用户
python manage.py createsuperuser
```

## 许可证

MIT License
