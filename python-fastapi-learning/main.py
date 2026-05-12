"""
FastAPI 应用入口模块

本模块是应用的启动入口，负责创建和运行 FastAPI 应用。

学习要点：
- FastAPI 应用的创建和配置
- 路由注册方式
- 依赖注入的使用
- 环境变量的读取
- 应用生命周期管理
"""

# 导入 os 模块，用于读取环境变量
import os

# 导入 FastAPI 核心类
from fastapi import FastAPI, HTTPException, Query, Depends
from typing import List, Optional

# 导入配置模块
from config import config_by_name

# 导入用户模型
from app.models.user import User, UserCreate, UserUpdate

# 导入 API 服务
from app.services.api_service import ApiService


class ApiServiceSingleton:
    """
    API 服务单例类
    
    使用单例模式确保整个应用中只有一个 ApiService 实例，
    避免每次请求都创建新的连接。
    
    学习要点：
    - 单例模式的实现
    - 线程安全的实例创建
    - 延迟初始化
    """
    _instance = None
    _lock = None  # 线程锁
    
    @classmethod
    def get_instance(cls, base_url: str = None) -> ApiService:
        """
        获取 ApiService 单例实例
        
        参数:
            base_url (str): API 基础 URL
        
        返回:
            ApiService: 单例实例
        """
        # 延迟导入 threading 以避免启动时的不必要开销
        import threading
        
        # 初始化锁
        if cls._lock is None:
            cls._lock = threading.Lock()
        
        # 双重检查锁定（线程安全）
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    # 获取配置（如果没有提供 base_url）
                    if base_url is None:
                        config_name = os.environ.get('FASTAPI_ENV', 'development')
                        config = config_by_name[config_name]
                        base_url = config.API_BASE_URL
                    
                    cls._instance = ApiService(base_url)
        
        return cls._instance
    
    @classmethod
    def reset_instance(cls):
        """
        重置单例实例（用于测试）
        
        在单元测试中可以调用此方法重置实例状态
        """
        if cls._instance:
            cls._instance.close()
            cls._instance = None


def get_api_service() -> ApiService:
    """
    API 服务依赖注入函数
    
    使用单例模式确保每次请求都使用同一个 ApiService 实例，
    避免频繁创建和销毁 HTTP 连接。
    
    返回:
        ApiService: API 服务实例（单例）
    
    依赖注入说明：
        使用 Depends 装饰器可以实现依赖注入，
        在路由函数中声明需要的依赖，FastAPI 会自动注入。
    """
    return ApiServiceSingleton.get_instance()


def create_app(config_name: str = 'development') -> FastAPI:
    """
    应用工厂函数
    
    参数:
        config_name (str): 配置环境名称（development/production/testing）
    
    返回:
        FastAPI: 配置好的 FastAPI 应用实例
    
    工厂模式说明：
        工厂模式允许我们根据不同环境创建不同配置的应用实例，
        避免全局状态，便于测试和部署。
    """
    # 获取配置类
    config = config_by_name[config_name]
    
    # 创建 FastAPI 应用实例
    # title: 应用标题，会显示在自动生成的文档中
    # description: 应用描述
    # version: 应用版本
    app = FastAPI(
        title="用户管理 API",
        description="一个使用 FastAPI 构建的用户管理系统，支持用户的增删改查操作",
        version="1.0.0"
    )
    
    # 保存配置到应用状态
    app.state.config = config
    
    # 注册路由
    register_routes(app)
    
    return app


