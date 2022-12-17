import sys
log_file = None
stdout = sys.stdout

def init_logfile():
    global log_file
    log_file = open('log.txt','w')

def reset_stdout():
    global log_file
    sys.stdout = stdout
    if log_file is not None:
        log_file.close()

def stdout2logfile():
    init_logfile()
    sys.stdout = log_file

