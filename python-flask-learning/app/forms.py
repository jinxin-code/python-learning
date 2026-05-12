"""
表单处理模块

本模块使用 Flask-WTF 定义用户表单，展示了表单验证的最佳实践。

学习要点：
- Flask-WTF 的使用
- 表单字段的定义
- 验证器的使用
- CSRF 保护的原理
- 类继承的使用
"""

# 导入 Flask-WTF 表单基类
# FlaskForm 是所有表单类的基类，提供 CSRF 保护和表单验证功能
from flask_wtf import FlaskForm

# 导入 WTForms 字段类型
# StringField: 文本输入字段
# SubmitField: 提交按钮字段
from wtforms import StringField, SubmitField

# 导入验证器
# DataRequired: 确保字段不为空
# Email: 验证邮箱格式
# Length: 验证字符串长度
from wtforms.validators import DataRequired, Email, Length


class UserForm(FlaskForm):
    """
    用户表单类，用于创建和编辑用户
    
    继承关系：
        UserForm -> FlaskForm -> Form
    
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
    # validators 参数是一个验证器列表，按顺序执行验证
    name = StringField('Name', validators=[
        # DataRequired 验证器：确保字段不为空
        # message 参数用于自定义错误消息
        DataRequired(message='Name is required'),
        # Length 验证器：限制字符串长度
        # min 和 max 参数指定最小和最大长度
        Length(min=2, max=50, message='Name must be between 2 and 50 characters')
    ])
    
    # 用户名字段
    # 同样使用 DataRequired 和 Length 验证器
    username = StringField('Username', validators=[
        DataRequired(message='Username is required'),
        Length(min=3, max=30, message='Username must be between 3 and 30 characters')
    ])
    
    # 邮箱字段
    # 使用 Email 验证器检查邮箱格式
    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        # Email 验证器：检查邮箱格式是否正确
        # 需要安装 email_validator 包：pip install email-validator
        Email(message='Invalid email address')
    ])
    
    # SubmitField 用于提交按钮
    # 参数是按钮上显示的文本
    submit = SubmitField('Submit')
