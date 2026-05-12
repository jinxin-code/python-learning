"""
用户模型测试模块

本模块展示了如何测试 Python 类的方法。

学习要点：
- 测试类的初始化方法
- 测试类方法（@classmethod）
- 测试实例方法
- unittest 断言方法的使用
"""

# 导入 unittest 测试框架
import unittest

# 导入要测试的 User 模型类
from app.models.user import User


class TestUserModel(unittest.TestCase):
    """
    User 模型测试类
    
    测试 User 类的三个核心方法：
    - from_dict: 从字典创建对象
    - to_dict: 将对象转换为字典
    - update: 更新对象属性
    """
    
    def test_user_from_dict(self):
        """测试从字典创建用户对象"""
        # 准备测试数据
        user_data = {
            'id': 1,
            'name': 'John Doe',
            'username': 'johndoe',
            'email': 'john@example.com',
            'address': {'street': '123 Main St', 'city': 'New York'},
            'phone': '123-456-7890',
            'website': 'johndoe.com',
            'company': {'name': 'Acme Inc'}
        }
        
        # 调用类方法创建用户对象
        user = User.from_dict(user_data)
        
        # 验证对象属性是否正确设置
        self.assertEqual(user.id, 1)
        self.assertEqual(user.name, 'John Doe')
        self.assertEqual(user.username, 'johndoe')
        self.assertEqual(user.email, 'john@example.com')
        self.assertEqual(user.address, {'street': '123 Main St', 'city': 'New York'})
        self.assertEqual(user.phone, '123-456-7890')
        self.assertEqual(user.website, 'johndoe.com')
        self.assertEqual(user.company, {'name': 'Acme Inc'})
    
    def test_user_to_dict(self):
        """测试用户对象转换为字典"""
        # 创建用户对象（只提供必填字段）
        user = User(
            id=1,
            name='John Doe',
            username='johndoe',
            email='john@example.com'
            # 可选字段不提供，默认为 None
        )
        
        # 调用实例方法转换为字典
        user_dict = user.to_dict()
        
        # 验证字典内容
        self.assertEqual(user_dict['id'], 1)
        self.assertEqual(user_dict['name'], 'John Doe')
        self.assertEqual(user_dict['username'], 'johndoe')
        self.assertEqual(user_dict['email'], 'john@example.com')
        # 验证可选字段为 None
        self.assertIsNone(user_dict['address'])
        self.assertIsNone(user_dict['phone'])
        self.assertIsNone(user_dict['website'])
        self.assertIsNone(user_dict['company'])
    
    def test_user_update(self):
        """测试更新用户信息"""
        # 创建初始用户对象
        user = User(
            id=1,
            name='John Doe',
            username='johndoe',
            email='john@example.com'
        )
        
        # 准备更新数据（只更新部分字段）
        update_data = {
            'name': 'Jane Doe',
            'username': 'janedoe',
            'email': 'jane@example.com'
        }
        
        # 调用实例方法更新用户信息
        user.update(update_data)
        
        # 验证更新后的属性
        self.assertEqual(user.name, 'Jane Doe')
        self.assertEqual(user.username, 'janedoe')
        self.assertEqual(user.email, 'jane@example.com')


if __name__ == '__main__':
    # 运行测试
    unittest.main()
