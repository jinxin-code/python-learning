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

## 项目结构

```
nodejs-learning/
├── app/
│   ├── __init__.py      # 应用初始化
│   ├── routes.py        # 路由和业务逻辑
│   ├── static/          # 静态文件目录
│   └── templates/       # HTML模板目录
├── tests/               # 测试目录
├── config.py            # 配置文件
├── requirements.txt     # 依赖文件
├── run.py               # 应用入口点
└── README.md            # 项目说明
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
   ```bash
   python run.py
   ```

5. **访问应用**：
   打开浏览器访问 http://127.0.0.1:5000

## 技术栈

- Python 3.14
- Flask 3.1.3
- Requests 2.31.0

## 注意事项

- 本应用使用JSONPlaceholder API进行数据操作，所有操作都是模拟的，不会实际修改服务器数据
- 应用运行在开发模式下，不建议在生产环境中使用
