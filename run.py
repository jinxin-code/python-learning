"""
Flask 应用入口模块

本模块是应用的启动入口，负责创建和运行 Flask 应用。

学习要点：
- Python 程序入口的标准写法
- 环境变量的读取
- 应用工厂的调用
- 模块级代码的执行控制
"""

# 导入 os 模块，用于读取环境变量
import os

# 导入应用工厂函数
from app import create_app


if __name__ == '__main__':
    """
    应用入口点
    
    语法说明：
        - if __name__ == '__main__' 是 Python 的程序入口模式
        - 当脚本直接运行时，__name__ 等于 '__main__'
        - 当脚本被导入时，__name__ 等于模块名（不会执行此代码块）
    
    执行流程：
        1. 从环境变量获取配置环境名称
        2. 使用工厂函数创建应用实例
        3. 运行应用
    
    环境变量：
        - FLASK_ENV: 指定运行环境（development/production/testing）
                     默认值为 'development'
    
    使用示例：
        # 开发环境（默认）
        python run.py
        
        # 或显式指定环境
        FLASK_ENV=development python run.py
        
        # 生产环境
        FLASK_ENV=production SECRET_KEY=your-secret-key python run.py
    """
    # 从环境变量获取配置名称，默认使用 'development'
    # os.environ.get(key, default) 如果环境变量不存在，返回默认值
    config_name = os.environ.get('FLASK_ENV', 'development')
    
    # 使用工厂函数创建应用实例
    app = create_app(config_name)
    
    # 运行应用
    # app.run() 启动 Flask 开发服务器
    # 默认监听 127.0.0.1:5000
    app.run()
