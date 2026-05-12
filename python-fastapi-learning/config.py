"""
FastAPI 应用配置模块

本模块展示了 FastAPI 多环境配置的最佳实践。

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
    - API_BASE_URL: 外部 API 的基础 URL
    - LOG_LEVEL: 日志级别
    """
    
    # API 基础 URL：支持通过环境变量配置
    # 默认使用 jsonplaceholder 作为测试 API
    API_BASE_URL = os.environ.get('API_BASE_URL') or 'https://jsonplaceholder.typicode.com/users'
    
    # 日志级别：默认 INFO 级别
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')


class DevelopmentConfig(Config):
    """
    开发环境配置
    
    开发环境特点：
    - 开启调试模式，便于开发和调试
    - 日志级别设为 DEBUG，输出详细日志
    """
    DEBUG = True
    LOG_LEVEL = 'DEBUG'


class ProductionConfig(Config):
    """
    生产环境配置
    
    生产环境特点：
    - 关闭调试模式，提高安全性
    """
    DEBUG = False


class TestingConfig(Config):
    """
    测试环境配置
    
    测试环境特点：
    - 开启调试模式
    - 可以使用测试专用的 API
    """
    DEBUG = True
    TESTING = True
    # 测试环境可以使用不同的 API 地址
    API_BASE_URL = os.environ.get('TEST_API_BASE_URL') or 'https://jsonplaceholder.typicode.com/users'


# 配置映射字典，用于根据环境名称获取对应的配置类
# 使用示例: config_by_name['development'] 返回 DevelopmentConfig
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
