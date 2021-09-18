# -*- coding: utf-8 -*-
import PySimpleGUI as sg
import GameData as gd
import TimeUtils as tu
import os
import threading
import subprocess
import time

# 用于隐藏黑框
st=subprocess.STARTUPINFO()
# 隐藏黑框
# st.dwFlags=subprocess.STARTF_USESHOWWINDOW  
# 隐藏窗体
st.wShowWindow=subprocess.SW_HIDE


# create main window
def make_main_window():
    games = gd.get_data()
    list_box = sg.Listbox([],size = (None,15),auto_size_text=True,key = '-GAME-LIST-',enable_events = True)
    for game in games:
        list_box.Values.append(game)
    left_col = [
        [list_box],
        [sg.Button('增加游戏',key = '-GAME-ADD-'),sg.Button('删除游戏',key = '-GAME-DEL-')]
    ]
    right_col = [
        [sg.Text('启动次数:'),sg.Text('',key = '-LAUNCH-CNT-')],
        [sg.Text('总运行时间:'), sg.Text('', key = '-TIME-SUM-',size=(17,None))],
        [sg.Text('上次启动时间:'), sg.Text('', key = '-LAST-RUN-TIME-')],
        [sg.Text('当前状态:'), sg.Text('未运行',key = '-GAME-STATUS-')],
        [sg.Button('启动游戏',key = '-RUN-'),sg.Button('详细信息')],
    ]
    layout = [
        [sg.Column(left_col),sg.Column(right_col,expand_y=True)],
    ]
    # Create the Window
    window = sg.Window('GalLauncher', layout = layout, finalize=True)
    return window

def make_add_game_window():
    layout = [
        [sg.Text('游戏名：'), sg.Input()],
        [sg.Text('路径：   '),sg.Input(),sg.FileBrowse('打开')],
        [sg.Button('保存',key = '-SAVE-GAME-'),sg.Button('关闭',key = '-CLOSE-')]
    ]
    window = sg.Window('增加游戏',layout=layout,finalize=True)
    return window


# 当前正在运行的游戏
running_game = None


# 创建线程执行游戏程序
def run_game(path,window):
    exename = path[path.rfind('/')+1:]
    path = path[:path.rfind('/')]
    def run(path,window):
        bg = tu.get_now()
        # 直接使用绝对路径执行的话可能会出错
        os.chdir(path)
        pc = subprocess.Popen(exename, stdin=subprocess.PIPE,stdout=subprocess.PIPE, stderr=subprocess.PIPE,startupinfo=st)
        pc.wait()

        ed = tu.get_now()

        # 进程结束，产生事件
        window.write_event_value('-GAME-CLOSE-',(bg,ed))

    t = threading.Thread(target=run,args=(path,window))
    t.start()


def update_game_info_in_window(name,window):
    """
    更新当前窗体的游戏数据
    """
    game_info = gd.get_game_info(name)
    sumtime = tu.calc_sum_running_time(game_info['timeline'])
    last_run_time = tu.calc_last_running_time(game_info['timeline'])
    window['-TIME-SUM-'].update(f'{sumtime[0]}h {sumtime[1]}m {sumtime[2]}s')
    window['-LAST-RUN-TIME-'].update(f'{last_run_time}')
    window['-LAUNCH-CNT-'].update(f"{len(game_info['timeline'])}")



def eventloop():
    global running_game
    main_window = make_main_window()
    add_game_window = None
    while True:
        window, event, values = sg.read_all_windows()
        # print(event,values)

        # 所有窗体-x按钮-点击
        if event is None:
            if window == main_window:
                break
            elif window == add_game_window:
                add_game_window = None
            window.close()
        
        # 主窗体-运行游戏按钮-点击
        if window == main_window and event == '-RUN-':
            if running_game is not None: # 当前正在运行游戏
                sg.popup('已有游戏正在运行！')
                continue

            game_name = values['-GAME-LIST-'][0]
            running_game = game_name

            window['-GAME-STATUS-'].update('运行中')
            game = gd.get_game_info(values['-GAME-LIST-'][0])
            path = game['path']
            run_game(path,window)

        # 主窗体-增加游戏按钮-点击
        if window == main_window and add_game_window is None and event == '-GAME-ADD-':
            add_game_window = make_add_game_window()

        # 主窗体-删除游戏按钮-点击
        if window == main_window and event == '-GAME-DEL-':
            pass
        # 主窗体-游戏进程结束
        if window == main_window and event == '-GAME-CLOSE-':
            time_duration = values['-GAME-CLOSE-']
            gd.add_game_time(running_game,time_duration[0],time_duration[1])
            update_game_info_in_window(running_game,window)
            running_game = None

        # 主窗体-游戏列表条目-点击
        if window == main_window and event == '-GAME-LIST-':
            name = values['-GAME-LIST-'][0]
            if name == running_game:
                window['-GAME-STATUS-'].update('运行中')
            else:
                window['-GAME-STATUS-'].update('未运行')
            update_game_info_in_window(name,window)


        # 增加游戏窗体-保存按钮-点击
        if window == add_game_window and event == '-SAVE-GAME-':
            add_game_window.close()
            add_game_window = None
            game_name = values[0]
            game_path = values[1]
            list_box = main_window['-GAME-LIST-']
            list_box.Values.append(game_name)
            list_box.update(list_box.Values)
            gd.add_game(game_name,game_path)

        # 增加游戏窗体-关闭按钮-点击
        if window == add_game_window and event == '-CLOSE-':
            add_game_window = None
            window.close()


    main_window.close()

if __name__ == '__main__':
    eventloop()