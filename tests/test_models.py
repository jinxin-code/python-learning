import unittest
from app.models.user import User

class TestUserModel(unittest.TestCase):
    def test_user_from_dict(self):
        """测试从字典创建用户对象"""
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
        
        user = User.from_dict(user_data)
        
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
        user = User(
            id=1,
            name='John Doe',
            username='johndoe',
            email='john@example.com'
        )
        
        user_dict = user.to_dict()
        
        self.assertEqual(user_dict['id'], 1)
        self.assertEqual(user_dict['name'], 'John Doe')
        self.assertEqual(user_dict['username'], 'johndoe')
        self.assertEqual(user_dict['email'], 'john@example.com')
        self.assertIsNone(user_dict['address'])
        self.assertIsNone(user_dict['phone'])
        self.assertIsNone(user_dict['website'])
        self.assertIsNone(user_dict['company'])
    
    def test_user_update(self):
        """测试更新用户信息"""
        user = User(
            id=1,
            name='John Doe',
            username='johndoe',
            email='john@example.com'
        )
        
        update_data = {
            'name': 'Jane Doe',
            'username': 'janedoe',
            'email': 'jane@example.com'
        }
        
        user.update(update_data)
        
        self.assertEqual(user.name, 'Jane Doe')
        self.assertEqual(user.username, 'janedoe')
        self.assertEqual(user.email, 'jane@example.com')

if __name__ == '__main__':
    unittest.main()
