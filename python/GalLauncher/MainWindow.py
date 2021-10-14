import PySimpleGUI as sg
import GameData as gd
import TimeUtils as tu
import Global 

# create main window
def make_main_window():
    list_box = sg.Listbox([],size = (None,15),auto_size_text=True,key = '-GAME-LIST-',enable_events = True)
    left_col = [
        [list_box],
        [sg.Button('增加游戏',key = '-GAME-ADD-'),
        sg.Button('修改游戏',key = '-GAME-MOD-'),
        ]
    ]
    right_col = [
        [sg.Text('启动次数:'),sg.Text('',key = '-LAUNCH-CNT-')],
        [sg.Text('总运行时间:'), sg.Text('', key = '-TIME-SUM-',size=(17,None))],
        [sg.Text('上次启动时间:'), sg.Text('', key = '-LAST-RUN-TIME-')],
        [sg.Text('当前状态:'), sg.Text('未运行',key = '-GAME-STATUS-')],
        [sg.Button('启动游戏',key = '-RUN-'),sg.Button('时间线',key = '-BUTTON-TIME-LINE-'),sg.Button('攻略',key = '-NOTE-')],
    ]
    layout = [
        [sg.Column(left_col),sg.Column(right_col,expand_y=True)],
    ]
    # Create the Window
    window = sg.Window('GalLauncher', layout = layout, finalize=True)
    return window

def update_game_list(window):
    """ 更新游戏列表 """
    games = gd.get_data()
    list_box = window['-GAME-LIST-']
    values = []
    values = sorted(games,key = lambda x : games[x]['id'])
    list_box.update(values)
    

def update_game_info(name,window):
    """ 更新主窗体的游戏数据 """
    if name == Global.running_game:
        window['-GAME-STATUS-'].update('运行中')
    else:
        window['-GAME-STATUS-'].update('未运行')
    game_info = gd.get_game_info_by_name(name)
    sumtime = tu.calc_sum_running_time(game_info['timeline'])
    last_run_time = tu.calc_last_running_time(game_info['timeline'])
    window['-TIME-SUM-'].update(f'{sumtime[0]}h {sumtime[1]}m {sumtime[2]}s')
    window['-LAST-RUN-TIME-'].update(f'{last_run_time}')
    window['-LAUNCH-CNT-'].update(f"{len(game_info['timeline'])}")