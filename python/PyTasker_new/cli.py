from PyTasker.core import *
from PyTasker.core.logger import stdprint
from threading import Thread
import os

loop_thread = Thread(target=loop,name="event_loop")
loop_thread.start()
while True:
    stdprint("""
    0. exit
    1. list all tasks
    """)
    stdprint("input:",end='')
    op = input()
    if op == '0':
        break
    os.system('cls' if os.name == 'nt' else 'clear')

TaskProc.stop_loop()
loop_thread.join()
