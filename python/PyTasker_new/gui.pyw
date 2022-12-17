from PyTasker.gui.main_window import *



app = QApplication(sys.argv)
window = PyTaskerMainWindow()
window.show()
sys.exit(app.exec())