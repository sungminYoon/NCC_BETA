"""
Created by SungMin Yoon on 2022-12-29..
Copyright (c) 2022 year NCC (National Cancer Center). All rights reserved.
"""
import time
import cv2 as cv
import numpy as np
from copy import copy
from PySide6.QtGui import QMouseEvent
from PySide6 import QtWidgets, QtGui, QtCore
from LAB.config import setting
from LAB.common.util import img_empty


class TableRightZoom(QtWidgets.QGraphicsView):

    # call back method
    call_sync_mask = None

    # 윈도우 크기
    screen_rect: QtCore.QRectF

    '''로컬 좌표'''
    # 드래그
    start_x = None
    start_y = None
    end_x = None
    end_y = None

    # 윈도우 창 과 로컬 좌표 차이
    margin_x = None
    margin_y = None

    # 마우스 이벤트
    move_x = None
    move_y = None

    # 드래그 영역 자르기
    cut_x = None
    cut_y = None
    cut_w = None
    cut_h = None

    '''cv 이미지'''
    make_mask = None        # 가공 mask -> 무수정 image size 크기 적용 -> make mask
    cv_img = None           # 무수정 받은 이미지
    cv_color = None         # 결과 색칠 한 이미지
    flood_mask = None       # 사용자 선택 roi mask 추출
    threshold_img = None    # 사용자 선택 threshold
    cut_img = None          # 사용자 선택 rect 자른
    big_img = None          # 사용자 선택 rect *2 늘이기
    mask = None             # 사용자 선택 roi 가공

    ''' Active value '''
    user_threshold_change = None

    # 라벨 생성
    def __init__(self, parent=None):
        super(TableRightZoom, self).__init__(parent)
        self.scene = QtWidgets.QGraphicsScene(self)
        self.q_graphic = QtWidgets.QGraphicsPixmapItem()
        self.scene.addItem(self.q_graphic)
        self.setScene(self.scene)

        # 변수 초기화
        self.user_threshold_change = 0

        # 뷰 시작 좌표
        self.margin_x = 0
        self.margin_y = 0

        self.setup()

    # 윈도우 창 과 view 사이의 좌표 크기 고정
    def setup(self):
        self.screen_rect: QtCore.QRectF = QtCore.QRectF(0.0, 0.0, 510, 510)
        self.setSceneRect(QtCore.QRectF(self.screen_rect))

    def set_screen_rect(self, rect):
        # view 크기
        self.screen_rect = rect

    def set_user_threshold(self, value):
        self.user_threshold_change = value

    # mark -  Event method
    def mouseMoveEvent(self, e):
        print('TableRightZoom: mouseMoveEvent')

        # 로컬 좌표
        event: QMouseEvent = e
        position = event.pos()

        # 이동 중인 좌표
        self.move_x = position.x() - self.margin_x
        self.move_y = position.y() - self.margin_y

        # cv image 복사
        copy_image = copy(self.cv_color)

        # 사각형 그리기
        copy_image = cv.rectangle(copy_image, (self.start_x, self.start_y), (self.move_x, self.move_y), (255, 0, 0), 1)
        copy_image = self.bgr_to_pixImage(copy_image)

        # 보여 지는 view 에 image 를 넣어 주고
        self.q_graphic.setPixmap(copy_image)

    # mark -  Event method
    def mousePressEvent(self, e):
        print('TableRightZoom: mousePressEvent -> START')

        # 로컬 좌표
        event: QMouseEvent = e
        position = event.pos()

        self.start_x = position.x() - self.margin_x
        self.start_y = position.y() - self.margin_y

    # mark -  Event method
    def mouseReleaseEvent(self, e):
        print('TableRightZoom: mouseReleaseEvent -> END')

        # 로컬 좌표
        event: QMouseEvent = e
        position = event.pos()

        # 월드 좌표
        self.end_x = position.x()
        self.end_y = position.y()

        # 드래그 크기가 50 이하 이면 동작
        if self.move_x < 50 or self.move_y < 50:

            # start 좌표 threshold
            self.img_threshold()

        else:
            # 이미지 자르기
            self.img_cut()

            # 드래그 초기화
            self.move_x = 0
            self.move_y = 0

    def img_threshold(self):

        # 자른 확대 이미지 복사
        self.threshold_img = copy(self.big_img)
        h, w = self.big_img.shape[:2]

        CONNECTIVITY = 4  # 연결성
        flood_fill_flags = (CONNECTIVITY | cv.FLOODFILL_FIXED_RANGE | cv.FLOODFILL_MASK_ONLY | 255 << 8)

        # 마스크 영역 채우기
        self.flood_mask = np.zeros((h + 2, w + 2), np.uint8)
        time.sleep(0.2)

        self.flood_mask[:] = 0
        time.sleep(0.2)

        cv.floodFill(self.threshold_img, self.flood_mask, (self.start_x, self.start_y), 1,
                     20,
                     20,
                     flood_fill_flags)
        self.mask = self.flood_mask[1:-1, 1:-1].copy()
        time.sleep(0.2)

        self.threshold_img = cv.cvtColor(self.threshold_img, cv.COLOR_RGB2BGR)

        # 사용자 선택 threshold 내부 칠하기
        a, b, c = setting.ROI_COLOR[self.user_threshold_change]
        self.threshold_img[self.mask == 255] = [a, b, c]

        # 보여 지는 view 에 image 를 넣어 주고
        pix_image = self.bgr_to_pixImage(self.threshold_img)
        self.q_graphic.setPixmap(pix_image)

    def img_cut(self):
        print('TableRightZoom: img_cut')

        # 이미지 복사
        copy_image = copy(self.cv_img)

        # 마우스 좌표에 영향을 받지 않는 cut 에 좌표 저장
        self.cut_x = self.start_x
        self.cut_y = self.start_y
        self.cut_w = self.move_x
        self.cut_h = self.move_y

        # 이미지 자르기
        self.cut_img = copy_image[self.cut_y:self.cut_h, self.cut_x:self.cut_w]
        time.sleep(0.5)

        # 크기 2배 확대
        xb = int(self.cut_w * 2)
        yb = int(self.cut_h * 2)

        # 2배 늘이기
        self.big_img = cv.resize(self.cut_img, (xb, yb), interpolation=cv.INTER_AREA)
        time.sleep(0.5)

        # 보여 지는 view 에 image 를 넣어 주고
        pix_image = self.gray_to_pixImage(self.big_img)
        self.q_graphic.setPixmap(pix_image)

    def resize_apply(self):

        # 수정 되지 않은 자른 이미지
        h, w = self.cut_img.shape[:2]

        # 무수정 image 크기
        size_h, size_w = self.cv_img.shape[:2]

        # 줄이기
        small_img = cv.resize(self.mask, (w, h), interpolation=cv.INTER_AREA)
        time.sleep(1)

        # cut image 시작 좌표, 합성, 준비
        x = int(self.cut_x)
        y = int(self.cut_y)
        image = copy(self.cv_img)
        image_color = cv.cvtColor(image, cv.COLOR_RGB2BGR)
        time.sleep(0.2)

        # 무수정 size 에 맞는 mask 생성
        make_mask = img_empty.np_add(size_w, size_h, x, y, small_img)
        time.sleep(0.2)

        # 생성 mask 보내기
        call = self.call_sync_mask
        call(make_mask, self.user_threshold_change)

        # 사용자 선택 threshold 내부 칠하기
        a, b, c = setting.ROI_COLOR[self.user_threshold_change]
        image_color[make_mask == 255] = [a, b, c]
        time.sleep(0.2)

        # 보여 지는 view 에 image 를 넣어 주고
        pix_image = self.bgr_to_pixImage(image_color)
        self.q_graphic.setPixmap(pix_image)

    # cv image Gray Q_Pix_map 변환 합니다.
    @classmethod
    def gray_to_pixImage(cls, gray_img):
        height, width = gray_img.shape[:2]
        g_image = QtGui.QImage(gray_img, width, height, QtGui.QImage.Format_Grayscale8)
        pix_image = QtGui.QPixmap.fromImage(g_image)
        return pix_image

    # cv image BGR Q_Pix_map 변환 합니다.
    @classmethod
    def bgr_to_pixImage(cls, gray_img):
        height, width = gray_img.shape[:2]
        g_image = QtGui.QImage(gray_img, width, height, QtGui.QImage.Format_BGR888)
        pix_image = QtGui.QPixmap.fromImage(g_image)
        return pix_image
