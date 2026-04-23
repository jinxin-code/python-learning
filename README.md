# 用户管理系统 / User Management System

这是一个基于Flask的用户管理系统，用于管理从JSONPlaceholder API获取的用户数据。

This is a Flask-based user management system for managing user data fetched from the JSONPlaceholder API.

## 功能特性 / Features

- **用户卡片展示**：以卡片形式展示所有用户信息
- **用户详情查看**：查看用户的详细信息
- **用户搜索**：通过用户名或姓名搜索用户
- **用户筛选**：按用户名或邮箱前缀筛选用户
- **用户编辑**：修改用户的姓名、用户名和邮箱
- **用户新增**：添加新用户
- **用户删除**：删除用户
- **表单验证**：客户端和服务器端表单验证
- **CSRF保护**：防止跨站请求伪造攻击
- **缓存机制**：提高性能，减少API调用
- **错误处理**：完善的错误处理和日志记录

- **User Card Display**: Display all user information in card format
- **User Detail View**: View detailed user information
- **User Search**: Search users by username or name
- **User Filtering**: Filter users by username or email prefix
- **User Editing**: Modify user's name, username, and email
- **User Addition**: Add new users
- **User Deletion**: Delete users
- **Form Validation**: Client-side and server-side form validation
- **CSRF Protection**: Prevent cross-site request forgery attacks
- **Caching Mechanism**: Improve performance and reduce API calls
- **Error Handling**: Comprehensive error handling and logging

## 项目结构 / Project Structure

```
python-learning/
├── app/
│   ├── __init__.py      # 应用初始化 / Application initialization
│   ├── routes.py        # 路由和业务逻辑 / Routes and business logic
│   ├── forms.py         # 表单处理 / Form handling
│   ├── models/          # 数据模型 / Data models
│   │   └── user.py      # 用户模型 / User model
│   ├── services/        # 服务层 / Service layer
│   │   └── api_service.py # API服务 / API service
│   ├── static/          # 静态文件目录 / Static files directory
│   └── templates/       # HTML模板目录 / HTML templates directory
├── tests/               # 测试目录 / Test directory
│   ├── test_api_service.py # API服务测试 / API service tests
│   └── test_models.py   # 模型测试 / Model tests
├── .gitignore           # Git忽略文件 / Git ignore file
├── config.py            # 配置文件 / Configuration file
├── requirements.txt     # 依赖文件 / Dependency file
├── run.py               # 应用入口点 / Application entry point
└── README.md            # 项目说明 / Project description
```

## 安装和运行 / Installation and Running

1. **创建虚拟环境**：
   ```bash
   python3 -m venv venv
   ```

   **Create virtual environment**:
   ```bash
   python3 -m venv venv
   ```

2. **激活虚拟环境**：
   ```bash
   source venv/bin/activate
   ```

   **Activate virtual environment**:
   ```bash
   source venv/bin/activate
   ```

3. **安装依赖**：
   ```bash
   pip install -r requirements.txt
   ```

   **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **运行应用**：
   ```bash
   python run.py
   ```

   **Run application**:
   ```bash
   python run.py
   ```

5. **访问应用**：
   打开浏览器访问 http://127.0.0.1:5000

   **Access application**:
   Open browser and visit http://127.0.0.1:5000

## 运行测试 / Running Tests

```bash
python -m pytest tests/
```

## 技术栈 / Technology Stack

- Python 3.14
- Flask 3.1.3
- Requests 2.31.0
- Flask-WTF 1.2.1 (表单处理和CSRF保护)
- Flask-Caching 2.1.0 (缓存机制)
- pytest 8.3.3 (测试框架)

## 注意事项 / Notes

- 本应用使用JSONPlaceholder API进行数据操作，所有操作都是模拟的，不会实际修改服务器数据
- 应用运行在开发模式下，不建议在生产环境中使用
- 缓存默认使用简单内存缓存，生产环境建议使用Redis等更可靠的缓存方案

- This application uses the JSONPlaceholder API for data operations. All operations are simulated and will not actually modify server data.
- The application runs in development mode and is not recommended for use in production environments.
- The cache uses simple memory cache by default. For production environments, it is recommended to use more reliable caching solutions like Redis.
