"""
Created by SungMin Yoon on 2022-07-08..
Copyright (c) 2022 year NCC (National Cancer Center). All rights reserved.
"""
import cv2 as cv
from PySide6 import QtCore, QtWidgets
from PySide6.QtGui import QImage
from PySide6.QtGui import QPixmap

from LAB.config import setting
from LAB.common.algorithm import magic_wand
from LAB.common.util import img_convert_qt


class TableRightCell(QtWidgets.QGraphicsView):

    call_radio_chk = None           # 상단 tool 뷰의 사용자 선택 라디오 버튼 확인
    call_push_chk = None            # cell 눌려 졌는지 확인

    threshold = setting.THRESHOLD   # 현재 적용된 threshold 값

    # 셀의 크기
    w = None
    h = None

    slider_sw = None                # 자신이 속한 CELL 의 Slider event 가 일어 났는지 판정
    name_index = None               # 셀 뷰 자신의 인덱스 이름 입니다.
    level_save_img = None           # origin -> image level 변경 이미지
    gray_scale_img = None           # 뷰 mask 이미지
    color_scale_img = None          # 뷰 color 이미지
    mask_list: list                 # 사용자 선택 mask
    mouse_list: list                # 사용자 선택 마스크 마우스 좌표

    def __init__(self, parent=None):
        super(TableRightCell, self).__init__(parent)

        # 사용자 선택 mask, mouse 저장 데이터 생성
        self.mask_list = [None for _ in range(setting.USER_CHOICE_COUNT)]
        self.mouse_list = [None for _ in range(setting.USER_CHOICE_COUNT)]

        # 화면 초기화
        self.scene = QtWidgets.QGraphicsScene(self)
        self.q_graphic = QtWidgets.QGraphicsPixmapItem()
        self.scene.addItem(self.q_graphic)
        self.setScene(self.scene)
        self.slider_sw = False

    def setup(self):

        # 화면 설정
        self.h, self.w = self.gray_scale_img.shape[:2]
        screen_rect: QtCore.QRectF = QtCore.QRectF(0.0, 0.0, self.w, self.h)
        self.setSceneRect(QtCore.QRectF(screen_rect))

    # 화면 갱신
    def view_update(self):

        # 초기 이미지 보여 주기
        self.slider_sw = False
        self.level_save_img = self.color_scale_img
        color_image = QImage(self.color_scale_img, self.w, self.h, QImage.Format_BGR888)
        pix_image = QPixmap.fromImage(color_image)
        self.q_graphic.setPixmap(pix_image)
        self.repaint()

    def view_update_level(self, level_image):

        # level 변경 이미지 보여 주기
        self.slider_sw = True
        self.level_save_img = level_image
        pix_image = img_convert_qt.bgr_to_pixImage(level_image)
        self.q_graphic.setPixmap(pix_image)
        self.repaint()

    # 마스크 저장
    def set_mask(self, number, mask):
        self.mask_list[number] = mask

    # 마스크 리스트 export
    def get_mask_list(self):
        return self.mask_list

    # 마스크 다시 None 채우기
    def re_mask_list(self):
        count = len(self.mask_list)
        for i in range(0, count):
            self.mask_list[i] = None

    # mark -  Event method
    def moveEvent(self, e):
        print('TableMaskCell: moveEvent')

    # mark -  Event method
    def mouseMoveEvent(self, e):
        print('TableMaskCell: mouseMoveEvent')

    # mark -  Event method
    def mouseReleaseEvent(self, e):
        print('TableMaskCell: mouseReleaseEvent')

        # 마우스 선택 cell 인덱스 export
        call_push = self.call_push_chk
        call_push(self.name_index)

        # 화면 갱신
        self.view_update()

    # mark -  Event method
    def mousePressEvent(self, e):
        print('TableMaskCell: mousePressEvent')

        # 마우스 좌표
        x = e.x()
        y = e.y()

        if self.w < x or self.h < y:
            print('TableMaskCell: mouse position OVER')
            return
        if x is 0:
            return

        # cell 의 slider event on & off
        if self.slider_sw is True:
            img_gray = cv.cvtColor(self.level_save_img, cv.COLOR_BGR2GRAY)
        else:
            img_gray = cv.cvtColor(self.color_scale_img, cv.COLOR_BGR2GRAY)

        # 마법봉
        new_mask = magic_wand.get_threshold(self.threshold, img_gray, x, y)

        # 마스크 타입 카피
        blank = new_mask.copy()

        # 0 으로 채우기
        blank.fill(0)

        # 사용 자가 선택한 라디오 번호
        call_radio = self.call_radio_chk
        radio_number = call_radio()

        # 마우스 좌표와 마스크 저장
        mouse_position = (x, y)
        self.mask_list[radio_number] = new_mask
        self.mouse_list[radio_number] = mouse_position

        # 그레이 스케일 image 칼라로 변환
        self.color_scale_img = cv.cvtColor(img_gray, cv.COLOR_RGB2BGR)

        # 마스크 list 마스크 가져 오기
        i = 0
        for mask in self.mask_list:

            # mask 없다면
            if mask is None:
                pass
            else:

                # 사용자 선택 ROI 색 가져 오기
                a, b, c = setting.ROI_COLOR[i]

                # 사용자 선택 threshold 내부 칠하기
                try:
                    self.color_scale_img[mask == 255] = [a, b, c]

                # mask 차원이 맞지 않으면
                except IndexError:

                    # 빈 이미지 마스크 결합
                    blank = cv.add(blank, mask)

                    # 이미지 마스크 내부 칠하기
                    self.color_scale_img[blank == 255] = [a, b, c]

            # 색 고르기 값 증감
            i = i + 1
