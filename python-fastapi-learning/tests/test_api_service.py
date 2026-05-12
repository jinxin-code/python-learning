"""
API 服务测试

本模块包含对 ApiService 的单元测试。

学习要点：
- 服务层的单元测试
- HTTP 请求的模拟
- 异常处理测试
"""

import pytest
from unittest.mock import Mock, patch
from app.services.api_service import ApiService


def test_get_users_success():
    """
    测试获取用户列表成功
    
    验证：
    - 成功返回用户列表
    """
    with patch('httpx.Client') as mock_client:
        # 设置模拟返回值
        mock_response = Mock()
        mock_response.json.return_value = [
            {"id": 1, "name": "John", "username": "john", "email": "john@example.com"}
        ]
        mock_response.raise_for_status.return_value = None
        
        mock_client.return_value.__enter__.return_value.get.return_value = mock_response
        
        # 创建服务并调用
        service = ApiService("https://api.example.com")
        users = service.get_users()
        
        # 验证结果
        assert len(users) == 1
        assert users[0]["name"] == "John"


def test_get_users_failure():
    """
    测试获取用户列表失败
    
    验证：
    - 请求失败时返回空列表
    """
    with patch('httpx.Client') as mock_client:
        # 设置模拟异常
        mock_client.return_value.__enter__.return_value.get.side_effect = Exception("Connection error")
        
        # 创建服务并调用
        service = ApiService("https://api.example.com")
        users = service.get_users()
        
        # 验证结果
        assert users == []


def test_get_user_success():
    """
    测试获取单个用户成功
    
    验证：
    - 成功返回用户信息
    """
    with patch('httpx.Client') as mock_client:
        mock_response = Mock()
        mock_response.json.return_value = {
            "id": 1, "name": "John", "username": "john", "email": "john@example.com"
        }
        mock_response.raise_for_status.return_value = None
        
        mock_client.return_value.__enter__.return_value.get.return_value = mock_response
        
        service = ApiService("https://api.example.com")
        user = service.get_user(1)
        
        assert user["id"] == 1
        assert user["name"] == "John"


def test_get_user_failure():
    """
    测试获取单个用户失败
    
    验证：
    - 请求失败时返回 None
    """
    with patch('httpx.Client') as mock_client:
        mock_client.return_value.__enter__.return_value.get.side_effect = Exception("Not found")
        
        service = ApiService("https://api.example.com")
        user = service.get_user(999)
        
        assert user is None


def test_create_user():
    """
    测试创建用户
    
    验证：
    - 成功创建用户并返回用户信息
    """
    with patch('httpx.Client') as mock_client:
        mock_response = Mock()
        mock_response.json.return_value = {
            "id": 10, "name": "New User", "username": "newuser", "email": "new@example.com"
        }
        mock_response.raise_for_status.return_value = None
        
        mock_client.return_value.__enter__.return_value.post.return_value = mock_response
        
        service = ApiService("https://api.example.com")
        new_user = service.create_user({
            "name": "New User",
            "username": "newuser",
            "email": "new@example.com"
        })
        
        assert new_user["id"] == 10
        assert new_user["username"] == "newuser"


def test_update_user():
    """
    测试更新用户
    
    验证：
    - 成功更新用户信息
    """
    with patch('httpx.Client') as mock_client:
        mock_response = Mock()
        mock_response.json.return_value = {
            "id": 1, "name": "Updated", "username": "updated", "email": "updated@example.com"
        }
        mock_response.raise_for_status.return_value = None
        
        mock_client.return_value.__enter__.return_value.put.return_value = mock_response
        
        service = ApiService("https://api.example.com")
        updated_user = service.update_user(1, {"name": "Updated"})
        
        assert updated_user["name"] == "Updated"


def test_delete_user():
    """
    测试删除用户
    
    验证：
    - 成功删除时返回 True
    - 删除失败时返回 False
    """
    # 测试成功删除
    with patch('httpx.Client') as mock_client:
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        
        mock_client.return_value.__enter__.return_value.delete.return_value = mock_response
        
        service = ApiService("https://api.example.com")
        result = service.delete_user(1)
        
        assert result is True
    
    # 测试删除失败
    with patch('httpx.Client') as mock_client:
        mock_client.return_value.__enter__.return_value.delete.side_effect = Exception("Delete failed")
        
        service = ApiService("https://api.example.com")
        result = service.delete_user(999)
        
        assert result is False


def test_api_service_initialization():
    """
    测试 ApiService 初始化
    
    验证：
    - 基础 URL 被正确设置
    """
    service = ApiService("https://custom-api.com")
    assert service.base_url == "https://custom-api.com"
