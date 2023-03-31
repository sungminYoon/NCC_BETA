"""
Created by SungMin Yoon on 2022-10-31..
Copyright (c) 2022 year NCC (National Cancer Center). All rights reserved.
"""
from PySide6 import QtGui, QtCore
from PySide6.QtWidgets import *
from PIL import ImageQt
from LAB.config.path import path_local


class Popup(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        # popup 들어갈 이미지
        qim = ImageQt.ImageQt(path_local.UI_HELP)
        pixMap = QtGui.QPixmap.fromImage(qim)

        # popup box 생성
        self.popup_box = QVBoxLayout()

        # Scroll 생성
        self.imageScrollArea = QScrollArea()
        self.imageScrollArea.setWidgetResizable(True)

        # image label 생성
        self.imageLabel = QLabel()
        self.imageLabel.setPixmap(pixMap)
        self.imageLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.imageScrollArea.setWidget(self.imageLabel)

        # box 에 image label 을 넣어 줍니다.
        self.popup_box.addWidget(self.imageScrollArea)
        self.setLayout(self.popup_box)


