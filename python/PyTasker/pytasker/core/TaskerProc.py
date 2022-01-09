"""
任务处理器
"""
import asyncio,copy,datetime,logging
from sortedcontainers import SortedSet

def create_time_set():
    return SortedSet(key=lambda x:x.nt)

# 没有任务时循环等待时间
NO_TASK_WAIT = 5

class TaskerProc:
    TASKS = create_time_set()
    def __init__(self) -> None:
        pass

    @classmethod
    def remove_task(cls,id):
        pass

    @classmethod
    def append_task(cls,task):
        task = copy.deepcopy(task)
        cls.TASKS.add(task)
    
    @classmethod
    async def _re_arrange(cls):
        """
        移除非重复性任务；
        重新对重复性任务排序
        """
        running = create_time_set()
        for task in cls.TASKS:
            if task.running:
                running.add(task)
            else:
                logging.info(f'{task.get_name()} close.')
        cls.TASKS = running


    @classmethod
    async def loop(cls):
        while True:
            if not cls.TASKS: # 没有任务
                await asyncio.sleep(NO_TASK_WAIT)
                continue
            else:
                for task in cls.TASKS:
                    if not await task._has_expired():
                        break
                    await task.run()
                await cls._re_arrange()
                if not cls.TASKS:
                    await asyncio.sleep(NO_TASK_WAIT)
                else:
                    next_will_expired = cls.TASKS[0]
                    seconds = (next_will_expired.nt - datetime.datetime.now()).total_seconds()
                await asyncio.sleep(seconds)
                