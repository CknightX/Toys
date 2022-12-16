
from enum import Enum
from .utils import gen_task_fullname

class TaskStatus(Enum):
    running = 1
    paused = 2
    stoped = 3

class TaskInfo:
    def __init__(cls,name,subname,status) -> None:
        cls.name = name
        cls.subname = subname
        cls.status = status
    
    @property
    def fullname(cls):
        return gen_task_fullname(cls.name,cls.subname)

class TaskManager:
    tasks = {}
    @classmethod
    def add_task(cls,name,subname):
        if name == '*' or subname == '*':
            raise Exception('do not use "*" when add task')
        sub_tasks = cls.tasks.setdefault(name,{})
        if subname in sub_tasks:
            raise Exception('same task name')
        sub_tasks[subname] = TaskInfo(name,subname,TaskStatus.running)
    
    @classmethod
    def del_task(cls,name,subname):
        # remove all task
        if name == '*':
            cls.tasks = {}
            return
        elif name not in cls.tasks:
            raise Exception(f'task: {name} is not existed')
        elif subname == '*':
            cls.tasks[name] = {}
        elif subname not in cls.tasks[name]:
            raise Exception(f'task: {gen_task_fullname(name,subname)} is not existed')
        else:
            cls.tasks[name].pop(subname)
    
    @classmethod
    def set_task_status(cls,name,subname,status):
        tasks = cls.get_tasks(name,subname)
        for task in tasks:
            task.status = status
    
    @classmethod
    def get_task_status(cls,name,subname):
        tasks = cls.get_tasks(name,subname)
        if not tasks:
            raise Exception(f'task not exist')
        else:
            return tasks[0].status
    
    @classmethod
    def get_tasks(cls,name,subname):
        res = []
        if name == '*':
            for name in cls.tasks:
                for subname in cls.tasks[name]:
                    res.append(cls.tasks[name][subname])
        elif name not in cls.tasks:
            raise Exception(f'task: {name} is not existed')
        elif subname == '*':
            for subtask in cls.tasks[name]:
                res.append(cls.tasks[name][subname])
        elif subname not in cls.tasks[name]:
            raise Exception(f'task: {gen_task_fullname(name,subname)} is not existed')
        else:
            res.append(cls.tasks[name][subname])

        return res