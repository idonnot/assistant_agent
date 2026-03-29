"""
Agent服务层：包装WeatherAgent，提供与FastAPI集成的接口
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from agent.agent import WeatherAgent
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class AgentService:
    """WeatherAgent服务包装类"""
    
    def __init__(self):
        """初始化WeatherAgent实例"""
        try:
            self.agent = WeatherAgent()
            logger.info("WeatherAgent initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize WeatherAgent: {e}")
            raise
    
    def process_message(self, message: str, thread_id: str = "default_user") -> Dict:
        """
        处理用户消息，与WeatherAgent交互
        
        Args:
            message: 用户输入的消息
            thread_id: 会话ID，用于保持对话历史
            
        Returns:
            包含响应的字典 {"response": "...", "status": "ok"}
        """
        try:
            logger.info(f"Processing message: {message} (thread_id: {thread_id})")
            
            # 调用WeatherAgent的run方法
            response = self.agent.run(message, thread_id=thread_id)
            
            logger.info(f"Response generated successfully")
            
            return {
                "response": response,
                "status": "ok",
                "message": message,
                "thread_id": thread_id
            }
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return {
                "response": f"抱歉，处理您的查询时出现错误：{str(e)}",
                "status": "error",
                "message": message,
                "thread_id": thread_id,
                "error": str(e)
            }
    
    def get_conversation_history(self, thread_id: str) -> List[Dict]:
        """
        获取对话历史（当前实现返回空列表，未来可扩展）
        
        Args:
            thread_id: 会话ID
            
        Returns:
            对话历史消息列表
        """
        # TODO: 实现对话历史存储和检索
        return []


# 全局agent service实例
_agent_service = None


def get_agent_service() -> AgentService:
    """获取或创建AgentService单例"""
    global _agent_service
    if _agent_service is None:
        _agent_service = AgentService()
    return _agent_service
