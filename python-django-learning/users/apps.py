"""
用户应用配置模块

本模块定义了用户应用的配置类。

学习要点：
- Django 应用配置的方式
- AppConfig 类的使用
"""

from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    用户应用配置类
    
    配置说明：
    - default_auto_field: 默认主键字段类型
    - name: 应用名称
    - verbose_name: 应用的可读名称（用于后台管理）
    """
    
    # 默认主键字段类型
    default_auto_field = 'django.db.models.BigAutoField'
    
    # 应用名称（必须与应用目录名一致）
    name = 'users'
    
    # 应用的可读名称（中文）
    verbose_name = '用户管理'
