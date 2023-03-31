"""
Created by SungMin Yoon on 2020-01-09..
Copyright (c) 2019 year SungMin Yoon. All rights reserved.
"""
import time
import cv2 as cv
import numpy as np
from PySide6 import QtCore, QtWidgets
from LAB.config import setting
from LAB.common.util import img_level
from LAB.common.util import img_convert_qt
from LAB.common.util import img_threshold

CONNECTIVITY = 4  # 연결성
MASK_LIST = [None for _ in range(setting.USER_CHOICE_COUNT)]
MOUSE_LIST = [None for _ in range(setting.USER_CHOICE_COUNT)]


# 마법봉 윤곽 좌표
def _find_exterior_contours(img):
    ret = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    if len(ret) == 2:
        return ret[0]
    elif len(ret) == 3:
        return ret[1]


class ViewCenter(QtWidgets.QGraphicsView):

    tool_radio_chk = 1                              # 상단 tool 뷰의 라디오 버튼 확인
    threshold = setting.THRESHOLD                   # 현재 적용된 threshold 값
    level_window = setting.DEFAULT_LEVEL_WINDOW     # 윈도우 값 세팅
    level_muscle = setting.DEFAULT_LEVEL_MUSCLE     # 근육 값 세팅

    call_click_threshold = None     # 콜백 메소드 Label tabel threshold 좌표 정보를 call back.
    q_graphic = None                # view 세팅에 사용 됩니다.
    screen_img = None               # 화면에 shown 이미지
    screen_rect = None              # 화면에 shown 이미지 사각형 크기
    update_level_img = None         # 화면에 update 레벨 이미지
    gray_scale_img = None           # 원본 GRAY SCALE 이미지
    flood_mask = None               # 마법봉 algorithm 변수
    flood_fill_flags = None         # 마법봉 채우기 변수
    mask_img = None                 # 사용자 클릭 마스크 저장
    mouse_position_list: list = []  # 사용자 mouse position 저장

    # QT 예제 기본 VIEW 구조
    def __init__(self, parent=None):
        super(ViewCenter, self).__init__(parent)
        self.scene = QtWidgets.QGraphicsScene(self)
        self.q_graphic = QtWidgets.QGraphicsPixmapItem()
        self.scene.addItem(self.q_graphic)
        self.setScene(self.scene)

    def setup(self):
        self.screen_rect: QtCore.QRectF = QtCore.QRectF(0.0, 0.0, 513, 513)
        self.setSceneRect(QtCore.QRectF(self.screen_rect))

    # 마법봉 관련 변수 초기화
    def re_default(self):
        self.flood_mask = None
        self.flood_fill_flags = None

    # 마법봉 다시 세팅
    def re_setting(self, img):
        print('ViewMain: resetting')

        # 이미지 관련 변수 초기화
        self.re_default()

        # 이미지 포멧
        cv_gray = img
        cv_color = cv.cvtColor(cv_gray, cv.COLOR_BGR2RGB)

        # cv 이미지 사이즈
        h, w = cv_color.shape[:2]

        # open cv image 준비 시간 0.1 초 Delay
        self.screen_img = cv_color.copy()
        self.gray_scale_img = cv_gray.copy()
        time.sleep(0.1)
        self.flood_mask = np.zeros((h + 2, w + 2), np.uint8)
        time.sleep(0.1)
        self.flood_fill_flags = (CONNECTIVITY | cv.FLOODFILL_FIXED_RANGE | cv.FLOODFILL_MASK_ONLY | 255 << 8)
        time.sleep(0.1)

    # mark -  Event method
    def moveEvent(self, e):
        print('ViewMain: moveEvent')

    # mark -  Event method
    def mouseMoveEvent(self, e):
        print('ViewMain: mouseMoveEvent')

    # mark -  Event method
    def mouseReleaseEvent(self, e):
        print('ViewMain: mouseReleaseEvent')

    # mark -  Event method
    def mousePressEvent(self, e):
        print('ViewMain: mousePressEvent')

        x = e.x()
        y = e.y()

        choice = self.tool_radio_chk
        self.make_threshold(x, y, choice)

    def make_threshold(self, x, y, choice):

        # 정수형 으로 변환
        _x = int(x)
        _y = int(y)

        # error 예외 처리
        h, w = self.gray_scale_img.shape[:2]
        if w < _x or h < _y:
            print('ViewMain: position OVER')
            return
        if _x is 0:
            return

        # 마스크 영역 채우기
        self.flood_mask[:] = 0
        cv.floodFill(self.gray_scale_img, self.flood_mask, (_x, _y), 1,
                     self.threshold,
                     self.threshold,
                     self.flood_fill_flags)
        mask_copy = self.flood_mask[1:-1, 1:-1].copy()

        # 사용자 선택한 라디오 값 의 mask 마우스 포지션 저장
        mouse_position = (_x, _y)
        MASK_LIST[choice] = mask_copy
        MOUSE_LIST[choice] = mouse_position

        # 사용자 클릭 threshold 정보를 call back.
        _call = self.call_click_threshold
        _call(MOUSE_LIST)

        # main view 화면을 update 합니다.
        self.update_screen()

    def update_screen(self):
        print('ViewMain: update_screen')

        # 화면에 보여질 칼라 이미지 레벨을 조정 하고
        level_image = img_level.tissue_process(self.screen_img,
                                               0,
                                               self.level_window,
                                               self.level_muscle,
                                               0.1)

        # 이미지 광역 threshold
        level_image = img_threshold.all_bgr(level_image)

        length = len(MASK_LIST)
        for i in range(0, length):

            # 사용자 선택한 라디오 값 의 마스크 가져 오기
            self.mask_img = MASK_LIST[i]

            # 사용자 선택 threshold 내부 칠하기
            a, b, c = setting.ROI_COLOR[i]
            level_image[self.mask_img == 255] = [a, b, c]

        # 화면에 보여 주기
        pix_image = img_convert_qt.bgr_to_pixImage(level_image)
        self.q_graphic.setPixmap(pix_image)
        self.repaint()

    # 레벨이 적용된 환면을 update 합니다.
    def update_level(self):
        print('ViewMain: update_level')

        # 이미지 레벨링
        level_image = img_level.tissue_process(self.screen_img,
                                               0,
                                               self.level_window,
                                               self.level_muscle,
                                               0.1)
        # 레벨 적용 이미지 화면에 보이기
        level_image = img_threshold.all_bgr(level_image)

        # threshold 가능한 이미지 update
        self.gray_scale_img = level_image

        # 화면에 보이는 이미지
        pix_image = img_convert_qt.bgr_to_pixImage(level_image)
        self.q_graphic.setPixmap(pix_image)
        self.repaint()
        return level_image

    # 사용 자가 선택한 threshold radio 버튼을 update 합니다.
    def user_threshold_change(self, user_choice):
        self.tool_radio_chk = user_choice
        self.update_screen()

    def mouse_to_threshold(self, mouse_data):
        for i in range(0, len(mouse_data)):
            _tuple = mouse_data[i]
            if _tuple is None:
                pass
            else:
                x = _tuple[0]
                y = _tuple[1]

                # 포지션 값으로 threshold 만들어 줍니다.
                self.make_threshold(x, y, i)

    @classmethod
    def clean_mask(cls):
        for i in range(0, setting.USER_CHOICE_COUNT):
            MASK_LIST[i] = None

    @classmethod
    def clean_mouse(cls):
        for i in range(0, setting.USER_CHOICE_COUNT):
            MOUSE_LIST[i] = None

    @classmethod
    def get_mask_list(cls):
        return MASK_LIST

    @classmethod
    def get_mouse_list(cls):
        return MOUSE_LIST

    @classmethod
    def set_mask(cls, mask, number):
        MASK_LIST[number] = mask
