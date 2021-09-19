import PySimpleGUI as sg

def make_modify_game_window():

    layout_center =[
        [sg.Button('保存',key = '-SAVE-'),sg.Button('删除',key = '-DEL-',button_color='red'),sg.Button('关闭',key = '-WINDOW-CLOSE-')]
    ]

    layout = [
        [sg.Text('游戏名：'), sg.Input(key = '-NAME-')],
        [sg.Text('路径：   '),sg.Input(key = '-PATH-'),sg.FileBrowse('打开')],
        [sg.Column(layout_center,element_justification='center',expand_x=True)]
    ]
    window = sg.Window('',layout=layout,finalize=True)
    return window

def update_game_info(name,path,window):
    window.set_title(name)
    window.Title = name # 只是set_title的话window.Title不会变
    window['-NAME-'].update(name)
    window['-PATH-'].update(path)

