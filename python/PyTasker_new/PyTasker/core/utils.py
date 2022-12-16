import threading

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