from ...core.Tasker import TimeTask
from ...core.TaskerProc import TaskerProc
task = TimeTask("lalala")


@task.Interval(0,0,3)
async def func():
    print(f'任务数：{len(TaskerProc.TASKS)}')

@task.AtTime(17,30,40)
async def func():
    print('我来拉------------------')