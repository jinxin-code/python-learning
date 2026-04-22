# 导入app实例
from app import app

# 如果当前模块是主模块，则运行应用
if __name__ == '__main__':
    # 运行Flask应用
    # debug=True表示启用调试模式，在开发环境中使用
    # 调试模式下，当代码修改时应用会自动重启，并且会显示详细的错误信息
    app.run(debug=True)