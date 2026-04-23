# 导入Flask的模板渲染、请求处理、重定向和URL生成函数
from flask import render_template, request, redirect, url_for, flash
# 导入app实例和cache
from app import app, cache
# 导入API服务
from app.services.api_service import ApiService
# 导入用户模型
from app.models.user import User
# 导入表单
from app.forms import UserForm

# 初始化API服务
api_service = ApiService(app.config['BASE_URL'])

# 首页路由，显示用户列表
@app.route('/')
def index():
    """
    处理首页请求，显示用户列表，支持搜索和筛选
    """
    # 从URL参数中获取搜索关键词和筛选条件
    search_term = request.args.get('search', '')  # 默认值为空字符串
    filter_by = request.args.get('filter', 'all')  # 默认值为'all'
    
    # 使用缓存获取用户数据，减少API调用
    @cache.cached(timeout=300, key_prefix='all_users')
    def get_cached_users():
        users_data = api_service.get_users()
        return [User.from_dict(user_data) for user_data in users_data]
    
    # 获取缓存的用户列表
    users = get_cached_users()
    
    # 搜索功能：如果有搜索关键词，过滤用户列表
    if search_term:
        # 使用列表推导式过滤用户，检查用户名或姓名是否包含搜索关键词
        users = [user for user in users if 
                 search_term.lower() in user.name.lower() or 
                 search_term.lower() in user.username.lower()]
    
    # 筛选功能：根据筛选条件对用户列表进行排序
    if filter_by != 'all':
        if filter_by == 'username':
            # 按用户名排序
            users.sort(key=lambda x: x.username)
        elif filter_by == 'email':
            # 按邮箱前缀排序
            users.sort(key=lambda x: x.email.split('@')[0])
    
    # 渲染index.html模板，传递用户列表、搜索关键词和筛选条件
    return render_template('index.html', users=users, search_term=search_term, filter_by=filter_by)

# 用户详情路由
@app.route('/user/<int:user_id>')
def user_detail(user_id):
    """
    处理用户详情请求，显示指定ID的用户详细信息
    参数: user_id - 用户ID
    """
    # 使用缓存获取用户数据
    @cache.cached(timeout=300, key_prefix=f'user_{user_id}')
    def get_cached_user():
        user_data = api_service.get_user(user_id)
        if user_data:
            return User.from_dict(user_data)
        return None
    
    # 获取缓存的用户数据
    user = get_cached_user()
    
    # 检查用户是否存在
    if not user:
        flash('User not found', 'danger')
        return redirect(url_for('index'))
    
    # 渲染detail.html模板，传递用户数据
    return render_template('detail.html', user=user)

# 用户编辑路由
@app.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    """
    处理用户编辑请求，支持GET（显示编辑表单）和POST（提交编辑数据）方法
    参数: user_id - 用户ID
    """
    # 获取指定ID的用户数据
    user_data = api_service.get_user(user_id)
    
    # 检查用户是否存在
    if not user_data:
        flash('User not found', 'danger')
        return redirect(url_for('index'))
    
    # 转换为User对象
    user = User.from_dict(user_data)
    
    # 创建表单实例
    form = UserForm(obj=user)
    
    # 如果是POST请求，处理表单提交
    if request.method == 'POST' and form.validate():
        # 从表单中获取更新的数据
        updated_data = {
            'name': form.name.data,
            'username': form.username.data,
            'email': form.email.data
        }
        
        # 调用API服务更新用户数据
        result = api_service.update_user(user_id, updated_data)
        
        # 检查更新是否成功
        if result:
            # 清除相关缓存
            cache.delete(f'user_{user_id}')
            cache.delete('all_users')
            flash('User updated successfully', 'success')
            return redirect(url_for('index'))
        else:
            flash('Failed to update user', 'danger')
    
    # 如果是GET请求或表单验证失败，渲染edit.html模板
    return render_template('edit.html', user=user, form=form)

# 新增用户路由
@app.route('/add', methods=['GET', 'POST'])
def add_user():
    """
    处理新增用户请求，支持GET（显示新增表单）和POST（提交新增数据）方法
    """
    # 创建表单实例
    form = UserForm()
    
    # 如果是POST请求，处理表单提交
    if request.method == 'POST' and form.validate():
        # 从表单中获取新用户数据
        new_user_data = {
            'name': form.name.data,
            'username': form.username.data,
            'email': form.email.data
        }
        
        # 调用API服务创建新用户
        result = api_service.create_user(new_user_data)
        
        # 检查创建是否成功
        if result:
            # 清除用户列表缓存
            cache.delete('all_users')
            flash('User created successfully', 'success')
            return redirect(url_for('index'))
        else:
            flash('Failed to create user', 'danger')
    
    # 如果是GET请求或表单验证失败，渲染add.html模板
    return render_template('add.html', form=form)

# 删除用户路由
@app.route('/delete/<int:user_id>', methods=['POST'])
def delete_user_route(user_id):
    """
    处理删除用户请求，只支持POST方法
    参数: user_id - 用户ID
    """
    # 调用API服务删除用户
    success = api_service.delete_user(user_id)
    
    # 根据删除结果显示不同的消息
    if success:
        # 清除相关缓存
        cache.delete(f'user_{user_id}')
        cache.delete('all_users')
        flash('User deleted successfully', 'success')
    else:
        flash('Failed to delete user', 'danger')
    
    # 重定向到首页
    return redirect(url_for('index'))