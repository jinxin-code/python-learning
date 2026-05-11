"""
用户模型模块

本模块定义了 User 数据模型，展示了 Python 类的定义和数据转换方法。

学习要点：
- Python 类的定义和初始化方法
- 类方法的使用（@classmethod）
- 类型提示的使用
- 数据转换模式（dict <-> object）
- Optional 类型的使用
"""

# 导入类型提示模块
from typing import Optional, Dict, Any


class User:
    """
    用户数据模型
    
    用于封装用户信息，提供数据转换方法。
    
    属性说明：
    - id: 用户唯一标识
    - name: 用户姓名
    - username: 用户名
    - email: 邮箱地址
    - address: 地址信息（可选）
    - phone: 电话号码（可选）
    - website: 个人网站（可选）
    - company: 公司信息（可选）
    """
    
    def __init__(self, id: int, name: str, username: str, email: str, 
                 address: Optional[Dict[str, Any]] = None, 
                 phone: Optional[str] = None, 
                 website: Optional[str] = None, 
                 company: Optional[Dict[str, Any]] = None):
        """
        初始化用户对象
        
        参数:
            id (int): 用户 ID
            name (str): 用户姓名
            username (str): 用户名
            email (str): 邮箱地址
            address (Optional[Dict]): 地址字典，默认 None
            phone (Optional[str]): 电话号码，默认 None
            website (Optional[str]): 个人网站，默认 None
            company (Optional[Dict]): 公司信息字典，默认 None
        
        Optional 类型说明：
            Optional[X] 表示该参数可以是 X 类型或者 None
            等同于 Union[X, None]
        """
        self.id = id
        self.name = name
        self.username = username
        self.email = email
        self.address = address
        self.phone = phone
        self.website = website
        self.company = company
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        """
        从字典创建 User 对象（工厂方法）
        
        参数:
            data (Dict[str, Any]): 包含用户信息的字典
        
        返回:
            User: 创建的 User 对象
        
        使用场景：
            当从 API 获取 JSON 数据后，需要将字典转换为对象
            示例:
                user_data = {'id': 1, 'name': 'John', 'username': 'john', 'email': 'john@example.com'}
                user = User.from_dict(user_data)
        
        getattr vs get:
            data.get('key', default) 如果 key 不存在返回 default
            这里使用 get 方法可以处理 API 返回数据不完整的情况
        """
        return cls(
            id=data.get('id', 0),           # 如果 'id' 不存在，默认值为 0
            name=data.get('name', ''),       # 如果 'name' 不存在，默认值为空字符串
            username=data.get('username', ''),
            email=data.get('email', ''),
            address=data.get('address'),     # 可选字段，不存在返回 None
            phone=data.get('phone'),
            website=data.get('website'),
            company=data.get('company')
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        将 User 对象转换为字典
        
        返回:
            Dict[str, Any]: 包含用户信息的字典
        
        使用场景：
            当需要将用户对象发送到 API 或保存到数据库时
            示例:
                user = User(id=1, name='John', username='john', email='john@example.com')
                user_dict = user.to_dict()
                # 结果: {'id': 1, 'name': 'John', 'username': 'john', 'email': 'john@example.com', ...}
        """
        return {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'email': self.email,
            'address': self.address,
            'phone': self.phone,
            'website': self.website,
            'company': self.company
        }
    
    def update(self, data: Dict[str, Any]) -> None:
        """
        更新用户信息
        
        参数:
            data (Dict[str, Any]): 包含更新信息的字典
        
        使用场景：
            当用户提交编辑表单后，只更新提供的字段
            示例:
                user.update({'name': 'New Name', 'email': 'new@example.com'})
        
        注意事项：
            只更新字典中存在的键，不会删除未提及的字段
        """
        if 'name' in data:
            self.name = data['name']
        if 'username' in data:
            self.username = data['username']
        if 'email' in data:
            self.email = data['email']
        if 'address' in data:
            self.address = data['address']
        if 'phone' in data:
            self.phone = data['phone']
        if 'website' in data:
            self.website = data['website']
        if 'company' in data:
            self.company = data['company']
