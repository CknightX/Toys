from ...core.task import Task
from ...core.task_proc import TaskProc
job_name = 'test_job'

task = Task(job_name)

@task.run_with("test1",task.every(1).second)
def runner():
    print(TaskProc.get_tasks())