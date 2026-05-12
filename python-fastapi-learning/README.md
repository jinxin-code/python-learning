# Python FastAPI Learning

一个使用 FastAPI 构建的用户管理系统学习项目。

## 项目特点

- 使用 **FastAPI** 框架构建高性能 API
- 使用 **Pydantic** 进行数据验证和序列化
- 使用 **httpx** 进行 HTTP 请求（支持同步和异步）
- 支持多环境配置（development/production/testing）
- 自动生成交互式 API 文档

## 技术栈

- Python 3.10+
- FastAPI 0.100+
- Pydantic 2.0+
- httpx 0.24+
- Uvicorn（ASGI 服务器）

## 项目结构

```
python-fastapi-learning/
├── app/                     # 应用核心代码
│   ├── models/              # 数据模型（Pydantic）
│   │   └── user.py          # 用户模型定义
│   ├── services/            # 服务层
│   │   └── api_service.py   # API 服务封装
│   └── __init__.py          # 应用包初始化
├── tests/                   # 测试目录
├── config.py                # 配置模块
├── main.py                  # 应用入口
├── requirements.txt         # 依赖列表
├── .gitignore              # Git 忽略文件
└── README.md               # 项目说明文档
```

## 快速开始

### 1. 安装依赖

```bash
# 进入项目目录
cd python-fastapi-learning

# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 运行应用

```bash
# 开发环境（默认）
python main.py

# 或使用 uvicorn 直接运行
uvicorn main:app --reload
```

### 3. 访问应用

- **API 服务**: http://localhost:8000
- **自动文档 (Swagger UI)**: http://localhost:8000/docs
- **自动文档 (ReDoc)**: http://localhost:8000/redoc

## API 接口

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | / | 获取用户列表（支持搜索和筛选） |
| GET | /users/{user_id} | 获取单个用户详情 |
| POST | /users/ | 创建新用户 |
| PUT | /users/{user_id} | 更新用户信息 |
| DELETE | /users/{user_id} | 删除用户 |

### 使用示例

#### 获取用户列表

```bash
# 获取所有用户
curl http://localhost:8000/

# 搜索用户（包含 "John" 的用户）
curl "http://localhost:8000/?search=John"

# 按用户名排序
curl "http://localhost:8000/?filter_by=username"
```

#### 获取单个用户

```bash
curl http://localhost:8000/users/1
```

#### 创建用户

```bash
curl -X POST http://localhost:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "username": "johndoe",
    "email": "john@example.com"
  }'
```

#### 更新用户

```bash
curl -X PUT http://localhost:8000/users/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Doe",
    "email": "jane@example.com"
  }'
```

#### 删除用户

```bash
curl -X DELETE http://localhost:8000/users/1
```

## 环境配置

可以通过环境变量配置应用：

| 环境变量 | 说明 | 默认值 |
|----------|------|--------|
| FASTAPI_ENV | 运行环境 | development |
| API_BASE_URL | 外部 API 地址 | https://jsonplaceholder.typicode.com/users |
| LOG_LEVEL | 日志级别 | INFO |

```bash
# 生产环境运行
FASTAPI_ENV=production python main.py
```

## 学习要点

本项目展示了以下 FastAPI 核心概念：

1. **路由定义**: 使用装饰器定义 API 端点
2. **路径参数**: 从 URL 路径获取参数
3. **查询参数**: 从 URL 查询字符串获取参数
4. **请求体**: 使用 Pydantic 模型验证请求数据
5. **响应模型**: 使用 Pydantic 模型序列化响应数据
6. **依赖注入**: 使用 Depends 实现依赖注入
7. **HTTP 异常**: 使用 HTTPException 返回错误响应
8. **自动文档**: FastAPI 自动生成 Swagger 和 ReDoc 文档

## 测试

```bash
# 运行测试（需要安装 pytest）
pip install pytest
pytest tests/
```

## 许可证

MIT License
