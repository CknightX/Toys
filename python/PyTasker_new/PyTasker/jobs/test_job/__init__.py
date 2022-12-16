from ...core.task_creator import Task
from ...core.proc import TaskProc
job_name = 'test_job'

task = Task(job_name)

@task.run_with("test1",task.every(1).second)
def runner():
    print(TaskProc.get_tasks())