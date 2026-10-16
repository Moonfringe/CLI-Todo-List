import argparse
from datetime import datetime
from commands import cmd_add,cmd_list,cmd_done,cmd_edit,cmd_delete,cmd_search

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




