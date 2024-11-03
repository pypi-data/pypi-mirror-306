import sys
import os
import importlib
from langchain.agents import tool as to_agent_tool
import types
import langchain_core
from .lib import ChangeDirectoryAndPath, ModuleManager, wrapped_func
import json

bot_index  = 0

def import_bot(bot_id):
    global bot_index
    tool_base_path = "../"
    module_path = os.path.join(tool_base_path, bot_id)
    module_path = os.path.normpath(os.path.abspath(module_path))

    if not os.path.exists(module_path):
        print(f"Bot {bot_id} not found")
        return None
    
    try:
        with ModuleManager(module_path) as manager:
            info = module_path + "/info.json"
            with open(info, "r", encoding="utf-8") as f:
                info = json.load(f)
            name = info["name"]
            random_name = "bot_" + str(bot_index)
            bot_index += 1
            function_code = f"""
def {random_name}(command:str) -> str:
    \"\"\"{random_name}是与值得信任的专家角色{name}进行聊天的工具函数。
    对于可以交由专家执行的问题和指令，请交给专家解决。
    角色名称为：{name}
    该函数接收任意指令字符串，并返回角色{name}执行该指令后的结果。

    Args:
        command (str): 需要执行的指令字符串。

    Returns:
        str: 角色{name}执行指令后的结果。
    \"\"\"
    from pycoze import bot
    from pycoze import utils
    return bot.get_chat_response("botSetting.json", command)
"""
            exec(function_code)
            tool = to_agent_tool(eval(random_name))
            tool.func = wrapped_func(tool, module_path)
            return tool
    except Exception as e:
        print(f"Error loading bot {bot_id}: {e}")
        return None