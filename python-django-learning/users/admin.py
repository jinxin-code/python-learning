"""
Django 后台管理配置

本模块注册用户模型到 Django 管理后台。

学习要点：
- Django admin 的基本配置
- 自定义管理界面
- 列表显示和搜索配置
"""

from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    用户模型的后台管理配置
    
    配置说明：
    - list_display: 列表页显示的字段
    - search_fields: 可搜索的字段
    - list_filter: 侧边栏过滤条件
    - ordering: 默认排序
    - fields: 编辑页显示的字段
    """
    
    # 列表页显示的字段
    list_display = ('id', 'username', 'name', 'email', 'phone', 'created_at')
    
    # 可搜索的字段
    search_fields = ('username', 'name', 'email')
    
    # 侧边栏过滤条件
    list_filter = ('created_at',)
    
    # 默认排序（按创建时间降序）
    ordering = ('-created_at',)
    
    # 编辑页显示的字段分组
    fieldsets = (
        (None, {
            'fields': ('username', 'name', 'email')
        }),
        ('联系信息', {
            'fields': ('phone', 'website')
        }),
        ('其他信息', {
            'fields': ('address', 'company'),
            'classes': ('collapse',)  # 默认折叠
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    # 只读字段（不能在后台编辑）
    readonly_fields = ('created_at', 'updated_at')
