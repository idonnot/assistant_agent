#!/bin/bash

# 启动Weather Agent 完整系统脚本

echo "🚀 启动Weather Agent系统..."
echo ""

# 检查docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 启动Elasticsearch
echo "1️⃣  启动Elasticsearch..."
cd docker
docker-compose up -d

# 等待Elasticsearch启动
echo "⏳ 等待Elasticsearch启动..."
sleep 10

cd ..

# 启动后端
echo "2️⃣  启动FastAPI后端..."
cd backend
pip install -r requirements.txt > /dev/null 2>&1
python -m uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!

# 启动前端
echo "3️⃣  启动React前端..."
cd ../frontend
npm install > /dev/null 2>&1
npm run dev > /dev/null 2>&1 &
FRONTEND_PID=$!

echo ""
echo "✅ 系统已启动！"
echo ""
echo "服务地址："
echo "  • 前端: http://localhost:5173"
echo "  • 后端API: http://localhost:8000"
echo "  • API文档: http://localhost:8000/docs"
echo "  • Elasticsearch: http://localhost:9202"
echo ""
echo "按Ctrl+C停止所有服务"
echo ""

# 等待进程
wait
