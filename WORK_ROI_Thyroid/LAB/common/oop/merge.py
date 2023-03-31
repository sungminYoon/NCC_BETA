"""
Created by SungMin Yoon on 2021-01-06..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""
import cv2 as cv
from ..model.roi import Roi


class Merge:

    # 기준이 되는 가장 큰 리스트
    mutable: list

    def __init__(self):
        self.mutable = list()

    def clear(self):
        self.mutable.clear()

    '''     Method explanation: set_list
        서로 다른 길이의 list 병합 하기 위해
        1. 가장 큰 길이의 self.mutable list 기준이 되어
        2. 입력 list 튜플 index 값을 보고 중간 중간 병합을 합니다.
        3. 다른 작은 리스트(input_list)를 계속 받아 들 입니다..
    '''
    def mask_overwrite(self, size, input_list):

        # 입력된 작은 리스트
        count = len(input_list)

        # size 를 입력 받아 가장 큰 list 만들고
        if len(self.mutable) == 0:
            self.mutable = [0]*size

        for i in range(0, count):

            # 인덱스 값을 get
            mask, index = input_list[i]

            # mutable 의 해당 index 정보를 넣어 줍니다.
            if self.mutable[index] == 0:
                self.mutable[index] = (mask, index)

            else:
                # mutable mask 입력 mask 합하고 다시 mutable 저장 합니다.
                mutable_mask, mutable_index = self.mutable[index]
                plus_mask = cv.add(mutable_mask, mask)
                self.mutable[mutable_index] = (plus_mask, mutable_index)

        # 병합 완료된 mutable
        return self.mutable

    def roi_overwrite(self, size, input_list):

        count = len(input_list)

        if len(self.mutable) == 0:
            self.mutable = [0]*size

        for i in range(0, count):

            roi, index = input_list[i]

            if self.mutable[index] == 0:
                self.mutable[index] = (roi, index)

        return self.mutable

    # 그룹 을 하나의 결과로 만듭니다.
    def auto_result_image(self, group, cv_images):
        print('Auto: _result_image')

        # 결과 저장 리스트
        merge_list = None

        # 그룹 에서 처리 완료된 roi 리스트 가져 오기
        for i in range(0, len(group)):

            # 병합(self.merge.mask_overwrite) param 에 넣기 위한 형식 으로 변환
            mask_list = []
            for _obj in group[i]:

                # obj 에 객체 예외 처리
                roi: Roi
                try:
                    # 리스트 객체의 하위 객체를 가져 옵니다.
                    roi = _obj[1]
                    image_index = _obj[0]

                    # mask 리스트 저장
                    mask = (roi.image_mask, image_index)
                    mask_list.append(mask)

                # obj 객체 error 처리
                except TypeError as e:
                    print('Auto: _result_image -> ', e)
                    pass

            # 완료 mask 병합
            merge_list = self.mask_overwrite(len(cv_images), mask_list)

        # 결과 리스트
        return merge_list




