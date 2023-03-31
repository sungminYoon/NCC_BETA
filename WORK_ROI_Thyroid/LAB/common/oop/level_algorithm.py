"""
Created by SungMin Yoon on 2022-03-03..
Copyright (c) 2021 year NCC (National Cancer Center). All rights reserved.
"""
import random
import cv2 as cv
from LAB.common.util import img_level, img_threshold, point2D, img_empty
from LAB.common.algorithm import magic_wand
from LAB.common.model.roi import Roi
from LAB.config import setting


class LevelAlgorithm:

    current_roi: Roi            # 현재 처리할 roi

    h = None                    # 이미지 높이
    w = None                    # 이미지 넓이
    user_choice = None          # 사용자 선택 algorithm
    x_current_center = None     # 현재 roi 중심 좌표 x
    y_current_center = None     # 현재 roi 중심 좌표 y

    threshold_list: list    # 이미지 1개의 전체 threshold
    compare_list: list      # level img 비교 결과
    break_list: list        # level img 나눈 결과
    magic_list: list        # 마법봉 처리 결과 마스크 리스트

    def __init__(self):
        print('Level: init')

        # 리스트 초기화
        self.threshold_list = []
        self.compare_list = []
        self.break_list = []
        self.magic_list = []

    # image level 로 분할 합니다.
    def img_break(self, img, level_window, level_muscle, value):

        # 리스트 비움
        self.break_list.clear()

        # 처리 image 크기를 save
        self.h, self.w = img.shape[:2]

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

        # level complete 리스트
        return self.break_list

    # level 로 나눈 image 비교 합니다.
    def img_compare(self, current_roi, level_images):

        # 비교 리스트 비우고
        self.compare_list.clear()
        self.threshold_list.clear()
        self.magic_list.clear()

        # 현재 처리할 ROI
        self.current_roi = current_roi

        # 현재 roi 좌표의 중심
        self.x_current_center, self.y_current_center = self.moments_to_points(self.current_roi.position_list)

        # level 이미지 roi 처리 시작
        for img in level_images:

            # 사용자 선택 algorithm 분기
            if 'LEVEL_1' is setting.ALGORITHM[self.user_choice]:
                """
                    LEVEL_1: 최적화 algorithm
                    갑상선 
                    연속 적인 모양 변화 roi 찾기에 좋다.
                    속도 제일 빠름
                """

                # 이미지 하나에 대한 모든 threshold 좌표 리스트
                self.threshold_list = img_threshold.all_cnt(img)
                self.level_1()

            if 'LEVEL_2' is setting.ALGORITHM[self.user_choice]:
                """
                    LEVEL_2: threshold 변화만 추가된 algorithm
                    갑상선 노이즈
                    모양 변화 와 노이즈 roi 대응이 가능 하다
                    속도 중간
                """

                # 증감 값의 threshold 와 반환 마스크
                for i in range(10, setting.LOOP_LEVEL_2):

                    # level 처리 된 image 현재 관심 영역 중심 좌표와 threshold 값을 이용해 mask 생성 합니다.
                    mask = magic_wand.get_threshold(i, img, self.x_current_center, self.y_current_center)

                    # 마스크 ROI 객체로 변환
                    roi = Roi()
                    roi.set_mask(mask)

                    # 마스크 좌표  저장
                    self.threshold_list.append(roi.position_list)

                # level_2 algorithm 실행
                self.level_2()

            if 'LEVEL_3' is setting.ALGORITHM[self.user_choice]:
                """
                    LEVEL_3: threshold 변화 와 랜덤이 추가된 algorithm
                    침샘 noise 심한 roi 찾기에 능하다
                    하지만 갑상선 같은 경우는 띄엄 띄엄 못찾는 경우가 많다.
                    속도 LEVEL_1 대비 느린편
                """

                # 증감 값의 threshold 와 반환 마스크
                for i in range(10, setting.LOOP_LEVEL_3):

                    # level 처리 된 image 현재 관심 영역 중심 좌표와 threshold 값을 이용해 mask 생성 합니다.
                    mask = magic_wand.get_threshold(i, img, self.x_current_center, self.y_current_center)

                    # 마스크 ROI 객체로 변환
                    roi = Roi()
                    roi.set_mask(mask)

                    # 마스크 좌표  저장
                    self.threshold_list.append(roi.position_list)

                # level_3 algorithm 실행
                self.level_3()

            # 비교 결과 반환
            return self.compare_list

    def level_1(self):

        # 찾은 threshold 만큼 반복
        for cnt in self.threshold_list:

            # 찾아넨 threshold 크기에 마진을 값을 줍니다 (필터 역할 마진값 보다 큰 값은 통과 못함: 속도와 정확도 높임).
            _, _, w, h = cv.boundingRect(cnt)
            margin_w: int = w / setting.ROI_SIZE_MARGIN
            margin_h: int = h / setting.ROI_SIZE_MARGIN
            margin_w = margin_w
            margin_h = margin_h
            a = self.current_roi.rect_width + margin_w
            b = self.current_roi.rect_width - margin_w
            c = self.current_roi.rect_height + margin_h
            d = self.current_roi.rect_height - margin_h

            # 마진 영역 안의 크기만 받습니다.
            if a > w > b and c > h > d:

                # roi 리스트 의 좌표의 중심
                cX, cY = self.moments_to_points(cnt)

                # 2점 사이 거리 (현재 roi 의 사각형 중심)
                dist = point2D.dot_distance(self.current_roi.rect_center_x,
                                            self.current_roi.rect_center_y,
                                            cX,
                                            cY)

                # MINIMUM_DISTANCE 미만의 거리 저장
                if setting.DISTANCE_LEVEL_1 > dist:

                    # roi 에 그려 넣을 마스크 생성
                    mask = img_empty.np_image(self.h, self.w)
                    cv.drawContours(mask, [cnt], 0, (255, 0, 0), cv.FILLED)

                    # roi 생성
                    roi = Roi()
                    roi.set_mask(mask)
                    self.compare_list.append(roi)

    def level_2(self):

        # 찾은 threshold 만큼 반복
        for cnt in self.threshold_list:

            # roi 리스트 의 좌표의 중심
            cX, cY = self.moments_to_points(cnt)

            # 2점 사이 거리 (현재 roi 모멘트 중심)
            dist = point2D.dot_distance(self.x_current_center,
                                        self.y_current_center,
                                        cX,
                                        cY)

            # MINIMUM_DISTANCE 미만의 거리 저장
            if setting.DISTANCE_LEVEL_1 > dist:

                # roi 에 그려 넣을 마스크 생성
                mask = img_empty.np_image(self.h, self.w)
                cv.drawContours(mask, [cnt], 0, (255, 0, 0), cv.FILLED)

                # roi 생성
                roi = Roi()
                roi.set_mask(mask)
                self.compare_list.append(roi)

    def level_3(self):

        # 찾은 threshold 만큼 반복
        for cnt in self.threshold_list:

            # roi 리스트 의 좌표의 중심
            cX, cY = self.moments_to_points(cnt)

            # 반복 으로 다양한 값 입력
            for i in range(0, setting.RANDOM_LEVEL_3):

                # 램덤 값으로 위치 변화
                rx = random.randrange(-20, 20)
                ry = random.randrange(-20, 20)
                current_x = self.x_current_center + rx
                current_y = self.y_current_center + ry

                # 2점 사이 거리 (현재 roi 모멘트 중심)
                dist = point2D.dot_distance(current_x,
                                            current_y,
                                            cX,
                                            cY)

                # MINIMUM_DISTANCE 미만의 거리 저장
                if setting.DISTANCE_LEVEL_3 > dist:

                    # roi 에 그려 넣을 마스크 생성
                    mask = img_empty.np_image(self.h, self.w)
                    cv.drawContours(mask, [cnt], 0, (255, 0, 0), cv.FILLED)

                    # roi 생성
                    roi = Roi()
                    roi.set_mask(mask)
                    self.compare_list.append(roi)

    @classmethod
    def moments_to_points(cls, cnt):

        M = cv.moments(cnt)
        if M["m00"] != 0:
            x = int(M["m10"] / M["m00"])
            y = int(M["m01"] / M["m00"])

        else:
            # threshold 중심 좌표를 가져옴
            x, y = 0, 0

        return x, y
