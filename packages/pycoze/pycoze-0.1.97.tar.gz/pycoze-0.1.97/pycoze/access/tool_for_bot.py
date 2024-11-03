import sys
import os
import importlib
from langchain.agents import tool as to_agent_tool
import types
import langchain_core
from .lib import ChangeDirectoryAndPath, ModuleManager



def wrapped_tool(tool, module_path):
    """Wrap the tool function to include additional logging and path management."""
    original_tool_function = tool.func

    def _wrapped_tool(*args, **kwargs):
        print(f"调用了{tool.name}")
        with ChangeDirectoryAndPath(module_path):
            result = original_tool_function(*args, **kwargs)
        print(f"{tool.name}调用完毕,结果为:", result)
        return result

    return _wrapped_tool


def import_tools(tool_id):
    """Import tools from a specified tool_id."""
    tool_base_path = "../../tool"
    module_path = os.path.join(tool_base_path, tool_id)
    module_path = os.path.normpath(os.path.abspath(module_path))

    if not os.path.exists(module_path):
        print(f"Tool {tool_id} not found")
        return []

    try:
        with ModuleManager(module_path) as manager:
            module = importlib.import_module("tool")
            export_tools = getattr(module, "export_tools")
            valid_tools = []
            for tool in export_tools:
                assert isinstance(tool, langchain_core.tools.StructuredTool) or isinstance(
                    tool, types.FunctionType
                ), f"Tool is not a StructuredTool or function: {tool}"
                if not isinstance(tool, langchain_core.tools.StructuredTool):
                    tool = to_agent_tool(tool)
                valid_tools.append(to_agent_tool(tool))
            export_tools = valid_tools

    except Exception as e:
        print(f"Error loading tool {tool_id}: {e}")
        return []

    for tool in export_tools:
        tool.func = wrapped_tool(tool, module_path)

    return export_tools
