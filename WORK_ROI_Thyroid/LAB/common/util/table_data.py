"""
Created by SungMin Yoon on 2022-12-28..
Copyright (c) 2022 year NCC (National Cancer Center). All rights reserved.
"""
from LAB.common.model.roi import Roi
from LAB.work.view.table_right_cell import TableRightCell


def pop(number, data_list):
    print('TableRight: data_pop')

    # 데이터 객체 꺼내기
    for obj_group in data_list:

        # 리스트로 캐스팅
        obj_list: list = obj_group

        # 리스트 카운트 i
        i = 0

        for obj in obj_list:

            # 객체가 비어 있다면
            if obj is None:

                # 해당 데이터 를 지워 준다.
                obj_list.pop(i)

            else:
                # 객체를 튜플로 캐스팅
                t: tuple = obj
                image_num = 0

                # 예외 처리
                try:
                    image_num, _ = t
                except TypeError:
                    print('TableRight: data_pop -> TypeError =', t)

                # 이미지 넘버 와 사용자 선택 넘버 같다면
                if image_num == number:
                    # 해당 데이터 를 지워 준다.
                    obj_list.pop(i)

            # 리스트 카운트 증감
            i = i + 1

    print('TableRight: data_pop =', data_list)


def add(number, group_list, cell_data: TableRightCell):
    print('TableRight: data_add')

    # 셀에서 마스크 데이터 를 가져 옵니다.
    masks = cell_data.get_mask_list()

    i = 0
    for mask in masks:

        if mask is not None:

            # roi 생성
            roi = Roi()
            roi.set_mask(mask)

            # 그룹 리스트에 생성한 roi 저장
            t = (number, roi)

            try:
                # 원 싸이클 아래 위 검색 그룹
                data_list = group_list[i]

            except IndexError:

                for j in range(0, i):
                    new_list = []
                    group_list.append(new_list)

                # 원 싸이클 아래 위 검색 그룹
                data_list = group_list[i]

            # 데이터 가져 오기
            j = 0
            for data in data_list:
                if data is not None:

                    # 데이터 객체 캐스팅
                    idx, obj = data
                    idx_int = int(idx)

                    # 중복 교환
                    if idx_int == number:
                        data_list[j] = t
                        return

                    # 다음 리스트 인덱스
                    j = j + 1

            # 사용자 선택 roi 추가
            data_list.append(t)
            # print('TableRight: data_add =', t, '->', group_list)

        # 다음 마스크
        i = i + 1