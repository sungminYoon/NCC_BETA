"""
Created by SungMin Yoon on 2022-10-19..
Copyright (c) 2022 year NCC (National Cancer Center). All rights reserved.
"""
from ..algorithm import cv_orb
from ..model.roi import Roi
from LAB.config import setting


def input_list(standard, group_list: list):

    print('verification: input_list')
    user_roi: Roi = standard

    i = 0
    for _obj in group_list:

        if _obj is None:
            pass
        else:

            # obj 에 객체 예외 처리
            roi: Roi

            try:
                # 리스트 객체의 하위 객체를 가져 옵니다.
                roi = _obj[1]
                image_index = _obj[0]

                # ORB 알고 리즘을 사용 사용자 이미지 와 비교
                score, count = cv_orb.features_orb(user_roi.image_mask, roi.image_mask)
                print('verification: ', image_index + 1, ' score -> ', score, ' : count -> ', count)

                # 너무 다른 것은 POP 합니다. score 낮을 수록 비슷함, count 높을 수록 비슷함
                if score > setting.ORB_SCORE or count < setting.ORB_COUNT:
                    group_list.pop(i)
                    group_list.insert(i, None)

            # obj 객체 error 처리
            except TypeError:
                pass

        i = i + 1

