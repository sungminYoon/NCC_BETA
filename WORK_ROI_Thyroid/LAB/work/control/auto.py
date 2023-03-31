"""
Created by SungMin Yoon on 2021-06-15..
Copyright (c) 2021 year NCC (National Cancer Center). All rights reserved.
"""
import time
import cv2 as cv
from LAB.config import setting
from LAB.common.util import verification
from LAB.common.model.roi import Roi
from LAB.common.oop.level_algorithm import LevelAlgorithm
from LAB.common.oop.find_dimensions import FindDimensions


STATE_UP = 1        # 위로 탐색 상태
STATE_DOWN = 0      # 아래로 탐색 상태


class Auto:
    """
        단어 설명
        threshold -> 사용 자가 선택한 영역 입니다.
        mask -> 선택 또는 찾은 영역의 이미지 입니다.
        roi -> 사용 자가 선택한 threshold 와 mask 정보를 model 객체로 변환한 "관심 영역" 입니다.
    """

    level_window = setting.DEFAULT_LEVEL_WINDOW     # 윈도우 레벨
    level_muscle = setting.PARAM_LEVEL_MUSCLE       # 근육 레벨

    call_progress = None                # 콜백 객체로 진행 상황을 알립 니다.
    cv_images = None                    # CV 이미지 들

    current_roi: Roi                    # 현재 처리 진행 되는 roi 모델 객체
    standard_roi: Roi                   # 처리 표준 roi 모델 객체
    level_algorithm: LevelAlgorithm     # level 관련 객체 (비교)
    find_dimensions: FindDimensions     # 기준 roi 비슷한 level 찾기

    color_list: list                    # 무수정 image 에 mask 색칠한 이미지 입니다.
    user_roi_list: list                 # 사용자 선택 roi 모델 객체 리스트
    group_list: list                    # 사용자 roi 처리 list 모음  : n 저장

    level_start: int = 0                # level 시작
    level_end: int = 0                  # level 종료
    update_level_count: int = 0         # level 처리 범위 개수 update

    current_img = None                  # 현재 처리 이미지
    current_index: int = 0              # 현재 처리 이미지 인덱스
    result_tuple_roi = None             # 결과 저장 튜플

    def __init__(self):
        print('Auto: init')
        print(self.__doc__)

        # 리스트 생성
        self.user_roi_list = []
        self.group_list = []
        self.color_list = []

        # 객체 생성
        self.level_algorithm = LevelAlgorithm()
        self.find_dimensions = FindDimensions()

    def clean(self):

        # 리스트 초기화
        self.user_roi_list.clear()
        self.group_list.clear()
        self.color_list.clear()

    # 사용자 선택 mask 를 roi 로 변환 합니다.
    def create_roi(self, mask_list):
        print('Auto: create_roi')

        # 사용자 선택 roi mask 만큼 반복
        length = len(mask_list)
        for i in range(0, length):

            # 사용자 선택 mask 가져 오기
            img = mask_list[i]

            if img is None:
                self.user_roi_list.append(None)
            else:
                # mask image roi 모델 객체로 저장
                roi = Roi()
                roi.set_mask(img)
                self.user_roi_list.append(roi)

    def image_format(self, cv_images):

        for img in cv_images:

            # image RGB 칼라로 변환 합니다.
            img = cv.cvtColor(img, cv.COLOR_RGB2BGR)
            self.color_list.append(img)

    # 이미지 roi 처리를 시작 합니다.
    def handler_roi(self, cv_images, start_point, end_point, user_select_index, algorithm_choice):
        print('Auto: handler_roi')

        # 처리 할 cv image 들 저장
        self.cv_images = cv_images

        # 이미지 준비
        self.image_format(cv_images)

        # 정수형 으로 변환
        if start_point is None:
            start_point = 1
        start = int(start_point)
        end = int(end_point)

        # 사용자 지정 인덱스
        middle = user_select_index

        # 사용자 지정 윈도우, 근육 값
        window = int(self.level_window)
        muscle = int(self.level_muscle)

        # 처리 시간 계산
        time_start = time.time()

        # 사용자 선택 roi 개수 만큼 반복
        mask_count = 0
        for user_roi in self.user_roi_list:

            # 아래 , 위 순으로 처리
            self.auto_process_roi(STATE_DOWN, start, middle, window, muscle, algorithm_choice, user_roi, mask_count)
            self.auto_process_roi(STATE_UP, end, middle, window, muscle, algorithm_choice, user_roi, mask_count)
            mask_count = mask_count + 1

        print("Auto: handler_roi -> Algorithm auto_process_roi Time = ", time.time() - time_start)

        # 검증 (사용자 선택 mask 와 비슷한 mask 만 저장 합니다.)
        i = 0
        for mask in self.user_roi_list:
            if mask is not None:
                g_list = self.group_list[i]
                verification.input_list(mask, g_list)
            i = i + 1

        # 처리 결과 반환
        return self.group_list

    # roi 를 처리 합니다.
    def auto_process_roi(self, state, value, middle, window, muscle, algorithm_choice_list, obj, user_mask_count):

        # 한 주기 처리 결과 roi 저장
        one_cycle_list = []

        # 사용자 선택 roi
        user_roi: Roi = obj
        if user_roi is not None:

            # 사용자 선택 roi 를 처리할 current_roi 저장 합니다.
            self.current_roi = self.user_roi_list[user_mask_count]

            # 처리 표준(standard_roi)이 될 current_roi 를 저장 하고
            self.standard_roi = self.current_roi

            # middle(사용자 선택 index) 을 기준 으로 위아래 탐색 한다.
            self.current_index = 0
            _min = 0
            _max = 0

            # 아래로 탐색
            if state == STATE_DOWN:
                _min = value
                _max = middle

            # 위로 탐색
            if state == STATE_UP:
                _min = middle
                _max = value

            i = 1
            for _ in range(_min, _max):

                # 아래로 탐색
                if state == STATE_DOWN:
                    self.current_index = middle - i

                # 위로 탐색
                if state == STATE_UP:
                    self.current_index = middle + i

                # 현재 이미지 index 처리 image 개수 보다 크면 정지
                if self.current_index >= len(self.cv_images):
                    break

                # 현재 처리 할 이미지
                self.current_img = self.cv_images[self.current_index]

                # algorithm 리스트 에서 사용자 선택 algorithm 가져 오기
                self.level_algorithm.user_choice = algorithm_choice_list[user_mask_count]

                while True:

                    # images level 나누기
                    level_list = self.level_algorithm.img_break(self.current_img, window, muscle, self.update_level_count)

                    # images level 비교 처리
                    process_list = self.level_algorithm.img_compare(self.current_roi, level_list)

                    # level 처리 ROI 넓이가 가장 비슷 한것 찾기: 기본 algorithm
                    self.result_tuple_roi = self.find_dimensions.find_roi(self.current_roi,
                                                                          process_list,
                                                                     self.current_index)

                    # 비슷한 넓이를 찾지 못하면 update 후 레벨 처리 계속
                    if self.find_dimensions.loop_pro_level is True:
                        self.update_level_count = self.find_dimensions.update_level_count
                    else:
                        break

                    # 레벨 처리 반복 횟 수가 200 개가 넘으면 정지
                    if self.update_level_count > setting.MAX_LEVEL_COUNT:
                        break

                # 결과를 list 저장
                one_cycle_list.append(self.result_tuple_roi)

                # 처리 범위 초기화
                self.update_level_count = 0
                self.find_dimensions.__init__()

                # 진행바
                i = i + 1
                call = self.call_progress
                call(100, i)

            # 사용자 선택 one cycle 리스트 끝에 추가
            add_user_tuple = (middle, self.standard_roi)
            one_cycle_list.append(add_user_tuple)

            # 1주기 결과 를 무수정 image 색칠 합니다.
            self.change_img_color(one_cycle_list, user_mask_count)

            # 1주기 처리 ROI 저장 그룹화
            self.group_list.append(one_cycle_list)

    # 1주기 proc_roi 를 무수정 image 색칠 합니다.
    def change_img_color(self, cycle_list, user_mask_count):

        # 색을 저장 합니다.
        roi_color: list = []

        # user 선택한 roi 들에 색을 정해 줍니다.
        for i in range(0, setting.USER_CHOICE_COUNT):
            a, b, c = setting.ROI_COLOR[i]
            roi_color.append(tuple([a, b, c]))

        # 순환 list roi 객체를 가져 옵니다.
        for obj in cycle_list:
            if obj is not None:

                # roi 처리된 object, image index, roi 를 가지고 옵니다.
                index, roi = obj

                # 무수정 image 가져 옵니다.
                img = self.color_list[index]

                # roi 를 그려 주고 색칠 합니다.
                a, b, c = roi_color[user_mask_count]
                cv.drawContours(img, [roi.position_list], 0, (a, b, c), cv.FILLED)

                # 색칠한 image 리스트에 저장 합니다.
                self.color_list[index] = img


