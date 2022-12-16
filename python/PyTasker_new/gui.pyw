from PyTasker.gui.main_window import *

# 程序入口
if __name__ == "__main__":
    # 初始化QApplication，界面展示要包含在QApplication初始化之后，结束之前
    app = QApplication(sys.argv)
    # 初始化并展示我们的界面组件
    window = PyTaskerMainWindow()
    window.show()
    
    sys.exit(app.exec())