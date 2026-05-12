"""
视图模块

本模块定义了用户管理相关的视图函数。

学习要点：
- Django 视图函数的定义
- 基于类的视图（CBV）
- 模板渲染
- 表单处理
- 重定向和消息闪现
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.db.models import Q

from .models import User
from .forms import UserForm
from .services.api_service import ApiService


class UserListView(ListView):
    """
    用户列表视图
    
    使用 Django 的 ListView 通用视图，展示用户列表。
    
    功能：
    - 支持搜索和筛选
    - 分页显示
    """
    model = User
    template_name = 'users/index.html'
    context_object_name = 'users'
    paginate_by = 10  # 每页显示 10 条记录
    
    def get_queryset(self):
        """
        获取查询集
        
        支持搜索功能：根据姓名或用户名搜索
        """
        queryset = super().get_queryset()
        
        # 获取搜索关键词
        search_term = self.request.GET.get('search', '')
        
        if search_term:
            # 使用 Q 对象进行 OR 查询
            queryset = queryset.filter(
                Q(name__icontains=search_term) | 
                Q(username__icontains=search_term)
            )
        
        # 获取筛选条件
        filter_by = self.request.GET.get('filter', 'all')
        
        if filter_by == 'username':
            queryset = queryset.order_by('username')
        elif filter_by == 'email':
            queryset = queryset.order_by('email')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        """
        获取上下文数据
        
        添加搜索关键词和筛选条件到上下文
        """
        context = super().get_context_data(**kwargs)
        context['search_term'] = self.request.GET.get('search', '')
        context['filter_by'] = self.request.GET.get('filter', 'all')
        return context


class UserDetailView(DetailView):
    """
    用户详情视图
    
    使用 Django 的 DetailView 通用视图，展示单个用户的详细信息。
    """
    model = User
    template_name = 'users/detail.html'
    context_object_name = 'user'


class UserCreateView(CreateView):
    """
    创建用户视图
    
    使用 Django 的 CreateView 通用视图，处理用户创建表单。
    """
    model = User
    form_class = UserForm
    template_name = 'users/add.html'
    success_url = reverse_lazy('user_list')  # 创建成功后重定向到列表页
    
    def form_valid(self, form):
        """
        处理有效的表单
        
        在保存前添加成功消息
        """
        messages.success(self.request, '用户创建成功！')
        return super().form_valid(form)


class UserUpdateView(UpdateView):
    """
    更新用户视图
    
    使用 Django 的 UpdateView 通用视图，处理用户编辑表单。
    """
    model = User
    form_class = UserForm
    template_name = 'users/edit.html'
    success_url = reverse_lazy('user_list')  # 更新成功后重定向到列表页
    
    def form_valid(self, form):
        """
        处理有效的表单
        
        在保存前添加成功消息
        """
        messages.success(self.request, '用户更新成功！')
        return super().form_valid(form)


class UserDeleteView(DeleteView):
    """
    删除用户视图
    
    使用 Django 的 DeleteView 通用视图，处理用户删除操作。
    """
    model = User
    template_name = 'users/confirm_delete.html'
    success_url = reverse_lazy('user_list')  # 删除成功后重定向到列表页
    
    def delete(self, request, *args, **kwargs):
        """
        处理删除请求
        
        在删除前添加成功消息
        """
        messages.success(self.request, '用户删除成功！')
        return super().delete(request, *args, **kwargs)


class SyncUsersView(View):
    """
    同步用户视图
    
    从外部 API 同步用户数据到本地数据库。
    """
    def get(self, request):
        """
        处理 GET 请求
        
        执行同步操作并显示结果
        """
        api_service = ApiService()
        count = api_service.sync_users()
        messages.success(request, f'成功同步 {count} 个用户！')
        return redirect('user_list')


def index(request):
    """
    首页视图（函数式视图示例）
    
    重定向到用户列表页
    """
    return redirect('user_list')
