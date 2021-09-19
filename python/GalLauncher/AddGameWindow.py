import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import Column

def make_add_game_window():
    layout_center = [
        [sg.Button('保存',key = '-SAVE-GAME-'),sg.Button('关闭',key = '-WINDOW-CLOSE-')]
    ]

    layout = [
        [sg.Text('游戏名：'), sg.Input()],
        [sg.Text('路径：   '),sg.Input(),sg.FileBrowse('打开')],
        [sg.Column(layout_center,vertical_alignment = 'center',element_justification='center',expand_x=True)]
    ]
    window = sg.Window('增加游戏',layout=layout,finalize=True,grab_anywhere=True)
    return window