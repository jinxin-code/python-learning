"""
表单处理模块

本模块使用 Flask-WTF 定义用户表单，展示了表单验证的最佳实践。

学习要点：
- Flask-WTF 的使用
- 表单字段的定义
- 验证器的使用
- CSRF 保护的原理
"""

# 导入 Flask-WTF 表单基类
from flask_wtf import FlaskForm

# 导入 WTForms 字段类型
from wtforms import StringField, SubmitField

# 导入验证器
from wtforms.validators import DataRequired, Email, Length


class UserForm(FlaskForm):
    """
    用户表单类，用于创建和编辑用户
    
    Flask-WTF 特点：
    1. 自动生成 CSRF 令牌，防止跨站请求伪造
    2. 提供服务端表单验证
    3. 自动处理表单数据的获取和转换
    4. 与 Flask 模板无缝集成
    
    字段说明：
    - name: 用户姓名（必填，2-50字符）
    - username: 用户名（必填，3-30字符）
    - email: 邮箱地址（必填，需符合邮箱格式）
    - submit: 提交按钮
    """
    
    # StringField 用于文本输入
    # 第一个参数是字段标签，会在模板中显示
    name = StringField('Name', validators=[
        # DataRequired 验证器：确保字段不为空
        DataRequired(message='Name is required'),
        # Length 验证器：限制字符串长度
        Length(min=2, max=50, message='Name must be between 2 and 50 characters')
    ])
    
    username = StringField('Username', validators=[
        DataRequired(message='Username is required'),
        Length(min=3, max=30, message='Username must be between 3 and 30 characters')
    ])
    
    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        # Email 验证器：检查邮箱格式是否正确
        # 需要安装 email_validator 包：pip install email-validator
        Email(message='Invalid email address')
    ])
    
    # SubmitField 用于提交按钮
    submit = SubmitField('Submit')
