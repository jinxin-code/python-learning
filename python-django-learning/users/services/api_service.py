"""
API 服务模块

本模块封装了与外部 API 的交互逻辑。

学习要点：
- HTTP 请求的封装
- 异常处理
- 日志记录
- 服务层的设计模式
"""

import os
import requests
import logging
from typing import List, Dict, Optional, Any

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ApiService:
    """
    API 服务类，封装了所有与用户相关的 API 操作
    
    使用 requests.Session 来保持连接复用，提高性能。
    """
    
    def __init__(self, base_url: str = None):
        """
        初始化 API 服务
        
        参数:
            base_url (str): API 的基础 URL，默认为环境变量中的值
        """
        # 优先使用传入的 base_url，否则从环境变量获取
        self.base_url = base_url or os.environ.get('API_BASE_URL', 'https://jsonplaceholder.typicode.com/users')
        
        # 创建 Session 对象，保持连接复用
        self.session = requests.Session()
        self.session.timeout = 10  # 设置超时时间
    
    def get_users(self) -> List[Dict[str, Any]]:
        """
        获取所有用户列表
        
        返回:
            List[Dict[str, Any]]: 用户列表，如果请求失败返回空列表
        """
        try:
            response = self.session.get(self.base_url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"获取用户列表失败: {str(e)}")
            return []
    
    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        获取单个用户信息
        
        参数:
            user_id (int): 用户 ID
        
        返回:
            Optional[Dict[str, Any]]: 用户信息字典，如果失败返回 None
        """
        try:
            response = self.session.get(f'{self.base_url}/{user_id}')
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"获取用户 {user_id} 失败: {str(e)}")
            return None
    
    def create_user(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        创建新用户
        
        参数:
            data (Dict[str, Any]): 新用户的数据
        
        返回:
            Optional[Dict[str, Any]]: 创建的用户信息，如果失败返回 None
        """
        try:
            response = self.session.post(self.base_url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"创建用户失败: {str(e)}")
            return None
    
    def update_user(self, user_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        更新用户信息
        
        参数:
            user_id (int): 用户 ID
            data (Dict[str, Any]): 要更新的数据
        
        返回:
            Optional[Dict[str, Any]]: 更新后的用户信息，如果失败返回 None
        """
        try:
            response = self.session.put(f'{self.base_url}/{user_id}', json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"更新用户 {user_id} 失败: {str(e)}")
            return None
    
    def delete_user(self, user_id: int) -> bool:
        """
        删除用户
        
        参数:
            user_id (int): 用户 ID
        
        返回:
            bool: 删除是否成功
        """
        try:
            response = self.session.delete(f'{self.base_url}/{user_id}')
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            logger.error(f"删除用户 {user_id} 失败: {str(e)}")
            return False
    
    def sync_users(self) -> int:
        """
        同步外部 API 用户数据到本地数据库
        
        返回:
            int: 成功同步的用户数量
        """
        from users.models import User
        
        users_data = self.get_users()
        count = 0
        
        for user_data in users_data:
            # 检查用户是否已存在
            try:
                user = User.objects.get(username=user_data.get('username'))
                # 更新现有用户
                user.name = user_data.get('name', '')
                user.email = user_data.get('email', '')
                user.address = user_data.get('address')
                user.phone = user_data.get('phone')
                user.website = user_data.get('website')
                user.company = user_data.get('company')
                user.save()
            except User.DoesNotExist:
                # 创建新用户
                User.objects.create(
                    username=user_data.get('username', ''),
                    name=user_data.get('name', ''),
                    email=user_data.get('email', ''),
                    address=user_data.get('address'),
                    phone=user_data.get('phone'),
                    website=user_data.get('website'),
                    company=user_data.get('company')
                )
            count += 1
        
        return count
