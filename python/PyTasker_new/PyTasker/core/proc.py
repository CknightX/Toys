import schedule
import time
from concurrent.futures import ThreadPoolExecutor
from .utils import *
from .manager import *
from .executor import *
from .logger import *

POOL_SIZE = 100
LOOP_TICK = 1

class TaskProc:
    sche = schedule.Scheduler()
    loop_stoped = False

    @classmethod
    def init(cls):
        stdout2logfile()
    
    @classmethod
    def before_stop(cls):
        reset_stdout()

    @classmethod
    def get_tasks(cls, name='*', subname='*'):
        return TaskManager.get_tasks(name,subname)
    
    @classmethod
    def get_task(cls, name, subname):
        return TaskManager.get_tasks(name,subname)[0]
    
    @classmethod
    def loop(cls):
        cls.init()
        while not cls.loop_stoped:
            cls.sche.run_pending()
            time.sleep(LOOP_TICK)

        TaskExecutor.stop()
    
    @classmethod
    def stop_loop(cls):
        cls.loop_stoped = True
        cls.before_stop()


    @classmethod
    def add_task(cls, name, subname,job):
        TaskManager.add_task(name,subname,job)

    @classmethod
    def pause_task(cls, name, subname):
        TaskManager.set_task_status(name,subname,TaskStatus.paused)

    @classmethod
    def is_paused(cls, name, subname):
        return TaskManager.get_task_status(name,subname) == TaskStatus.paused

    @classmethod
    def restart_task(cls, name, subname):
        TaskManager.set_task_status(name,subname,TaskStatus.running)
    

