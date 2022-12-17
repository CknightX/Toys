import time,schedule,threading
import datetime
from .executor import TaskExecutor
from .proc import TaskProc
from .manager import TaskManager
from .utils import safe_run,gen_task_fullname
from .trigger import *

def run_with_new_thread(name,subname,job_func,trigger = None):
    if TaskProc.is_paused(name,subname):
        return

    if trigger is not None and not trigger._check():
        return
    
    print(f'{datetime.datetime.now()} -- {gen_task_fullname(name,subname)}')
    
    TaskExecutor.run(safe_run(job_func))

class TaskCreator:
    def __init__(self,name) -> None:
        self.name = name
    
    def run_with(self,subname,job : schedule.Job):
        TaskManager.add_task(self.name,subname)
        def wrapper(func):
            job.do(run_with_new_thread,self.name,subname,func)
            return func
        return wrapper
    
    def run_with(self,subname,trigger):
        TaskManager.add_task(self.name,subname)
        def wrapper(func):
            if type(trigger) == schedule.Job:
                trigger.do(run_with_new_thread,self.name,subname,func)
            else:
                job = schedule.Job(Trigger.tick,TaskProc.sche)
                job.do(run_with_new_thread,self.name,subname,func,trigger)
            return func

        return wrapper
    

