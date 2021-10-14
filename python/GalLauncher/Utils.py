import subprocess
import threading
import os
import TimeUtils as tu


def run_game(path,window):
    """创建线程，执行游戏程序,游戏结束后产生事件，value为(开始时间，结束时间)，从而监控进程的结束"""
    # 用于隐藏黑框
    st=subprocess.STARTUPINFO()
    # 隐藏窗体
    # st.dwFlags=subprocess.STARTF_USESHOWWINDOW  
    # 隐藏黑框
    st.wShowWindow=subprocess.SW_HIDE

    exename = path[path.rfind('/')+1:]
    path = path[:path.rfind('/')]
    def run(path,window):
        bg = tu.get_now()
        # 直接使用绝对路径执行的话可能会出错
        os.chdir(path)
        pc = subprocess.Popen(exename, stdin=subprocess.PIPE,stdout=subprocess.PIPE, stderr=subprocess.PIPE,startupinfo=st)
        pc.wait()

        ed = tu.get_now()

        # 进程结束，产生事件，value = (开始时间，结束时间)
        window.write_event_value('-GAME-CLOSE-',(bg,ed))

    t = threading.Thread(target=run,args=(path,window))
    t.start()