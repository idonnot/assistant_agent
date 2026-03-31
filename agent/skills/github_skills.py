# # mcp/tools/github_tools.py
# from typing import Dict, Any, List, Optional
# from langchain.tools import tool
# from ..mcp.mcp_client import get_mcp_manager
# from ..schemas.tool_schema import ToolResponse

# @tool
# async def get_repository_info(owner: str, repo: str) -> str:
#     """
#     Get basic information about a GitHub repository.

#     Use this tool when the user asks about:
#     - repository details
#     - GitHub project overview
#     - stars, forks, or description of a repo

#     Args:
#         owner: Repository owner (e.g., "openai")
#         repo: Repository name (e.g., "gpt-4")

#     Returns:
#         JSON string containing repository metadata.
#     """
#     manager = await get_mcp_manager()
#     search_tool = manager.get_tool_by_name("search_repositories")

#     if not search_tool:
#         return ToolResponse(
#             status="error",
#             message="GitHub repository tool unavailable",
#             data=None
#         ).model_dump_json()


#     try:
#         result = await search_tool.ainvoke({
#             "owner": owner,
#             "repo": repo
#         })

#         return ToolResponse(
#             status="success",
#             message=None,
#             data=result
#         ).model_dump_json()
        

#     except Exception as e:
#         return ToolResponse(
#             status="error",
#             message=str(e),
#             data=None
#         ).model_dump_json()

# @tool
# async def list_repository_files(owner: str, repo: str, path: str = "") -> str:
#     """
#     List files and directories in a GitHub repository.

#     Use this tool when the user asks about:
#     - project structure
#     - file list
#     - directory contents

#     Args:
#         owner: Repository owner
#         repo: Repository name
#         path: Directory path (empty for root)

#     Returns:
#         JSON string with file structure information.
#     """
#     manager = await get_mcp_manager()
#     file_tool = manager.get_tool_by_name("get_file_contents")

#     if not file_tool:
#         return ToolResponse(
#             status="error",
#             message="GitHub file listing tool unavailable",
#             data=None
#         ).model_dump_json()

#     try:
#         result = await file_tool.ainvoke({
#             "owner": owner,
#             "repo": repo,
#             "path": path
#         })

#         return ToolResponse(
#             status="success",
#             message=None,
#             data={
#                 "path": path or "root",
#                 "files": result
#             }
#         ).model_dump_json()
    
#     except Exception as e:
#         return ToolResponse(
#             status="error",
#             message=str(e),
#             data=None
#         ).model_dump_json()

# @tool
# async def read_file_content(owner: str, repo: str, path: str, branch: str = "main") -> str:
#     """
#     Read the content of a file from a GitHub repository.

#     Use this tool when the user asks about:
#     - source code
#     - README content
#     - specific file details

#     Args:
#         owner: Repository owner
#         repo: Repository name
#         path: File path
#         branch: Branch name (default: main)

#     Returns:
#         JSON string containing file content.
#     """
#     manager = await get_mcp_manager()
#     file_tool = manager.get_tool_by_name("get_file_contents")

#     if not file_tool:
#         return ToolResponse(
#             status="error",
#             message="GitHub file content tool unavailable",
#             data=None
#         ).model_dump_json()

#     try:
#         result = await file_tool.ainvoke({
#             "owner": owner,
#             "repo": repo,
#             "path": path
#         })

#         return ToolResponse(
#             status="success",
#             message=None,
#             data={
#                 "path": path,
#                 "content": result
#             }
#         ).model_dump_json()

#     except Exception as e:
#         return ToolResponse(
#             status="error",
#             message=str(e),
#             data=None
#         ).model_dump_json()

# @tool
# async def analyze_repository(owner: str, repo: str) -> str:
#     """
#     Analyze a GitHub repository and provide a structured summary.

#     Use this tool when the user asks about:
#     - project analysis
#     - codebase overview
#     - tech stack identification
#     - repo structure summary

#     This tool will:
#     - Detect project type (Python, Node.js, etc.)
#     - Summarize file structure
#     - Extract README content
#     - Provide improvement suggestions

#     Args:
#         owner: Repository owner
#         repo: Repository name

#     Returns:
#         JSON string containing analysis results.
#     """
#     manager = await get_mcp_manager()

#     try:
#         search_tool = manager.get_tool_by_name("search_repositories")
#         file_tool = manager.get_tool_by_name("get_file_contents")

#         repo_info = await repo_tool.ainvoke({"owner": owner, "repo": repo})
#         files = await list_tool.ainvoke({"owner": owner, "repo": repo, "path": ""})

#         readme_content = ""
#         for ext in ["README.md", "README.txt", "README"]:
#             try:
#                 readme_content = await readme_tool.ainvoke({
#                     "owner": owner,
#                     "repo": repo,
#                     "path": ext
#                 })
#                 break
#             except:
#                 continue

#         project_type = _detect_project_type(files)

#         return ToolResponse(
#             status="success",
#             message=None,
#             data={
#                 "repo": f"{owner}/{repo}",
#                 "basic_info": repo_info,
#                 "project_type": project_type,
#                 "structure": _summarize_files(files),
#                 "readme": readme_content[:1000] if readme_content else None,
#                 "suggestions": _generate_suggestions(project_type, files)
#             }
#         ).model_dump_json()

#     except Exception as e:
#         return ToolResponse(
#             status="error",
#             message=str(e),
#             data=None
#         ).model_dump_json()


# def _detect_project_type(files: str) -> str:
#     """
#     Detect project type based on common configuration files.

#     Args:
#         files: Raw file list string

#     Returns:
#         Detected project type description
#     """
#     files_lower = files.lower()
#     if "package.json" in files_lower:
#         return "Node.js / JavaScript Project"
#     elif "requirements.txt" in files_lower or "setup.py" in files_lower:
#         return "Python Project"
#     elif "go.mod" in files_lower:
#         return "Go Project"
#     elif "pom.xml" in files_lower:
#         return "Java / Maven Project"
#     elif "cargo.toml" in files_lower:
#         return "Rust Project"
#     else:
#         return "Unknown Project Type"


# def _summarize_files(files: str, max_items: int = 20) -> str:
#     """
#     Extract and summarize important files from file list.

#     Args:
#         files: Raw file list string
#         max_items: Maximum number of items to display

#     Returns:
#         Filtered and summarized file list
#     """
#     lines = files.split('\n')
#     important = [l for l in lines if any(x in l.lower() for x in 
#                 ['readme', 'src', 'main', 'app', 'config', 'docker', 'test'])]
    
#     if len(important) > max_items:
#         important = important[:max_items]
#         important.append(f"... {len(lines) - max_items} more files")
    
#     return '\n'.join(important) if important else files[:500]


# def _generate_suggestions(project_type: str, files: str) -> str:
#     """
#     Generate improvement suggestions based on repository structure.

#     Args:
#         project_type: Detected project type
#         files: Raw file list string

#     Returns:
#         A list of improvement suggestions
#     """
#     suggestions = []
    
#     if "dockerfile" not in files.lower():
#         suggestions.append("- Consider adding a Dockerfile for containerized deployment")
    
#     if "test" not in files.lower():
#         suggestions.append("- Add test cases and ensure test coverage")
    
#     if ".github/workflows" not in files.lower():
#         suggestions.append("- Configure GitHub Actions for CI/CD")
    
#     return '\n'.join(suggestions) if suggestions else "Well-structured project!"