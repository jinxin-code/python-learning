"""
WSGI 配置

本文件定义了 WSGI 应用，用于生产环境部署。

学习要点：
- WSGI 的概念
- Django 的 WSGI 配置
- 生产环境部署准备
"""

import os

from django.core.wsgi import get_wsgi_application

# 设置 Django 配置模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# 获取 WSGI 应用实例
application = get_wsgi_application()
