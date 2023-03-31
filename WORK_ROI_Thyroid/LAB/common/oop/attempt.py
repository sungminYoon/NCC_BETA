"""
Created by SungMin Yoon on 2022-03-07..
Copyright (c) 2021 year NCC (National Cancer Center). All rights reserved.
"""
import cv2 as cv
import numpy as np
from LAB.common.model.roi import Roi


class Attempt:

    find_roi = None                 # 새로 찾은 결과 반환 ROI
    flood_mask = None               # 마법봉 algorithm 변수
    flood_fill_flags = None         # 마법봉 채우기 변수

    def __init__(self):
        print('Attempt: init')

    def unclear_process(self, current_roi, input_img, input_index):

        # 기준 roi 로 변경해 주고
        standard_roi: Roi = current_roi

        # roi 넓이 최소 값 10
        roi_size_value = 10

        # 연결성
        connectivity = 4

        # 마스크 영역 채우기 설정
        self.flood_fill_flags = (connectivity | cv.FLOODFILL_FIXED_RANGE | cv.FLOODFILL_MASK_ONLY | 255 << 8)

        # 마스크 영역 채우기
        self.flood_mask = np.zeros((512 + 2, 512 + 2), np.uint8)

        # 기준 threshold 좌표
        x = standard_roi.rect_center_x
        y = standard_roi.rect_center_y

        # threshold 포지션 증감 변수
        i: int = 1
        j: int = 0
        while True:

            # threshold 크기 3 ~ 50 까지 반복
            for threshold_value in range(3, 50):

                # 마법봉
                self.flood_mask[:] = 0
                cv.floodFill(input_img, self.flood_mask, (x,
                                                          y), 1,
                             threshold_value,
                             threshold_value,
                             self.flood_fill_flags)
                mask_copy = self.flood_mask[1:-1, 1:-1].copy()

                # roi 생성
                local_roi = Roi()
                local_roi.set_mask(mask_copy)
                self.find_roi = local_roi

                # threshold 증감 값 j 가 3 이상 이면 결과 반환
                if j > 3:

                    # 결과 튜플로 반환
                    result_tuple = (input_index, self.find_roi)
                    return result_tuple

                # 찾은 roi 넓이 편차 +, - 100 보다 크면
                if roi_size_value > 100:

                    # 허용 넓이 편차 0 초기화
                    roi_size_value = 0

                    # threshold 위치 x, y값 j 증감
                    j = j + 1

                    # for 문 계속
                    continue

                # value 범위 의 크기를 찾으면 종료
                if standard_roi.rect_dimensions + roi_size_value > local_roi.rect_dimensions > standard_roi.rect_dimensions - roi_size_value:

                    # 결과 튜플로 반환
                    result_tuple = (input_index, self.find_roi)
                    return result_tuple

                # value 범위 의 크기를 찾지 못하면 계속
                roi_size_value = roi_size_value + 1

                # threshold 위치 좌표를 이동 사 방위로 넓게 변화를 줌
                a = i % 2
                b = i % 3
                c = i % 4
                d = i % 5
                if a == 0:
                    x = x + j
                    y = y + j
                if b == 0:
                    x = x - j
                    y = y - j
                if c == 0:
                    x = x + j
                    y = y - j
                if d == 0:
                    x = x - j
                    y = y + j


