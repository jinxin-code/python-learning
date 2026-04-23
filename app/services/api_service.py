import requests
import logging
from typing import List, Dict, Optional, Any

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ApiService:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        # 设置请求超时
        self.session.timeout = 10
    
    def get_users(self) -> List[Dict[str, Any]]:
        """
        获取所有用户
        返回值: 包含用户信息的列表
        """
        try:
            response = self.session.get(self.base_url)
            response.raise_for_status()  # 检查响应状态码
            return response.json()
        except Exception as e:
            logger.error(f"获取用户列表失败: {str(e)}")
            return []
    
    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        获取单个用户
        参数: user_id - 用户ID
        返回值: 包含用户信息的字典，如果失败返回None
        """
        try:
            response = self.session.get(f'{self.base_url}/{user_id}')
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"获取用户 {user_id} 失败: {str(e)}")
            return None
    
    def update_user(self, user_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        更新用户
        参数: user_id - 用户ID, data - 要更新的数据
        返回值: 更新后的用户信息，如果失败返回None
        """
        try:
            response = self.session.put(f'{self.base_url}/{user_id}', json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"更新用户 {user_id} 失败: {str(e)}")
            return None
    
    def create_user(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        创建用户
        参数: data - 新用户的数据
        返回值: 创建的用户信息，如果失败返回None
        """
        try:
            response = self.session.post(self.base_url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"创建用户失败: {str(e)}")
            return None
    
    def delete_user(self, user_id: int) -> bool:
        """
        删除用户
        参数: user_id - 用户ID
        返回值: 是否删除成功
        """
        try:
            response = self.session.delete(f'{self.base_url}/{user_id}')
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            logger.error(f"删除用户 {user_id} 失败: {str(e)}")
            return False
