"""
用户应用 URL 配置

本文件定义了用户应用的 URL 路由映射。

学习要点：
- URL 模式的定义
- 命名空间的使用
- 视图函数和类视图的映射
"""

from django.urls import path
from . import views

# URL 命名空间
app_name = 'users'

urlpatterns = [
    # 用户列表页（首页）
    path('', views.UserListView.as_view(), name='user_list'),
    
    # 用户列表页（备用路径）
    path('users/', views.UserListView.as_view(), name='user_list_alt'),
    
    # 用户详情页
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
    
    # 创建用户页
    path('users/add/', views.UserCreateView.as_view(), name='user_add'),
    
    # 编辑用户页
    path('users/<int:pk>/edit/', views.UserUpdateView.as_view(), name='user_edit'),
    
    # 删除用户页
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
    
    # 同步用户
    path('users/sync/', views.SyncUsersView.as_view(), name='user_sync'),
]
