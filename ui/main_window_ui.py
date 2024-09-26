# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
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
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QMainWindow,
    QPushButton, QSizePolicy, QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(938, 549)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.input_media = QLabel(self.centralwidget)
        self.input_media.setObjectName(u"input_media")
        self.input_media.setGeometry(QRect(90, 160, 281, 241))
        self.input_media.setScaledContents(True)
        self.input_media.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.output_media = QLabel(self.centralwidget)
        self.output_media.setObjectName(u"output_media")
        self.output_media.setGeometry(QRect(540, 160, 281, 241))
        self.output_media.setScaledContents(True)
        self.output_media.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(380, 160, 141, 241))
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        self.button_picture = QPushButton(self.centralwidget)
        self.button_picture.setObjectName(u"button_picture")
        self.button_picture.setGeometry(QRect(160, 450, 141, 51))
        self.button_video = QPushButton(self.centralwidget)
        self.button_video.setObjectName(u"button_video")
        self.button_video.setGeometry(QRect(600, 450, 141, 51))
        self.button_camera = QPushButton(self.centralwidget)
        self.button_camera.setObjectName(u"button_camera")
        self.button_camera.setGeometry(QRect(380, 450, 141, 51))
        self.button_offset = QPushButton(self.centralwidget)
        self.button_offset.setObjectName(u"button_offset")
        self.button_offset.setGeometry(QRect(0, 0, 91, 31))
        self.button_stop = QPushButton(self.centralwidget)
        self.button_stop.setObjectName(u"button_stop")
        self.button_stop.setGeometry(QRect(90, 0, 91, 31))
        self.Label_HandStop_Status = QLabel(self.centralwidget)
        self.Label_HandStop_Status.setObjectName(u"Label_HandStop_Status")
        self.Label_HandStop_Status.setGeometry(QRect(810, 10, 121, 21))
        self.Label_HandFeed_Status = QLabel(self.centralwidget)
        self.Label_HandFeed_Status.setObjectName(u"Label_HandFeed_Status")
        self.Label_HandFeed_Status.setGeometry(QRect(810, 40, 121, 21))
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.input_media.setText(QCoreApplication.translate("MainWindow", u"\u539f\u59cb\u8f38\u5165", None))
        self.output_media.setText(QCoreApplication.translate("MainWindow", u"\u6aa2\u6e2c\u7d50\u679c", None))
        self.button_picture.setText(QCoreApplication.translate("MainWindow", u"\u5716\u7247\u6aa2\u6e2c", None))
        self.button_video.setText(QCoreApplication.translate("MainWindow", u"\u5f71\u7247\u6aa2\u6e2c", None))
        self.button_camera.setText(QCoreApplication.translate("MainWindow", u"\u93e1\u982d\u6aa2\u6e2c", None))
        self.button_offset.setText(QCoreApplication.translate("MainWindow", u"\u8abf\u6574offset", None))
        self.button_stop.setText(QCoreApplication.translate("MainWindow", u"stop", None))
        self.Label_HandStop_Status.setText(QCoreApplication.translate("MainWindow", u"Hand on Stop: N/A", None))
        self.Label_HandFeed_Status.setText(QCoreApplication.translate("MainWindow", u"Hand on Feed: N/A", None))
    # retranslateUi

