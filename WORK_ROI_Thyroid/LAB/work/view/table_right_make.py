"""
Created by SungMin Yoon on 2022-12-28..
Copyright (c) 2022 year NCC (National Cancer Center). All rights reserved.
"""
import numpy as np
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QImage, QPixmap, QIcon
from PySide6.QtWidgets import QSlider
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QGroupBox
from LAB.common.model.roi import Roi
from .table_right_cell import TableRightCell

TITLE_BTN_Normal = 'Normal'
TITLE_BTN_ZOOM = 'Zoom'
TITLE_BTN_APPLY = 'Apply'
LAYOUT_MARGIN_HEIGHT = 20   # 이미지 표시 셀의 레이 아웃 세로 마진
LAYOUT_MARGIN_WIDTH = 10    # 이미지 표시 셀의 레이 아웃 가로 마진


class TableRightMake:

    call_btn_zoom = None    # 줌 관련 선택 버튼 이름을 보냅 니다.

    zoom_btn = None
    normal_btn = None
    apply_btn = None

    def __init__(self):
        print('TableRightMake init')

    def event_zoom_clicked(self, sender):
        print('TableRightMake: event_zoom_clicked')

        btn_list, name = sender
        zoom_btn: QPushButton = btn_list[0]
        normal_btn: QPushButton = btn_list[1]
        apply_btn: QPushButton = btn_list[2]
        index = zoom_btn.objectName()

        if name == 'normal':
            zoom_btn.setStyleSheet('background-color: white; color: black')
            normal_btn.setStyleSheet('background-color: indigo; color: white')
            apply_btn.setStyleSheet('background-color: white; color: black')

        if name == 'zoom':
            zoom_btn.setStyleSheet('background-color: indigo; color: white')
            normal_btn.setStyleSheet('background-color: white; color: black')
            apply_btn.setStyleSheet('background-color: white; color: black')

        if name == 'apply':
            zoom_btn.setStyleSheet('background-color: white; color: black')
            normal_btn.setStyleSheet('background-color: white; color: black')
            apply_btn.setStyleSheet('background-color: indigo; color: white')

        call = self.call_btn_zoom
        call(name, index)

    def button(self, index):

        # zoom 버튼 생성
        zoom_btn = QPushButton()
        zoom_btn.setText(TITLE_BTN_ZOOM)
        zoom_btn.setObjectName(index)
        zoom_btn.setStyleSheet('background-color: white; color: black')

        # 보통 화면 전환 버튼
        normal_btn = QPushButton()
        normal_btn.setText(TITLE_BTN_Normal)
        normal_btn.setObjectName(index)
        normal_btn.setStyleSheet('background-color: Indigo; color: white')

        # 사용자 선택 적용 버튼
        apply_btn = QPushButton()
        apply_btn.setText(TITLE_BTN_APPLY)
        apply_btn.setObjectName(index)
        apply_btn.setStyleSheet('background-color: white; color: black')

        button_list = [zoom_btn, normal_btn, apply_btn]
        zoom_btn.clicked.connect(lambda stat=False, param=[button_list, 'zoom']: self.event_zoom_clicked(param))
        normal_btn.clicked.connect(lambda stat=False, param=[button_list, 'normal']: self.event_zoom_clicked(param))
        apply_btn.clicked.connect(lambda stat=False, param=[button_list, 'apply']: self.event_zoom_clicked(param))

        return zoom_btn, normal_btn, apply_btn

    # 마스크 표시용 빈 이미지
    @ classmethod
    def empty_display(cls, h, w):

        # 빈 이미지 세팅
        im_np = np.zeros((w, h))
        empty_right = QImage(im_np.data, w, h, QImage.Format_Indexed8)
        pix_mask = QPixmap.fromImage(empty_right)
        icon_mask = QIcon(pix_mask)
        return icon_mask

    # image 와 마스크 표시용 테이블 그룹 세팅
    @ classmethod
    def table_ui_setting(cls, i, w, h):
        # 스크롤 박스에 장착될 그룹 박스
        pointSize = QSize((w + LAYOUT_MARGIN_WIDTH) * 2, h)
        group_box = QGroupBox()
        group_box.setTitle(f'{i + 1}')
        group_box.setFixedSize(pointSize)
        return group_box

    # 마스크 버튼 만들기
    @ classmethod
    def mask_button(cls, table_cell_count, icon_mask, w, h, target):
        # 마스크 버튼 생성
        mask_button_right = QPushButton()

        # 마스크 버튼 상태 체크
        mask_button_right.setCheckable(True)

        # 마스크 버튼 세팅
        mask_button_right.setObjectName(f'{table_cell_count}')
        mask_button_right.clicked.connect(lambda stat=False, parameter=table_cell_count:
                                          target(parameter))

        mask_button_right.setGeometry(0, 0, w, h)
        mask_button_right.setIcon(icon_mask)
        mask_button_right.setIconSize(QSize(w, h))
        mask_button_right.setFixedSize(w, h)

        return mask_button_right

    # 이미지 버튼 만들기
    @ classmethod
    def image_button(cls, group_mask, cv_color_img, pix_image, i, w, h,
                     cv_image_list, get_radio_number, click_event_image):

        # 테이블 장착될 셀 생성 및 이미지 출력 세팅
        cell_view_image: TableRightCell = TableRightCell()
        cell_view_image.color_scale_img = cv_color_img
        cell_view_image.gray_scale_img = cv_image_list[i]
        cell_view_image.q_graphic.setPixmap(pix_image)
        cell_view_image.setFixedSize(w, h + LAYOUT_MARGIN_HEIGHT)
        cell_view_image.name_index = f'{i + 1}'
        cell_view_image.call_radio_chk = get_radio_number
        cell_view_image.call_push_chk = click_event_image
        cell_view_image.setup()

        j = 0
        # 데이터 객체 꺼내기
        for obj_s in group_mask:

            # 리스트로 캐스팅
            obj_list: list = obj_s
            for obj in obj_list:

                # 객체가 비어 있지 않으면
                if obj is not None:

                    # 객체를 튜플로 캐스팅
                    t: tuple = obj
                    image_num, data = t

                    # 데이터 를 roi 로 변환
                    roi: Roi = data
                    mask = roi.image_mask

                    # 이미지 넘버 와 cv 이미지 카운트 i 같다면
                    if image_num == i:
                        # 셀에 마스크 저장
                        cell_view_image.set_mask(j, mask)

                        # 마스크 인덱스 증감
                        j = j + 1

        return cell_view_image

    # slider 윈도우 만들기
    @ classmethod
    def slider_level(cls, cell_name, target):
        default = 100

        # slider 생성
        slider_window = QSlider(Qt.Horizontal, None)
        slider_window.setObjectName(cell_name)
        slider_window.move(100, 1000)
        slider_window.setRange(100, 1000)
        slider_window.setSingleStep(1)
        slider_window.setValue(default)
        slider_window.valueChanged.connect(lambda stat=False, parameter=cell_name:
                                           target(parameter))
        slider_window.setFixedSize(512, 10)

        return slider_window


