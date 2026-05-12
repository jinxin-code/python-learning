"""
用户模型模块

本模块定义了 User 数据模型，展示了 FastAPI 中使用 Pydantic 进行数据验证的最佳实践。

学习要点：
- Pydantic 模型的定义和使用
- 字段验证和类型提示
- 可选字段的定义
- 模型配置选项
- 数据转换方法（dict <-> object）
"""

# 导入 Pydantic 模型基类和字段类型
# BaseModel: Pydantic 模型的基类
# Field: 用于定义字段的验证规则和元数据
# Optional: 表示字段可以是指定类型或 None
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class Address(BaseModel):
    """
    地址信息模型
    
    Pydantic 嵌套模型示例：用于表示复杂的嵌套数据结构
    
    属性说明：
    - street: 街道
    - suite: 套房号
    - city: 城市
    - zipcode: 邮政编码
    - geo: 地理坐标（嵌套字典）
    """
    street: Optional[str] = None
    suite: Optional[str] = None
    city: Optional[str] = None
    zipcode: Optional[str] = None
    geo: Optional[Dict[str, Any]] = None


class Company(BaseModel):
    """
    公司信息模型
    
    属性说明：
    - name: 公司名称
    - catchPhrase: 公司口号
    - bs: 业务描述
    """
    name: Optional[str] = None
    catchPhrase: Optional[str] = None
    bs: Optional[str] = None


class User(BaseModel):
    """
    用户数据模型
    
    使用 Pydantic BaseModel 定义，自动提供数据验证、序列化和文档功能。
    
    属性说明：
    - id: 用户唯一标识（整数）
    - name: 用户姓名（字符串）
    - username: 用户名（字符串）
    - email: 邮箱地址（字符串）
    - address: 地址信息（可选，嵌套模型）
    - phone: 电话号码（可选，字符串）
    - website: 个人网站（可选，字符串）
    - company: 公司信息（可选，嵌套模型）
    
    模型配置：
    - from_attributes: 允许从 ORM 对象创建模型实例
    """
    
    # Field 函数用于添加字段验证规则和元数据
    # ge=0 表示值必须大于等于 0
    # description 用于自动生成 API 文档
    id: int = Field(ge=0, description="用户唯一标识")
    
    # ... 表示必填字段（没有默认值）
    name: str = Field(..., description="用户姓名")
    username: str = Field(..., description="用户名")
    email: str = Field(..., description="邮箱地址")
    
    # Optional 字段，默认值为 None
    address: Optional[Address] = Field(None, description="地址信息")
    phone: Optional[str] = Field(None, description="电话号码")
    website: Optional[str] = Field(None, description="个人网站")
    company: Optional[Company] = Field(None, description="公司信息")
    
    # 模型配置类
    model_config = {
        # 允许从 ORM 对象创建模型（如 SQLAlchemy 模型）
        "from_attributes": True,
        # 允许额外的字段（用于向后兼容）
        "extra": "allow"
    }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        """
        从字典创建 User 对象（工厂方法）
        
        参数:
            data (Dict[str, Any]): 包含用户信息的字典
        
        返回:
            User: 创建的 User 对象
        
        使用场景：
            当从 API 获取 JSON 数据后，需要将字典转换为 Pydantic 模型
            示例:
                user_data = {'id': 1, 'name': 'John', 'username': 'john', 'email': 'john@example.com'}
                user = User.from_dict(user_data)
        """
        # 处理嵌套的 address 字段
        if 'address' in data and data['address']:
            data['address'] = Address(**data['address'])
        # 处理嵌套的 company 字段
        if 'company' in data and data['company']:
            data['company'] = Company(**data['company'])
        
        # 使用 ** 解包字典创建模型实例
        return cls(**data)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        将 User 对象转换为字典
        
        返回:
            Dict[str, Any]: 包含用户信息的字典
        
        使用场景：
            当需要将用户对象发送到 API 或保存到数据库时
        """
        # model_dump() 是 Pydantic v2 的方法，替代旧版的 dict() 方法
        return self.model_dump(exclude_none=True)


class UserCreate(BaseModel):
    """
    创建用户请求模型
    
    用于验证创建用户时的输入数据。
    注意：id 字段由服务器生成，因此不需要在创建时提供。
    
    属性说明：
    - name: 用户姓名（必填）
    - username: 用户名（必填）
    - email: 邮箱地址（必填）
    """
    name: str = Field(..., description="用户姓名")
    username: str = Field(..., description="用户名")
    email: str = Field(..., description="邮箱地址")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "John Doe",
                "username": "johndoe",
                "email": "john@example.com"
            }
        }
    }


class UserUpdate(BaseModel):
    """
    更新用户请求模型
    
    用于验证更新用户时的输入数据。
    所有字段都是可选的，只更新提供的字段。
    
    属性说明：
    - name: 用户姓名（可选）
    - username: 用户名（可选）
    - email: 邮箱地址（可选）
    """
    name: Optional[str] = Field(None, description="用户姓名")
    username: Optional[str] = Field(None, description="用户名")
    email: Optional[str] = Field(None, description="邮箱地址")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Jane Doe",
                "email": "jane@example.com"
            }
        }
    }
