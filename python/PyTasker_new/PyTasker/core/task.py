import time,schedule,threading
from .task_proc import TaskProc


class Task:
    def __init__(self,name) -> None:
        self.name = name
    
    def every(self,intv):
        return schedule.Job(intv,TaskProc.sche)
    
    def run_with(self,subname,job : schedule.Job):
        def wrapper(func):
            if TaskProc.get_tasks(self.name,subname):
                return func
            TaskProc.add_task(self.name,subname,job)
            job.do(run_with_new_thread,self.name,subname,func)
            return func
        return wrapper

def run_with_new_thread(name,subname,job_func):
    if TaskProc.is_paused(name,subname):
        return
    
    def wrapper():
        try:
            job_func()
        except:
            pass
    
    TaskProc.tpool.submit(wrapper)


