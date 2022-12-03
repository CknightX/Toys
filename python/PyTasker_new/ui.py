# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tasker.ui'
##
## Created by: Qt User Interface Compiler version 6.4.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QListWidget,
    QListWidgetItem, QPushButton, QSizePolicy, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(318, 362)
        self.listWidget = QListWidget(Form)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setGeometry(QRect(10, 30, 191, 261))
        self.horizontalLayoutWidget = QWidget(Form)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(30, 290, 160, 61))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.restart = QPushButton(self.horizontalLayoutWidget)
        self.restart.setObjectName(u"restart")

        self.horizontalLayout.addWidget(self.restart)

        self.pause = QPushButton(self.horizontalLayoutWidget)
        self.pause.setObjectName(u"pause")

        self.horizontalLayout.addWidget(self.pause)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(210, 30, 54, 16))
        self.task_status = QLabel(Form)
        self.task_status.setObjectName(u"task_status")
        self.task_status.setGeometry(QRect(210, 50, 54, 16))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"PyTasker", None))
        self.restart.setText(QCoreApplication.translate("Form", u"\u5f00\u59cb", None))
        self.pause.setText(QCoreApplication.translate("Form", u"\u6682\u505c", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u4efb\u52a1\u72b6\u6001\uff1a", None))
        self.task_status.setText("")
    # retranslateUi

