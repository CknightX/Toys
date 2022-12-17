import threading,traceback
from .logger import stdout



def gen_task_fullname(name,subname):
    return f'{name}@{subname}'

def get_split_name(fullname):
    return fullname.split('@')

def safe_run(fc):
    def wrapper():
        try:
            fc()
        except Exception as e:
            traceback.print_exc()
            pass
    return wrapper
