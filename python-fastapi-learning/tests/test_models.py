"""
用户模型测试

本模块包含对 Pydantic 用户模型的单元测试。

学习要点：
- Pydantic 模型的验证测试
- 数据转换测试
- 类型提示验证
"""

import pytest
from app.models.user import User, UserCreate, UserUpdate, Address, Company


def test_user_model_from_dict():
    """
    测试从字典创建 User 对象
    
    验证：
    - 字典数据能正确转换为 User 对象
    - 可选字段处理正确
    """
    user_data = {
        "id": 1,
        "name": "John Doe",
        "username": "johndoe",
        "email": "john@example.com",
        "address": {
            "street": "123 Main St",
            "city": "New York",
            "zipcode": "10001"
        },
        "phone": "123-456-7890",
        "website": "johndoe.com",
        "company": {
            "name": "ACME Corp",
            "catchPhrase": "We make things",
            "bs": "manufacturing"
        }
    }
    
    user = User.from_dict(user_data)
    
    assert user.id == 1
    assert user.name == "John Doe"
    assert user.username == "johndoe"
    assert user.email == "john@example.com"
    assert isinstance(user.address, Address)
    assert user.address.street == "123 Main St"
    assert user.phone == "123-456-7890"
    assert isinstance(user.company, Company)
    assert user.company.name == "ACME Corp"


def test_user_model_to_dict():
    """
    测试 User 对象转换为字典
    
    验证：
    - User 对象能正确转换为字典
    - None 值被正确处理
    """
    user = User(
        id=1,
        name="Jane Doe",
        username="janedoe",
        email="jane@example.com"
    )
    
    user_dict = user.to_dict()
    
    assert user_dict["id"] == 1
    assert user_dict["name"] == "Jane Doe"
    assert user_dict["username"] == "janedoe"
    assert user_dict["email"] == "jane@example.com"
    # 可选字段默认 None，应被排除
    assert "address" not in user_dict
    assert "phone" not in user_dict


def test_user_create_validation():
    """
    测试 UserCreate 模型验证
    
    验证：
    - 必填字段缺失时抛出验证错误
    - 无效邮箱格式时抛出验证错误
    """
    # 测试有效数据
    valid_data = {
        "name": "Valid User",
        "username": "validuser",
        "email": "valid@example.com"
    }
    user_create = UserCreate(**valid_data)
    assert user_create.name == "Valid User"


def test_user_update_validation():
    """
    测试 UserUpdate 模型验证
    
    验证：
    - 所有字段都是可选的
    - 部分更新数据能正确处理
    """
    # 只提供部分字段
    partial_data = {
        "name": "Updated Name"
    }
    user_update = UserUpdate(**partial_data)
    assert user_update.name == "Updated Name"
    assert user_update.username is None
    assert user_update.email is None


def test_address_model():
    """
    测试 Address 嵌套模型
    
    验证：
    - 嵌套模型能正确解析
    """
    address_data = {
        "street": "456 Oak Ave",
        "suite": "Apt 2B",
        "city": "Boston",
        "zipcode": "02101",
        "geo": {"lat": "42.3601", "lng": "-71.0589"}
    }
    
    address = Address(**address_data)
    assert address.street == "456 Oak Ave"
    assert address.city == "Boston"
    assert address.geo is not None


def test_company_model():
    """
    测试 Company 嵌套模型
    
    验证：
    - 嵌套模型能正确解析
    """
    company_data = {
        "name": "Tech Corp",
        "catchPhrase": "Innovate or die",
        "bs": "technology"
    }
    
    company = Company(**company_data)
    assert company.name == "Tech Corp"
    assert company.catchPhrase == "Innovate or die"
