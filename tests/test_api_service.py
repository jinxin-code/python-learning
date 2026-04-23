import unittest
from unittest.mock import Mock, patch
from app.services.api_service import ApiService

class TestApiService(unittest.TestCase):
    def setUp(self):
        """设置测试环境"""
        self.api_service = ApiService('https://jsonplaceholder.typicode.com/users')
    
    @patch('app.services.api_service.requests.Session.get')
    def test_get_users_success(self, mock_get):
        """测试成功获取用户列表"""
        # 模拟响应
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = [
            {'id': 1, 'name': 'John Doe'},
            {'id': 2, 'name': 'Jane Doe'}
        ]
        mock_get.return_value = mock_response
        
        # 调用方法
        users = self.api_service.get_users()
        
        # 验证结果
        self.assertEqual(len(users), 2)
        self.assertEqual(users[0]['name'], 'John Doe')
        self.assertEqual(users[1]['name'], 'Jane Doe')
    
    @patch('app.services.api_service.requests.Session.get')
    def test_get_users_failure(self, mock_get):
        """测试获取用户列表失败"""
        # 模拟异常
        mock_get.side_effect = Exception('Network error')
        
        # 调用方法
        users = self.api_service.get_users()
        
        # 验证结果
        self.assertEqual(users, [])
    
    @patch('app.services.api_service.requests.Session.get')
    def test_get_user_success(self, mock_get):
        """测试成功获取单个用户"""
        # 模拟响应
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
        # 模拟异常
        mock_get.side_effect = Exception('Network error')
        
        # 调用方法
        user = self.api_service.get_user(1)
        
        # 验证结果
        self.assertIsNone(user)
    
    @patch('app.services.api_service.requests.Session.put')
    def test_update_user_success(self, mock_put):
        """测试成功更新用户"""
        # 模拟响应
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
        # 模拟响应
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
        # 模拟响应
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_delete.return_value = mock_response
        
        # 调用方法
        success = self.api_service.delete_user(1)
        
        # 验证结果
        self.assertTrue(success)

if __name__ == '__main__':
    unittest.main()
