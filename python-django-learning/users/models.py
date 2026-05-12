"""
用户模型模块

本模块定义了用户相关的数据模型。

学习要点：
- Django ORM 模型的定义
- 字段类型的使用
- 模型方法
- 数据迁移的概念
"""

from django.db import models
from django.urls import reverse


class User(models.Model):
    """
    用户数据模型
    
    用于存储用户信息的数据库模型。
    
    属性说明：
    - id: 用户唯一标识（自动生成的主键）
    - name: 用户姓名
    - username: 用户名
    - email: 邮箱地址
    - address: 地址信息（JSON 格式存储）
    - phone: 电话号码
    - website: 个人网站
    - company: 公司信息（JSON 格式存储）
    """
    
    # 用户名（唯一）
    username = models.CharField(max_length=150, unique=True, verbose_name='用户名')
    
    # 用户姓名
    name = models.CharField(max_length=255, verbose_name='姓名')
    
    # 邮箱地址（唯一）
    email = models.EmailField(unique=True, verbose_name='邮箱')
    
    # 地址信息（使用 JSONField 存储结构化数据）
    address = models.JSONField(null=True, blank=True, verbose_name='地址')
    
    # 电话号码
    phone = models.CharField(max_length=50, null=True, blank=True, verbose_name='电话')
    
    # 个人网站
    website = models.URLField(null=True, blank=True, verbose_name='网站')
    
    # 公司信息（使用 JSONField 存储结构化数据）
    company = models.JSONField(null=True, blank=True, verbose_name='公司')
    
    # 创建时间和更新时间（自动维护）
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        """
        元数据配置
        
        verbose_name: 模型的可读名称
        verbose_name_plural: 模型的复数可读名称
        ordering: 默认排序方式
        """
        verbose_name = '用户'
        verbose_name_plural = '用户列表'
        ordering = ['-created_at']  # 按创建时间降序排列
    
    def __str__(self):
        """
        返回对象的字符串表示
        
        当打印用户对象时，显示用户名
        """
        return self.username
    
    def get_absolute_url(self):
        """
        返回用户详情页的 URL
        
        用于模板中的 {% url %} 标签和 redirect() 函数
        """
        return reverse('user_detail', kwargs={'pk': self.pk})
    
    def get_address_display(self):
        """
        返回格式化的地址显示
        
        将 JSON 格式的地址转换为可读字符串
        """
        if not self.address:
            return ''
        
        address = self.address
        parts = []
        if 'street' in address:
            parts.append(address['street'])
        if 'suite' in address:
            parts.append(address['suite'])
        if 'city' in address:
            parts.append(address['city'])
        if 'zipcode' in address:
            parts.append(address['zipcode'])
        
        return ', '.join(parts)
    
    def get_company_name(self):
        """
        返回公司名称
        
        从 JSON 字段中提取公司名称
        """
        if self.company and 'name' in self.company:
            return self.company['name']
        return ''
