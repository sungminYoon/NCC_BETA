"""
Created by SungMin Yoon on 2021-05-24..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""
import time
import cv2 as cv
from LAB.common.util import img_empty

# 예외 처리 전역 변수
DEFECTS = None


# 마스크 컨투어 처리 함수 입니다.
def contour_to_bgr(img_gray):
    # print('img_threshold: contour_to_bgr')

    global DEFECTS

    # threshold 로직
    cv_image = cv.cvtColor(img_gray, cv.COLOR_BGR2RGB)
    ret, th = cv.threshold(img_gray, 127, 255, 0)
    contours, hierarchy = cv.findContours(th, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

    # mask 컨투어 그리기 로직
    group_number: int = 0

    for cnt in contours:
        group_number = group_number + 1

        # 빈 이미지
        h, w = img_gray.shape[:2]
        mask = img_empty.np_image(h, w)

        # 빈 image 마스크 그리기
        cv.drawContours(mask, [cnt], 0, (255, 0, 0), cv.FILLED)
        time.sleep(0.1)

    # 컨투어 그린 마스크
    return cv_image


# GRAY 처리 광역 threshold 입니다.
def all_bgr(cv_image):
    print('img_threshold: all_bgr')

    img_gray = cv.cvtColor(cv_image, cv.COLOR_BGR2GRAY)
    ret, img_binary = cv.threshold(img_gray, 127, 255, 0)
    contours, hierarchy = cv.findContours(img_binary, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        # (255, 0, 0) 파란색
        cv.drawContours(cv_image, [cnt], 0, (255, 0, 0), 1)

    return cv_image


# BGR2RGB 처리 광역 threshold 입니다.
def all_gray_to_bgr(img_gray):
    print('img_threshold: all_gray_to_bgr')

    cv_image = cv.cvtColor(img_gray, cv.COLOR_BGR2RGB)
    ret, img_binary = cv.threshold(img_gray, 127, 255, 0)
    contours, hierarchy = cv.findContours(img_binary, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        # (255, 0, 0) 파란색
        cv.drawContours(cv_image, [cnt], 0, (255, 0, 0), 1)

    return cv_image


# 사각형 으로 그려 줍니다.
def all_rectangle(cv_image):
    print('img_threshold: all_rectangle')

    ret, img_binary = cv.threshold(cv_image, 127, 255, 0)
    contours, hierarchy = cv.findContours(img_binary, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        # 관심 영역 사각형 표시
        x, y, w, h = cv.boundingRect(cnt)
        cv_image = cv.rectangle(cv_image, (x, y), (x + w, y + h), (255, 255, 255), 1)

    return cv_image


# 빈 image threshold 전부 그립 니다.
def all_mask(image):
    print('img_threshold: all_mask')

    cut_img_list: list = []

    ret, img_binary = cv.threshold(image, 127, 255, 0)
    contours, hierarchy = cv.findContours(img_binary, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        h, w = image.shape[:2]
        mask = img_empty.np_image(h, w)
        cv.drawContours(mask, [cnt], 0, (255, 0, 0), cv.FILLED)
        cut_img_list.append(mask)

    return cut_img_list


# threshold 좌표를 리스트 형태로 반환 합니다.
def all_cnt(image):
    print('img_threshold: all_cnt')

    cnt_list: list = []

    ret, img_binary = cv.threshold(image, 127, 255, 0)
    contours, hierarchy = cv.findContours(img_binary, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        cnt_list.append(cnt)

    return cnt_list


# threshold 크기가 적정 50 크기 인지 확인 합니다.
def all_mask_chk(image):
    print('img_threshold: all_mask_chk')

    ret, img_binary = cv.threshold(image, 127, 255, 0)
    contours, hierarchy = cv.findContours(img_binary, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        # 빈 이미지
        h, w = image.shape[:2]
        mask = img_empty.np_image(h, w)

        # 빈 이미지 에 마스크 그리기
        cv.drawContours(mask, [cnt], 0, (255, 0, 0), cv.FILLED)

        # 마스크 그리기 지연 처리
        time.sleep(0.1)

        # 마스크 사이즈
        chk_size = cv.countNonZero(mask)

        # Contours 그릴 수 있는 마스크 크기면 실행
        if chk_size > 50:
            chk = True
        else:
            chk = False

    return chk
