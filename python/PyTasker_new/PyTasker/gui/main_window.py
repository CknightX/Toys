import sys

from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import QThread
from PyTasker.ui.ui import Ui_Form
import PyTasker

class TaskLoopThread(QThread):
    def __init__(self) -> None:
        super().__init__()
    
    def run(self):
        PyTasker.start_loop()

class PyTaskerMainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.task_loop_thread = TaskLoopThread()
        self.task_loop_thread.start()

        self.init_buttion()
        self.init_listWidget()
        
    
    def closeEvent(self, event) -> None:
        PyTasker.stop_loop()
        self.task_loop_thread.quit()
    
    def pause_task(self):
        fullname = self.ui.listWidget.currentItem().text()
        name,subname = PyTasker.utils.get_split_name(fullname)
        PyTasker.TaskProc.pause_task(name,subname)
        self.refresh_list_item_status()
    
    def restart_task(self):
        fullname = self.ui.listWidget.currentItem().text()
        name,subname = PyTasker.utils.get_split_name(fullname)
        PyTasker.TaskProc.restart_task(name,subname)
        self.refresh_list_item_status()

    def init_buttion(self):
        self.ui.pause.clicked.connect(self.pause_task)
        self.ui.restart.clicked.connect(self.restart_task)
    
    def init_listWidget(self):
        tasks = PyTasker.TaskProc.get_tasks()
        for task in tasks:
            self.ui.listWidget.addItem(task.fullname)
        
        self.ui.listWidget.itemClicked.connect(self.refresh_list_item_status)

    def refresh_list_item_status(self):
        fullname = self.ui.listWidget.currentItem().text()
        name,subname = PyTasker.utils.get_split_name(fullname)
        if PyTasker.TaskProc.is_paused(name,subname):
            self.ui.task_status.setText('paused')
            self.ui.task_status.setStyleSheet('color:red')
        else:
            self.ui.task_status.setText('running')
            self.ui.task_status.setStyleSheet('color:green')

# 程序入口
if __name__ == "__main__":
    # 初始化QApplication，界面展示要包含在QApplication初始化之后，结束之前
    app = QApplication(sys.argv)
 
    # 初始化并展示我们的界面组件
    window = PyTaskerMainWindow()
    window.show()
    
    sys.exit(app.exec())