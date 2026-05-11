"""
Flask 应用初始化模块

本模块展示了 Flask 应用的工厂模式实现，是 Flask 大型应用的标准结构。

工厂模式的优势：
1. 支持多环境配置（开发/测试/生产）
2. 便于单元测试，可以创建独立的测试应用实例
3. 避免循环导入问题
4. 支持应用的动态配置

学习要点：
- Flask 应用实例的创建方式
- 配置加载机制
- Flask 扩展的初始化方式
- 工厂模式在 Flask 中的应用
- 路由注册的最佳实践
"""

# 导入 Flask 核心类
from flask import Flask

# 导入配置模块，包含多环境配置类
from config import config_by_name

# 导入 Flask-Caching 扩展，用于实现缓存功能
from flask_caching import Cache

# 创建全局缓存实例，但不立即初始化
# 延迟初始化可以支持多应用实例和测试场景
cache = Cache()


def create_app(config_name='development'):
    """
    Flask 应用工厂函数
    
    参数:
        config_name (str): 配置环境名称，可选值: 'development', 'production', 'testing'
    
    返回:
        Flask: 配置好的 Flask 应用实例
    
    使用示例:
        app = create_app('development')
        app.run()
    """
    # 创建 Flask 应用实例
    # __name__ 参数告诉 Flask 应用的根目录位置，用于查找模板和静态文件
    app = Flask(__name__)
    
    # 从配置字典中加载对应环境的配置
    # config_by_name 是一个映射，将环境名称映射到配置类
    app.config.from_object(config_by_name[config_name])
    
    # 初始化缓存扩展
    # 使用 init_app 方法可以延迟初始化，支持多应用场景
    cache.init_app(app)
    
    # 导入路由注册函数
    # 放在这里导入可以避免循环导入问题
    from app.routes import register_routes
    
    # 注册路由到应用实例
    register_routes(app)
    
    # 返回配置好的应用实例
    return app
