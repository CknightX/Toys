from ...core import TaskCreator
from ...core import TaskProc
import time
job_name = 'say'

task = TaskCreator(job_name)

@task.run_with("say_caoke",task.every(1).seconds)
def runner():
    print('hello caoke')

@task.run_with("say_ww",task.every(1).seconds)
def runner():
    print('hello ww')