def register_routes(app: FastAPI):
    """
    注册路由到应用实例
    
    参数:
        app (FastAPI): FastAPI 应用实例
    
    路由注册说明：
        在工厂模式下，路由需要在应用实例创建后注册，
        这样可以避免循环导入问题。
    """
    
    @app.get("/", response_model=List[User], summary="获取用户列表")
    def get_users(
        search: Optional[str] = Query(None, description="搜索关键词（匹配姓名或用户名）"),
        filter_by: Optional[str] = Query('all', description="筛选条件：all（全部）、username（按用户名排序）、email（按邮箱排序）"),
        api_service: ApiService = Depends(get_api_service)
    ):
        """
        获取用户列表，支持搜索和筛选
        
        参数：
            search: 搜索关键词，匹配姓名或用户名（不区分大小写）
            filter_by: 筛选条件
                - all: 返回所有用户（默认）
                - username: 按用户名排序
                - email: 按邮箱前缀排序
        
        返回：
            List[User]: 用户对象列表
        """
        # 从 API 获取用户列表
        users = api_service.get_users()
        
        # 搜索功能：过滤包含搜索关键词的用户
        if search:
            users = [user for user in users if 
                     search.lower() in user.name.lower() or 
                     search.lower() in user.username.lower()]
        
        # 筛选功能：根据条件排序
        if filter_by == 'username':
            users.sort(key=lambda x: x.username)
        elif filter_by == 'email':
            users.sort(key=lambda x: x.email.split('@')[0] if x.email else '')
        
        return users
    
    @app.get("/users/{user_id}", response_model=User, summary="获取单个用户")
    def get_user(
        user_id: int,
        api_service: ApiService = Depends(get_api_service)
    ):
        """
        获取单个用户的详细信息
        
        参数：
            user_id: 用户 ID
        
        返回：
            User: 用户对象
        
        异常：
            404: 用户不存在
        """
        user = api_service.get_user(user_id)
        
        if not user:
            # 抛出 HTTP 异常，FastAPI 会自动处理并返回正确的状态码
            raise HTTPException(status_code=404, detail="用户不存在")
        
        return user
    
    @app.post("/users/", response_model=User, status_code=201, summary="创建新用户")
    def create_user(
        user_data: UserCreate,
        api_service: ApiService = Depends(get_api_service)
    ):
        """
        创建新用户
        
        参数：
            user_data: 用户创建请求体（包含 name, username, email）
        
        返回：
            User: 创建的用户对象
        
        状态码：
            201: 创建成功
        """
        # 将 Pydantic 模型转换为字典
        data = user_data.model_dump()
        
        # 调用 API 服务创建用户
        new_user = api_service.create_user(data)
        
        if not new_user:
            raise HTTPException(status_code=500, detail="创建用户失败")
        
        return new_user
    
    @app.put("/users/{user_id}", response_model=User, summary="更新用户信息")
    def update_user(
        user_id: int,
        user_data: UserUpdate,
        api_service: ApiService = Depends(get_api_service)
    ):
        """
        更新用户信息
        
        参数：
            user_id: 用户 ID
            user_data: 用户更新请求体（可选字段：name, username, email）
        
        返回：
            User: 更新后的用户对象
        
        异常：
            404: 用户不存在
        """
        # 检查用户是否存在
        existing_user = api_service.get_user(user_id)
        if not existing_user:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        # 获取更新数据（过滤掉 None 值）
        data = user_data.model_dump(exclude_none=True)
        
        # 如果没有提供任何更新字段，返回原用户
        if not data:
            return existing_user
        
        # 调用 API 服务更新用户
        updated_user = api_service.update_user(user_id, data)
        
        if not updated_user:
            raise HTTPException(status_code=500, detail="更新用户失败")
        
        return updated_user
    
    @app.delete("/users/{user_id}", status_code=204, summary="删除用户")
    def delete_user(
        user_id: int,
        api_service: ApiService = Depends(get_api_service)
    ):
        """
        删除用户
        
        参数：
            user_id: 用户 ID
        
        返回：
            无内容（204 No Content）
        
        异常：
            404: 用户不存在
        """
        # 检查用户是否存在
        user = api_service.get_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        # 调用 API 服务删除用户
        success = api_service.delete_user(user_id)
        
        if not success:
            raise HTTPException(status_code=500, detail="删除用户失败")
        
        # FastAPI 会自动返回 204 No Content


# 创建模块级别的应用实例（供 uvicorn reload 模式使用）
config_name = os.environ.get('FASTAPI_ENV', 'development')
app = create_app(config_name)


# 如果脚本直接运行，启动开发服务器
if __name__ == '__main__':
    """
    应用入口点
    
    使用说明：
        # 开发环境（默认）
        python main.py
        
        # 或显式指定环境
        FASTAPI_ENV=development python main.py
        
        # 生产环境
        FASTAPI_ENV=production python main.py
    """
    # 导入 uvicorn，FastAPI 的 ASGI 服务器
    import uvicorn
    
    # 从环境变量获取配置环境名称，默认使用 'development'
    config_name = os.environ.get('FASTAPI_ENV', 'development')
    
    # 使用工厂函数创建应用实例
    app = create_app(config_name)
    
    # 运行应用
    # uvicorn.run() 启动 ASGI 服务器
    # host='0.0.0.0' 允许外部访问
    # port=8000 使用 8000 端口
    # reload=True 开启热重载（开发环境）
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
