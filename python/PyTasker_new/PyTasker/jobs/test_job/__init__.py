from ...core import *
import time
job_name = 'loveyou'

task = TaskCreator(job_name)

@task.run_with("1",TimeTrigger().every(2).seconds)
def runner():
    print('i love you')
    raise Exception("error")