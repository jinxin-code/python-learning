# 导入Flask类，用于创建Flask应用实例
from flask import Flask
# 导入配置类，用于加载应用配置
from config import Config

# 创建Flask应用实例
# __name__是模块名，Flask会根据这个参数确定应用的根目录
app = Flask(__name__)

# 从配置类加载配置
app.config.from_object(Config)

# 导入路由模块，必须在创建app实例后导入，避免循环导入
from app import routes