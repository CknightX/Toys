import schedule
import time
from concurrent.futures import ThreadPoolExecutor
from .utils import gen_task_fullname


POOL_SIZE = 20

class TaskProc:
    sche = schedule.Scheduler()
    task_map = {}
    paused_task = set()
    tpool = ThreadPoolExecutor(max_workers=POOL_SIZE)
    loop_stoped = False

    @classmethod
    def get_tasks(cls, name='*', subname='*'):
        res = []
        if name == '*':
            for k, v in cls.task_map.items():
                for _k, _v in v.items():
                    res.append((k, _k, v))
        elif subname == '*' and name in cls.task_map:
            for k, v in cls.task_map[name].items():
                res.append((name, k, v))
        elif name in cls.task_map and subname in cls.task_map[name]:
            res.append((name, subname, cls.task_map[name][subname]))
        return res

    @classmethod
    def loop(cls):
        while not cls.loop_stoped:
            cls.sche.run_pending()
            time.sleep(1)

    @classmethod
    def cancel_task(cls, name, subname):
        if name == '':
            return
        elif subname == '':
            if name in cls.task_map:
                for k, v in cls.task_map[name].items():
                    v.cancel()
        else:
            if name in cls.task_map and subname in cls.task_map[name]:
                cls.task_map[name][subname].cancel()

    @classmethod
    def add_task(cls, name, subname, job):
        if name in cls.task_map:
            cls.task_map[name][subname] = job
        else:
            cls.task_map[name] = {subname: job}

    @classmethod
    def pause_task(cls, name, subname):
        cls.paused_task.add(gen_task_fullname(name,subname))

    @classmethod
    def restart_task(cls, name, subname):
        cls.paused_task.remove(gen_task_fullname(name,subname))
    
    @classmethod
    def is_paused(cls, name, subname):
        return gen_task_fullname(name,'*') in cls.paused_task or gen_task_fullname(name,subname) in cls.paused_task

