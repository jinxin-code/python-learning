from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class UserForm(FlaskForm):
    """
    用户表单，用于创建和编辑用户
    """
    name = StringField('Name', validators=[
        DataRequired(message='Name is required'),
        Length(min=2, max=50, message='Name must be between 2 and 50 characters')
    ])
    username = StringField('Username', validators=[
        DataRequired(message='Username is required'),
        Length(min=3, max=30, message='Username must be between 3 and 30 characters')
    ])
    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Invalid email address')
    ])
    submit = SubmitField('Submit')
