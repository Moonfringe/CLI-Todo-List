import json
import sys
import os

TODO_FILE = "../tasks.json"


def load_tasks():
    """从 tasks.json 读取任务，文件不存在就当作空清单"""
    if not os.path.exists(TODO_FILE):
        return {}

    # 文件损坏时直接退出，而不是返回空字典——
    # 否则用户接着敲 add 会把坏文件整个覆盖掉，原内容再也找不回来
    try:
        with open(TODO_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print(f"{TODO_FILE}内容损坏，不是合法的 JSON 文件。\n请手动检查该文件，或删掉它重新开始。")
        sys.exit(1)

    if not isinstance(data, dict):
        print(f"{TODO_FILE}的内容格式不对，应该是一个任务清单。\n请手动检查该文件，或删掉它重新开始。")
        sys.exit(1)
    return data


def save_tasks(tasks):
    """把任务写回 tasks.json """
    with open(TODO_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)
