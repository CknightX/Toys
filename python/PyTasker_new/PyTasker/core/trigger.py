import schedule
import os
from .proc import TaskProc
from enum import Enum

TRIGGER_TICK = 3

class TriggerType(Enum):
    Base = 0
    Time = 1
    File = 2
    

class Trigger:
    tick = TRIGGER_TICK
    def __init__(self) -> None:
        self.type = TriggerType.Base

    def _check(self) -> bool:
        return True

class TimeTrigger(Trigger):
    def __init__(self) -> None:
        super().__init__()
        self.type = TriggerType.Time

    def every(self,intv):
        return schedule.Job(intv,TaskProc.sche)


class FileTrigger(Trigger):
    def __init__(self) -> None:
        super().__init__()
        self.type = TriggerType.File
    
    def file_exist(self,file_path):
        self.mode = 'file_exist'
        self.file_path = file_path

    def _check(self):
        if self.mode == 'file_exist':
            if os.path.exists(self.file_path):
                return True
        return False
