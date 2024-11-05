#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2024/11/1 22:20
# @Author  : 兵
# @email    : 1747193328@qq.com
from rich.progress import Progress, BarColumn, TextColumn
import time

# 创建进度条对象
progress = Progress(
    TextColumn("[progress.description]{task.description}"),
    BarColumn(bar_width=None),
)
progress.start()
# 添加任务
task_id = progress.add_task("Processing", total=100)

# 手动更新进度条
for i in range(100):
    time.sleep(0.02)  # 模拟工作
    progress.update(task_id, advance=1)  # 更新进度条

# 检查进度条是否完成
if not progress.tasks[task_id].completed:
    print("Progress not completed yet.")
else:
    print("Processing complete!")

# 关闭进度条
progress.stop()