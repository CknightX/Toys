import threading
from .logger import stdout



def gen_task_fullname(name,subname):
    return f'{name}@{subname}'

def get_split_name(fullname):
    return fullname.split('@')

def safe_run(fc):
    def wrapper():
        try:
            fc()
        except:
            pass
    return wrapper

def stdprint(str,end='\n'):
    print(str,file=stdout,end=end,flush=True)