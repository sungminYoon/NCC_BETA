"""
Created by SungMin Yoon on 2020-04-27..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import *
from LAB.config.path import path_local
from LAB.config import setting

TITLE_HELP = 'Help?'
TITLE_PATH = 'Path'
TITLE_ROI = 'ROI Image'
TITLE_WINDOW = 'Window'
TITLE_MUSCLE = 'Muscle'
TITLE_START = 'Start'
TITLE_END = 'End'
TITLE_FILTER_CHOICE = 'Img  Filter'
TITLE_THRESHOLD_CHOICE = 'Threshold'
TITLE_BTN_ALGORITHM = 'Algorithm'
TITLE_BTN_REFRESH = 'Refresh'
TITLE_BTN_JSON = 'Json'
TITLE_BTN_Normal = 'Normal'
TITLE_BTN_ZOOM = 'Zoom'
TITLE_BTN_APPLY = 'Apply'

VALUE_SELECT_IMAGE = ': No select image'
VALUE_DEFAULT_WINDOW = 800
VALUE_DEFAULT_MUSCLE = 0
VALUE_DEFAULT_START = 0
VALUE_DEFAULT_END = 0


class Tool(QHBoxLayout):

    call_refresh = None             # 콜백 메소드 ROI 전체 삭제 버튼
    call_radio_chk = None           # 콜백 라디오 버튼 Threshold 선택
    call_push_filter = None         # 콜백 라디오 버튼 필터 선택
    call_level_window = None        # 콜백 메소드 윈도우
    call_level_muscle = None        # 콜백 메소드 근육
    call_process_start = None       # 콜백 이미지 처리 시작점
    call_process_end = None         # 콜백 이미지 처리 종료점
    call_btn_algorithm = None       # 콜백 Algorithm 버튼
    call_btn_json = None            # 콜백 JSON
    call_btn_number = None          # 콜백 NUMBER 버튼
    call_btn_help = None            # 콜백 Help 버튼
    call_btn_zoom = None            # 콜백 Zoom 버튼
    call_btn_normal = None          # 콜백 Normal 버튼
    call_btn_apply = None           # 콜백 사용자 선택 적용 버튼

    choice_threshold = None         # 사용자 선택 조직
    choice_filter = None            # 사용자 선택 필터
    slider_window = None            # slider 윈도우
    slider_muscle = None            # slider 근육
    slider_start = None             # slider 이미지 처리 시작점
    slider_end = None               # slider 이미지 처리 종료점

    # 버튼 리스트
    algorithm_btn_list = None       # algorithm 버튼 리스트
    radio_btn_list = None           # Threshold 선택 리스트
    filter_btn_list = None          # filter 선택 리스트

    # event method
    showWindowSliderValue = None
    showMuscleSliderValue = None
    showStartSliderValue = None
    showEndSliderValue = None
    event_threshold = None
    event_filter = None
    event_algorithm = None
    event_re_roi_clicked = None
    event_json_clicked = None
    event_number_clicked = None
    event_help_clicked = None

    def __init__(self, parent=None):
        super(Tool, self).__init__(parent)

        # Title
        self.filter_title = QLabel()
        self.radio_title = QLabel()
        self.filter_title.setText(TITLE_FILTER_CHOICE)
        self.radio_title.setText(TITLE_THRESHOLD_CHOICE)

        # help 버튼 생성
        self.help_btn = QPushButton()
        self.help_btn.setText(TITLE_HELP)
        self.help_btn.clicked.connect(self.event_help_clicked)

        # filter 버튼 생성
        self.filter_btn_list = [None for _ in range(len(setting.FILTER))]
        for i in range(0, len(self.filter_btn_list)):

            # setting 정해진 이름을 가지고 옵니다.
            name = f'{i+1} {setting.FILTER[i]}'

            # 버튼 생성
            self.filter_btn_list[i] = QPushButton(name)
            push: QPushButton = self.filter_btn_list[i]
            push.clicked.connect(lambda stat=False, param=push:
                                 self.event_filter(param))

            # 초기 설정
            if i is 0:
                push.setStyleSheet('background-color: Green; color: white')
            else:
                push.setStyleSheet('background-color: Gray; color: white')

        # Radio threshold 버튼 생성
        self.radio_btn_list = [None for _ in range(setting.USER_CHOICE_COUNT)]
        for i in range(0, setting.USER_CHOICE_COUNT):
            name = f'{i+1}'

            # 라디오 버튼 생성
            self.radio_btn_list[i] = QRadioButton(name)
            radio: QRadioButton = self.radio_btn_list[i]
            radio.clicked.connect(self.event_threshold)

            # 초기 설정 및 라디오 버튼 Title text
            if i is 0:
                radio.setChecked(True)

        # algorithm 버튼 생성
        self.algorithm_btn_list = [None for _ in range(len(setting.ALGORITHM))]
        btn_count = len(setting.ALGORITHM)
        for i in range(0, btn_count):
            self.algorithm_btn_list[i] = QPushButton()
            btn: QPushButton = self.algorithm_btn_list[i]
            btn.setText(setting.ALGORITHM[i])
            btn.setGeometry(0, 0, 50, 50)
            btn.setIconSize(QSize(20, 20))
            btn.setChecked(True)
            btn.setStyleSheet('background-color: gray; color: white')
            btn.clicked.connect(lambda stat=False, param=i: self.event_algorithm(param))

            if i is 0:
                btn.setStyleSheet('background-color: green; color: white')

        # zoom 버튼 생성
        self.zoom_btn = QPushButton()
        self.zoom_btn.setText(TITLE_BTN_ZOOM)
        self.zoom_btn.clicked.connect(lambda stat=False, param=self.zoom_btn: self.event_zoom_clicked(param))
        self.zoom_btn.setObjectName('zoom')
        self.zoom_btn.setStyleSheet('background-color: white; color: black')

        # 보통 화면 전환 버튼
        self.normal_btn = QPushButton()
        self.normal_btn.setText(TITLE_BTN_Normal)
        self.normal_btn.clicked.connect(lambda stat=False, param=self.normal_btn: self.event_zoom_clicked(param))
        self.normal_btn.setObjectName('normal')
        self.normal_btn.setStyleSheet('background-color: Indigo; color: white')

        # 사용자 선택 적용 버튼
        self.apply_btn = QPushButton()
        self.apply_btn.setText(TITLE_BTN_APPLY)
        self.apply_btn.clicked.connect(lambda stat=False, param=self.apply_btn: self.event_zoom_clicked(param))
        self.apply_btn.setObjectName('apply')
        self.apply_btn.setStyleSheet('background-color: white; color: black')

        # Tool UI
        self.verticalBox = QVBoxLayout()
        self.top_box = QHBoxLayout()
        self.top_path = QHBoxLayout()
        self.top_child_box = QHBoxLayout()
        self.level_box = QHBoxLayout()
        self.btn2_box = QHBoxLayout()
        self.refresh_box = QHBoxLayout()
        self.filter_box = QHBoxLayout()
        self.radio_box = QHBoxLayout()
        self.json_box = QHBoxLayout()
        self.zoom_box = QHBoxLayout()
        self.result_box = QVBoxLayout()

        self.slider_box_top = QHBoxLayout()
        self.slider_box_middle = QHBoxLayout()
        self.slider_box_down = QHBoxLayout()
        self.slider_box_floor = QHBoxLayout()

        # Algorithm 버튼
        self.btn1_box = QHBoxLayout()
        self.btn1_box.setAlignment(Qt.AlignLeft)
        self.title_label = QLabel(TITLE_PATH)
        self.title_count = QLabel(TITLE_ROI)
        self.title_algorithm = QLabel(TITLE_BTN_ALGORITHM)
        self.select_label = QLabel(VALUE_SELECT_IMAGE)

        # Refresh ROI 해재 버튼
        self.re_label = QLabel(TITLE_BTN_REFRESH)
        self.re_btn = QPushButton()
        self.re_btn.setGeometry(0, 0, 50, 50)
        self.re_btn.setIcon(QIcon(path_local.UI_BTN_RED))
        self.re_btn.setIconSize(QSize(20, 20))
        self.re_btn.clicked.connect(self.event_re_roi_clicked)
        self.re_btn.setChecked(True)

        # json label 버튼
        self.json_label = QLabel(TITLE_BTN_JSON)
        self.json_btn = QPushButton()
        self.json_btn.setGeometry(0, 0, 50, 50)
        self.json_btn.setIcon(QIcon(path_local.UI_BTN_L))
        self.json_btn.setIconSize(QSize(20, 20))
        self.json_btn.clicked.connect(self.event_json_clicked)
        self.json_btn.setCheckable(True)

        # Level Window
        self.window_label = QLabel(' : level')

        # Level Muscle
        self.muscle_label = QLabel(' : level')

        # process start & end
        self.start_process_label = QLabel(' : number')
        self.end_process_label = QLabel(' : number')

        # slider 라벨 생성
        window_value_str = f'{VALUE_DEFAULT_WINDOW}'
        muscle_value_str = f'{VALUE_DEFAULT_MUSCLE}'
        start_value_str = f'{VALUE_DEFAULT_START}'
        end_value_str = f'{VALUE_DEFAULT_END}'

        self.label_title_window = QLabel(TITLE_WINDOW)
        self.label_title_muscle = QLabel(TITLE_MUSCLE)
        self.label_title_start = QLabel(TITLE_START)
        self.label_title_end = QLabel(TITLE_END)

        self.label_value_window = QLabel(window_value_str)
        self.label_value_muscle = QLabel(muscle_value_str)
        self.label_value_start = QLabel(start_value_str)
        self.label_value_end = QLabel(end_value_str)

        # slider 생성
        self.slider_window = QSlider(Qt.Horizontal, None)
        self.slider_window.move(100, 2000)
        self.slider_window.setRange(100, 2000)
        self.slider_window.setSingleStep(1)
        self.slider_window.setValue(VALUE_DEFAULT_WINDOW)
        self.slider_window.valueChanged.connect(self.showWindowSliderValue)

        self.slider_muscle = QSlider(Qt.Horizontal, None)
        self.slider_muscle.move(0, 1000)
        self.slider_muscle.setRange(0, 1000)
        self.slider_muscle.setSingleStep(1)
        self.slider_muscle.setValue(VALUE_DEFAULT_MUSCLE)
        self.slider_muscle.valueChanged.connect(self.showMuscleSliderValue)

        self.slider_start = QSlider(Qt.Horizontal, None)
        self.slider_start.move(0, 1000)
        self.slider_start.setRange(0, 1000)
        self.slider_start.setSingleStep(1)
        self.slider_start.setValue(0)
        self.slider_start.valueChanged.connect(self.showStartSliderValue)

        self.slider_end = QSlider(Qt.Horizontal, None)
        self.slider_end.move(0, 1000)
        self.slider_end.setRange(0, 1000)
        self.slider_end.setSingleStep(1)
        self.slider_end.setValue(0)
        self.slider_end.valueChanged.connect(self.showEndSliderValue)

        # 줌박스 좌측 정렬
        self.zoom_box.setAlignment(Qt.AlignLeft)

        self.ui_setup()

    def ui_setup(self):

        # Mount to Widget
        self.top_box.addLayout(self.top_path)
        self.top_box.addLayout(self.top_child_box)
        self.top_path.setAlignment(Qt.AlignLeft)
        self.top_path.addWidget(self.title_label, alignment=Qt.AlignLeft)
        self.top_path.addWidget(self.select_label, alignment=Qt.AlignLeft)
        self.top_child_box.addWidget(self.help_btn, alignment=Qt.AlignRight)

        # filter 선택 버튼
        self.filter_box.addWidget(self.filter_title, alignment=Qt.AlignLeft)
        self.filter_box.setAlignment(Qt.AlignLeft)
        for i in range(0, len(self.filter_btn_list)):
            self.filter_box.addWidget(self.filter_btn_list[i])
        self.btn2_box.addLayout(self.filter_box)

        # algorithm 선택 버튼
        self.btn1_box.addWidget(self.title_algorithm, alignment=Qt.AlignLeft)
        for i in range(0, len(self.algorithm_btn_list)):
            algorithm_button: QPushButton = self.algorithm_btn_list[i]
            self.btn1_box.addWidget(algorithm_button)

        # 라디오 선택 버튼
        self.radio_box.addWidget(self.radio_title, alignment=Qt.AlignLeft)
        for i in range(0, len(self.radio_btn_list)):
            radio_button: QRadioButton = self.radio_btn_list[i]
            radio_button.setStyleSheet('QRadioButton::indicator { width: 15px; height: 15px;};')
            self.radio_box.addWidget(radio_button, alignment=Qt.AlignRight)
        self.radio_box.addLayout(self.refresh_box)
        self.radio_box.addLayout(self.json_box)

        # slider
        self.slider_box_top.addWidget(self.label_title_window)
        self.slider_box_top.addWidget(self.slider_window)
        self.slider_box_top.addWidget(self.label_value_window)
        self.slider_box_top.addWidget(self.window_label)

        self.slider_box_middle.addWidget(self.label_title_muscle)
        self.slider_box_middle.addWidget(self.slider_muscle)
        self.slider_box_middle.addWidget(self.label_value_muscle)
        self.slider_box_middle.addWidget(self.muscle_label)

        self.slider_box_down.addWidget(self.label_title_start)
        self.slider_box_down.addWidget(self.slider_start)
        self.slider_box_down.addWidget(self.label_value_start)
        self.slider_box_down.addWidget(self.start_process_label)

        self.slider_box_floor.addWidget(self.label_title_end)
        self.slider_box_floor.addWidget(self.slider_end)
        self.slider_box_floor.addWidget(self.label_value_end)
        self.slider_box_floor.addWidget(self.end_process_label)

        # roi 해제 버튼 등록
        self.refresh_box.addWidget(self.re_label, alignment=Qt.AlignRight)
        self.refresh_box.addWidget(self.re_btn, alignment=Qt.AlignRight)
        self.refresh_box.setAlignment(Qt.AlignRight)

        # json 쓰기 지우기 테이블
        self.json_box.addWidget(self.json_label, alignment=Qt.AlignRight)
        self.json_box.addWidget(self.json_btn, alignment=Qt.AlignRight)
        self.json_box.setAlignment(Qt.AlignRight)

        # zoom
        self.zoom_box.addWidget(self.normal_btn, alignment=Qt.AlignLeft)
        self.zoom_box.addWidget(self.zoom_btn, alignment=Qt.AlignLeft)
        self.zoom_box.addWidget(self.apply_btn, alignment=Qt.AlignLeft)

        # 최상단 툴 박스에 Layout 등록
        self.verticalBox.addLayout(self.top_box)
        self.verticalBox.addLayout(self.btn1_box)
        self.verticalBox.addLayout(self.btn2_box)
        self.verticalBox.addLayout(self.slider_box_top)
        self.verticalBox.addLayout(self.slider_box_middle)
        self.verticalBox.addLayout(self.slider_box_down)
        self.verticalBox.addLayout(self.slider_box_floor)
        self.verticalBox.addLayout(self.radio_box)
        self.verticalBox.addLayout(self.result_box)
        self.verticalBox.addLayout(self.zoom_box)

        # 검증 박스 장착
        self.addLayout(self.verticalBox)

    # layout 안의 widget 을 delete 합니다.
    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget() is not None:
                    child.widget().deleteLater()
                elif child.layout() is not None:
                    self.clearLayout(child.layout())

    def create_result_btn(self, index_list):

        # layout 초기화
        self.clearLayout(self.result_box)

        # 버튼 왼쪽 정렬
        # self.result_box.setAlignment(Qt.AlignLeft)
        count = len(index_list)

        # index 버튼 1열 생성
        number_box = QHBoxLayout()
        number_box.setAlignment(Qt.AlignLeft)
        self.result_box.addLayout(number_box)

        j = 1
        # 버튼 생성 카운트
        for i in range(0, count):
            obj = index_list[i]

            # 20 개 index 버튼 생성 되면
            if j % 30 == 0:
                number_box = QHBoxLayout()
                number_box.setAlignment(Qt.AlignLeft)
                self.result_box.addLayout(number_box)

            if obj == 0:
                pass
            else:
                # index 버튼 생성
                j = j + 1
                _, index = obj
                text = f'{index+1}'
                result_button = QPushButton()
                result_button.setText(text)
                result_button.setFixedSize(35, 25)
                result_button.clicked.connect(lambda stat=False, parameter=result_button: self.event_number_clicked(parameter))
                number_box.addWidget(result_button)



