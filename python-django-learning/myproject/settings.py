"""
Django 项目配置文件

本文件包含 Django 项目的所有配置项。

学习要点：
- Django 配置的结构和组织方式
- 数据库配置
- 应用注册
- 静态文件和模板配置
- 安全配置
"""

import os
from pathlib import Path

# 项目基础目录
# BASE_DIR 是项目根目录的绝对路径
BASE_DIR = Path(__file__).resolve().parent.parent

# 安全密钥
# 用于加密会话数据、密码重置令牌等
SECRET_KEY = os.environ.get('SECRET_KEY') or 'django-insecure-dev-key-for-learning'

# 调试模式
# 开发环境设为 True，生产环境必须设为 False
DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'

# 允许访问的主机
# 生产环境需要设置具体的域名
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# 注册的应用
# Django 会自动加载这些应用中的模型、视图等
INSTALLED_APPS = [
    # Django 内置应用
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # 第三方应用
    'django_extensions',  # 提供额外的管理命令
    
    # 自定义应用
    'users',  # 用户管理应用
]

# 中间件配置
# 中间件按顺序执行，处理请求和响应
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URL 配置根路径
ROOT_URLCONF = 'myproject.urls'

# 模板配置
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 模板文件搜索路径
        'DIRS': [BASE_DIR / 'templates'],
        # 是否在应用目录下搜索模板
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI 应用配置
WSGI_APPLICATION = 'myproject.wsgi.application'

# 数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 密码验证配置
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# 国际化配置
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_TZ = True

# 静态文件配置
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# 媒体文件配置
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# 默认主键字段类型
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 外部 API 配置
API_BASE_URL = os.environ.get('API_BASE_URL') or 'https://jsonplaceholder.typicode.com/users'
