"""
API 服务模块

本模块封装了与外部 API 的交互逻辑，展示了 Python 中 HTTP 请求的最佳实践。

学习要点：
- requests 库的使用（Session 对象、超时设置）
- 异常处理的正确方式
- 日志记录的实践
- 类型提示的使用
- 服务层的封装模式
"""

# 导入 requests 库，用于发送 HTTP 请求
import requests

# 导入 logging 模块，用于日志记录
import logging

# 导入类型提示模块
from typing import List, Dict, Optional, Any

# 配置日志
# level=logging.INFO 表示只记录 INFO 级别及以上的日志
logging.basicConfig(level=logging.INFO)

# 创建日志记录器，__name__ 表示当前模块名
logger = logging.getLogger(__name__)


class ApiService:
    """
    API 服务类，封装了所有与用户相关的 API 操作
    
    使用 requests.Session 来保持连接复用，提高性能。
    
    主要功能：
    - 获取用户列表
    - 获取单个用户
    - 创建用户
    - 更新用户
    - 删除用户
    """
    
    def __init__(self, base_url: str):
        """
        初始化 API 服务
        
        参数:
            base_url (str): API 的基础 URL
        """
        # 保存基础 URL
        self.base_url = base_url
        
        # 创建 Session 对象
        # Session 可以保持连接，复用 TCP 连接，提高性能
        self.session = requests.Session()
        
        # 设置请求超时时间（10秒）
        # 避免请求无限等待，防止资源耗尽
        self.session.timeout = 10
    
    def get_users(self) -> List[Dict[str, Any]]:
        """
        获取所有用户列表
        
        返回:
            List[Dict[str, Any]]: 用户列表，如果请求失败返回空列表
        
        异常处理：
            捕获 requests.RequestException，记录日志并返回空列表
        """
        try:
            # 发送 GET 请求
            response = self.session.get(self.base_url)
            
            # 检查响应状态码
            # raise_for_status() 会在状态码 >= 400 时抛出异常
            response.raise_for_status()
            
            # 解析 JSON 响应
            return response.json()
        
        except requests.RequestException as e:
            # 记录错误日志
            logger.error(f"获取用户列表失败: {str(e)}")
            
            # 返回空列表，保证函数返回类型一致
            return []
    
    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        获取单个用户信息
        
        参数:
            user_id (int): 用户 ID
        
        返回:
            Optional[Dict[str, Any]]: 用户信息字典，如果失败返回 None
        
        URL 构建示例:
            base_url = 'https://example.com/users'
            user_id = 1
            最终 URL: 'https://example.com/users/1'
        """
        try:
            # 构建完整的请求 URL
            response = self.session.get(f'{self.base_url}/{user_id}')
            response.raise_for_status()
            return response.json()
        
        except requests.RequestException as e:
            logger.error(f"获取用户 {user_id} 失败: {str(e)}")
            return None
    
    def update_user(self, user_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        更新用户信息
        
        参数:
            user_id (int): 用户 ID
            data (Dict[str, Any]): 要更新的数据
        
        返回:
            Optional[Dict[str, Any]]: 更新后的用户信息，如果失败返回 None
        
        PUT 请求说明:
            PUT 请求用于更新资源，通常需要提供完整的资源数据
            这里使用 json=data 自动设置 Content-Type: application/json
        """
        try:
            # 发送 PUT 请求，使用 json 参数传递数据
            response = self.session.put(f'{self.base_url}/{user_id}', json=data)
            response.raise_for_status()
            return response.json()
        
        except requests.RequestException as e:
            logger.error(f"更新用户 {user_id} 失败: {str(e)}")
            return None
    
    def create_user(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        创建新用户
        
        参数:
            data (Dict[str, Any]): 新用户的数据
        
        返回:
            Optional[Dict[str, Any]]: 创建的用户信息，如果失败返回 None
        
        POST 请求说明:
            POST 请求用于创建新资源
            服务器通常会返回新创建资源的完整信息，包括生成的 ID
        """
        try:
            # 发送 POST 请求
            response = self.session.post(self.base_url, json=data)
            response.raise_for_status()
            return response.json()
        
        except requests.RequestException as e:
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
            成功时通常返回 204 No Content 状态码
        """
        try:
            # 发送 DELETE 请求
            response = self.session.delete(f'{self.base_url}/{user_id}')
            response.raise_for_status()
            return True
        
        except requests.RequestException as e:
            logger.error(f"删除用户 {user_id} 失败: {str(e)}")
            return False
