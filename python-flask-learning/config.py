"""
Flask 应用配置模块

本模块展示了 Flask 多环境配置的最佳实践。

配置管理的重要性：
1. 分离敏感配置（如密钥、数据库密码）和代码
2. 支持不同环境使用不同配置
3. 提高安全性，避免敏感信息泄露

学习要点：
- 配置类的继承结构
- 环境变量的读取方式
- 多环境配置的实现
- 默认值的设置策略
"""

# 导入 os 模块，用于读取环境变量
import os


class Config:
    """
    基础配置类，包含所有环境共享的配置
    
    配置项说明：
    - SECRET_KEY: Flask 应用的密钥，用于会话管理和 CSRF 保护
    - BASE_URL: 外部 API 的基础 URL
    - LOG_LEVEL: 日志级别
    - CACHE_TYPE: 缓存类型
    - CACHE_DEFAULT_TIMEOUT: 默认缓存超时时间（秒）
    """
    
    # 密钥配置：优先从环境变量获取，否则使用默认值
    # 生产环境中必须通过环境变量设置安全的密钥
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    
    # API 基础 URL：支持通过环境变量配置
    BASE_URL = os.environ.get('API_BASE_URL') or 'https://jsonplaceholder.typicode.com/users'
    
    # 日志级别：默认 INFO 级别
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    
    # 缓存类型：默认使用简单内存缓存
    CACHE_TYPE = os.environ.get('CACHE_TYPE', 'simple')
    
    # 缓存超时时间：默认 300 秒（5分钟）
    CACHE_DEFAULT_TIMEOUT = int(os.environ.get('CACHE_TIMEOUT', '300'))


class DevelopmentConfig(Config):
    """
    开发环境配置
    
    开发环境特点：
    - 开启调试模式，便于开发和调试
    - 日志级别设为 DEBUG，输出详细日志
    - 使用简单的内存缓存
    """
    DEBUG = True
    LOG_LEVEL = 'DEBUG'


class ProductionConfig(Config):
    """
    生产环境配置
    
    生产环境特点：
    - 关闭调试模式，提高安全性
    - 强制要求设置 SECRET_KEY 环境变量
    - 默认使用 Redis 缓存（需要额外安装 redis 依赖）
    """
    DEBUG = False
    # 生产环境必须设置密钥，不提供默认值
    SECRET_KEY = os.environ.get('SECRET_KEY')
    # 生产环境建议使用 Redis 作为缓存后端
    CACHE_TYPE = os.environ.get('CACHE_TYPE', 'redis')


class TestingConfig(Config):
    """
    测试环境配置
    
    测试环境特点：
    - 开启调试模式
    - 开启测试模式，Flask 会跳过某些检查
    - 使用简单内存缓存，避免外部依赖
    """
    DEBUG = True
    TESTING = True
    CACHE_TYPE = 'simple'


# 配置映射字典，用于根据环境名称获取对应的配置类
# 使用示例: config_by_name['development'] 返回 DevelopmentConfig
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
