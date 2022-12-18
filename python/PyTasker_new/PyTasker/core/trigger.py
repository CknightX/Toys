import schedule
import os
from .proc import TaskProc
from enum import Enum

TRIGGER_TICK = 3

class TriggerType(Enum):
    Base = 0
    Time = 1
    File = 2
    Process = 3
    

class Trigger:
    tick = TRIGGER_TICK # trigger check tick, except time trigger
    def __init__(self) -> None:
        self.type = TriggerType.Base
        self.context = {}

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
        """triggered when file/fold exist"""
        self.mode = 'file_exist'
        self.file_path = file_path
        return self
    
    def new_file_with_list(self,fold_path):
        """triggered when new file in fold_path"""
        self.mode = 'new_file_with_list'
        pass

    def _check(self) -> bool:
        if self.mode == 'file_exist':
            if os.path.exists(self.file_path):
                self.context['file'] = self.file_path
                return True
        return False

class ProcessTrigger(Trigger):
    def __init__(self) -> None:
        super().__init__()
        self.type = TriggerType.Process