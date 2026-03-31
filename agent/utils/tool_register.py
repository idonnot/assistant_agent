import importlib
import inspect
import pkgutil
from langchain_core.tools import BaseTool
from ..mcp.mcp_client import get_mcp_manager

def load_all_tools_from_package(package_name: str):
    tools = []
    package = importlib.import_module(package_name)

    for _, module_name, _ in pkgutil.walk_packages(
        package.__path__, package.__name__ + "."
    ):
        module = importlib.import_module(module_name)

        for _, obj in inspect.getmembers(module):
            if isinstance(obj, BaseTool):
                tools.append(obj)

    print(f"load {len(tools)} local tools")
    return tools

async def get_all_tools():
    manager = await get_mcp_manager()
    tools = []
    
    tools += await manager.get_tools()
    print(f"load {len(tools)} mcp tools")
    tools += load_all_tools_from_package("agent.skills")

    return tools