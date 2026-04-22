from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests

app = Flask(__name__)

# 基础URL
BASE_URL = 'https://jsonplaceholder.typicode.com/users'

# 获取所有用户
def get_users():
    response = requests.get(BASE_URL)
    return response.json()

# 获取单个用户
def get_user(user_id):
    response = requests.get(f'{BASE_URL}/{user_id}')
    return response.json()

# 更新用户
def update_user(user_id, data):
    response = requests.put(f'{BASE_URL}/{user_id}', json=data)
    return response.json()

# 创建用户
def create_user(data):
    response = requests.post(BASE_URL, json=data)
    return response.json()

# 删除用户
def delete_user(user_id):
    response = requests.delete(f'{BASE_URL}/{user_id}')
    return response.status_code

@app.route('/')
def index():
    search_term = request.args.get('search', '')
    filter_by = request.args.get('filter', 'all')
    
    users = get_users()
    
    # 搜索功能
    if search_term:
        users = [user for user in users if 
                 search_term.lower() in user['name'].lower() or 
                 search_term.lower() in user['username'].lower()]
    
    # 筛选功能
    if filter_by != 'all':
        if filter_by == 'username':
            users.sort(key=lambda x: x['username'])
        elif filter_by == 'email':
            users.sort(key=lambda x: x['email'].split('@')[0])
    
    return render_template('index.html', users=users, search_term=search_term, filter_by=filter_by)

@app.route('/user/<int:user_id>')
def user_detail(user_id):
    user = get_user(user_id)
    return render_template('detail.html', user=user)

@app.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = get_user(user_id)
    
    if request.method == 'POST':
        updated_data = {
            'name': request.form['name'],
            'username': request.form['username'],
            'email': request.form['email']
        }
        update_user(user_id, updated_data)
        return redirect(url_for('index'))
    
    return render_template('edit.html', user=user)

@app.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        new_user = {
            'name': request.form['name'],
            'username': request.form['username'],
            'email': request.form['email']
        }
        create_user(new_user)
        return redirect(url_for('index'))
    
    return render_template('add.html')

@app.route('/delete/<int:user_id>', methods=['POST'])
def delete_user_route(user_id):
    delete_user(user_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)