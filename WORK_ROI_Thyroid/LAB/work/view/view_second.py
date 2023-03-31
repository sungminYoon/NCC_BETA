"""
Created by SungMin Yoon on 2022-09-15..
Copyright (c) 2022 year NCC (National Cancer Center). All rights reserved.
"""

import time
import cv2 as cv
import numpy as np
from copy import copy
from LAB.config import setting
from LAB.common.util import img_empty
from PySide6 import QtWidgets, QtGui, QtCore


class ViewSecond(QtWidgets.QGraphicsView):

    # call back method
    call_window_rect = None
    call_sync_mask = None

    # 윈도우 크기
    default_rect: QtCore.QRectF
    window_current_rect: QtCore.QRectF

    # world window 좌표 계
    world_x = None
    world_y = None
    world_x_move = None
    world_y_move = None

    '''로컬 좌표'''

    # 드래그
    start_x = None
    start_y = None
    end_x = None
    end_y = None

    # 윈도우 창
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
    cv_img = None           # 무수정 받은 이미지
    mask = None             # 사용자 선택 roi 가공
    make_mask = None        # 가공 mask -> 무수정 image size 크기 적용 -> make mask
    flood_mask = None       # 사용자 선택 roi mask 추출
    threshold_img = None    # 사용자 선택 threshold
    cut_img = None          # 사용자 선택 rect 자른
    big_img = None          # 사용자 선택 rect *2 늘이기

    ''' Active value '''
    user_threshold_change = None

    # 라벨 생성
    def __init__(self, parent=None):
        super(ViewSecond, self).__init__(parent)
        self.scene = QtWidgets.QGraphicsScene(self)
        self.q_graphic = QtWidgets.QGraphicsPixmapItem()
        self.scene.addItem(self.q_graphic)
        self.setScene(self.scene)

        # 변수 초기화
        self.user_threshold_change = 0

        # 뷰 시작 좌표
        self.margin_x = 240
        self.margin_y = 281

        self.setup()

    # 윈도우 창 과 view 사이의 좌표 크기 고정
    def setup(self):
        screen_rect: QtCore.QRectF = QtCore.QRectF(0.0, 0.0, 513, 513)
        self.setSceneRect(QtCore.QRectF(screen_rect))

    def set_window_rect(self, rect):
        # 윈도우 크기
        self.window_current_rect = rect

    def set_user_threshold(self, value):
        self.user_threshold_change = value

    # 로컬 -> 월드 좌표 변환
    def local_to_world_position(self, e):
        p = e.pos()                             # relative to widget
        gp = self.mapToGlobal(p)                # relative to screen
        rw = self.window().mapFromGlobal(gp)    # relative to window
        return rw

    # mark -  Event method
    def mouseMoveEvent(self, e):
        print('ViewSecond: mouseMoveEvent')

        # 로컬 좌표 -> 월드 좌표
        world_position = self.local_to_world_position(e)

        # 월드 좌표(윈도우 창) 변화 있는지 감지
        if self.world_x != 0 or self.world_y != 0:
            self.move_x = world_position.x() - self.world_x_move
            self.move_y = world_position.y() - self.world_y_move
        else:
            self.move_x = world_position.x() - self.margin_x
            self.move_y = world_position.y() - self.margin_y

        # cv image 복사
        copy_image = copy(self.cv_img)

        # 사각형 그리기
        copy_image = cv.rectangle(copy_image, (self.start_x, self.start_y), (self.move_x, self.move_y), (255, 0, 0), 1)
        copy_image = self.gray_to_pixImage(copy_image)

        # 보여 지는 view 에 image 를 넣어 주고
        self.q_graphic.setPixmap(copy_image)

    # mark -  Event method
    def mousePressEvent(self, e):
        print('ViewSecond: mousePressEvent -> START')

        # 윈도우 크기 요청
        call = self.call_window_rect
        call()

        # 로컬 좌표 -> 월드 좌표
        world_position = self.local_to_world_position(e)

        # 윈도우 크기 초기값 현재 값
        wr_x = self.window_current_rect[2]
        wr_y = self.window_current_rect[3]
        dr_x = self.default_rect[2]
        dr_y = self.default_rect[3]

        # 현재 윈도우 크기 초기 값 빼기
        self.world_x = wr_x - dr_x
        self.world_y = wr_y - dr_y

        # 윈도우 변화된 크기 계산
        self.world_x_move = self.margin_x + int(self.world_x * 0.5)
        self.world_y_move = self.margin_y + int(self.world_y * 0.5)

        # 윈도우 크기가 변화 되면 월드 좌표 계산 아니면 마진 계산
        if self.world_x != 0 or self.world_y != 0:
            self.start_x = world_position.x() - self.world_x_move
            self.start_y = world_position.y() - self.world_y_move
        else:
            self.start_x = world_position.x() - self.margin_x
            self.start_y = world_position.y() - self.margin_y

    # mark -  Event method
    def mouseReleaseEvent(self, e):
        print('ViewSecond: mouseReleaseEvent -> END')

        # 로컬 좌표 -> 월드 좌표
        world_position = self.local_to_world_position(e)

        # 월드 좌표
        self.end_x = world_position.x()
        self.end_y = world_position.y()

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
        print('ViewSecond: img_cut')

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
        xb = self.cut_w * 2
        yb = self.cut_h * 2

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
