"""
Created by SungMin Yoon on 2022-03-17..
Copyright (c) 2021 year NCC (National Cancer Center). All rights reserved.
"""
from LAB.common.oop.attempt import Attempt
from LAB.common.util import data_structure
from LAB.common.model.roi import Roi


class FindThreshold:

    attempt = Attempt()
    current_roi: Roi

    def __init__(self):
        print('FindThreshold: init')
        self.attempt = Attempt()

    def attempt_roi(self, before_roi, process_list, image_index, img):

        # standard_roi 와 가장 비슷한 넓이의 roi 저장 리스트 생성
        dimension_list = []

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

        '''roi 찾지 못 했다면 처리 roi 는 예전을 유지 한다'''
        # 찾은 roi 로 현재 처리 진행 roi 를 바꿔 줍니다.
        self.current_roi = find_roi

        _tuple = self.attempt.unclear_process(self.current_roi, img, image_index)
        return _tuple
