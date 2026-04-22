# 导入Flask的模板渲染、请求处理、重定向和URL生成函数
from flask import render_template, request, redirect, url_for
# 导入requests库，用于发送HTTP请求
import requests
# 导入app实例
from app import app

# 从配置中获取API基础URL
BASE_URL = app.config['BASE_URL']

# 获取所有用户的函数
def get_users():
    """
    发送GET请求到JSONPlaceholder API获取所有用户数据
    返回值: 包含用户信息的列表
    """
    # 发送GET请求
    response = requests.get(BASE_URL)
    # 将响应转换为JSON格式并返回
    return response.json()

# 获取单个用户的函数
def get_user(user_id):
    """
    发送GET请求到JSONPlaceholder API获取指定ID的用户数据
    参数: user_id - 用户ID
    返回值: 包含用户信息的字典
    """
    # 发送GET请求，URL中包含用户ID
    response = requests.get(f'{BASE_URL}/{user_id}')
    # 将响应转换为JSON格式并返回
    return response.json()

# 更新用户的函数
def update_user(user_id, data):
    """
    发送PUT请求到JSONPlaceholder API更新指定ID的用户数据
    参数: user_id - 用户ID, data - 要更新的数据
    返回值: 更新后的用户信息
    """
    # 发送PUT请求，URL中包含用户ID，数据以JSON格式发送
    response = requests.put(f'{BASE_URL}/{user_id}', json=data)
    # 将响应转换为JSON格式并返回
    return response.json()

# 创建用户的函数
def create_user(data):
    """
    发送POST请求到JSONPlaceholder API创建新用户
    参数: data - 新用户的数据
    返回值: 创建的用户信息
    """
    # 发送POST请求，数据以JSON格式发送
    response = requests.post(BASE_URL, json=data)
    # 将响应转换为JSON格式并返回
    return response.json()

# 删除用户的函数
def delete_user(user_id):
    """
    发送DELETE请求到JSONPlaceholder API删除指定ID的用户
    参数: user_id - 用户ID
    返回值: 响应状态码
    """
    # 发送DELETE请求，URL中包含用户ID
    response = requests.delete(f'{BASE_URL}/{user_id}')
    # 返回响应状态码
    return response.status_code

# 首页路由，显示用户列表
@app.route('/')
def index():
    """
    处理首页请求，显示用户列表，支持搜索和筛选
    """
    # 从URL参数中获取搜索关键词和筛选条件
    search_term = request.args.get('search', '')  # 默认值为空字符串
    filter_by = request.args.get('filter', 'all')  # 默认值为'all'
    
    # 获取所有用户数据
    users = get_users()
    
    # 搜索功能：如果有搜索关键词，过滤用户列表
    if search_term:
        # 使用列表推导式过滤用户，检查用户名或姓名是否包含搜索关键词
        users = [user for user in users if 
                 search_term.lower() in user['name'].lower() or 
                 search_term.lower() in user['username'].lower()]
    
    # 筛选功能：根据筛选条件对用户列表进行排序
    if filter_by != 'all':
        if filter_by == 'username':
            # 按用户名排序
            users.sort(key=lambda x: x['username'])
        elif filter_by == 'email':
            # 按邮箱前缀排序
            users.sort(key=lambda x: x['email'].split('@')[0])
    
    # 渲染index.html模板，传递用户列表、搜索关键词和筛选条件
    return render_template('index.html', users=users, search_term=search_term, filter_by=filter_by)

# 用户详情路由
@app.route('/user/<int:user_id>')
def user_detail(user_id):
    """
    处理用户详情请求，显示指定ID的用户详细信息
    参数: user_id - 用户ID
    """
    # 获取指定ID的用户数据
    user = get_user(user_id)
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
    user = get_user(user_id)
    
    # 如果是POST请求，处理表单提交
    if request.method == 'POST':
        # 从表单中获取更新的数据
        updated_data = {
            'name': request.form['name'],
            'username': request.form['username'],
            'email': request.form['email']
        }
        # 调用update_user函数更新用户数据
        update_user(user_id, updated_data)
        # 重定向到首页
        return redirect(url_for('index'))
    
    # 如果是GET请求，渲染edit.html模板，传递用户数据
    return render_template('edit.html', user=user)

# 新增用户路由
@app.route('/add', methods=['GET', 'POST'])
def add_user():
    """
    处理新增用户请求，支持GET（显示新增表单）和POST（提交新增数据）方法
    """
    # 如果是POST请求，处理表单提交
    if request.method == 'POST':
        # 从表单中获取新用户数据
        new_user = {
            'name': request.form['name'],
            'username': request.form['username'],
            'email': request.form['email']
        }
        # 调用create_user函数创建新用户
        create_user(new_user)
        # 重定向到首页
        return redirect(url_for('index'))
    
    # 如果是GET请求，渲染add.html模板
    return render_template('add.html')

# 删除用户路由
@app.route('/delete/<int:user_id>', methods=['POST'])
def delete_user_route(user_id):
    """
    处理删除用户请求，只支持POST方法
    参数: user_id - 用户ID
    """
    # 调用delete_user函数删除用户
    delete_user(user_id)
    # 重定向到首页
    return redirect(url_for('index'))