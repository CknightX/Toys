from ...core import *
import time
job_name = 'loveyou'

task = TaskCreator(job_name)

@task.run_with("1",TimeTrigger().every(2).seconds)
def runner():
    print('i love you')


@task.run_with("2",FileTrigger().file_exist('./1.txt'))
def runner():
    print('have 1 txt')