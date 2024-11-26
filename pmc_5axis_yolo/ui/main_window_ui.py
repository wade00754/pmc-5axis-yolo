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
        MainWindow.resize(1030, 546)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_3 = QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.horizontalSpacer_6 = QSpacerItem(107, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_6, 0, 0, 1, 1)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.button_offset = QPushButton(self.centralwidget)
        self.button_offset.setObjectName(u"button_offset")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_offset.sizePolicy().hasHeightForWidth())
        self.button_offset.setSizePolicy(sizePolicy)

        self.verticalLayout_4.addWidget(self.button_offset)

        self.button_stop = QPushButton(self.centralwidget)
        self.button_stop.setObjectName(u"button_stop")
        sizePolicy.setHeightForWidth(self.button_stop.sizePolicy().hasHeightForWidth())
        self.button_stop.setSizePolicy(sizePolicy)

        self.verticalLayout_4.addWidget(self.button_stop)

        self.button_takepicture = QPushButton(self.centralwidget)
        self.button_takepicture.setObjectName(u"button_takepicture")
        sizePolicy.setHeightForWidth(self.button_takepicture.sizePolicy().hasHeightForWidth())
        self.button_takepicture.setSizePolicy(sizePolicy)

        self.verticalLayout_4.addWidget(self.button_takepicture)


        self.horizontalLayout.addLayout(self.verticalLayout_4)

        self.horizontalSpacer_3 = QSpacerItem(88, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_step_last = QLabel(self.centralwidget)
        self.label_step_last.setObjectName(u"label_step_last")

        self.verticalLayout_3.addWidget(self.label_step_last)

        self.label_step_now = QLabel(self.centralwidget)
        self.label_step_now.setObjectName(u"label_step_now")

        self.verticalLayout_3.addWidget(self.label_step_now)

        self.label_step_next = QLabel(self.centralwidget)
        self.label_step_next.setObjectName(u"label_step_next")

        self.verticalLayout_3.addWidget(self.label_step_next)


        self.horizontalLayout.addLayout(self.verticalLayout_3)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.button_step_last = QPushButton(self.centralwidget)
        self.button_step_last.setObjectName(u"button_step_last")

        self.verticalLayout_5.addWidget(self.button_step_last)

        self.button_step_next = QPushButton(self.centralwidget)
        self.button_step_next.setObjectName(u"button_step_next")

        self.verticalLayout_5.addWidget(self.button_step_next)


        self.horizontalLayout.addLayout(self.verticalLayout_5)

        self.label_ste_text = QLabel(self.centralwidget)
        self.label_ste_text.setObjectName(u"label_ste_text")

        self.horizontalLayout.addWidget(self.label_ste_text)

        self.horizontalSpacer_8 = QSpacerItem(18, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_8)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.Label_HumanPose_status = QLabel(self.centralwidget)
        self.Label_HumanPose_status.setObjectName(u"Label_HumanPose_status")
        sizePolicy.setHeightForWidth(self.Label_HumanPose_status.sizePolicy().hasHeightForWidth())
        self.Label_HumanPose_status.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.Label_HumanPose_status)

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


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.verticalLayout_7.addLayout(self.horizontalLayout)

        self.verticalSpacer_3 = QSpacerItem(20, 68, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.input_media = QLabel(self.centralwidget)
        self.input_media.setObjectName(u"input_media")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.input_media.sizePolicy().hasHeightForWidth())
        self.input_media.setSizePolicy(sizePolicy1)
        self.input_media.setMinimumSize(QSize(150, 125))
        self.input_media.setScaledContents(True)
        self.input_media.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.input_media, 0, 1, 1, 1)


        self.verticalLayout_6.addLayout(self.gridLayout_2)

        self.verticalSpacer = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer)

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

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.button_camera = QPushButton(self.centralwidget)
        self.button_camera.setObjectName(u"button_camera")
        sizePolicy.setHeightForWidth(self.button_camera.sizePolicy().hasHeightForWidth())
        self.button_camera.setSizePolicy(sizePolicy)
        self.button_camera.setMinimumSize(QSize(150, 25))
        self.button_camera.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        self.verticalLayout_2.addWidget(self.button_camera)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.camera_change1 = QPushButton(self.centralwidget)
        self.camera_change1.setObjectName(u"camera_change1")

        self.horizontalLayout_2.addWidget(self.camera_change1)

        self.camera_change2 = QPushButton(self.centralwidget)
        self.camera_change2.setObjectName(u"camera_change2")

        self.horizontalLayout_2.addWidget(self.camera_change2)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.horizontalLayout_3.addLayout(self.verticalLayout_2)

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


        self.verticalLayout_6.addLayout(self.horizontalLayout_3)


        self.horizontalLayout_4.addLayout(self.verticalLayout_6)

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

        self.horizontalLayout_4.addWidget(self.line)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.output_media = QLabel(self.centralwidget)
        self.output_media.setObjectName(u"output_media")
        sizePolicy1.setHeightForWidth(self.output_media.sizePolicy().hasHeightForWidth())
        self.output_media.setSizePolicy(sizePolicy1)
        self.output_media.setMinimumSize(QSize(150, 125))
        self.output_media.setScaledContents(True)
        self.output_media.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.output_media, 0, 0, 1, 1)

        self.output_media2 = QLabel(self.centralwidget)
        self.output_media2.setObjectName(u"output_media2")
        sizePolicy1.setHeightForWidth(self.output_media2.sizePolicy().hasHeightForWidth())
        self.output_media2.setSizePolicy(sizePolicy1)
        self.output_media2.setMinimumSize(QSize(150, 125))
        self.output_media2.setScaledContents(True)
        self.output_media2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.output_media2, 1, 0, 1, 1)


        self.horizontalLayout_4.addLayout(self.gridLayout)


        self.verticalLayout_7.addLayout(self.horizontalLayout_4)


        self.gridLayout_3.addLayout(self.verticalLayout_7, 0, 1, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(106, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_7, 0, 2, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 69, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer_2, 1, 1, 1, 1)

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
        self.button_takepicture.setText(QCoreApplication.translate("MainWindow", u"\u7167\u76f8", None))
        self.label_step_last.setText(QCoreApplication.translate("MainWindow", u"\u4e0a\u4e00\u6b65", None))
        self.label_step_now.setText(QCoreApplication.translate("MainWindow", u"\u73fe\u5728\u64cd\u4f5c", None))
        self.label_step_next.setText(QCoreApplication.translate("MainWindow", u"\u4e0b\u4e00\u6b65", None))
        self.button_step_last.setText(QCoreApplication.translate("MainWindow", u"PREV", None))
        self.button_step_next.setText(QCoreApplication.translate("MainWindow", u"NEXT", None))
        self.label_ste_text.setText(QCoreApplication.translate("MainWindow", u"STEP_TEXT", None))
        self.Label_HumanPose_status.setText(QCoreApplication.translate("MainWindow", u"Human pose: N/A", None))
        self.Label_HandStop_Status.setText(QCoreApplication.translate("MainWindow", u"Hand on Stop: N/A", None))
        self.Label_HandFeed_Status.setText(QCoreApplication.translate("MainWindow", u"Hand on Feed: N/A", None))
        self.Label_KnifeBaseCollid_status.setText(QCoreApplication.translate("MainWindow", u"Knife_Base_Collided: N/A", None))
        self.input_media.setText(QCoreApplication.translate("MainWindow", u"\u539f\u59cb\u8f38\u5165", None))
        self.button_picture.setText(QCoreApplication.translate("MainWindow", u"\u5716\u7247\u6aa2\u6e2c", None))
        self.button_camera.setText(QCoreApplication.translate("MainWindow", u"\u93e1\u982d\u6aa2\u6e2c", None))
        self.camera_change1.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.camera_change2.setText(QCoreApplication.translate("MainWindow", u"2", None))
        self.button_video.setText(QCoreApplication.translate("MainWindow", u"\u5f71\u7247\u6aa2\u6e2c", None))
        self.output_media.setText(QCoreApplication.translate("MainWindow", u"\u6aa2\u6e2c\u7d50\u679c", None))
        self.output_media2.setText(QCoreApplication.translate("MainWindow", u"\u6aa2\u6e2c\u7d50\u679c", None))
    # retranslateUi

