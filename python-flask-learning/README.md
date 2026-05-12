# 用户管理系统

这是一个基于Flask的用户管理系统，用于管理从JSONPlaceholder API获取的用户数据。

## 功能特性

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
- **工厂模式**：支持多环境配置（开发/测试/生产）
- **详细注释**：代码中包含丰富的学习注释，适合Python/Flask学习

## 项目结构

```
python-learning/
├── app/
│   ├── __init__.py          # 应用初始化（工厂模式）
│   ├── routes.py            # 路由和业务逻辑
│   ├── forms.py             # 表单处理
│   ├── models/              # 数据模型
│   │   └── user.py          # 用户模型
│   ├── services/            # 服务层
│   │   └── api_service.py   # API服务
│   ├── static/              # 静态文件目录
│   └── templates/           # HTML模板目录
├── tests/                   # 测试目录
│   ├── test_api_service.py  # API服务测试
│   ├── test_models.py       # 模型测试
│   └── test_routes.py       # 路由测试
├── .gitignore               # Git忽略文件
├── config.py                # 配置文件（多环境）
├── requirements.txt         # 依赖文件
├── run.py                   # 应用入口点
└── README.md                # 项目说明
```

## 安装和运行

1. **创建虚拟环境**：
   ```bash
   python3 -m venv venv
   ```

2. **激活虚拟环境**：
   ```bash
   source venv/bin/activate
   ```

3. **安装依赖**：
   ```bash
   pip install -r requirements.txt
   ```

4. **运行应用**：
   - 开发环境（默认）：
   ```bash
   python3 run.py
   ```
   或
   ```bash
   FLASK_ENV=development python3 run.py
   ```

   - 生产环境：
   ```bash
   FLASK_ENV=production SECRET_KEY=your-secret-key python3 run.py
   ```

5. **访问应用**：
   打开浏览器访问 http://127.0.0.1:5000

## 运行测试

```bash
python3 -m pytest tests/ -v
```

## 环境变量配置

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `FLASK_ENV` | 运行环境（development/production/testing） | development |
| `SECRET_KEY` | Flask密钥，用于会话管理和CSRF保护 | dev-secret-key |
| `API_BASE_URL` | JSONPlaceholder API基础URL | https://jsonplaceholder.typicode.com/users |
| `CACHE_TYPE` | 缓存类型（simple/redis等） | simple |
| `CACHE_TIMEOUT` | 缓存超时时间（秒） | 300 |

## 技术栈

- Python 3.14
- Flask 3.1.3
- Requests 2.31.0
- Flask-WTF 1.2.1 (表单处理和CSRF保护)
- Flask-Caching 2.1.0 (缓存机制)
- pytest 8.3.3 (测试框架)
- email-validator 2.3.0 (邮箱验证)

## 注意事项

- 本应用使用JSONPlaceholder API进行数据操作，所有操作都是模拟的，不会实际修改服务器数据
- 开发环境默认开启调试模式，生产环境会自动关闭
- 缓存默认使用简单内存缓存，生产环境建议使用Redis等更可靠的缓存方案
- 代码中包含详细的中文注释，适合学习Python和Flask框架

---

# User Management System

This is a Flask-based user management system for managing user data fetched from the JSONPlaceholder API.

## Features

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
- **Factory Pattern**: Support multi-environment configuration (development/testing/production)
- **Detailed Comments**: Rich learning comments in code, suitable for Python/Flask learning

## Project Structure

```
python-learning/
├── app/
│   ├── __init__.py          # Application initialization (Factory Pattern)
│   ├── routes.py            # Routes and business logic
│   ├── forms.py             # Form handling
│   ├── models/              # Data models
│   │   └── user.py          # User model
│   ├── services/            # Service layer
│   │   └── api_service.py   # API service
│   ├── static/              # Static files directory
│   └── templates/           # HTML templates directory
├── tests/                   # Test directory
│   ├── test_api_service.py  # API service tests
│   ├── test_models.py       # Model tests
│   └── test_routes.py       # Route tests
├── .gitignore               # Git ignore file
├── config.py                # Configuration file (Multi-environment)
├── requirements.txt         # Dependency file
├── run.py                   # Application entry point
└── README.md                # Project description
```

## Installation and Running

1. **Create virtual environment**:
   ```bash
   python3 -m venv venv
   ```

2. **Activate virtual environment**:
   ```bash
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run application**:
   - Development environment (default):
   ```bash
   python3 run.py
   ```
   or
   ```bash
   FLASK_ENV=development python3 run.py
   ```

   - Production environment:
   ```bash
   FLASK_ENV=production SECRET_KEY=your-secret-key python3 run.py
   ```

5. **Access application**:
   Open browser and visit http://127.0.0.1:5000

## Running Tests

```bash
python3 -m pytest tests/ -v
```

## Environment Variables

| Variable | Description | Default Value |
|----------|-------------|---------------|
| `FLASK_ENV` | Running environment (development/production/testing) | development |
| `SECRET_KEY` | Flask secret key for session management and CSRF protection | dev-secret-key |
| `API_BASE_URL` | JSONPlaceholder API base URL | https://jsonplaceholder.typicode.com/users |
| `CACHE_TYPE` | Cache type (simple/redis etc.) | simple |
| `CACHE_TIMEOUT` | Cache timeout in seconds | 300 |

## Technology Stack

- Python 3.14
- Flask 3.1.3
- Requests 2.31.0
- Flask-WTF 1.2.1 (Form handling and CSRF protection)
- Flask-Caching 2.1.0 (Caching mechanism)
- pytest 8.3.3 (Testing framework)
- email-validator 2.3.0 (Email validation)

## Notes

- This application uses the JSONPlaceholder API for data operations. All operations are simulated and will not actually modify server data.
- Debug mode is enabled by default in development environment and automatically disabled in production.
- The cache uses simple memory cache by default. For production environments, it is recommended to use more reliable caching solutions like Redis.
- The code contains detailed Chinese comments, suitable for learning Python and Flask framework.