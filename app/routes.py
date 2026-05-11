"""
路由模块

本模块定义了所有的 Flask 路由，展示了路由装饰器、请求处理和模板渲染的使用。

学习要点：
- Flask 路由装饰器的使用
- HTTP 方法的定义（GET, POST）
- 请求参数的获取（request.args, request.form）
- 模板渲染（render_template）
- 重定向（redirect, url_for）
- 消息闪现（flash）
- 缓存装饰器的使用
- 工厂模式下的路由注册
"""

# 导入 Flask 核心函数
from flask import render_template, request, redirect, url_for, flash, current_app

# 导入缓存
from app import cache

# 导入 API 服务
from app.services.api_service import ApiService

# 导入用户模型
from app.models.user import User

# 导入表单类
from app.forms import UserForm


def register_routes(app):
    """
    注册路由到应用实例
    
    参数:
        app (Flask): Flask 应用实例
    
    在工厂模式下，路由需要在应用实例创建后注册
    这样可以避免循环导入问题
    """
    
    # 初始化 API 服务
    api_service = ApiService(app.config['BASE_URL'])
    
    @app.route('/')
    def index():
        """
        首页路由 - 显示用户列表，支持搜索和筛选
        
        URL 参数：
            search: 搜索关键词（可选）
            filter: 筛选条件（可选，值为 'all', 'username', 'email'）
        
        功能：
            1. 从 URL 参数获取搜索和筛选条件
            2. 使用缓存获取用户数据
            3. 根据条件过滤和排序用户列表
            4. 渲染首页模板
        
        缓存说明：
            使用 @cache.cached 装饰器缓存用户列表
            缓存键为 'all_users'，超时时间 300 秒
        """
        # 获取 URL 查询参数
        # request.args.get('key', default) 获取 URL 中的查询参数
        search_term = request.args.get('search', '')  # 搜索关键词，默认为空
        filter_by = request.args.get('filter', 'all')  # 筛选条件，默认为 'all'
        
        # 定义缓存的用户获取函数
        @cache.cached(timeout=300, key_prefix='all_users')
        def get_cached_users():
            """从 API 获取用户数据并转换为 User 对象列表"""
            users_data = api_service.get_users()
            # 使用列表推导式将字典列表转换为 User 对象列表
            return [User.from_dict(user_data) for user_data in users_data]
        
        # 获取缓存的用户列表
        users = get_cached_users()
        
        # 搜索功能：过滤包含搜索关键词的用户
        if search_term:
            # 使用列表推导式过滤
            # lower() 方法实现不区分大小写的搜索
            users = [user for user in users if 
                     search_term.lower() in user.name.lower() or 
                     search_term.lower() in user.username.lower()]
        
        # 筛选功能：根据条件排序
        if filter_by != 'all':
            if filter_by == 'username':
                # 按用户名排序
                users.sort(key=lambda x: x.username)
            elif filter_by == 'email':
                # 按邮箱前缀排序（@ 符号之前的部分）
                users.sort(key=lambda x: x.email.split('@')[0])
        
        # 渲染模板，传递变量到模板
        return render_template('index.html', users=users, search_term=search_term, filter_by=filter_by)
    
    @app.route('/user/<int:user_id>')
    def user_detail(user_id):
        """
        用户详情路由 - 显示单个用户的详细信息
        
        参数：
            user_id (int): 用户 ID（从 URL 路径获取）
        
        功能：
            1. 根据用户 ID 获取用户信息
            2. 如果用户不存在，显示错误消息并重定向到首页
            3. 渲染用户详情模板
        
        URL 示例：
            /user/1 - 显示 ID 为 1 的用户详情
        """
        # 定义缓存的用户获取函数
        @cache.cached(timeout=300, key_prefix=f'user_{user_id}')
        def get_cached_user():
            """获取单个用户并转换为 User 对象"""
            user_data = api_service.get_user(user_id)
            if user_data:
                return User.from_dict(user_data)
            return None
        
        # 获取缓存的用户数据
        user = get_cached_user()
        
        # 检查用户是否存在
        if not user:
            # flash 函数用于显示一次性消息
            # 'danger' 是消息类别，用于 Bootstrap 样式
            flash('User not found', 'danger')
            # redirect 函数重定向到指定路由
            # url_for('index') 获取首页路由的 URL
            return redirect(url_for('index'))
        
        # 渲染用户详情模板
        return render_template('detail.html', user=user)
    
    @app.route('/edit/<int:user_id>', methods=['GET', 'POST'])
    def edit_user(user_id):
        """
        用户编辑路由 - 支持 GET（显示表单）和 POST（提交数据）
        
        参数：
            user_id (int): 用户 ID
        
        HTTP 方法：
            GET: 显示编辑表单，预填现有数据
            POST: 处理表单提交，更新用户信息
        
        功能：
            1. 获取用户现有数据
            2. 创建表单实例，使用现有数据填充
            3. 如果是 POST 请求且表单验证通过，更新用户信息
            4. 更新成功后清除相关缓存，显示成功消息
        """
        # 获取用户现有数据
        user_data = api_service.get_user(user_id)
        
        # 检查用户是否存在
        if not user_data:
            flash('User not found', 'danger')
            return redirect(url_for('index'))
        
        # 转换为 User 对象
        user = User.from_dict(user_data)
        
        # 创建表单实例
        # obj=user 参数会自动将 user 对象的属性填充到表单字段
        form = UserForm(obj=user)
        
        # 处理 POST 请求
        # request.method == 'POST' 检查是否为 POST 请求
        # form.validate() 检查表单验证是否通过
        if request.method == 'POST' and form.validate():
            # 从表单获取更新数据
            updated_data = {
                'name': form.name.data,
                'username': form.username.data,
                'email': form.email.data
            }
            
            # 调用 API 服务更新用户
            result = api_service.update_user(user_id, updated_data)
            
            # 检查更新是否成功
            if result:
                # 清除相关缓存，确保下次获取最新数据
                cache.delete(f'user_{user_id}')
                cache.delete('all_users')
                
                # 显示成功消息
                flash('User updated successfully', 'success')
                
                # 重定向到首页
                return redirect(url_for('index'))
            else:
                flash('Failed to update user', 'danger')
        
        # GET 请求或表单验证失败，渲染编辑模板
        return render_template('edit.html', user=user, form=form)
    
    @app.route('/add', methods=['GET', 'POST'])
    def add_user():
        """
        新增用户路由 - 支持 GET（显示表单）和 POST（提交数据）
        
        HTTP 方法：
            GET: 显示空的新增表单
            POST: 处理表单提交，创建新用户
        
        功能：
            1. 创建空表单实例
            2. 如果是 POST 请求且表单验证通过，创建新用户
            3. 创建成功后清除用户列表缓存，显示成功消息
        """
        # 创建空表单实例
        form = UserForm()
        
        # 处理 POST 请求
        if request.method == 'POST' and form.validate():
            # 从表单获取新用户数据
            new_user_data = {
                'name': form.name.data,
                'username': form.username.data,
                'email': form.email.data
            }
            
            # 调用 API 服务创建新用户
            result = api_service.create_user(new_user_data)
            
            # 检查创建是否成功
            if result:
                # 清除用户列表缓存
                cache.delete('all_users')
                
                # 显示成功消息
                flash('User created successfully', 'success')
                
                # 重定向到首页
                return redirect(url_for('index'))
            else:
                flash('Failed to create user', 'danger')
        
        # GET 请求或表单验证失败，渲染新增模板
        return render_template('add.html', form=form)
    
    @app.route('/delete/<int:user_id>', methods=['POST'])
    def delete_user_route(user_id):
        """
        删除用户路由 - 仅支持 POST 方法
        
        参数：
            user_id (int): 用户 ID
        
        HTTP 方法：
            POST: 执行删除操作
        
        安全说明：
            删除操作使用 POST 方法而非 GET 方法，防止误删
            （GET 请求可能被搜索引擎爬虫或浏览器预加载触发）
        
        功能：
            1. 调用 API 服务删除用户
            2. 删除成功后清除相关缓存
            3. 显示相应的消息并跳转到首页
        """
        # 调用 API 服务删除用户
        success = api_service.delete_user(user_id)
        
        # 根据删除结果显示消息
        if success:
            # 清除相关缓存
            cache.delete(f'user_{user_id}')
            cache.delete('all_users')
            flash('User deleted successfully', 'success')
        else:
            flash('Failed to delete user', 'danger')
        
        # 重定向到首页
        return redirect(url_for('index'))
    
    # 返回注册的应用实例
    return app
