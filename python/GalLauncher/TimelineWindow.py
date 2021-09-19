import PySimpleGUI as sg
import GameData as gd
import TimeUtils as tu

def make_timeline_window():
    """详细展示游玩时间线的窗口"""
    layout = [
        [sg.Text('游玩次数:'),sg.Text('')],
        [sg.Listbox([],key = '-LISTBOX-TIME-LINE-',size = (40,15))]
    ]
    window = sg.Window('时间线',layout = layout,finalize=True)
    return window

def update_timeline_window(name,window):
    window.Title = name
    window.set_title(name)
    game_info = gd.get_game_info_by_name(name)
    timeline = game_info['timeline']
    time_list = []
    for per in timeline:
        bg,ed = per.split('-')
        formatted = f'{tu.timestamp_format(bg)}~~{tu.timestamp_format(ed)}'
        time_list.append(formatted)

    window['-LISTBOX-TIME-LINE-'].update(time_list)



