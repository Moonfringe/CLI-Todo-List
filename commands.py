from storage import load_tasks, save_tasks
from rich.console import Console
from rich.table import Table

console = Console()


def cmd_add(args):
    """添加一条待办任务到 tasks.json """
    tasks = load_tasks()

    if not args.content.strip():
        print("添加的内容不可为空")
        return

    # 新编号 = 现有最大号 + 1；清单为空时就是 1
    new_id = 1
    for k in tasks:
        if int(k) >= new_id:
            new_id = int(k) + 1

    tasks[str(new_id)] = {
        "time": args.time,
        "content": args.content,
        "status": args.status,
    }
    save_tasks(tasks)
    print("添加：", new_id, args.content, args.status, args.time)


def cmd_list(args):
    """列出 tasks.json 里所有的待办任务"""
    tasks = load_tasks()

    if not tasks:
        print("还没有添加待办")
        return
    table = Table(title="待办清单")
    table.add_column("编号", justify="center")
    table.add_column("内容")
    table.add_column("时间")
    table.add_column("状态")
    for k in sorted(tasks, key=int):
        t = tasks[k]
        if t["status"] == "Done":
            status = "[green]Done[/green]"
            row_style = "dim"
        else:
            status = "[yellow]Pending[/yellow]"
            row_style = None
        table.add_row(k, t["content"], t["time"], status, style=row_style)
    console.print(table)


def cmd_done(args):
    """将你输入的第几条的待办任务标记 pending 改为 done 表示完成"""
    tasks = load_tasks()

    key = str(args.index)
    if key not in tasks:
        print("没有第", args.index, "条")
        return

    tasks[key]["status"] = "Done"
    save_tasks(tasks)
    print("把第", args.index, "条改成 Done")


def cmd_edit(args):
    """修改你输入的第几条的待办任务的 content 待办内容"""
    tasks = load_tasks()

    key = str(args.index)
    if key not in tasks:
        print("没有第", args.index, "条")
        return

    tasks[key]["content"] = args.content
    save_tasks(tasks)
    print("修改第", args.index, "条为：", args.content)


def cmd_delete(args):
    """删除在 tasks.json 里你输入的第几条的待办任务"""
    tasks = load_tasks()

    key = str(args.index)
    if key not in tasks:
        print("没有第", args.index, "条")
        return

    del tasks[key]

    # 删除后序号会出现空档（如 1、3），重新排成连续的 1、2、3…
    new_id = 1
    new_dict = {}
    for k in sorted(tasks, key=int):
        new_dict[str(new_id)] = tasks[k]
        new_id += 1

    save_tasks(new_dict)
    print("已删除第", args.index, "条")


def cmd_search(args):
    """在待办任务里搜索你输入的关键字的对应的任务 """
    tasks = load_tasks()

    table = Table(title="搜索结果")
    table.add_column("编号", justify="center")
    table.add_column("内容")
    table.add_column("时间")
    table.add_column("状态")

    search_found = 0
    for k in sorted(tasks, key=int):
        t = tasks[k]
        if args.keyword in tasks[k]["content"]:
            if t["status"] == "Done":
                status = "[green]Done[/green]"
                row_style = "dim"
            else:
                status = "[yellow]Pending[/yellow]"
                row_style = None
            table.add_row(k, t["content"], t["time"], status, style=row_style)
            search_found += 1

    if search_found == 0:
        print("没有找到")
    else:
        console.print(table)
