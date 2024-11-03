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
            # 定义函数的内容
            function_code = f"""
from pycoze import bot
from pycoze import utils

def chat(input_text:str):
    return bot.get_chat_response("botSetting.json", input_text)

def {random_name}(command:str) -> str:
    \"\"\"与虚拟人角色（{name}）进行交互。
    该函数接收一个指令字符串，并返回虚拟人（{name}）执行该指令后的结果。

    Args:
        command: 需要执行的指令字符串。

    Returns:
        str: 虚拟人执行指令后的结果。
    \"\"\"
    return chat(command)
"""
            exec(function_code)
            tool = to_agent_tool(eval(random_name))
            tool.func = wrapped_func(tool, module_path)
            return tool
    except Exception as e:
        print(f"Error loading bot {bot_id}: {e}")
        return None