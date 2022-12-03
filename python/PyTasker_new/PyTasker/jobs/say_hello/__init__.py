from ...core.task import Task
import time
job_name = 'say'

task = Task(job_name)

@task.run_with("say_caoke",task.every(1).seconds)
@task.run_with("say_caoke2",task.every(1).seconds)
def runner():
    print('hello caoke')
    time.sleep(10)

@task.run_with("say_ww",task.every(1).seconds)
def runner():
    print('hello ww')