# mcp/mcp_client.py
import asyncio
import json
from typing import Dict, List, Optional
from pathlib import Path

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.tools import BaseTool
from config.settings import GITHUB_TOKEN, GITHUB_MCP_ENABLED, MCP_CONFIG_PATH


class MCPClientManager:
    """MCP Client - for all the servers"""
    
    def __init__(self):
        self.client: Optional[MultiServerMCPClient] = None
        self.tools: List[BaseTool] = []
        self._initialized = False
        self._servers_config = self._load_servers_config()
    
    def _load_servers_config(self) -> Dict:
        config_path = MCP_CONFIG_PATH

        with open(config_path, 'r') as f:
            print("load mcp config")
            config = json.load(f)

        enabled_servers = {}

        for name, server_config in config["servers"].items():
            if not server_config.get("enabled", True):
                continue

            clean_config = {
                "transport": server_config.get("transport", "stdio"),
                "command": server_config.get("command"),
                "args": server_config.get("args", []),
            }

            if "env" in server_config:
                clean_config["env"] = server_config["env"]

            enabled_servers[name] = clean_config

        if "github" in enabled_servers and GITHUB_TOKEN:
            enabled_servers["github"]["env"] = {
                "GITHUB_PERSONAL_ACCESS_TOKEN": GITHUB_TOKEN
            }

        return enabled_servers
    
    async def initialize(self):
        """init MCP client"""
        if not self._servers_config:
            print("⚠️ No enabled MCP servers")
            return
        
        try:
            # create MultiServerMCPClient
            self.client = MultiServerMCPClient(self._servers_config)
            
            # transfer mcp tools to langchain tools
            self.tools = await self.client.get_tools()
            
            self._initialized = True
            print(f"✅  Init MCP Client successfully, and load {len(self.tools)}  tools")
            print(f"   Available tools: {[tool.name for tool in self.tools]}")
            
        except Exception as e:
            print(f"❌ Fail to init MCP client: {e}")
            self._initialized = False
    
    async def get_tools(self) -> List[BaseTool]:
        """Get all tools"""
        if not self._initialized:
            await self.initialize()
        return self.tools
    
    async def close(self):
        """Close MCP client"""
        if self.client:
            self._initialized = False
            print("🔌 MCP client closed")
    
    def get_tool_by_name(self, name: str) -> Optional[BaseTool]:
        """Get tool by name"""
        for tool in self.tools:
            if tool.name == name:
                return tool
        return None


_mcp_manager: Optional[MCPClientManager] = None

async def get_mcp_manager() -> MCPClientManager:
    """Get mcp client singleton"""
    global _mcp_manager
    if _mcp_manager is None:
        _mcp_manager = MCPClientManager()
        await _mcp_manager.initialize()
    return _mcp_manager