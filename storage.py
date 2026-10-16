import json
import sys
import os

TODO_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(TODO_FILE):
        return {}
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
    with open(TODO_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)