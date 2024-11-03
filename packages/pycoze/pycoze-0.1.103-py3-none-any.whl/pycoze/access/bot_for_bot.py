import sys
import os
import importlib
from langchain.agents import tool as to_agent_tool
import types
import langchain_core
from .lib import ChangeDirectoryAndPath, ModuleManager, wrapped_func
import json


def import_bot(bot_id):
    tool_base_path = "../"
    module_path = os.path.join(tool_base_path, bot_id)
    module_path = os.path.normpath(os.path.abspath(module_path))

    if not os.path.exists(module_path):
        print(f"Bot {bot_id} not found")
        return None
    
    try:
        with ModuleManager(module_path) as manager:
            bot_setting = module_path + "/botSetting.json"
            with open(bot_setting, "r", encoding="utf-8") as f:
                bot_setting = json.load(f)
            module = importlib.import_module("bot_function")
            chat_func = getattr(module, "chat")
            random_name = "bot_" + bot_id[-6:]
            # 定义函数的内容
            function_code = f"""
def {random_name}(command:str) -> str:
    \"\"\"
    本函数可以让你与虚拟人角色（{bot_setting["name"]}）进行交互。
    该函数接收一个指令字符串，并返回虚拟人执行该指令后的结果。

    Args:
        command: 需要执行的指令字符串。

    Returns:
        str: 虚拟人执行指令后的结果。
    \"\"\"
    return chat_func(command)
"""
            
            return wrapped_func(to_agent_tool(eval(random_name)))
    except Exception as e:
        print(f"Error loading bot {bot_id}: {e}")
        return None