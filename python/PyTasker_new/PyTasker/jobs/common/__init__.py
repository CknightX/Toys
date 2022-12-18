from ...core import *
from ...core.logger import flush_log

common = TaskCreator("common",is_hide=True)


@common.run_with("flush_log",TimeTrigger().every(10).seconds)
def run(ctx):
    flush_log()