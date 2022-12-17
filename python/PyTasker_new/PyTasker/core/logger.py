import sys,builtins
stdout = sys.stdout
stderr = sys.stderr

origin_print = builtins.print

def init_logfile():
    global log_file
    log_file = open('log.txt','w')

def reset_stdout():
    global log_file
    sys.stdout = stdout
    sys.stderr = stderr
    if log_file is not None:
        log_file.close()

def stdout2logfile():
    init_logfile()
    sys.stdout = log_file
    sys.stderr = log_file

def flush_log():
    global log_file
    if log_file is not None:
        log_file.flush()

def stdprint(str,end='\n'):
    origin_print(str,file=stdout,end=end,flush=True)