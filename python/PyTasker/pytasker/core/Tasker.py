import datetime
import asyncio
import logging
from .TaskerProc import TaskerProc


class Task:
    def __init__(self,name) -> None:
        self.id = -1
        self.name = name
        self.type_ = 'Task.'   # 类型
        self.action_type = ''
        self.task_ = None   # 要执行的任务
        self.running = True
    def get_name(self):
        return f'{self.name} -- {self.type_ + self.action_type} '

    def __str__(self):
        return self.get_name()
    
    async def _before_run(self):
        """执行任务前"""
        pass

    async def _after_run(self):
        """执行任务后"""
        pass
    
    async def run(self):
        await self._before_run()
        await self.task_()
        await self._after_run()

class TimeTask(Task):
    def __init__(self,name) -> None:
        super().__init__(name)
        self.type_ += 'TimeTask.'
        self.nt = datetime.datetime.now()
        self.delta = None
        self.repeat = False

    def AtTime(self,h,m,s):
        """定点执行"""
        self.action_type = 'AtTime'
        def wrapper(func_):
            self.repeat = False
            self.task_ = func_
            now = datetime.datetime.now()
            if_today = datetime.datetime(now.year,now.month,now.day,h,m,s)
            if if_today < now:
                logging.warn(f'{self.get_name()} 永远不会执行')
            else:
                self.nt = if_today
                TaskerProc.append_task(self)

        return wrapper
    
    def EveryDay(self,h=6,m=0,s=0):
        self.action_type = 'EveryDay'
        def wrapper(func_):
            self.repeat = True
            self.task_ = func_
            self.delta = datetime.timedelta(days=1)
            now = datetime.datetime.now()
            if_today = datetime.datetime(now.year,now.month,now.day,h,m,s)
            # 当天无法再执行
            if now > if_today:
                self.nt += self.delta
            else:
                self.nt = if_today
            TaskerProc.append_task(self)
        return wrapper
    
    def Interval(self,h,m,s):
        """间隔执行"""
        self.action_type = 'Interval'

        def wrapper(func_):
            self.delta = datetime.timedelta(hours=h,minutes=m,seconds=s)
            self.repeat = True
            self.nt += self.delta
            self.task_ = func_
            TaskerProc.append_task(self)
        return wrapper
    
    async def _set_next_time(self):
        """更新下一次执行点"""
        if not self.repeat:
            self.running = False
            self.nt = None
        else:
            self.nt += self.delta

    async def _has_expired(self):
        """是否到期"""
        now = datetime.datetime.now()
        return self.nt <= now
    
    async def _after_run(self):
        await self._set_next_time()


from ..modules import *


def run():
    for task in TaskerProc.TASKS:
        print(task)
    asyncio.run(TaskerProc.loop())