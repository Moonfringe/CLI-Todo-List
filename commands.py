from storage import load_tasks, save_tasks

def cmd_add(args):
    tasks = load_tasks()
    if not args.content.strip():
        print("添加的内容不可为空")
        return
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