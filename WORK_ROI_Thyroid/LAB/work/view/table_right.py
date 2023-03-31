"""
Created by SungMin Yoon on 2020-12-08..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""
from PySide6.QtGui import QImage, QPixmap

from LAB.common.oop.merge import Merge
from LAB.common.util import data_structure, table_data
from .table_right_cell import TableRightCell
from .table_right_zoom import TableRightZoom
from .table_right_make import TableRightMake

import cv2 as cv


class TableRight:

    # 콜백 객체로 진행 상황을 알립 니다.
    call_progress = None

    # 사용 되는 이미지 데이터 size
    h: int
    w: int

    # 툴의 라디오 버튼 값
    tool_radio_default = 0
    tool_radio_current = 0

    # Table UI 입니다.
    top_widget = None
    top_layout = None
    group_layout = None

    zoom = None
    make = None     # Table cell 의 button 생성
    merge = None    # cell list 를 병합 합니다.

    # Tool 에서 받은 세팅 값 입니다.
    muscle_value = None
    window_value = None

    export_list: list           # export 리스트 입니다.
    user_select_list: list      # 사용자 선택 마스크
    group_mask_list: list       # 마스크 를 roi 그룹 별로 저장한 리스트
    cv_image_list: list         # 그레이 스케일 CT 무수정
    image_button_list: list     # 테이블 cell 에 보여 지는 image button 리스트
    mask_button_list: list      # 테이블 cell 에 보여 지는 mask button 리스트
    zoom_view_list: list        # 테이블 cell 에 숨겨 있는 zoom view 리스트
    slider_list: list           # 테이블 cell 에 보여 지는 slider 리스트
    result_mask_list: list      # 테이블 cell 에 보여 지는 CT mask
    cv_color_list: list         # 테이블 cell 에 보여 지는 CT image

    click_event_mask = None     # 테이블 마스크 view 클릭 이벤트
    click_event_image = None    # 테이블 이미지 view 클릭 이벤트
    table_slider_value = None   # 테이블 slider move 이벤트

    def __init__(self):

        # 사용 되는 이미지 데이터 size 초기화
        self.h = 0
        self.w = 0

        # 버튼, 리스트 병합 객체 생성
        self.make = TableRightMake()
        self.make.call_btn_zoom = self.click_zoom_group
        self.merge = Merge()

        # 리스트 를 생성 합니다.
        self.export_list = []
        self.contour_list = []
        self.user_select_list = []
        self.image_button_list = []
        self.mask_button_list = []
        self.zoom_view_list = []
        self.slider_list = []

    def list_clear(self):
        print('TableRight: list_clear')

        # 리스트 를 초기화 합니다.
        self.export_list.clear()
        self.contour_list.clear()
        self.user_select_list.clear()
        self.image_button_list.clear()
        self.mask_button_list.clear()
        self.zoom_view_list.clear()
        self.slider_list.clear()

    def create(self, result_list, group_list, cv_color_list, cv_images):
        print('TableRight: create')

        # 리스트 초기화
        self.list_clear()

        # 결과 마스크, 그룹화 마스크, 표시 cv 이미지, 무수정 gray 이미지 리스트에 저장
        self.result_mask_list = result_list
        self.cv_color_list = cv_color_list
        self.cv_image_list = cv_images

        # 데이터 교정
        self.group_mask_list = data_structure.duplication_compare(group_list)

        # 이미지 데이터 size 저장
        gray_img = self.cv_image_list[0]
        self.h, self.w = gray_img.shape[:2]

        # 진행 바 초기화
        call = self.call_progress
        call(100, 10)

    def cell_threshold_update(self, value):
        print('TableRight: cell_threshold_update')
        for btn in self.image_button_list:
            cell: TableRightCell = btn
            cell.threshold = value

    def get_export_data(self):
        print('TableRight: get_export_data -> ', self.group_mask_list)
        self.result_mask_list = self.merge.auto_result_image(self.group_mask_list, self.cv_image_list)
        return self.group_mask_list, self.result_mask_list

    # 툴 라디오 버튼 넘버 가져 오기
    def get_radio_number(self):
        return self.tool_radio_default

    # 툴 라디오 버튼 넘버 저장
    def set_radio_number(self, number):
        self.tool_radio_default = number

    def export_update(self, idx):
        print('TableRight: export_update')

        # int 형 변환
        number = int(idx)
        number = number - 1

        # 내보낼 데이터 빼고, 추가
        table_data.pop(number, self.group_mask_list)
        table_data.add(number, self.group_mask_list, self.image_button_list[number])

        print('TableRight: export_update -> ', self.group_mask_list, '\n')

    def export_pop(self, idx):

        # int 형 변환
        number = int(idx)

        # 내보낼 데이터 빼고, 추가
        table_data.pop(number, self.group_mask_list)

    # mark - Call back Method: TableRightMake
    def click_zoom_group(self, name, index):
        print('TableRightExtends: click_zoom_button -> ', name, index)

        num = int(index)

        image_view: TableRightCell = self.image_button_list[num]
        zoom_view: TableRightZoom = self.zoom_view_list[num]
        origin_img = self.cv_image_list[num]

        color_image = QImage(image_view.color_scale_img, self.w, self.h, QImage.Format_BGR888)
        pix_image = QPixmap.fromImage(color_image)

        zoom_view.cv_img = origin_img
        zoom_view.cv_color = image_view.color_scale_img
        zoom_view.q_graphic.setPixmap(pix_image)
        zoom_view.repaint()

        if name == 'normal':
            image_view.show()
            zoom_view.hide()

        if name == 'zoom':
            image_view.hide()
            zoom_view.show()

        if name == 'apply':
            image_view.hide()
            zoom_view.show()





