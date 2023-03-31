"""
Created by SungMin Yoon on 2022-03-17..
Copyright (c) 2021 year NCC (National Cancer Center). All rights reserved.
"""
from LAB.common.oop.attempt import Attempt
from LAB.common.util import data_structure
from LAB.common.model.roi import Roi


class FindFusion:

    update_level_count: int
    process_level_count: int
    loop_pro_level: bool

    loop_attempt = False  # attempt 반복 처리 할지 판정

    attempt = Attempt()
    current_roi: Roi

    def __init__(self):
        print('FindFusion: init')
        self.update_level_count = 0
        self.process_level_count = 0
        self.loop_pro_level = False

        self.attempt = Attempt()

    def challenge_roi(self, before_roi, process_list, image_index, img):

        # standard_roi 와 가장 비슷한 넓이의 roi 저장 리스트 생성
        dimension_list = []

        # 이미지 레벨 범위 처리를 증가 시키는 카운트 입니다.
        self.update_level_count = self.update_level_count + 1

        # 이미지 level 카운트 입니다.
        self.process_level_count = self.process_level_count + 1

        # data 없으면 종료
        if len(process_list) < 1:
            return

        # 리스트 속의 roi 객체의 넓이를 따로 저장 합니다.
        for obj in process_list:
            roi: Roi = obj
            dimension_list.append(roi.rect_dimensions)

        # 앞전 결과 roi 넓이와 가장 가까운 값의 number 찾 습니다.
        number = data_structure.min_diff_pos(dimension_list, before_roi.rect_dimensions)
        find_roi = process_list[number]

        # 이미지 level 횟수가 200 이상이 되면
        if self.process_level_count <= 200:

            # 이미지 level 카운트 초기화
            self.process_level_count = 0

            # 이미지 level 중지
            self.loop_pro_level = False

            # 이미지 index roi 묶어 보내기
            _tuple = (image_index, find_roi)
            return _tuple

        '''roi 찾지 못 했다면 처리 roi 는 예전을 유지 한다'''
        # 찾은 roi 로 현재 처리 진행 roi 를 바꿔 줍니다.
        self.current_roi = find_roi

        '''레벨 image 더 만들어 낼지 판정'''
        # 앞전에 roi 넓이를 a 에 입력 합니다.
        a = before_roi.rect_dimensions

        # 넓이 상한선 값과 하안선 값을 만들어 줍니다.
        b = a / 2
        v_min = a - b
        v_max = a + b

        # roi 찾은 넓이를 f 에 입력 합니다.
        find_dimensions = find_roi.rect_dimensions

        # 넓이 범위 안에 있다면
        if v_min > find_roi.rect_dimensions or find_roi.rect_dimensions > v_max:
            # 이미지 level 종료
            self.loop_pro_level = False

            # 이미지 index roi 묶어 보내기
            _tuple = (image_index, find_roi)
            return _tuple

        # 찾은 넓이가 너무 작다면
        if find_dimensions < 20:
            # threshold 증감 처리
            _tuple = self.attempt.unclear_process(self.current_roi, img, image_index)
            return _tuple

        # 이미지 index roi 묶어 보내기
        _tuple = (image_index, find_roi)
        return _tuple
