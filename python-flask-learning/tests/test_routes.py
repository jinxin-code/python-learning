"""
路由测试模块

本模块展示了如何使用 Flask 测试客户端进行集成测试。

学习要点：
- Flask 测试客户端的使用
- 模拟外部依赖（API 服务）
- 测试不同 HTTP 方法（GET, POST）
- 测试重定向和状态码
- CSRF 保护在测试中的处理
- 工厂模式下的路由测试
"""

# 导入 unittest 测试框架
import unittest

# 导入 mock 工具
from unittest.mock import patch, Mock

# 导入应用工厂函数
from app import create_app

# 导入 API 服务类，用于模拟
from app.services.api_service import ApiService


class TestRoutes(unittest.TestCase):
    """
    路由集成测试类
    
    使用 Flask 测试客户端模拟 HTTP 请求，测试路由的行为。
    
    测试流程：
    1. 创建测试应用实例
    2. 使用测试客户端发送请求
    3. 验证响应状态码和内容
    """
    
    def setUp(self):
        """设置测试环境"""
        # 创建测试环境的应用实例
        self.app = create_app('testing')
        
        # 禁用 CSRF 保护，便于测试
        # CSRF 保护在生产环境中应该启用
        self.app.config['WTF_CSRF_ENABLED'] = False
        
        # 获取测试客户端
        # 测试客户端可以模拟浏览器发送 HTTP 请求
        self.client = self.app.test_client()
    
    @patch.object(ApiService, 'get_users')
    def test_index_route(self, mock_get_users):
        """测试首页路由"""
        # 设置模拟返回值
        mock_get_users.return_value = [
            {'id': 1, 'name': 'John Doe', 'username': 'johndoe', 'email': 'john@example.com'}
        ]
        
        # 使用测试客户端发送 GET 请求
        response = self.client.get('/')
        
        # 验证响应状态码为 200（成功）
        self.assertEqual(response.status_code, 200)
    
    @patch.object(ApiService, 'get_users')
    def test_index_route_with_search(self, mock_get_users):
        """测试带搜索参数的首页路由"""
        mock_get_users.return_value = [
            {'id': 1, 'name': 'John Doe', 'username': 'johndoe', 'email': 'john@example.com'}
        ]
        
        # 发送带查询参数的 GET 请求
        response = self.client.get('/?search=John')
        
        # 验证响应状态码
        self.assertEqual(response.status_code, 200)
    
    @patch.object(ApiService, 'get_users')
    def test_index_route_with_filter(self, mock_get_users):
        """测试带筛选参数的首页路由"""
        mock_get_users.return_value = [
            {'id': 1, 'name': 'John Doe', 'username': 'johndoe', 'email': 'john@example.com'}
        ]
        
        # 发送带筛选参数的 GET 请求
        response = self.client.get('/?filter=username')
        
        # 验证响应状态码
        self.assertEqual(response.status_code, 200)
    
    @patch.object(ApiService, 'get_user')
    def test_user_detail_route(self, mock_get_user):
        """测试用户详情路由"""
        # 设置模拟返回值
        mock_get_user.return_value = {
            'id': 1, 'name': 'John Doe', 'username': 'johndoe', 'email': 'john@example.com'
        }
        
        # 发送 GET 请求到 /user/1
        response = self.client.get('/user/1')
        
        # 验证响应状态码
        self.assertEqual(response.status_code, 200)
    
    @patch.object(ApiService, 'get_user')
    def test_user_detail_not_found(self, mock_get_user):
        """测试用户不存在的情况"""
        # 设置模拟返回 None（用户不存在）
        mock_get_user.return_value = None
        
        # 发送 GET 请求
        response = self.client.get('/user/999')
        
        # 验证响应状态码为 302（重定向）
        # 用户不存在时应该重定向到首页
        self.assertEqual(response.status_code, 302)
    
    def test_add_user_get(self):
        """测试新增用户 GET 请求"""
        # 发送 GET 请求到 /add
        response = self.client.get('/add')
        
        # 验证响应状态码
        self.assertEqual(response.status_code, 200)
    
    @patch.object(ApiService, 'create_user')
    def test_add_user_post(self, mock_create_user):
        """测试新增用户 POST 请求"""
        # 设置模拟返回值
        mock_create_user.return_value = {'id': 11, 'name': 'New User'}
        
        # 发送 POST 请求，包含表单数据
        response = self.client.post('/add', data={
            'name': 'New User',
            'username': 'newuser',
            'email': 'new@example.com'
        })
        
        # 验证响应状态码为 302（重定向到首页）
        self.assertEqual(response.status_code, 302)
    
    @patch.object(ApiService, 'get_user')
    def test_edit_user_get(self, mock_get_user):
        """测试编辑用户 GET 请求"""
        mock_get_user.return_value = {
            'id': 1, 'name': 'John Doe', 'username': 'johndoe', 'email': 'john@example.com'
        }
        
        # 发送 GET 请求到 /edit/1
        response = self.client.get('/edit/1')
        
        # 验证响应状态码
        self.assertEqual(response.status_code, 200)
    
    @patch.object(ApiService, 'get_user')
    @patch.object(ApiService, 'update_user')
    def test_edit_user_post(self, mock_update_user, mock_get_user):
        """测试编辑用户 POST 请求"""
        mock_get_user.return_value = {
            'id': 1, 'name': 'John Doe', 'username': 'johndoe', 'email': 'john@example.com'
        }
        mock_update_user.return_value = {'id': 1, 'name': 'Updated'}
        
        # 发送 POST 请求，包含更新数据
        response = self.client.post('/edit/1', data={
            'name': 'Updated',
            'username': 'updateduser',
            'email': 'updated@example.com'
        })
        
        # 验证响应状态码为 302（重定向）
        self.assertEqual(response.status_code, 302)
    
    @patch.object(ApiService, 'delete_user')
    def test_delete_user(self, mock_delete_user):
        """测试删除用户"""
        # 设置模拟返回 True（删除成功）
        mock_delete_user.return_value = True
        
        # 发送 POST 请求到 /delete/1
        response = self.client.post('/delete/1')
        
        # 验证响应状态码为 302（重定向到首页）
        self.assertEqual(response.status_code, 302)


if __name__ == '__main__':
    # 运行测试
    unittest.main()
