"""
表单模块

本模块定义了用户相关的表单类。

学习要点：
- Django 表单的定义
- 表单验证
- 模型表单的使用
"""

from django import forms
from .models import User


class UserForm(forms.ModelForm):
    """
    用户表单
    
    基于 User 模型创建的表单，用于创建和编辑用户。
    
    表单字段：
    - name: 用户姓名（必填）
    - username: 用户名（必填，唯一）
    - email: 邮箱地址（必填，唯一）
    - phone: 电话号码（可选）
    - website: 个人网站（可选）
    """
    
    class Meta:
        """
        表单元数据配置
        
        model: 指定表单关联的模型
        fields: 指定要包含的字段
        labels: 自定义字段标签
        widgets: 自定义字段的 HTML 控件
        """
        model = User
        fields = ['name', 'username', 'email', 'phone', 'website']
        labels = {
            'name': '姓名',
            'username': '用户名',
            'email': '邮箱',
            'phone': '电话',
            'website': '网站',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
        }
    
    def clean_username(self):
        """
        验证用户名
        
        确保用户名唯一（编辑时排除当前用户）
        """
        username = self.cleaned_data.get('username')
        
        # 检查是否为编辑模式（存在 instance）
        if self.instance.pk:
            # 如果是编辑，排除当前用户
            if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('该用户名已被使用')
        else:
            # 如果是新建，检查是否已存在
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError('该用户名已被使用')
        
        return username
    
    def clean_email(self):
        """
        验证邮箱
        
        确保邮箱唯一（编辑时排除当前用户）
        """
        email = self.cleaned_data.get('email')
        
        if self.instance.pk:
            if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('该邮箱已被使用')
        else:
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError('该邮箱已被使用')
        
        return email
