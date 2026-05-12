"""
API 服务模块

本模块封装了与外部 API 的交互逻辑，展示了 Python 中 HTTP 请求的最佳实践。

学习要点：
- httpx 库的使用（替代 requests，支持异步）
- 异常处理的正确方式
- 日志记录的实践
- 类型提示的使用
- 服务层的封装模式
"""

# 导入 httpx 库，用于发送 HTTP 请求
# httpx 是 requests 的现代化替代，支持同步和异步
import httpx

# 导入 logging 模块，用于日志记录
import logging

# 导入类型提示模块
from typing import List, Dict, Optional, Any

# 导入用户模型
from app.models.user import User

# 配置日志
# level=logging.INFO 表示只记录 INFO 级别及以上的日志
# logging 的级别从低到高: DEBUG < INFO < WARNING < ERROR < CRITICAL
logging.basicConfig(level=logging.INFO)

# 创建日志记录器，__name__ 表示当前模块名
logger = logging.getLogger(__name__)


class ApiService:
    """
    API 服务类，封装了所有与用户相关的 API 操作
    
    使用 httpx.Client 来保持连接复用，提高性能。
    
    主要功能：
    - 获取用户列表
    - 获取单个用户
    - 创建用户
    - 更新用户
    - 删除用户
    """
    
    def __init__(self, base_url: str):
        """
        初始化 API 服务（构造方法）
        
        参数:
            base_url (str): API 的基础 URL
        
        语法说明：
            - __init__ 是 Python 的初始化方法，创建对象时自动调用
            - self 是实例方法的第一个参数，代表对象本身
            - 参数类型提示 (base_url: str) 标注参数期望的类型
        """
        # 保存基础 URL 到实例属性
        self.base_url = base_url
        
        # 创建 httpx.Client 对象
        # Client 可以保持连接，复用 TCP 连接，提高性能
        # 相当于浏览器的保持连接功能
        self.client = httpx.Client(
            # 设置请求超时时间（10秒）
            # timeout 是一个浮点数或 httpx.Timeout 对象
            timeout=httpx.Timeout(10.0),
            # 跟随重定向（最多 5 次）
            follow_redirects=True
        )
    
    def get_users(self) -> List[User]:
        """
        获取所有用户列表
        
        返回:
            List[User]: 用户对象列表，如果请求失败返回空列表
        
        返回类型提示说明：
            - List[User] 表示元素类型为 User 的列表
        
        异常处理：
            捕获 httpx.HTTPError，记录日志并返回空列表
        """
        try:
            # 发送 GET 请求
            # self.client.get() 使用 Client 对象发送请求
            response = self.client.get(self.base_url)
            
            # 检查响应状态码
            # raise_for_status() 会在状态码 >= 400 时抛出 HTTPError 异常
            response.raise_for_status()
            
            # 解析 JSON 响应
            # response.json() 将 JSON 字符串转换为 Python 字典/列表
            users_data = response.json()
            
            # 使用列表推导式将字典列表转换为 User 对象列表
            return [User.from_dict(user_data) for user_data in users_data]
        
        # 捕获 httpx 库的所有异常
        # httpx.HTTPError 是所有 httpx HTTP 异常的基类
        except httpx.HTTPError as e:
            # 记录错误日志
            logger.error(f"获取用户列表失败: {str(e)}")
            
            # 返回空列表，保证函数返回类型一致
            return []
    
    def get_user(self, user_id: int) -> Optional[User]:
        """
        获取单个用户信息
        
        参数:
            user_id (int): 用户 ID
        
        返回:
            Optional[User]: 用户对象，如果失败返回 None
        
        Optional 类型说明：
            Optional[X] 表示返回值可以是 X 类型或者 None
        
        URL 构建示例:
            base_url = 'https://example.com/users'
            user_id = 1
            最终 URL: 'https://example.com/users/1'
        """
        try:
            # 构建完整的请求 URL
            # f-string 格式化：{self.base_url} 和 {user_id} 会被替换为实际值
            response = self.client.get(f'{self.base_url}/{user_id}')
            response.raise_for_status()
            
            # 获取用户数据并转换为 User 对象
            user_data = response.json()
            return User.from_dict(user_data)
        
        except httpx.HTTPError as e:
            logger.error(f"获取用户 {user_id} 失败: {str(e)}")
            return None
    
    def update_user(self, user_id: int, data: Dict[str, Any]) -> Optional[User]:
        """
        更新用户信息
        
        参数:
            user_id (int): 用户 ID
            data (Dict[str, Any]): 要更新的数据
        
        返回:
            Optional[User]: 更新后的用户对象，如果失败返回 None
        
        PUT 请求说明:
            PUT 请求用于更新资源，通常需要提供完整的资源数据
            这里使用 json=data 自动设置 Content-Type: application/json
        """
        try:
            # 发送 PUT 请求，使用 json 参数传递数据
            response = self.client.put(f'{self.base_url}/{user_id}', json=data)
            response.raise_for_status()
            
            # 获取更新后的用户数据并转换为 User 对象
            user_data = response.json()
            return User.from_dict(user_data)
        
        except httpx.HTTPError as e:
            logger.error(f"更新用户 {user_id} 失败: {str(e)}")
            return None
    
    def create_user(self, data: Dict[str, Any]) -> Optional[User]:
        """
        创建新用户
        
        参数:
            data (Dict[str, Any]): 新用户的数据
        
        返回:
            Optional[User]: 创建的用户对象，如果失败返回 None
        
        POST 请求说明:
            POST 请求用于创建新资源
            服务器通常会返回新创建资源的完整信息，包括生成的 ID
        """
        try:
            # 发送 POST 请求
            response = self.client.post(self.base_url, json=data)
            response.raise_for_status()
            
            # 获取创建的用户数据并转换为 User 对象
            user_data = response.json()
            return User.from_dict(user_data)
        
        except httpx.HTTPError as e:
            logger.error(f"创建用户失败: {str(e)}")
            return None
    
    def delete_user(self, user_id: int) -> bool:
        """
        删除用户
        
        参数:
            user_id (int): 用户 ID
        
        返回:
            bool: 删除是否成功
        
        DELETE 请求说明:
            DELETE 请求用于删除资源
            成功时通常返回 204 No Content 状态码（无响应体）
        """
        try:
            # 发送 DELETE 请求
            response = self.client.delete(f'{self.base_url}/{user_id}')
            response.raise_for_status()
            return True
        
        except httpx.HTTPError as e:
            logger.error(f"删除用户 {user_id} 失败: {str(e)}")
            return False
    
    def close(self):
        """
        关闭 HTTP 客户端连接
        
        使用场景：
            在应用关闭时调用，释放资源
        """
        self.client.close()
