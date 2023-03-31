"""
Created by SungMin Yoon on 2020-04-27..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""
import os
import time

from PySide6 import QtGui
from PySide6.QtWidgets import *
from PIL import ImageQt
from LAB.common.util import img_convert_dicom, file_manager
from LAB.common.util import notice
from LAB.common.util import convenience
from LAB.config.path import path_local
from LAB.config.error import messages, check

TITLE_IMG_DICOM = '1. DICOM all change'
TITLE_IMG_LOAD = '2. Load image'
TITLE_ALGORITHM = '3. Pre-processing'
TITLE_EXPORT = '4. Export ROI'


class Menu(QVBoxLayout):
    call_scroll = None          # call_back 객체 입니다. 스크롤 데이터 를 생성 또는 가지고 옵니다.
    call_export = None          # call_back 객체 입니다. mask 이미지 를 2진 binary 데이터 로 내보냅 니다.
    call_preprocessing = None   # call_back 객체 입니다. preprocessing 처리를 합니다.

    file_extension = None       # 선택된 파일 확장자 입니다.
    menu_group = None           # 메뉴 그룹 입니다.

    label_logo = None           # 상단 라벨 이미지.
    dicom_btn = None            # dicom 폴더의 모든 dicom 에서 이미지 를 꺼내 png 로 변환 합니다.
    load_btn = None             # png 폴더의 모든 이미지 를 스크롤 에 불러 옵니다.
    export_btn = None           # 이진 binary 데이터 로 내보냄
    pre_processing_btn = None   # 전처리 처리 버튼 입니다.

    def __init__(self, parent=None):
        super(Menu, self).__init__(parent)
        print('Menu: init')

        self.file_extension = 'jpg'

        # logo label
        qim = ImageQt.ImageQt(path_local.UI_MENU_LOGO)
        logo_image = QtGui.QPixmap.fromImage(qim)

        # 이미지 크기를 조종.
        logo_image.setDevicePixelRatio(2.7)
        self.label_logo = QLabel()
        self.label_logo.setScaledContents(True)
        self.label_logo.setPixmap(logo_image)

        # DICOM 파일 에서 이미지 파일 꺼내기
        self.dicom_btn = QPushButton(TITLE_IMG_DICOM)
        self.dicom_btn.clicked.connect(self.changDicomButtonClicked)
        self.dicom_btn.setStyleSheet("QPushButton { text-align: left; }")

        # 이미지 load 버튼
        self.load_btn = QPushButton(TITLE_IMG_LOAD)
        self.load_btn.clicked.connect(self.loadButtonClicked)
        self.load_btn.setStyleSheet("QPushButton { text-align: left; }")

        # export 버튼
        self.export_btn = QPushButton(TITLE_EXPORT)
        self.export_btn.clicked.connect(self.exportButtonClicked)
        self.export_btn.setStyleSheet("QPushButton { text-align: left; }")

        # 전 처리 버튼
        self.pre_processing_btn = QPushButton(TITLE_ALGORITHM)
        self.pre_processing_btn.clicked.connect(self.preButtonClicked)
        self.pre_processing_btn.setStyleSheet("QPushButton { text-align: left; }")

        # ui 화면에 표시
        self.ui_setup()

    def ui_setup(self):

        # 위젯: 그룹
        self.menu_group = QVBoxLayout()
        self.menu_group.addWidget(self.label_logo)
        self.menu_group.addWidget(self.dicom_btn)
        self.menu_group.addWidget(self.load_btn)
        self.menu_group.addWidget(self.pre_processing_btn)
        self.menu_group.addWidget(self.export_btn)

        # 메뉴 그룹을 베이스 Layout 등록 합니다.
        self.addLayout(self.menu_group)

    def exportButtonGreenColor(self):
        print('Menu: exportButtonGreenColor')
        self.export_btn.setStyleSheet('background-color: Green')

    def exportButtonGrayColor(self):
        print('Menu: exportButtonGrayColor')
        self.export_btn.setStyleSheet('background-color: Gray')

    # mark - Event method
    def changeLevelButtonClicked(self):
        print('Menu: changeLevelButtonClicked')
        call = self.call_change_level
        call()

    # mark - Event method
    def changDicomButtonClicked(self):
        print('Menu: changButtonClicked')

        # user 선택한 파일 경로
        file_path = file_manager.file_open()

        if file_path is 0:
            return

        # user 선택한 파일 이름
        last_name = file_path[file_path.rfind('/') + 1:]

        # 파일 이름의 경로 폴더명
        dicom_folder = file_path.replace(last_name, '', 1)

        notice.message('messages..', '아래 Yes 를 누르면 파일 변환을 시작 합니다. 잠시만 기다려 주세요...')

        if check.extension_dicom(dicom_folder):

            # 폴더에 들어 있는 DICOM 에서 PNG 파일 export
            img_folder = file_manager.make_folder_date(dicom_folder)
            img_convert_dicom.dicom_imageToImg(dicom_folder, img_folder, self.file_extension)
            print('DICOM 파일 에서', {self.file_extension}, '파일 내보 내기 완료!')

            # 0.1초 delay 후
            time.sleep(0.1)

            # 썸내일 이미지 만들기
            convenience.check_thumbnail(img_folder)

            # Window method call scroll 에 경로 data send.
            call_data = self.call_scroll
            call_data(img_folder, self.file_extension)
        else:
            notice.message('Error', messages.ERROR_DICOM)
            return

        notice.message('messages..', '파일 변환이 완료. 아래 Yes 를 눌러 주세요!')

    # mark - Event method
    def loadButtonClicked(self):
        print('Menu: loadButtonClicked')

        # user 선택한 파일 경로
        file_path = file_manager.file_open()

        if file_path is 0:
            return

        # user 선택한 file name
        last_name = file_path[file_path.rfind('/') + 1:]
        _, fileExtension = os.path.splitext(last_name)
        image_folder = file_path.replace(last_name, '', 1)

        # 확장자 확인
        chioce = fileExtension

        # 썸내일 이미지 만들기
        convenience.check_thumbnail(image_folder)

        # Window method call scroll 에 경로 data send.
        call_data = self.call_scroll
        call_data(image_folder, chioce)

    # mark - Event method
    def propertyButtonClicked(self):
        print('Menu: propertyButtonClicked')
        if self.property_group.isHidden():
            self.property_group.show()
        else:
            self.property_group.hide()

    # mark - Event method
    def exportButtonClicked(self):
        print('Menu: exportButtonClicked')
        call = self.call_export
        call()

    # mark - Event method
    def preButtonClicked(self):
        print('Menu: algorithmButtonClicked')
        call = self.call_preprocessing
        call()


