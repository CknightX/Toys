import time,schedule,threading
from .executor import TaskExecutor
from .proc import TaskProc
from .manager import TaskManager
from .utils import safe_run

class TaskCreator:
    def __init__(self,name) -> None:
        self.name = name
    
    def every(self,intv):
        return schedule.Job(intv,TaskProc.sche)
    
    def run_with(self,subname,job : schedule.Job):
        def wrapper(func):
            TaskManager.add_task(self.name,subname)
            job.do(run_with_new_thread,self.name,subname,func)
            return func
        return wrapper
    
def run_with_new_thread(name,subname,job_func):
    if TaskProc.is_paused(name,subname):
        return
    
    TaskExecutor.run(safe_run(job_func))


