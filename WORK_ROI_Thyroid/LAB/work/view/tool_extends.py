"""
Created by SungMin Yoon on 2022-10-25..
Copyright (c) 2022 year NCC (National Cancer Center). All rights reserved.
"""

from ..view.tool import Tool
from PySide6.QtWidgets import QRadioButton, QPushButton

'''
    tool.py 의 
    확장(extends) 클레스 입니다. 
'''


class ToolExtends(Tool):

    def __init__(self):
        super(ToolExtends, self).__init__()
        print('ToolExtends: init')

    # mark - Event method
    def event_json_clicked(self):
        print('Tool: event_json_clicked')
        if self.json_btn.isCheckable() is False:
            self.json_btn.setCheckable(True)
        else:
            self.json_btn.setCheckable(False)
        call = self.call_btn_json
        call(self.json_btn.isCheckable())

    # mark - Event method
    def event_threshold(self):
        print('Tool: event_threshold')

        for i in range(0, len(self.radio_btn_list)):
            btn_t: QRadioButton = self.radio_btn_list[i]

            if btn_t.isChecked() is True:
                self.choice_threshold = i
            else:
                btn_t: QRadioButton = self.radio_btn_list[i]
                btn_t.setChecked(False)

        call = self.call_radio_chk
        call(self.choice_threshold)

    # mark - Event method
    def event_filter(self, sender):
        print('Tool: event_filter')

        # 전체 버튼 색을 Gray color 바꾸고
        for i in range(0, len(self.filter_btn_list)):
            btn_f: QPushButton = self.filter_btn_list[i]
            btn_f.setStyleSheet("background-color: Gray; color: white")

        # 사용자 클릭 버튼은 초록색 으로 변경
        btn: QPushButton = sender
        btn.setStyleSheet("background-color: Green; color: white")

        # string 인트형 으로 바꾸고
        new_string = btn.text()
        new_string = new_string[:1]
        int_value = int(new_string)

        # call back 사용자 선택 필터를 보냄
        self.choice_filter = int_value - 1
        call = self.call_push_filter
        call(self.choice_filter)

    # mark - Event method
    def event_algorithm(self, value):

        # algorithm 버튼 색 gray 초기화
        for btn in self.algorithm_btn_list:
            btn.setStyleSheet("background-color: Gray; color: white")

        # algorithm 사용자 선택 색 green 변경
        self.algorithm_btn_list[value].setStyleSheet("background-color: Green; color: white")

        # 버튼 선택 값 export
        call = self.call_btn_algorithm
        call(value)

    # mark - Event method
    def event_number_clicked(self, sender):
        btn: QPushButton = sender

        # 버튼 활성화
        if btn.isCheckable() is False:
            btn.setCheckable(True)
            btn.setStyleSheet('background-color: gray; color: white')

        # 버튼 비활성
        else:
            btn.setCheckable(False)
            btn.setStyleSheet('background-color: white; color: black')

        # 콜백 으로 버튼 text 보냄.
        call = self.call_btn_number
        call(btn.text())

    # mark - Event method
    def event_re_roi_clicked(self):
        print('tool: event_re_roi_clicked')
        call = self.call_refresh
        call()

    # mark - Event method
    def event_help_clicked(self):
        print('tool: event_help_clicked')
        call = self.call_btn_help
        call()

    # mark - Event method
    def event_zoom_clicked(self, sender):
        print('tool: event_zoom_clicked')
        btn: QPushButton = sender
        name = btn.objectName()

        if name == 'normal':
            self.zoom_btn.setStyleSheet('background-color: white; color: black')
            self.normal_btn.setStyleSheet('background-color: indigo; color: white')
            self.apply_btn.setStyleSheet('background-color: white; color: black')

        if name == 'zoom':
            self.zoom_btn.setStyleSheet('background-color: indigo; color: white')
            self.normal_btn.setStyleSheet('background-color: white; color: black')
            self.apply_btn.setStyleSheet('background-color: white; color: black')

        if name == 'apply':
            self.zoom_btn.setStyleSheet('background-color: white; color: black')
            self.normal_btn.setStyleSheet('background-color: white; color: black')
            self.apply_btn.setStyleSheet('background-color: indigo; color: white')

        call = self.call_btn_zoom
        call(name)

    # mark - Event method
    def showWindowSliderValue(self):
        self.label_value_window.setText(str(self.slider_window.value()))
        call = self.call_level_window
        call(self.slider_window.value())

    # mark - Event method
    def showMuscleSliderValue(self):
        self.label_value_muscle.setText(str(self.slider_muscle.value()))
        call = self.call_level_muscle
        call(self.slider_muscle.value())

    # mark - Event method
    def showStartSliderValue(self):
        self.label_value_start.setText(str(self.slider_start.value()))
        call = self.call_process_start
        call(self.slider_start.value())

    def showEndSliderValue(self):
        self.label_value_end.setText(str(self.slider_end.value()))
        call = self.call_process_end
        call(self.slider_end.value())

    # mark - Call back method: window_method
    def set_slider_window(self, value):
        self.slider_window.setValue(value)

    # mark - Call back method: window_method
    def set_slider_muscle(self, value):
        self.slider_muscle.setValue(value)

    # mark - Call back method: window_method
    def set_select_image(self, value):
        index = f': {value}'
        self.select_label.setText(index)