"""
Django URL 配置

本文件定义了项目的 URL 路由映射。

学习要点：
- URL 模式的定义
- include 的使用
- 命名空间的概念
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django 管理后台
    path('admin/', admin.site.urls),
    
    # 用户应用的 URL 路由
    # 使用 include 将 users 应用的 URL 包含进来
    path('', include('users.urls')),
]
