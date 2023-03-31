"""
Created by SungMin Yoon on 2022/08/03..
Copyright (c) 2022 year SungMin Yoon. All rights reserved.
"""

import cv2 as cv

from PySide6.QtWidgets import *
from PySide6.QtGui import QIcon
from PySide6.QtGui import QImage
from PySide6.QtGui import QPixmap
from LAB.common.util import img_threshold
from LAB.common.util import img_empty
from LAB.common.util import img_level
from .table_right import TableRight
from .table_right_cell import TableRightCell
from .table_right_zoom import TableRightZoom


'''
    table_right.py 의 
    확장(extends) 클레스 입니다. 
    UI (Table cell) 생성과 cell 기능이 구현 되어 있 습니다.
'''


class TableRightExtends(TableRight):

    def __init__(self):
        super(TableRightExtends, self).__init__()
        print('TableRightExtends: init')

    def ui_setup(self):
        print('TableRightExtends: ui_setup')

        # UI 객체 생성
        self.top_widget = QWidget()
        self.top_layout = QVBoxLayout()

        # 테이블 셀 개수만 카운트 해서 어긋남 을 방지 합니다.
        table_cell_count = 0

        for i in range(0, len(self.cv_color_list)):

            index_name = f'{i}'

            # 진행 바 채우기
            call = self.call_progress
            call(len(self.result_mask_list), 10 + i)

            '''테이블 우측 결과 마스크 표시'''

            # mask 가 0 이면 empty 처리
            if self.result_mask_list[i] == 0:
                icon_mask = self.make.empty_display(self.h, self.w)

                # 테이블 좌측 보이는 image 세팅
                cv_color_img = self.cv_image_list[i]
                cv_color_img = cv.cvtColor(cv_color_img, cv.COLOR_RGB2BGR)

            else:
                icon_mask = self.mask_display(self.result_mask_list, i, self.h, self.w, None)

                # 테이블 좌측 보이는 image 세팅
                cv_color_img = self.cv_color_list[i]

            # table_cell_name = 테이블 표시 번호 , i = cv 이미지 카운트, True = 버튼 상태
            table_cell_name = (f'{i}', True)
            self.user_select_list.append(table_cell_name)

            # BGR888 이미지 셀 세팅
            table_left = QImage(cv_color_img, self.w, self.h, QImage.Format_BGR888)
            pix_image = QPixmap.fromImage(table_left)

            # ZOOM 뷰 생성
            zoom_view: TableRightZoom = TableRightZoom()
            zoom_view.setFixedSize(510, 510)
            zoom_view.hide()

            # 이미지 버튼 생성
            image_button_cell: TableRightCell = self.make.image_button(self.group_mask_list,
                                                                       cv_color_img,
                                                                       pix_image,
                                                                       i, self.w, self.h,
                                                                       self.cv_image_list,
                                                                       self.get_radio_number,
                                                                       self.click_event_image)

            # 마스크 버튼 생성
            mask_button_cell = self.make.mask_button(table_cell_count,
                                                     icon_mask,
                                                     self.w, self.h,
                                                     self.click_event_mask)

            # result_layout 셀 추가
            result_layout = QHBoxLayout()
            result_layout.addWidget(zoom_view)
            result_layout.addWidget(image_button_cell)
            result_layout.addWidget(mask_button_cell)

            # zoom 버튼 생성
            group_btn_zoom = QHBoxLayout()
            _zoom, _normal, _apply = self.make.button(index_name)

            # Slider 생성
            _slider = self.make.slider_level(index_name, self.table_slider_value)
            self.slider_list.append(_slider)

            # 그룹 줌 레이 아웃에 등록
            group_btn_zoom.addWidget(_normal)
            group_btn_zoom.addWidget(_zoom)
            group_btn_zoom.addWidget(_apply)
            group_btn_zoom.addWidget(_slider)

            # group_layout Slider, result_layout 추가
            _group_box = self.make.table_ui_setting(i, self.w, self.h)
            self.group_layout = QVBoxLayout(_group_box)
            self.group_layout.addLayout(group_btn_zoom)
            self.group_layout.addLayout(result_layout)

            # 생성한 버튼 저장
            self.image_button_list.append(image_button_cell)
            self.mask_button_list.append(mask_button_cell)
            self.zoom_view_list.append(zoom_view)

            # 스크롤 의 가장 위에 보여질 그룹 박스
            self.top_layout.addWidget(_group_box)
            self.top_widget.setLayout(self.top_layout)

            # 샐 생성 카운트 증감
            table_cell_count = table_cell_count + 1

        # 진행바 종료
        call = self.call_progress
        call(100, 0)

    # cell update
    def ui_cell_update(self, index):
        print('TableRightExtends: ui_cell_update')

        # 진행 바
        call = self.call_progress
        call(100, 11)

        # 사용자 선택 인덱스 int 형 변환
        number = int(index)

        # 표시 된 index 실제 리스트 인덱스 오차 교정
        number = number - 1

        # 이미지 버튼 리스트 에서 선택 셀 가져 오기
        right_cell: TableRightCell = self.image_button_list[number]

        # 셀 에서 마스크 리스트 가져 오기
        mask_list = right_cell.get_mask_list()
        call(100, 20)

        # 마스크 리스트 화면 표시용 아이콘 변환
        icon_mask = self.mask_display(self.result_mask_list, number, self.h, self.w, mask_list)
        call(100, 70)

        # 사용자 선택 마스크 화면에 표시
        self.mask_button_list[number].setIcon(icon_mask)
        call(100, 80)

    # mark - Event Method
    def click_event_image(self, idx):
        print('TableRightExtends: click_event_image')

        # 진행 바
        call = self.call_progress
        call(100, 10)

        # 테이블 UI, export 데이터 update
        self.ui_cell_update(idx)
        call(100, 90)

        self.export_update(idx)
        call(100, 0)

    # mark - Event Method
    def click_event_mask(self, idx):
        print('TableRightExtends: click_event_mask')

        # 버튼 캐스팅
        button_mask: QPushButton = self.mask_button_list[idx]
        button_image: TableRightCell = self.image_button_list[idx]

        # 이미지 버튼 의 마스크 데이터 리스트 다시 None 세팅
        button_image.re_mask_list()

        # 버튼 이름 int 캐스팅
        mask_name = button_mask.objectName()
        number = int(mask_name)

        # 마스크 버튼 빈 이미지 생성
        empty = img_empty.np_image(self.w, self.h)
        mask_q = QImage(empty, self.w, self.h, QImage.Format_Grayscale8)
        pix_mask_q = QPixmap.fromImage(mask_q)

        # 이미지 버튼 원본 이미지 생성
        image = self.cv_image_list[number]
        color_image = cv.cvtColor(image, cv.COLOR_RGB2BGR)

        # 결과 마스크, 컬러 이미지 데이터 초기화
        self.export_pop(number)
        self.result_mask_list[number] = 0
        self.cv_color_list[number] = color_image

        # 버튼에 마스크, 이미지 교체
        button_mask.setIcon(pix_mask_q)
        button_image.color_scale_img = color_image
        button_image.view_update()

    # mark - Event method
    def table_slider_value(self, cell_name):

        # 인덱스 캐스팅
        index = int(cell_name)

        # slider 가져 오기
        _slider: QSlider = self.slider_list[index]
        value = _slider.value()

        # cell 가져 오기
        right_cell: TableRightCell = self.image_button_list[index]
        color_scale_img = right_cell.color_scale_img

        if value > 101:

            # 화면에 보여질 칼라 이미지 레벨을 조정 하고
            level_image = img_level.tissue_process(color_scale_img, 0, self.window_value, value, 0.1)

            # cell 화면 update
            right_cell.view_update_level(level_image)
        else:

            # cell 화면 update
            right_cell.view_update()

    # 마스크 표시용 아이콘 이미지
    def mask_display(self, result_list, number, h, w, mask_list):

        # 진행 바
        call = self.call_progress

        # 마스크 개수
        mask_count = 0

        # 빈 이미지
        mask_image = img_empty.np_image(w, h)

        # 마스크 리스트 크기 만큼 반복
        if mask_list is None:
            pass
        else:
            length = len(mask_list)
            for i in range(0, length):
                mask = mask_list[i]

                # 리스트 에 마스크 가 있다면 셀 이미지 에 마스크 결합
                if mask is not None:
                    mask_image = cv.add(mask_image, mask)
                    mask_count = mask_count + 1

        # mask list 에 mask 없어 카운트 가 0 이면
        if mask_count == 0:

            # 결과 리스트 에서 image 객체를 가져 옵니다.
            image_obj = result_list[number]
            if image_obj == 0:
                pass
            else:
                img, _ = image_obj
                mask_image = img

        call(100, 50)

        # mask image contour threshold
        threshold_image = img_threshold.contour_to_bgr(mask_image)

        # 오른쪽 테이블 마스크
        table_right = QImage(threshold_image, w, h, QImage.Format_BGR888)
        pix_mask = QPixmap.fromImage(table_right)
        icon_mask = QIcon(pix_mask)

        call(100, 60)

        # cell 장착용 icon mask
        return icon_mask


