#!/usr/bin/env python
"""
Django 项目管理命令行工具

本文件是 Django 项目的入口脚本，用于管理项目的各种操作。

学习要点：
- Django 项目管理命令的使用
- manage.py 的作用和功能
- 命令行参数的处理
"""

import os
import sys


def main():
    """
    主函数 - 执行 Django 管理命令
    
    执行流程：
        1. 设置 DJANGO_SETTINGS_MODULE 环境变量
        2. 导入 Django 模块
        3. 配置 Django
        4. 执行管理命令
    
    使用示例：
        # 创建数据库迁移
        python manage.py makemigrations
        
        # 应用数据库迁移
        python manage.py migrate
        
        # 启动开发服务器
        python manage.py runserver
        
        # 创建超级用户
        python manage.py createsuperuser
    """
    # 设置 Django 配置模块
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
    
    try:
        # 导入 Django 的命令执行函数
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # 处理 Django 未安装的情况
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # 执行命令行命令
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
