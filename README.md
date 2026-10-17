# 待办清单 CLI

一个用 Python 写的命令行待办清单工具。任务保存在本地 JSON 文件里，关掉程序再打开，数据还在。

## 功能

- 添加任务，可指定状态和时间
- 查看全部任务
- 标记任务为已完成
- 修改任务内容
- 删除任务（删完自动重新编号）
- 按关键字搜索任务

## 环境要求

- Python 3.x
- 无第三方依赖，只用标准库

## 快速开始

```bash
git clone https://github.com/Moonfringe/CMD-Todo-list.git
cd CMD-Todo-list
python todo.py list
```

## 命令用法

### 添加任务

```bash
python todo.py add "买牛奶"
python todo.py add "写实验报告" -s Done
```

输出：

```
添加： 1 买牛奶 Pending 2026-10-17 23:40
```

| 参数 | 说明 |
|---|---|
| `content` | 任务内容，必填 |
| `-t, --time` | 任务时间，不写就用当前时间 |
| `-s, --status` | 任务状态，只能是 `Done` 或 `Pending`，默认 `Pending` |

### 查看全部任务

```bash
python todo.py list
```

输出：

```
1 2026-10-17 23:40 买牛奶 Pending
2 2026-10-17 23:40 写实验报告 Done
```

每行依次是：编号、时间、内容、状态。

### 标记完成 / 修改 / 删除

```bash
python todo.py done 1                  # 把第 1 条标记为 Done
python todo.py edit 1 "买全脂牛奶"      # 修改第 1 条的内容
python todo.py delete 1                # 删除第 1 条
```

**删除后会自动重新编号**：删掉第 1 条，原来的第 2 条就变成第 1 条，保证编号始终连续。

### 搜索

```bash
python todo.py search 牛奶
```

在任务内容里查找关键字，匹配到的会按列表格式打印出来。

### 查看帮助

```bash
python todo.py -h
```

## 数据存储

任务保存在同目录下的 `tasks.json` 里：

```json
{
    "1": {
        "time": "2026-10-17 23:40",
        "content": "买牛奶",
        "status": "Pending"
    },
    "2": {
        "time": "2026-10-17 23:40",
        "content": "写实验报告",
        "status": "Done"
    }
}
```

- 外层字典的**键是任务编号**（字符串），值是这条任务的字段
- `status` 只有两个值：`Done` / `Pending`
- 文件不存在时自动当作空清单处理

### 文件损坏怎么办

如果 `tasks.json` 被手动改坏（内容不是合法 JSON，或者不是字典），程序会打印提示并**直接退出，不会覆盖原文件**。

这样做是为了保护数据：如果当作空清单继续跑，用户接着敲一次 `add`，坏掉的文件就会被整个覆盖，原来的内容再也找不回来。

修好文件、或者删掉它重新开始，程序就能正常运行。

## 项目结构

```
todo.py        入口：定义命令行参数，按命令分发
storage.py     数据读写：tasks.json 的加载与保存
commands.py    六个命令的具体实现
```

每个命令都是一次独立运行：读文件 → 改数据 → 写回文件。