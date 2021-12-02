import logging
from PyQt5 import QtWidgets
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl, pyqtSignal
from PyQt5.QtWidgets import  QApplication
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
import MainWindowUI

import sys,time,os
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.Qt import QThread
import Recognizer,Utils

mode = Utils.get_conf('BASE','mode')

def say2no(say):
    # TODO 说话信息转换对应元素序号
    for word in say:
        maybe_no = Utils.pe2no(word)
        if maybe_no != -1:
            return maybe_no
    return -1

class ListenThread(QThread):
    """ 监听线程 """
    _sig = pyqtSignal(str)
    _stop_sig = pyqtSignal()
    def __init__(self,window) -> None:
        super().__init__()
        self.window = window
        self._stop_sig.connect(self.stop)
        self.running = False
    def run(self):
        self.running = True
        while self.running is True:
            text = Recognizer.listen_once(mode,self.window)
            logging.info(f'识别到字符串:{text}')
            self._sig.emit(text)
            self.sleep(1)
        logging.info('录音终止')
    def stop(self):
        self.running = False

class MainWindow(QMainWindow,MainWindowUI.Ui_MainWindow):
    def __init__(self, parent = None):
        QMainWindow.__init__(self,parent=parent)
        self.setupUi(self)
        self.title = '元素周期表'
        self.listening = False
        self.listen_thread = None
        self.player = QMediaPlayer(self.VideoWidget)

        self.actionstart.triggered.connect(self.click_menu_start)
        self.actionstop.triggered.connect(self.click_menu_stop)
        self.setWindowTitle(self.title)
        logging.info(f"加载完毕，使用{Utils.get_conf('BASE','mode')}识别源")

    def play_video(self,msg : str):
        # TODO 播放视频
        no = say2no(msg)
        path = os.path.join('video',f'{no}.mp4')
        if not os.path.exists(path) or self.listening is False:
            return

        # self.listen_thread._stop_sig.emit()

        w = self.VideoWidget
        w.show()
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(f'video/{no}.mp4')))
        self.player.setVideoOutput(w)
        self.player.play()

    def click_menu_start(self):
        if self.listening:
            return
        self.setWindowTitle(f'{self.title}-监听中')
        self.listening = True
        self.listen_thread = ListenThread(self)
        self.listen_thread._sig.connect(self.play_video)
        self.listen_thread.start()

    def click_menu_stop(self):
        if not self.listening:
            return
        self.setWindowTitle(f'{self.title}-已停止')
        self.listening = False
        self.listen_thread._stop_sig.emit()
    