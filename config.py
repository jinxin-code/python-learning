# 导入os模块，用于获取环境变量
import os

# 配置类，用于存储应用的配置信息
class Config:
    # 密钥，用于Flask的会话管理和CSRF保护
    # 优先从环境变量中获取，如果环境变量不存在则使用默认值
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    
    # API基础URL，用于发送HTTP请求到JSONPlaceholder API
    BASE_URL = 'https://jsonplaceholder.typicode.com/users'