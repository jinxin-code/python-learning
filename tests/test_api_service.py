"""
API 服务测试模块

本模块展示了如何使用 unittest 和 mock 进行单元测试。

学习要点：
- unittest 框架的使用
- unittest.mock 的使用（Mock, patch）
- 测试用例的编写方法
- 模拟外部 API 调用
- 测试成功和失败场景
"""

# 导入 unittest 测试框架
import unittest

# 导入 requests 库，用于异常类型
import requests

# 导入 mock 相关工具
from unittest.mock import Mock, patch

# 导入要测试的 API 服务类
from app.services.api_service import ApiService


class TestApiService(unittest.TestCase):
    """
    API 服务测试类
    
    测试类继承自 unittest.TestCase，每个测试方法以 'test_' 开头。
    
    setUp 方法会在每个测试方法执行前运行，用于设置测试环境。
    """
    
    def setUp(self):
        """设置测试环境"""
        # 创建 API 服务实例
        self.api_service = ApiService('https://jsonplaceholder.typicode.com/users')
    
    @patch('app.services.api_service.requests.Session.get')
    def test_get_users_success(self, mock_get):
        """测试成功获取用户列表"""
        # 步骤1: 创建模拟响应对象
        mock_response = Mock()
        
        # 步骤2: 设置模拟响应的行为
        # raise_for_status 方法不抛出异常（模拟成功响应）
        mock_response.raise_for_status = Mock()
        
        # json() 方法返回模拟的用户数据
        mock_response.json.return_value = [
            {'id': 1, 'name': 'John Doe'},
            {'id': 2, 'name': 'Jane Doe'}
        ]
        
        # 步骤3: 将模拟响应绑定到模拟的 get 方法
        mock_get.return_value = mock_response
        
        # 步骤4: 调用被测试的方法
        users = self.api_service.get_users()
        
        # 步骤5: 验证结果
        # assertEqual 用于断言两个值相等
        self.assertEqual(len(users), 2)
        self.assertEqual(users[0]['name'], 'John Doe')
        self.assertEqual(users[1]['name'], 'Jane Doe')
    
    @patch('app.services.api_service.requests.Session.get')
    def test_get_users_failure(self, mock_get):
        """测试获取用户列表失败"""
        # 设置模拟的异常
        mock_get.side_effect = requests.RequestException('Network error')
        
        # 调用方法
        users = self.api_service.get_users()
        
        # 验证返回空列表
        self.assertEqual(users, [])
    
    @patch('app.services.api_service.requests.Session.get')
    def test_get_user_success(self, mock_get):
        """测试成功获取单个用户"""
        # 创建模拟响应
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = {'id': 1, 'name': 'John Doe'}
        mock_get.return_value = mock_response
        
        # 调用方法
        user = self.api_service.get_user(1)
        
        # 验证结果
        self.assertEqual(user['id'], 1)
        self.assertEqual(user['name'], 'John Doe')
    
    @patch('app.services.api_service.requests.Session.get')
    def test_get_user_failure(self, mock_get):
        """测试获取单个用户失败"""
        # 设置模拟异常
        mock_get.side_effect = requests.RequestException('Network error')
        
        # 调用方法
        user = self.api_service.get_user(1)
        
        # 验证返回 None
        self.assertIsNone(user)
    
    @patch('app.services.api_service.requests.Session.put')
    def test_update_user_success(self, mock_put):
        """测试成功更新用户"""
        # 创建模拟响应
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = {'id': 1, 'name': 'Updated Name'}
        mock_put.return_value = mock_response
        
        # 调用方法
        updated_user = self.api_service.update_user(1, {'name': 'Updated Name'})
        
        # 验证结果
        self.assertEqual(updated_user['name'], 'Updated Name')
    
    @patch('app.services.api_service.requests.Session.post')
    def test_create_user_success(self, mock_post):
        """测试成功创建用户"""
        # 创建模拟响应
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = {'id': 11, 'name': 'New User'}
        mock_post.return_value = mock_response
        
        # 调用方法
        new_user = self.api_service.create_user({'name': 'New User'})
        
        # 验证结果
        self.assertEqual(new_user['id'], 11)
        self.assertEqual(new_user['name'], 'New User')
    
    @patch('app.services.api_service.requests.Session.delete')
    def test_delete_user_success(self, mock_delete):
        """测试成功删除用户"""
        # 创建模拟响应
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_delete.return_value = mock_response
        
        # 调用方法
        success = self.api_service.delete_user(1)
        
        # 验证结果
        self.assertTrue(success)
    
    @patch('app.services.api_service.requests.Session.put')
    def test_update_user_failure(self, mock_put):
        """测试更新用户失败"""
        # 设置模拟异常
        mock_put.side_effect = requests.RequestException('Update failed')
        
        # 调用方法
        result = self.api_service.update_user(1, {'name': 'Test'})
        
        # 验证返回 None
        self.assertIsNone(result)
    
    @patch('app.services.api_service.requests.Session.post')
    def test_create_user_failure(self, mock_post):
        """测试创建用户失败"""
        # 设置模拟异常
        mock_post.side_effect = requests.RequestException('Create failed')
        
        # 调用方法
        result = self.api_service.create_user({'name': 'Test'})
        
        # 验证返回 None
        self.assertIsNone(result)
    
    @patch('app.services.api_service.requests.Session.delete')
    def test_delete_user_failure(self, mock_delete):
        """测试删除用户失败"""
        # 设置模拟异常
        mock_delete.side_effect = requests.RequestException('Delete failed')
        
        # 调用方法
        result = self.api_service.delete_user(1)
        
        # 验证返回 False
        self.assertFalse(result)


if __name__ == '__main__':
    # 运行测试
    unittest.main()
