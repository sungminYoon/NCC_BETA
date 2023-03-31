"""
Created by SungMin Yoon on 2021-12-15..
Copyright (c) 2021 year NCC (National Cancer Center). All rights reserved.
"""

from .menu import Menu
from LAB.common.util import convenience
from LAB.config import setting
from PySide6.QtCore import Qt
from PySide6.QtWidgets import *

TITLE_PROPERTY = '5. Property'
TITLE_THRESHOLD = 'Threshold value'

'''
    menu.py 의 
    확장(extends) 클레스 입니다. 
    TEXT 입력 UI 가 구현 되어 있습니다.
'''


class MenuExtends(Menu):
    call_threshold = None  # call_back 객체 입니다. threshold 값을 update 합니다.

    property_group = None  # 속성 그룹 입니다.
    property_btn = None  # ROI 속성 버튼 입니다.

    def __init__(self, parent=None):
        super(MenuExtends, self).__init__(parent)
        print('Menu_extends: init')

        # 속성 버튼
        self.property_btn = QPushButton(TITLE_PROPERTY)
        self.property_btn.clicked.connect(self.propertyButtonClicked)
        self.property_btn.setStyleSheet("QPushButton { text-align: left; }")

        # Label property
        self.label_threshold = QLabel()
        self.label_threshold_value = QLabel()
        convenience.setting_label(self.label_threshold, self.label_threshold_value, TITLE_THRESHOLD)

        # Line Edit
        self.threshold_input = QLineEdit()
        self.setting_line_edit(self.threshold_input)

        # 텍스트 상자 표시
        self.label_threshold_value.setText(f'{setting.THRESHOLD}')

        # layout
        _layout_threshold = QHBoxLayout()

        # 속성
        _property_box = QVBoxLayout()
        _property_box.addLayout(_layout_threshold)

        # 위젯 위치 정렬
        _layout_threshold.addWidget(self.label_threshold, alignment=Qt.AlignLeft)
        _layout_threshold.addWidget(self.label_threshold_value, alignment=Qt.AlignRight)
        _layout_threshold.addWidget(self.threshold_input, alignment=Qt.AlignRight)

        # property 버튼의 하위 라벨 텍스트 입력 위젯 입니다.
        self.property_group = QWidget()
        self.property_group.setLayout(_property_box)
        self.property_group.hide()

    def setting_line_edit(self, q_line: QLineEdit):
        q_line.setText('')
        q_line.setAlignment(Qt.AlignRight)
        q_line.returnPressed.connect(self.lineChanged)
        q_line.setFixedWidth(30)

    # mark - Event method
    def lineChanged(self):
        # label 텍스트 input value 변경
        print('call Menu: lineChanged')

        # 입력 한계값
        limit_threshold = 30

        # 최저 값
        lowest_threshold = 5

        if self.threshold_input.text() is '':
            t_value = self.label_threshold_value.text()
        else:
            t_value = self.threshold_input.text()

            # 입력값 초과시 메시지 알림
            if convenience.check_value(t_value, limit_threshold, lowest_threshold) is True:
                return

        self.label_threshold_value.setText(t_value)

        # view 의 threshold 값을 update 합니다.
        call_threshold = self.call_threshold

        # call back method -> value.
        call_threshold(t_value)
