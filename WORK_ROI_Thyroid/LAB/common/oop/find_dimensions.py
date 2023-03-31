"""
Created by SungMin Yoon on 2022-03-17..
Copyright (c) 2021 year NCC (National Cancer Center). All rights reserved.
"""
from LAB.common.util import data_structure
from LAB.common.model.roi import Roi
from LAB.config import setting


class FindDimensions:

    update_level_count: int
    process_level_count: int
    loop_pro_level: bool
    current_roi: Roi

    def __init__(self):
        print('FindDimensions: init')
        self.update_level_count = 0
        self.process_level_count = 0
        self.loop_pro_level = False

    # 사용자 roi 와 가장 비슷한 roi 를 검색.
    def find_roi(self, before_roi, process_list, image_index):

        # standard_roi 와 가장 비슷한 넓이의 roi 저장 리스트 생성
        dimension_list = []

        # 이미지 레벨 범위 처리를 증가 시키는 카운트 입니다.
        self.update_level_count = self.update_level_count + 1

        # data 없으면 종료
        if len(process_list) < 1:
            return

        # 리스트 속의 roi 객체의 넓이를 따로 저장 합니다.
        for obj in process_list:
            roi: Roi = obj
            dimension_list.append(roi.rect_dimensions)

        # 앞전 결과 roi 넓이와 가장 가까운 값의 number 검색.
        number = data_structure.min_diff_pos(dimension_list, before_roi.rect_dimensions)
        find_roi: Roi = process_list[number]

        # 레벨 처리를 더 할지 찾아낸 최소 크기 비교 판정
        if find_roi.rect_dimensions < setting.MINIMUM_DIMENSIONS:
            self.loop_pro_level = True
        else:
            self.loop_pro_level = False

            # 찾은 roi 로 현재 처리 진행 roi 를 바꿔 줍니다.
            self.current_roi = find_roi

        # image index 와 roi 묶어 보내기
        _tuple = (image_index, find_roi)
        return _tuple



