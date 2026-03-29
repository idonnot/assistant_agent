"""
聊天路由：处理HTTP和WebSocket请求
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, Query
from pydantic import BaseModel
from typing import Dict
import logging
import json

from backend.services.agent_service import get_agent_service

logger = logging.getLogger(__name__)

router = APIRouter()


class ChatRequest(BaseModel):
    """聊天请求数据模型"""
    message: str
    thread_id: str = "default_user"


class ChatResponse(BaseModel):
    """聊天响应数据模型"""
    response: str
    status: str
    message: str
    thread_id: str


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    处理单条聊天消息 (HTTP POST)
    
    Args:
        request: 包含消息和线程ID的请求对象
        
    Returns:
        ChatResponse: 代理的响应
        
    Example:
        POST /api/chat
        {
            "message": "杭州的天气怎么样？",
            "thread_id": "user_123"
        }
    """
    logger.info(f"Received chat request: {request.message}")
    
    try:
        # 获取agent服务并处理消息
        agent_service = get_agent_service()
        result = agent_service.process_message(
            request.message,
            thread_id=request.thread_id
        )
        
        if result["status"] != "ok":
            logger.warning(f"Agent processing failed: {result.get('error')}")
            raise HTTPException(
                status_code=500,
                detail=result["response"]
            )
        
        return ChatResponse(
            response=result["response"],
            status="ok",
            message=request.message,
            thread_id=request.thread_id
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in chat endpoint: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    thread_id: str = Query("default_user")
):
    """
    WebSocket端点：实时对话接口
    
    Args:
        websocket: WebSocket连接
        thread_id: 会话ID
        
    Usage:
        const ws = new WebSocket('ws://localhost:8000/api/ws?thread_id=user_123');
        ws.send(JSON.stringify({message: "杭州天气"}));
    """
    await websocket.accept()
    logger.info(f"WebSocket connection established (thread_id: {thread_id})")
    
    agent_service = get_agent_service()
    
    try:
        while True:
            # 接收来自前端的消息
            data = await websocket.receive_text()
            
            try:
                # 如果是JSON格式
                message_data = json.loads(data)
                message = message_data.get("message", "")
            except json.JSONDecodeError:
                # 否则直接作为消息
                message = data
            
            if not message:
                await websocket.send_json({
                    "error": "消息不能为空",
                    "status": "error"
                })
                continue
            
            logger.info(f"WebSocket message received: {message}")
            
            # 处理消息
            result = agent_service.process_message(message, thread_id=thread_id)
            
            # 发送响应
            await websocket.send_json({
                "response": result["response"],
                "status": result["status"],
                "message": message,
                "thread_id": thread_id
            })
            
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected (thread_id: {thread_id})")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        try:
            await websocket.send_json({
                "error": f"WebSocket error: {str(e)}",
                "status": "error"
            })
        except:
            pass
        finally:
            await websocket.close()
