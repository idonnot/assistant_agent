# test_mcp_github.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from agent.agent import MyAgent

async def test_github_integration():
    """测试 GitHub MCP 集成"""
    
    agent = await MyAgent.create()
    
    test_queries = [
        "分析仓库 idonnot/assistant_agent，告诉我这个项目主要做什么",
        # "列出 assistant_agent 仓库的根目录文件",
        # "读取这个仓库的 .gitignore 文件",
        # "总结一下这个项目的技术栈"
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"用户: {query}")
        print('='*60)
        
        response = await agent.graph.ainvoke(
    {
        "messages": [
            {"role": "user", "content": query}
        ]
    },
    {
        "configurable": {
            "thread_id": "test_github"
        }
    }
)
        
        print(f"Agent: {response}\n")
    
    # await agent.close()

if __name__ == "__main__":
    asyncio.run(test_github_integration())