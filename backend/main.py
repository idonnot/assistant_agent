"""
Weather Agent FastAPI Backend
提供REST API和WebSocket接口与WeatherAgent进行交互
"""

from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import logging
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.services.agent_service import AgentService
from backend.routes.chat import router as chat_router

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title="Weather Agent API",
    description="智能天气查询代理API",
    version="1.0.0"
)

# CORS中间件：允许前端跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",      # React开发服务器
        "http://localhost:5173",      # Vite开发服务器
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 信任的主机中间件
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1"]
)

# 健康检查端点
@app.get("/health")
async def health_check():
    """检查服务健康状态"""
    return {
        "status": "healthy",
        "service": "Weather Agent API",
        "version": "1.0.0"
    }

# 包含聊天路由
app.include_router(chat_router, prefix="/api", tags=["chat"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
