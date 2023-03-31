"""
Created by SungMin Yoon on 2021-06-07..
Copyright (c) 2021 year NCC (National Cancer Center). All rights reserved.
"""

import copy
from LAB.common.util import notice
from LAB.common.util import file_manager
from LAB.common.util import json_parser
from .window import Window

'''
    window.py 의 method 클레스 입니다. 
    ui 의 method 들이 구현 되어 있습니다.
'''


class WindowMethod(Window):

    def __init__(self, parent=None):
        super(WindowMethod, self).__init__(parent)
        print('WindowMethod: init')

    # mark -  Call back method: table_label -> save
    def get_active_path(self):
        return self.active_path

    # mark -  Call back method: table_label -> save
    def get_active_index(self):
        return self.active_image_index

    # mark -  Call back method: table_label -> save
    def get_window(self):
        return self.level_window_value

    # mark -  Call back method: table_label -> save
    def get_muscle(self):
        return self.level_muscle_value

    # mark -  Call back method: menu_extends -> menu_extends
    def threshold_update(self, value):
        value_int = int(value)

        # 중앙 뷰의 threshold 를 update 합니다.
        self.view_center.threshold = value_int

        # table 모든 뷰의 threshold 를 update 합니다.
        self.table_right.cell_threshold_update(value_int)

    # mark -  Call back method: tool
    def btn_algorithm(self, value):
        print('WindowMethod: btn_algorithm =', value)
        radio_number = self.radio_current_number
        if radio_number is None:
            radio_number = 0
        n = int(radio_number)
        self.algorithm_choice_list[n] = value

    # mark -  Call back method: menu
    def btn_preprocessing(self):
        print('WindowMethod: btn_preprocessing')

        # 전 처리 준비
        self.auto.clean()
        self.pre_complete_list.clear()

        # 사용자 선택 threshold 를 roi 로 생성 합니다.
        masks = self.view_center.get_mask_list()
        self.auto.create_roi(masks)

        # 사용자 마스크 데이터 유무 판정
        if masks[0] is None:
            return 0
        else:
            notice.message('algorithm 처리를 시작 합니다!', '잠시만 기다려 주세요!')

        # cv 이미지 들을 가져 옵니다.
        cv_images = self.input_cv_list

        # open cv image roi 처리 method 에 입력 합니다.
        group = self.auto.handler_roi(cv_images,
                                      self.start_value,
                                      self.end_value,
                                      self.active_image_index,
                                      self.algorithm_choice_list)

        result = self.merge.auto_result_image(group, cv_images)
        self.pre_complete_list = result
        self.group_complete_list = group

        # 결과를 우측 table 입력 합니다.
        self.table_right.window_value = self.level_window_value
        self.table_right.muscle_value = self.level_muscle_value
        self.table_right.create(result, group, self.auto.color_list, cv_images)
        self.table_right.ui_setup()

        # 처리 결과 table 화면 scroll 보여 줍니다.
        self.scroll_right.setWidget(self.table_right.top_widget)
        self.scroll_right.show()

        # 처리 결과 table cell 이동 가능한 버튼을 생성 합니다.
        self.tool.create_result_btn(result)

        # 진행 바 초기화
        self.progress_bar.setFixedSize(0, 10)

        notice.message('알림!', '영상 처리 완료. \n '
                              '다른 이미지 처리를 하려면 Refresh 후 진행 하세요!')

    # mark -  Call back method: tool
    def btn_json(self, sw):
        if sw is True:
            self.scroll_label.hide()
        else:
            self.scroll_label.show()

    # mark -  Call back method: tool
    def btn_number(self, index):
        print('WindowMethod: btn_number')
        number = int(index)
        h = number * 512

        # 스크롤 포커스 이동
        v = self.scroll_right.verticalScrollBar()
        v.setSliderPosition(h)

    # mark -  Call back method: menu
    def mask_export(self):
        print('WindowMethod: mask_export')

        # export 할 결과 데이터 저장
        self.group_complete_list, self.one3d_complete_list = self.table_right.get_export_data()

        if len(self.group_complete_list) < 1:
            notice.message('Error', 'Data 없음. \n ROI 선택 후 Algorithm 처리를 하세요!')
            return 0

        notice.message('알림', '잠시만 기다려 주세요! \n export 시작 합니다.')
        folder = file_manager.folder_path(self.active_path)

        # 날짜 이름을 가진 폴더를 생성 합니다.
        day_folder = file_manager.make_folder_date(folder)

        # 사용자 선택 마스크 테이블 과 export list 와 비교 후 export 리스트 교정
        result = self.image_text.list_compare(self.group_complete_list, self.table_right.user_select_list)

        # roi 그룹 풀어 1차원 리스트 만들기
        one_dimension = self.image_text.to_1_dimension(result)

        # 마스크 binary 변환 합니다.
        # 마스크 text -> image 변환 합니다.
        self.image_text.to_binary_group(day_folder, one_dimension)
        self.image_text.to_binary_one(day_folder, self.one3d_complete_list)

        # mask 좌표로 변환 합니다.
        json_parser.mask_position_save_text(day_folder, self.table_right.contour_list)

        msg = f'위치: {day_folder} 에 폴더를 생성. 완료!'
        notice.message('알림', msg)

        # 자동 폴더 열기
        file_manager.auto_open(day_folder)

    # mark -  Call back method: menu
    def threshold_input(self, update):
        self.view_center.threshold = int(update)

    # mark -  Call back method: menu
    def threshold_max(self, update):
        self.auto.level_logic.max_size = int(update)
        self.auto.roi_logic.max_size = int(update)

    # mark -  Call back method: menu
    def threshold_min(self, update):
        self.auto.level_logic.min_size = int(update)
        self.auto.roi_logic.min_size = int(update)

    # mark -  Call back method: menu
    def scroll_data(self, img_folder, extension):
        print('WindowMethod: scroll_data')

        # 필터 저장 list 초기화
        self.filter.save_img_list = None

        # 공급자 class 데이터 생성
        self.provider.info_list = []
        self.provider.create(img_folder, extension)
        self.provider.data_read()

        # table 데이터 넣기
        self.table_img.create(self.provider.info_list)
        self.scroll_img.setWidget(self.table_img.top_widget)

        # ui - tool 의 slider_start 범위를 설정 합니다.
        self.tool.slider_start.setRange(0, len(self.provider.img_container))
        self.tool.slider_end.setRange(0, len(self.provider.img_container))

        if self.end_value is None:
            self.end_value = len(self.provider.img_container)
        self.tool.label_value_end.setText(f'{self.end_value}')

        # 인풋 리스트(필터 처리전 원본 이미지)에 image 공급 합니다.
        self.input_cv_list = copy.copy(self.provider.img_container)

        # 테이블 라벨을 세팅 합니다.
        self.table_label.json_auto_read(img_folder)
        self.scroll_label.setWidget(self.table_label.top_widget)

    # mark -  Call back method: tool
    def tool_radio_number(self, chk_number):
        print('WindowMethod: tool_radio')
        self.view_center.user_threshold_change(chk_number)
        self.view_second.set_user_threshold(chk_number)
        self.radio_current_number = chk_number

        # 사용자 radio 변경 하면 해당 algorithm 표시로 변경 합니다.
        self.tool.event_algorithm(self.algorithm_choice_list[chk_number])

        # 오른쪽 결과 table 툴에서 체크된 라이오 넘버를 저장 합니다.
        self.table_right.set_radio_number(chk_number)

    def tool_radio_filter(self, chk_number):
        print('WindowMethod: tool_radio_filter')

        if self.active_image_index is None:
            notice.message('알림', '선택된 image 없음. \n 이미지 를 먼저 load 후 선택해 주세요!')

            # 라디오 버튼 초기 값으로 되돌 리기
            self.filter_check_number = 0
            return
        else:
            notice.message('알림', '필터 처리를 시작 합니다.')

        # 체크된 필터를 기억 합니다.
        self.filter_check_number = chk_number

        # 공급 자에서 cv 이미지 들을 가져 옵니다.
        cv_images = self.provider.img_container

        # 무수정 이미지 리스트 저장
        if self.filter.save_img_list is None:
            self.filter.save_img_list = copy.deepcopy(cv_images)

        # 필터 처리를 진행 합니다.
        filter_img_list = self.filter.choice(chk_number, cv_images)

        # 필터 처리된 이미지 list 저장 하고 reset 합니다.
        self.input_cv_list = filter_img_list
        self.re_setting(self.active_path, self.active_image_index)

        notice.message('알림', '필터 처리가 완료 되었 습니다.')

    # mark -  Call back method: tool
    def clean_roi(self):
        print('WindowMethod: clean_roi')

        # 선택한 roi, mask clean
        view_mask_list: list = self.view_center.get_mask_list()
        for obj in view_mask_list:
            if None is obj:
                pass
            else:
                # 객체들을 초기화 합니다.
                # 뷰 초기화
                self.view_center.clean_mask()
                self.view_center.clean_mouse()
                self.view_second.mask = None

                # 로직 초기화
                self.auto.clean()
                self.group_complete_list.clear()
                self.pre_complete_list.clear()
                self.re_setting(self.active_path, self.active_image_index)
                self.table_label.create(self.view_center.get_mouse_list(), None)
                self.scroll_label.setWidget(self.table_label.top_widget)
                return

    # mark - Call back method: tool
    def level_window(self, value):
        print('WindowMethod: level_window')

        if self.view_center.screen_img is None:
            return

        # 사용자 UI TOOL 조절 윈도우 레벨을 update 합니다.
        self.auto.level_window = value
        self.level_window_value = value
        self.view_center.level_window = value
        self.view_center.level_muscle = self.level_muscle_value
        self.view_center.update_level()

    # mark - Call back method: tool
    def level_muscle(self, value):
        print('WindowMethod: level_muscle')

        if self.view_center.screen_img is None:
            return

        # 사용자 UI TOOL 조절 근육 레벨을 update 합니다.
        self.auto.level_muscle = value
        self.level_muscle_value = value
        self.view_center.level_window = self.level_window_value
        self.view_center.level_muscle = value
        self.view_center.update_level()

    # mark - Call back method: tool
    def start_point(self, value):
        print('WindowMethod: start_point')
        if self.view_center.screen_img is None:
            notice.message('선택된 image 없음.', 'image 먼저 Load 후 선택해 주세요!')
            return

        # 사용자 지정 처리 이미지 시작점
        self.start_value = value

    # mark - Call back method: tool
    def end_point(self, value):
        print('WindowMethod: end_point')

        # 사용자 지정 처리 이미지 종료점
        self.end_value = value

    # mark - Call back method: view_second
    def window_rect(self):
        self.view_second.set_screen_rect(self.geometry().getRect())






