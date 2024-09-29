# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'offset_slider.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QGridLayout, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QSlider, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(407, 300)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_7)

        self.Stop_X_Label = QLabel(Dialog)
        self.Stop_X_Label.setObjectName(u"Stop_X_Label")

        self.horizontalLayout_7.addWidget(self.Stop_X_Label)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_8)


        self.verticalLayout_4.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.Stop_X_MinusButton = QPushButton(Dialog)
        self.Stop_X_MinusButton.setObjectName(u"Stop_X_MinusButton")
        self.Stop_X_MinusButton.setMaximumSize(QSize(20, 20))

        self.horizontalLayout_8.addWidget(self.Stop_X_MinusButton)

        self.Stop_X_Slider = QSlider(Dialog)
        self.Stop_X_Slider.setObjectName(u"Stop_X_Slider")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Stop_X_Slider.sizePolicy().hasHeightForWidth())
        self.Stop_X_Slider.setSizePolicy(sizePolicy)
        self.Stop_X_Slider.setMinimumSize(QSize(250, 0))
        self.Stop_X_Slider.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_8.addWidget(self.Stop_X_Slider)

        self.Stop_X_Plusbutton = QPushButton(Dialog)
        self.Stop_X_Plusbutton.setObjectName(u"Stop_X_Plusbutton")
        self.Stop_X_Plusbutton.setMaximumSize(QSize(20, 20))

        self.horizontalLayout_8.addWidget(self.Stop_X_Plusbutton)


        self.verticalLayout_4.addLayout(self.horizontalLayout_8)


        self.verticalLayout_5.addLayout(self.verticalLayout_4)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_5)

        self.Stop_Y_Label = QLabel(Dialog)
        self.Stop_Y_Label.setObjectName(u"Stop_Y_Label")

        self.horizontalLayout_5.addWidget(self.Stop_Y_Label)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_6)


        self.verticalLayout_3.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.Stop_Y_MinusButton = QPushButton(Dialog)
        self.Stop_Y_MinusButton.setObjectName(u"Stop_Y_MinusButton")
        self.Stop_Y_MinusButton.setMaximumSize(QSize(20, 20))

        self.horizontalLayout_6.addWidget(self.Stop_Y_MinusButton)

        self.Stop_Y_Slider = QSlider(Dialog)
        self.Stop_Y_Slider.setObjectName(u"Stop_Y_Slider")
        sizePolicy.setHeightForWidth(self.Stop_Y_Slider.sizePolicy().hasHeightForWidth())
        self.Stop_Y_Slider.setSizePolicy(sizePolicy)
        self.Stop_Y_Slider.setMinimumSize(QSize(250, 0))
        self.Stop_Y_Slider.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_6.addWidget(self.Stop_Y_Slider)

        self.Stop_Y_PlusButton = QPushButton(Dialog)
        self.Stop_Y_PlusButton.setObjectName(u"Stop_Y_PlusButton")
        self.Stop_Y_PlusButton.setMaximumSize(QSize(20, 20))

        self.horizontalLayout_6.addWidget(self.Stop_Y_PlusButton)


        self.verticalLayout_3.addLayout(self.horizontalLayout_6)


        self.verticalLayout_5.addLayout(self.verticalLayout_3)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)

        self.Feed_X_Label = QLabel(Dialog)
        self.Feed_X_Label.setObjectName(u"Feed_X_Label")

        self.horizontalLayout_3.addWidget(self.Feed_X_Label)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.Feed_X_MinusButton = QPushButton(Dialog)
        self.Feed_X_MinusButton.setObjectName(u"Feed_X_MinusButton")
        self.Feed_X_MinusButton.setMaximumSize(QSize(20, 20))

        self.horizontalLayout_4.addWidget(self.Feed_X_MinusButton)

        self.Feed_X_Slider = QSlider(Dialog)
        self.Feed_X_Slider.setObjectName(u"Feed_X_Slider")
        sizePolicy.setHeightForWidth(self.Feed_X_Slider.sizePolicy().hasHeightForWidth())
        self.Feed_X_Slider.setSizePolicy(sizePolicy)
        self.Feed_X_Slider.setMinimumSize(QSize(250, 0))
        self.Feed_X_Slider.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_4.addWidget(self.Feed_X_Slider)

        self.Feed_X_PlusButton = QPushButton(Dialog)
        self.Feed_X_PlusButton.setObjectName(u"Feed_X_PlusButton")
        self.Feed_X_PlusButton.setMaximumSize(QSize(20, 20))

        self.horizontalLayout_4.addWidget(self.Feed_X_PlusButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)


        self.verticalLayout_5.addLayout(self.verticalLayout_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.Feed_Y_Label = QLabel(Dialog)
        self.Feed_Y_Label.setObjectName(u"Feed_Y_Label")

        self.horizontalLayout_2.addWidget(self.Feed_Y_Label)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.Feed_Y_MinusButton = QPushButton(Dialog)
        self.Feed_Y_MinusButton.setObjectName(u"Feed_Y_MinusButton")
        self.Feed_Y_MinusButton.setMaximumSize(QSize(20, 20))

        self.horizontalLayout.addWidget(self.Feed_Y_MinusButton)

        self.Feed_Y_Slider = QSlider(Dialog)
        self.Feed_Y_Slider.setObjectName(u"Feed_Y_Slider")
        sizePolicy.setHeightForWidth(self.Feed_Y_Slider.sizePolicy().hasHeightForWidth())
        self.Feed_Y_Slider.setSizePolicy(sizePolicy)
        self.Feed_Y_Slider.setMinimumSize(QSize(250, 0))
        self.Feed_Y_Slider.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout.addWidget(self.Feed_Y_Slider)

        self.Feed_Y_PlusButton = QPushButton(Dialog)
        self.Feed_Y_PlusButton.setObjectName(u"Feed_Y_PlusButton")
        self.Feed_Y_PlusButton.setMaximumSize(QSize(20, 20))

        self.horizontalLayout.addWidget(self.Feed_Y_PlusButton)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.verticalLayout_5.addLayout(self.verticalLayout)


        self.gridLayout.addLayout(self.verticalLayout_5, 0, 0, 1, 4)

        self.Button_Offset_Picture = QPushButton(Dialog)
        self.Button_Offset_Picture.setObjectName(u"Button_Offset_Picture")

        self.gridLayout.addWidget(self.Button_Offset_Picture, 1, 0, 1, 1)

        self.horizontalSpacer_9 = QSpacerItem(30, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_9, 1, 1, 1, 1)

        self.Offset_Slider_Button = QDialogButtonBox(Dialog)
        self.Offset_Slider_Button.setObjectName(u"Offset_Slider_Button")
        self.Offset_Slider_Button.setOrientation(Qt.Orientation.Horizontal)
        self.Offset_Slider_Button.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.gridLayout.addWidget(self.Offset_Slider_Button, 1, 2, 1, 1)

        self.horizontalSpacer_10 = QSpacerItem(110, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_10, 1, 3, 1, 1)


        self.retranslateUi(Dialog)
        self.Offset_Slider_Button.accepted.connect(Dialog.accept)
        self.Offset_Slider_Button.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.Stop_X_Label.setText(QCoreApplication.translate("Dialog", u"Stop_X :", None))
        self.Stop_X_MinusButton.setText(QCoreApplication.translate("Dialog", u"-", None))
        self.Stop_X_Plusbutton.setText(QCoreApplication.translate("Dialog", u"+", None))
        self.Stop_Y_Label.setText(QCoreApplication.translate("Dialog", u"Stop_Y:", None))
        self.Stop_Y_MinusButton.setText(QCoreApplication.translate("Dialog", u"-", None))
        self.Stop_Y_PlusButton.setText(QCoreApplication.translate("Dialog", u"+", None))
        self.Feed_X_Label.setText(QCoreApplication.translate("Dialog", u"Feed_X :", None))
        self.Feed_X_MinusButton.setText(QCoreApplication.translate("Dialog", u"-", None))
        self.Feed_X_PlusButton.setText(QCoreApplication.translate("Dialog", u"+", None))
        self.Feed_Y_Label.setText(QCoreApplication.translate("Dialog", u"Feed_Y :", None))
        self.Feed_Y_MinusButton.setText(QCoreApplication.translate("Dialog", u"-", None))
        self.Feed_Y_PlusButton.setText(QCoreApplication.translate("Dialog", u"+", None))
        self.Button_Offset_Picture.setText(QCoreApplication.translate("Dialog", u"\u5716\u7247\u8a2d\u5b9a", None))
    # retranslateUi

