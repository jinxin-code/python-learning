"""
FastAPI 主应用测试

本模块包含对 FastAPI 应用的集成测试。

学习要点：
- FastAPI 测试客户端的使用
- 测试用例的编写
- HTTP 状态码和响应验证
"""

import pytest
from fastapi.testclient import TestClient

# 导入主应用
from main import app

# 创建测试客户端
client = TestClient(app)


def test_get_users():
    """
    测试获取用户列表
    
    验证：
    - 响应状态码为 200
    - 响应为列表格式
    """
    response = client.get("/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_user():
    """
    测试获取单个用户
    
    验证：
    - 响应状态码为 200
    - 返回用户对象包含预期字段
    """
    # 获取第一个用户
    response = client.get("/")
    users = response.json()
    
    if users:
        user_id = users[0]["id"]
        response = client.get(f"/users/{user_id}")
        assert response.status_code == 200
        user = response.json()
        assert "id" in user
        assert "name" in user
        assert "username" in user
        assert "email" in user


def test_get_user_not_found():
    """
    测试获取不存在的用户
    
    验证：
    - 响应状态码为 404
    - 返回错误信息
    """
    response = client.get("/users/99999")
    assert response.status_code == 404
    assert "用户不存在" in response.json()["detail"]


def test_create_user():
    """
    测试创建新用户
    
    验证：
    - 响应状态码为 201
    - 返回创建的用户对象
    """
    new_user = {
        "name": "Test User",
        "username": "testuser",
        "email": "test@example.com"
    }
    
    response = client.post("/users/", json=new_user)
    assert response.status_code == 201
    
    created_user = response.json()
    assert created_user["name"] == new_user["name"]
    assert created_user["username"] == new_user["username"]
    assert created_user["email"] == new_user["email"]


def test_update_user():
    """
    测试更新用户信息
    
    验证：
    - 响应状态码为 200
    - 返回更新后的用户对象
    """
    # 先获取一个用户
    response = client.get("/")
    users = response.json()
    
    if users:
        user_id = users[0]["id"]
        update_data = {
            "name": "Updated Name"
        }
        
        response = client.put(f"/users/{user_id}", json=update_data)
        assert response.status_code == 200
        
        updated_user = response.json()
        assert updated_user["name"] == update_data["name"]


def test_update_user_not_found():
    """
    测试更新不存在的用户
    
    验证：
    - 响应状态码为 404
    """
    update_data = {"name": "Test"}
    response = client.put("/users/99999", json=update_data)
    assert response.status_code == 404


def test_delete_user():
    """
    测试删除用户
    
    验证：
    - 响应状态码为 204
    - 用户被删除后无法再获取
    """
    # 先创建一个用户
    new_user = {
        "name": "To Delete",
        "username": "todelete",
        "email": "delete@example.com"
    }
    
    create_response = client.post("/users/", json=new_user)
    user_id = create_response.json()["id"]
    
    # 删除用户
    delete_response = client.delete(f"/users/{user_id}")
    assert delete_response.status_code == 204


def test_delete_user_not_found():
    """
    测试删除不存在的用户
    
    验证：
    - 响应状态码为 404
    """
    response = client.delete("/users/99999")
    assert response.status_code == 404


def test_search_users():
    """
    测试搜索用户功能
    
    验证：
    - 搜索关键词能正确过滤结果
    """
    response = client.get("/?search=Leanne")
    assert response.status_code == 200
    results = response.json()
    assert isinstance(results, list)


def test_filter_users():
    """
    测试筛选用户功能
    
    验证：
    - 按用户名排序
    - 按邮箱排序
    """
    # 按用户名排序
    response = client.get("/?filter_by=username")
    assert response.status_code == 200
    
    # 按邮箱排序
    response = client.get("/?filter_by=email")
    assert response.status_code == 200
