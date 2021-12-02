from PyQt5 import QtCore, QtGui, QtWidgets
from MainWindow import MainWindow
import sys,logging

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())