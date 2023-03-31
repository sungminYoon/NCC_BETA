"""
Created by SungMin Yoon on 2021-06-07..
Copyright (c) 2021 year NCC (National Cancer Center). All rights reserved.
"""
from PIL import ImageQt
from PySide6 import QtCore
from PySide6.QtCore import QSize
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from LAB.config import setting
from LAB.config.path import path_local
from ..common.oop.img_text import ImgText
from ..common.oop.merge import Merge

from .view.tool_extends import ToolExtends
from .view.menu_extends import MenuExtends
from .view.view_center import ViewCenter
from .view.view_second import ViewSecond
from .view.table_image import TableImage
from .view.table_right_extends import TableRightExtends
from .view.table_label import TableLabel
from .view.popup import Popup

from .control.auto import Auto
from .control.provider import Provider
from .control.filter import Filter


class Window(QWidget):

    """CONTROL"""
    auto = None                     # 자동 이미지 처리
    provider = None                 # 이미지 DATA 공급자
    filter = None                   # 이미지 필터

    """TABLE"""
    scroll_img = None               # 좌측 스크롤 이미지
    scroll_right = None             # 우측 스크롤 2줄
    scroll_label = None             # 우측 끝 스크롤 라벨
    table_label = None              # 우측 끝 라벨 테이블
    table_img = None                # 좌측 이미지 테이블
    table_right = None              # 우측 2줄 테이블

    """TOOL"""
    tool = None                     # 상단 도구 버튼 모음 입니다.
    level_window_value = None       # 화면에 보여 지는 뷰의 윈도우 레벨 값
    level_muscle_value = None       # 화면에 보여 지는 뷰의 근육 레벨 값
    start_value = None              # 사용자 지정 이미지 처리 시작점
    end_value = None                # 사용자 지정 이미지 처리 종료점
    progress_bar = None             # 진행 바

    """MENU"""
    menu = None                     # 좌측 상단 File Menu 버튼 모음 입니다.

    """VIEW"""
    view_center = None              # 화면에 보여 지는 image 뷰 입니다.
    view_second = None              # 화면에 보여 지는 zoom 뷰 입니다.
    popup = None

    """ACTIVE VALUE"""
    label_current_image = None          # 선택된 이미지 label path 표시 입니다.
    active_path = None                  # 뷰에 활성화 된 이미지 경로
    active_image_index = None           # 뷰에 활성화 된 이미지 인덱스 번호
    filter_check_number = None          # 사용자 선택 필터 번호
    radio_current_number = None         # 사용자 선택 현재 툴 라디오 버튼
    algorithm_choice_list: list = None  # algorithm 선택 저장 리스트
    one3d_complete_list: list = None    # export 하나의 3D 객체 생성 할 수 있는 리스트 입니다.
    group_complete_list: list = None    # export 마스크 리스트 입니다.
    input_cv_list: list = None          # 입력 되는(필터 처리) CV 이미지 리스트 입니다.

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        '''Default value'''
        self.active_path = path_local.ROOT_DIR

        '''Create'''
        self.group_complete_list = []
        self.pre_complete_list = []
        self.input_cv_list = []
        self.pickle_name_list = []
        self.pkl_name_list = []
        self.dataSet_time = []
        self.algorithm_choice_list = [0 for _ in range(setting.USER_CHOICE_COUNT)]

        # 이미지 -> 텍스트 변환기 생성
        self.image_text = ImgText()
        self.image_text.call_progress = self.progress_value

        # roi 병합 객체 생성
        self.merge = Merge()

        # 컨트롤 클래스 생성
        self.auto = Auto()
        self.provider = Provider()
        self.filter = Filter()
        self.filter_check_number = 0

        # 윈도우 세팅
        self.setWindowTitle(setting.TITLE_WINDOW)
        self.setGeometry(0, 0, setting.WINDOW_SCREEN_WIDTH, setting.WINDOW_SCREEN_HEIGHT)

        # View 생성
        self.view_center = ViewCenter()
        self.view_center.setup()
        self.view_center.threshold = setting.THRESHOLD
        self.view_center.tool_radio_chk = 0
        self.view_second = ViewSecond()
        self.view_second.default_rect = self.geometry().getRect()
        self.view_second.hide()
        self.popup = Popup()

        # 메뉴 생성
        self.menu = MenuExtends()
        self.menu.menu_group.addWidget(self.menu.property_btn)      # 메뉴 확장 위젯 등록
        self.menu.menu_group.addWidget(self.menu.property_group)    # 메뉴 확장 위젯 그룹

        # 툴 생성
        self.tool = ToolExtends()

        # 스크롤 생성
        self.scroll_img = QScrollArea()
        self.scroll_right = QScrollArea()
        self.scroll_label = QScrollArea()
        self.scroll_prediction = QScrollArea()
        self.scroll_training = QScrollArea()

        # 테이블 생성
        self.table_right = TableRightExtends()
        self.table_img = TableImage()
        self.table_label = TableLabel()

        # 진행바 생성
        qim = ImageQt.ImageQt(path_local.UI_BTN_GREEN)
        _bar = QPixmap.fromImage(qim)
        _bar.setDevicePixelRatio(6)
        self.progress_bar = QLabel()
        self.progress_bar.setScaledContents(True)
        self.progress_bar.setPixmap(_bar)
        self.progress_bar.setFixedSize(QSize(0, 10))

        '''Setting'''
        # 세팅 선택 된 이미지 (넘버)표시 라벨
        self.label_current_image = QLabel()
        self.label_current_image.setText('<font color="White">_No select image</font>')
        self.label_current_image.setFixedHeight(30)
        self.label_current_image.setStyleSheet("background-color: Purple")

        # 세팅 LEVEL 값 초기화
        self.level_window_value = setting.DEFAULT_LEVEL_WINDOW
        self.level_muscle_value = setting.DEFAULT_LEVEL_MUSCLE

        '''Call back method'''
        # Menu 콜백 객체에 Window method 등록 합니다.
        self.menu.call_scroll = self.scroll_data
        self.menu.call_export = self.mask_export
        self.menu.call_preprocessing = self.btn_preprocessing
        self.menu.call_threshold = self.threshold_update

        # Tool 콜백 객체에 Window method 등록 합니다.
        self.tool.call_refresh = self.clean_roi
        self.tool.call_level_window = self.level_window
        self.tool.call_level_muscle = self.level_muscle
        self.tool.call_process_start = self.start_point
        self.tool.call_process_end = self.end_point
        self.tool.call_radio_chk = self.tool_radio_number
        self.tool.call_push_filter = self.tool_radio_filter
        self.tool.call_btn_algorithm = self.btn_algorithm
        self.tool.call_btn_json = self.btn_json
        self.tool.call_btn_number = self.btn_number
        self.tool.call_btn_help = self.doit
        self.tool.call_btn_zoom = self.zoom

        # Auto 콜백 객체에 Window method 등록 합니다.
        self.auto.call_progress = self.progress_value
        self.auto.max_value = setting.PROPERTY_MIN
        self.auto.min_value = setting.PROPERTY_MAX

        # View 콜백 객체에 Window method 등록 합니다.
        self.view_center.call_click_threshold = self.view_label_update
        self.view_second.call_window_rect = self.window_rect
        self.view_second.call_sync_mask = self.sync_mask

        # Table 콜백 객체에 Window method 등록 합니다.
        self.table_img.call_back = self.re_setting
        self.table_right.call_progress = self.progress_value
        self.table_label.call_path = self.get_active_path
        self.table_label.call_index = self.get_active_index
        self.table_label.call_window = self.get_window
        self.table_label.call_muscle = self.get_muscle
        self.table_label.call_load_view = self.view_handling

        self.ui_setup()

    def ui_setup(self):
        print('Window: ui_setup')

        # 전체폼 박스
        form_box = QHBoxLayout()
        _frame_box = QVBoxLayout()
        _top = QVBoxLayout()
        _left = QVBoxLayout()
        _center = QHBoxLayout()
        _view_box = QVBoxLayout()
        _label_box = QVBoxLayout()
        _right = QVBoxLayout()
        _ai_box = QHBoxLayout()

        # 스크롤 뷰 등록
        _right.addWidget(self.scroll_right)

        # image view 등록
        self.view_center.setFixedSize(515, 530)
        self.view_second.setFixedSize(515, 530)
        self.view_center.setStyleSheet('background-color: Gray;')
        self.view_second.setStyleSheet('background-color: Gray;')
        _view_box.addWidget(self.view_center)
        _view_box.addWidget(self.view_second)

        # 스크롤 라벨 테이블 등록
        self.scroll_label.hide()
        _label_box.addWidget(self.scroll_label, alignment=QtCore.Qt.AlignLeft)

        # left layout
        _left.addLayout(self.menu)
        _left.addLayout(_ai_box)
        _left.addWidget(self.label_current_image)
        _left.addWidget(self.scroll_img)

        # top layout
        _top.setAlignment(QtCore.Qt.AlignTop)
        _top.addLayout(self.tool)
        _top.addWidget(self.progress_bar)

        # 창을 늘여도 왼쪽 상단 고정
        _center.setAlignment(QtCore.Qt.AlignLeft)
        _view_box.setAlignment(QtCore.Qt.AlignTop)
        _label_box.setAlignment(QtCore.Qt.AlignTop)
        _right.setAlignment(QtCore.Qt.AlignTop)

        # 중앙 layout 위젯 등록
        _center.addLayout(_view_box)
        _center.addLayout(_right)
        _center.addLayout(_label_box)

        # 툴과 뷰를 프레임 박스에 넣기
        _frame_box.addLayout(_top)
        _frame_box.addLayout(_center)

        # 전체 form box 배치
        form_box.addLayout(_left)
        form_box.addLayout(_frame_box)
        form_box.setStretchFactor(_left, 0)
        form_box.setStretchFactor(_frame_box, 1)

        # layout 폼박스 등록
        self.setLayout(form_box)
        self.show()














