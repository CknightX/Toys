# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1077, 882)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.VideoWidget = QVideoWidget(self.centralwidget)
        self.VideoWidget.setObjectName("VideoWidget")
        self.gridLayout.addWidget(self.VideoWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1077, 23))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionstart = QtWidgets.QAction(MainWindow)
        self.actionstart.setObjectName("actionstart")
        self.actionstop = QtWidgets.QAction(MainWindow)
        self.actionstop.setObjectName("actionstop")
        self.menu.addAction(self.actionstart)
        self.menu.addAction(self.actionstop)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "视频展示"))
        self.VideoWidget.setWindowTitle(_translate("MainWindow", "视频展示"))
        self.menu.setTitle(_translate("MainWindow", "状态"))
        self.actionstart.setText(_translate("MainWindow", "开始"))
        self.actionstop.setText(_translate("MainWindow", "停止"))
from PyQt5.QtMultimediaWidgets import QVideoWidget
