from .proc import TaskProc
from .task import TaskCreator
from .trigger import *
from . import utils

def start_loop():
    TaskProc.loop()

def stop_loop():
    TaskProc.stop_loop()

