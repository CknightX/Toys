from datetime import time
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import main
import GameData as gd
import MainWindow,AddGameWindow,TimelineWindow,ModifyGameWindow
import Global
import Utils
import os

def eventloop():

    main_window = MainWindow.make_main_window()
    add_game_window = None
    modify_game_window = None
    timeline_window = None


    MainWindow.update_game_list(main_window)

    while True:
        window, event, values = sg.read_all_windows()
        print(event,values)

        # 所有窗体-x按钮-点击
        if event == sg.WIN_CLOSED or event == '-WINDOW-CLOSE-': 
            if window == main_window:
                # 有游戏正在运行，不允许关闭主窗口
                if Global.running_game is not None:
                    sg.popup(f'{Global.running_game}运行中，请先退出游戏再退出本软件，否则会丢失本次时间记录!')
                    continue
                else:
                    break
            elif window == add_game_window:
                add_game_window = None
            elif window == modify_game_window:
                modify_game_window = None
            elif window == timeline_window:
                timeline_window = None
            window.close()
        
        # 主窗体-运行游戏按钮-点击
        if window == main_window and event == '-RUN-':
            if Global.running_game is not None: # 当前正在运行游戏
                sg.popup('已有游戏正在运行！')
                continue

            game_name = values['-GAME-LIST-'][0]
            game = gd.get_game_info_by_name(game_name)
            path = game['path']

            if not os.path.exists(path):
                sg.popup('路径有误，请检查游戏是否存在！')
                continue

            Utils.run_game(path,window)
            window['-GAME-STATUS-'].update('运行中')
            Global.running_game = game_name

        # 主窗体-增加游戏按钮-点击
        if window == main_window and add_game_window is None and event == '-GAME-ADD-':
            add_game_window = AddGameWindow.make_add_game_window()

        # 主窗体-修改游戏按钮-点击
        if window == main_window and modify_game_window is None and event == '-GAME-MOD-':
            # 没有选中任何游戏
            if not values['-GAME-LIST-']:
                continue

            name = values['-GAME-LIST-'][0]
            path = gd.get_game_info_by_name(name)['path']
            modify_game_window = ModifyGameWindow.make_modify_game_window()
            ModifyGameWindow.update_game_info(name,path,modify_game_window)


        # 主窗体-游戏进程结束
        if window == main_window and event == '-GAME-CLOSE-':
            time_duration = values['-GAME-CLOSE-']
            gd.add_game_time(Global.running_game,time_duration[0],time_duration[1])
            name = Global.running_game
            Global.running_game = None
            # 只有当前焦点在刚结束的游戏时才更新
            if values['-GAME-LIST-'][0] == name:
                MainWindow.update_game_info(name,window)

        # 主窗体-游戏列表条目-点击
        if window == main_window and event == '-GAME-LIST-':
            name = values['-GAME-LIST-'][0]
            MainWindow.update_game_info(name,window)

        # 主窗体-时间线按钮-点击
        if window == main_window and event == '-BUTTON-TIME-LINE-':
            if not values['-GAME-LIST-']:
                continue
            name = values['-GAME-LIST-'][0]
            timeline_window = TimelineWindow.make_timeline_window()
            TimelineWindow.update_timeline_window(name,timeline_window)

        # 增加游戏窗体-保存按钮-点击
        if window == add_game_window and event == '-SAVE-GAME-':
            game_name = values[0]
            game_path = values[1]
            if game_name == '':
                sg.popup('请输入游戏名')
                continue

            add_game_window.close()
            add_game_window = None
            gd.add_game(game_name,game_path)

            MainWindow.update_game_list(main_window)

        
        # 修改游戏窗体-保存按钮-点击
        if window == modify_game_window and event == '-SAVE-':
            name_before = window.Title
            game_name = values['-NAME-']
            game_path = values['-PATH-']
            game_id = gd.get_id_by_name(name_before)

            if game_name == '':
                sg.popup('请输入游戏名')
                continue

            gd.del_game_by_name(name_before,adjust_id = False)
            gd.add_game(game_name,game_path,game_id)

            modify_game_window.close()
            modify_game_window = None

            MainWindow.update_game_list(main_window)

        # 修改游戏窗体-删除按钮-点击
        if window == modify_game_window and event =='-DEL-':
            ret = sg.popup_yes_no('你确定要删除吗？')
            if ret == 'No':
                continue

            name_before = window.Title
            gd.del_game_by_name(name_before)

            MainWindow.update_game_list(main_window)

            modify_game_window.close()
            modify_game_window = None
        
        # 时间线窗口-

    main_window.close()
    main_window = None

if __name__ == '__main__':
    eventloop()