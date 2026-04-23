from typing import Optional, Dict, Any

class User:
    def __init__(self, id: int, name: str, username: str, email: str, 
                 address: Optional[Dict[str, Any]] = None, 
                 phone: Optional[str] = None, 
                 website: Optional[str] = None, 
                 company: Optional[Dict[str, Any]] = None):
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
        从字典创建 User 对象
        参数: data - 包含用户信息的字典
        返回值: User 对象
        """
        return cls(
            id=data.get('id', 0),
            name=data.get('name', ''),
            username=data.get('username', ''),
            email=data.get('email', ''),
            address=data.get('address'),
            phone=data.get('phone'),
            website=data.get('website'),
            company=data.get('company')
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        将 User 对象转换为字典
        返回值: 包含用户信息的字典
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
        参数: data - 包含更新信息的字典
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
