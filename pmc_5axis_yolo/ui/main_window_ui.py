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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QMainWindow, QPushButton, QSizePolicy,
    QSpacerItem, QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(820, 534)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalSpacer_6 = QSpacerItem(10, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_6, 0, 0, 1, 1)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.button_offset = QPushButton(self.centralwidget)
        self.button_offset.setObjectName(u"button_offset")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_offset.sizePolicy().hasHeightForWidth())
        self.button_offset.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.button_offset)

        self.button_stop = QPushButton(self.centralwidget)
        self.button_stop.setObjectName(u"button_stop")
        sizePolicy.setHeightForWidth(self.button_stop.sizePolicy().hasHeightForWidth())
        self.button_stop.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.button_stop)


        self.horizontalLayout_4.addLayout(self.horizontalLayout)

        self.horizontalSpacer_3 = QSpacerItem(444, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.Label_HandStop_Status = QLabel(self.centralwidget)
        self.Label_HandStop_Status.setObjectName(u"Label_HandStop_Status")
        sizePolicy.setHeightForWidth(self.Label_HandStop_Status.sizePolicy().hasHeightForWidth())
        self.Label_HandStop_Status.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.Label_HandStop_Status)

        self.Label_HandFeed_Status = QLabel(self.centralwidget)
        self.Label_HandFeed_Status.setObjectName(u"Label_HandFeed_Status")
        sizePolicy.setHeightForWidth(self.Label_HandFeed_Status.sizePolicy().hasHeightForWidth())
        self.Label_HandFeed_Status.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.Label_HandFeed_Status)

        self.Label_KnifeBaseCollid_status = QLabel(self.centralwidget)
        self.Label_KnifeBaseCollid_status.setObjectName(u"Label_KnifeBaseCollid_status")
        sizePolicy.setHeightForWidth(self.Label_KnifeBaseCollid_status.sizePolicy().hasHeightForWidth())
        self.Label_KnifeBaseCollid_status.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.Label_KnifeBaseCollid_status)


        self.horizontalLayout_4.addLayout(self.verticalLayout)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.verticalSpacer = QSpacerItem(17, 17, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.input_media = QLabel(self.centralwidget)
        self.input_media.setObjectName(u"input_media")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.input_media.sizePolicy().hasHeightForWidth())
        self.input_media.setSizePolicy(sizePolicy1)
        self.input_media.setMinimumSize(QSize(300, 250))
        self.input_media.setScaledContents(True)
        self.input_media.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_2.addWidget(self.input_media)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy2)
        self.line.setMinimumSize(QSize(0, 0))
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_2.addWidget(self.line)

        self.output_media = QLabel(self.centralwidget)
        self.output_media.setObjectName(u"output_media")
        sizePolicy1.setHeightForWidth(self.output_media.sizePolicy().hasHeightForWidth())
        self.output_media.setSizePolicy(sizePolicy1)
        self.output_media.setMinimumSize(QSize(300, 250))
        self.output_media.setScaledContents(True)
        self.output_media.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_2.addWidget(self.output_media)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.verticalSpacer_2 = QSpacerItem(17, 18, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_5)

        self.button_picture = QPushButton(self.centralwidget)
        self.button_picture.setObjectName(u"button_picture")
        sizePolicy.setHeightForWidth(self.button_picture.sizePolicy().hasHeightForWidth())
        self.button_picture.setSizePolicy(sizePolicy)
        self.button_picture.setMinimumSize(QSize(150, 50))

        self.horizontalLayout_3.addWidget(self.button_picture)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.button_camera = QPushButton(self.centralwidget)
        self.button_camera.setObjectName(u"button_camera")
        sizePolicy.setHeightForWidth(self.button_camera.sizePolicy().hasHeightForWidth())
        self.button_camera.setSizePolicy(sizePolicy)
        self.button_camera.setMinimumSize(QSize(150, 50))

        self.horizontalLayout_3.addWidget(self.button_camera)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)

        self.button_video = QPushButton(self.centralwidget)
        self.button_video.setObjectName(u"button_video")
        sizePolicy.setHeightForWidth(self.button_video.sizePolicy().hasHeightForWidth())
        self.button_video.setSizePolicy(sizePolicy)
        self.button_video.setMinimumSize(QSize(150, 50))

        self.horizontalLayout_3.addWidget(self.button_video)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)


        self.gridLayout.addLayout(self.verticalLayout_2, 0, 1, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(10, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_7, 0, 2, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.button_offset.setText(QCoreApplication.translate("MainWindow", u"\u8abf\u6574offset", None))
        self.button_stop.setText(QCoreApplication.translate("MainWindow", u"stop", None))
        self.Label_HandStop_Status.setText(QCoreApplication.translate("MainWindow", u"Hand on Stop: N/A", None))
        self.Label_HandFeed_Status.setText(QCoreApplication.translate("MainWindow", u"Hand on Feed: N/A", None))
        self.Label_KnifeBaseCollid_status.setText(QCoreApplication.translate("MainWindow", u"Knife_Base_Collided: N/A", None))
        self.input_media.setText(QCoreApplication.translate("MainWindow", u"\u539f\u59cb\u8f38\u5165", None))
        self.output_media.setText(QCoreApplication.translate("MainWindow", u"\u6aa2\u6e2c\u7d50\u679c", None))
        self.button_picture.setText(QCoreApplication.translate("MainWindow", u"\u5716\u7247\u6aa2\u6e2c", None))
        self.button_camera.setText(QCoreApplication.translate("MainWindow", u"\u93e1\u982d\u6aa2\u6e2c", None))
        self.button_video.setText(QCoreApplication.translate("MainWindow", u"\u5f71\u7247\u6aa2\u6e2c", None))
    # retranslateUi

