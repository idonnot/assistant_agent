# README: 快速启动指南

## 前置要求

- Python 3.9+
- Node.js 16+
- Docker & Docker Compose

## 项目结构

```
weather_agent/
├── backend/              # FastAPI后端
│   ├── main.py          # 应用入口
│   ├── routes/          # API路由
│   ├── services/        # 业务逻辑
│   └── requirements.txt
├── frontend/            # React前端
│   ├── src/            # 源代码
│   ├── public/         # 静态资源
│   └── package.json
├── docker/             # Docker配置
├── agent/              # 原有Agent代码
├── es_loader/          # Elasticsearch加载器
└── run.sh              # 一键启动脚本
```

## 快速启动

### 方式1：Docker全容器化启动（推荐）

#### 前置条件

- Docker & Docker Compose
- 配置环境变量

#### 步骤

1. **复制环境变量文件**

```bash
cp .env.example .env.local
# 编辑 .env.local，填入你的API密钥
```

2. **启动所有服务**

```bash
cd docker
docker-compose up -d
```

3. **访问应用**

```
🌐 前端: http://localhost:5173
🔌 后端API: http://localhost:8000
📚 API文档: http://localhost:8000/docs
🗂️  Elasticsearch: http://localhost:9202
```

4. **查看日志**

```bash
# 查看所有一些容器日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f weather-agent-frontend
docker-compose logs -f weather-agent-backend
docker-compose logs -f elasticsearch
```

5. **停止服务**

```bash
docker-compose down
```

**优点：**
- ✅ 无需本地配置Python/Node环境
- ✅ 完全隔离，不污染系统
- ✅ 一键启动/停止
- ✅ 便于生产部署

---

### 方式2：本地开发启动（需要Python/Node环境）

#### 前置条件

- Python 3.9+
- Node.js 16+
- Docker（仅用于Elasticsearch）

#### 步骤

1. **启动Elasticsearch**

```bash
cd docker
docker-compose up -d elasticsearch
```

2. **启动后端**

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```

3. **启动前端**

```bash
cd frontend
npm install
npm run dev
```

4. **访问应用**

```
🌐 前端: http://localhost:5173
🔌 后端API: http://localhost:8000
```

**优点：**
- ✅ 更快的开发迭代（hot reload）
- ✅ 更容易调试
- ✅ 便于修改代码

---

### 方式3：使用启动脚本（仅限Linux/Mac）

```bash
chmod +x run.sh
./run.sh
```

## API文档

启动后端后访问：http://localhost:8000/docs

## 开发指南

### 后端开发

- 添加新路由：在 `backend/routes/` 创建新文件
- 修改agent逻辑：编辑 `backend/services/agent_service.py`
- 安装新依赖：`pip install <package>` 然后更新 `backend/requirements.txt`

### 前端开发

- 添加新组件：在 `frontend/src/components/` 创建
- 修改样式：编辑对应的 `.css` 文件
- 安装新依赖：`npm install <package>`

## 常见问题

### 后端无法连接Elasticsearch

**本地开发模式：**
确保Elasticsearch已启动：
```bash
cd docker
docker-compose ps
```

**Docker模式：**
检查容器健康状态：
```bash
docker-compose ps
docker-compose logs elasticsearch
```

### Docker启动失败："port already in use"

```bash
# 查看占用的端口
lsof -i :5173  # 前端
lsof -i :8000  # 后端
lsof -i :9202  # Elasticsearch

# 方式1：杀死占用进程（不推荐）
kill -9 <PID>

# 方式2：修改docker-compose.yml的ports配置
# 例如将5173改为5174
ports:
  - "5174:5173"

# 方式3：停止现有容器
docker-compose down
```

### 前端CORS错误

**本地开发：** 确保后端运行在 `http://localhost:8000`

**Docker环境：** 检查`docker-compose.yml`中`VITE_API_URL`的设置：
```bash
# 如果前后端在同一Docker网络中，可以使用容器名
VITE_API_URL=http://weather-agent-backend:8000

# 如果从本机浏览器访问Docker容器，使用localhost
VITE_API_URL=http://localhost:8000
```

### Docker容器看起来能启动但应用无法访问

检查容器是否真的在运行：
```bash
docker-compose ps
docker-compose logs weather-agent-frontend
docker-compose logs weather-agent-backend
```

### 如何修改代码并热更新（Docker模式）

在Docker中，你在`frontend/src`和`backend`目录的改动会自动同步到容器中：

1. 编辑本地代码文件
2. 前端会自动hot reload（Vite）
3. 后端需要手动重启或使用`--reload`标志

重启后端：
```bash
docker-compose restart weather-agent-backend
```

### 如何清理Docker资源

```bash
# 停止所有服务
docker-compose down

# 删除所有容器和数据卷（谨慎！）
docker-compose down -v

# 删除未使用的镜像
docker image prune

# 查看所有镜像大小
docker images --format "table {{.Repository}}\t{{.Size}}"
```

## 部署

### 生产构建

```bash
cd frontend
npm run build
# 生成dist目录，部署到web服务器
```

### Docker部署

参考根目录的 `docker-compose.yml`，添加weather-agent服务配置。
