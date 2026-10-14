import argparse
import os
import json
from datetime import datetime

def load_tasks():
    if not os.path.exists("tasks.json"):
        return {}
    with open("tasks.json", "r", encoding="utf-8") as f:
        return json.load(f)


def save_tasks(tasks):
    with open("tasks.json", "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)

def build_parser():
    parser = argparse.ArgumentParser(
        prog="待办清单",
        description="这是此命令行小工具的菜单")
    subparsers = parser.add_subparsers(dest="command",required=True)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    sub_add = subparsers.add_parser("add",help="添加清单")
    sub_add.add_argument("content",help="清单内容")
    sub_add.add_argument("-t","--time",default=now,help="清单时间")
    sub_add.add_argument(
        "-s","--status",
        choices=["Done","Pending"],
        default="Pending",
        help="清单状态"
    )
    subparsers.add_parser("list", help="列出全部")

    sub_done = subparsers.add_parser("done", help="标记完成")
    sub_done.add_argument("index", type=int, help="第几条")

    sub_edit = subparsers.add_parser("edit", help="修改内容")
    sub_edit.add_argument("index", type=int, help="第几条")
    sub_edit.add_argument("content", help="新内容")

    sub_delete = subparsers.add_parser("delete", help="删除")
    sub_delete.add_argument("index", type=int, help="第几条")

    sub_search = subparsers.add_parser("search", help="搜索")
    sub_search.add_argument("keyword", help="关键字")

    return parser

def cmd_add(args):
    tasks = load_tasks()
    new_id = 1
    for k in tasks:
        if int(k)>= new_id:
            new_id = int(k)+1
    tasks[str(new_id)] = {
        "time": args.time,
        "content": args.content,
        "status": args.status,
    }
    save_tasks(tasks)
    print("添加：",new_id,args.content,args.status,args.time)

def cmd_list(args):
    tasks = load_tasks()
    if not tasks:
        print("还没有添加待办")
        return
    for k in sorted(tasks,key=int):
        print(k, tasks[k]["time"], tasks[k]["content"], tasks[k]["status"])

def cmd_done(args):
    tasks = load_tasks()
    key = str(args.index)
    if key not in tasks:
        print("没有第",args.index,"条")
        return
    tasks[key]["status"] = "Done"
    save_tasks(tasks)
    print("把第", args.index, "条改成 Done")

def cmd_edit(args):
    tasks = load_tasks()
    key = str(args.index)
    if key not in tasks:
        print("没有第",args.index,"条")
        return
    tasks[key]["content"] = args.content
    save_tasks(tasks)
    print("修改第", args.index, "条为：", args.content)

def cmd_delete(args):
    tasks = load_tasks()
    key = str(args.index)
    if key not in tasks:
        print("没有第",args.index,"条")
        return
    del tasks[key]
    delete_found = 1
    new_dict = {}
    for k in sorted(tasks,key=int):
        new_dict[str(delete_found)] = tasks[k]
        delete_found += 1
    save_tasks(new_dict)
    print("已删除第", args.index, "条")

def cmd_search(args):
    tasks = load_tasks()
    search_found = 0
    for k in sorted(tasks,key=int):
        if args.keyword in tasks[k]["content"]:
            print(k, tasks[k]["time"], tasks[k]["content"], tasks[k]["status"])
            search_found += 1
    if search_found == 0:
        print("没有找到")

def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "add":
        cmd_add(args)
    elif args.command == "list":
        cmd_list(args)
    elif args.command == "done":
        cmd_done(args)
    elif args.command == "edit":
        cmd_edit(args)
    elif args.command == "delete":
        cmd_delete(args)
    elif args.command == "search":
        cmd_search(args)


if __name__ == "__main__":
    main()




