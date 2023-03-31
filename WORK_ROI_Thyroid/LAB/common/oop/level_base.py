"""
Created by SungMin Yoon on 2022-03-21..
Copyright (c) 2021 year NCC (National Cancer Center). All rights reserved.
"""


import cv2 as cv
from LAB.common.util import img_level
from LAB.common.util import img_threshold, point2D, img_empty
from LAB.common.model.roi import Roi


class LevelBase:

    compare_list = None     # level img 비교 결과
    break_list = None       # level img 나눈 결과

    def __init__(self):
        print('Level: init')

        # 리스트 초기화
        self.compare_list = []
        self.break_list = []

    # image level 로 분할 합니다.
    def img_break(self, img, level_window, level_muscle, value):

        self.break_list.clear()

        # level_start ~ level_end 까지 반복
        start = level_muscle - value
        end = level_muscle + value

        # 위로 이미지 레벨링
        up_level_image = img_level.tissue_process(img, 0, level_window, end, 0.1)

        # level 결과 저장
        self.break_list.append(up_level_image)

        # 아래로 이미지 레벨링
        down_level_image = img_level.tissue_process(img, 0, level_window, start, 0.1)

        # level 결과 저장
        self.break_list.append(down_level_image)

        # level 처리 완료 리스트
        return self.break_list

    # level 로 나눈 image 비교 합니다.
    def img_compare(self, standard_roi, level_images):

        self.compare_list.clear()

        # level 이미지 roi 처리 시작
        for img in level_images:

            # 처리 image 크기를 save
            h, w = img.shape[:2]

            # 이미지 하나에 대한 모든 threshold 좌표 리스트
            threshold_list = img_threshold.all_cnt(img)

            for cnt in threshold_list:

                # 모멘트 algorithm 사용
                M = cv.moments(cnt)
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                else:
                    # threshold 중심 좌표를 가져옴
                    cX, cY = 0, 0

                # 2점 사이 거리
                dist = point2D.dot_distance(standard_roi.rect_center_x,
                                            standard_roi.rect_center_y,
                                            cX,
                                            cY)

                # MINIMUM_DISTANCE 미만의 거리 만 roi 변경 저장
                if dist < 20:

                    print('Auto: _level_compare -> mask generating..')
                    mask = img_empty.np_image(h, w)
                    cv.drawContours(mask, [cnt], 0, (255, 0, 0), cv.FILLED)

                    '''image Roi 객체로 생성'''
                    # roi 생성
                    roi = Roi()
                    roi.set_mask(mask)

                    # roi 저장
                    self.compare_list.append(roi)

        # 처리 완료 리스트
        return self.compare_list

