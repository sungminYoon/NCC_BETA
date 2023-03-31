"""
Created by SungMin Yoon on 2021-02-22..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""
import numpy as np


# target 값과 가장 유사한 값의 인덱스
def min_diff_pos(array_like, target):
    return np.abs(np.array(array_like) - target).argmin()


# 데이터 중복 제거
def duplication(data_list):
    result = list(set(data_list))
    print(result)


# 데이터 중복 제거 비교
def duplication_compare(data_list):

    save_list = []

    manufacturing_list = removal_garbage(data_list)

    for i in range(0, len(manufacturing_list), 2):

        add_list = []

        list_1 = manufacturing_list[i]
        SetList1 = set(list_1)

        list_2 = manufacturing_list[i + 1]
        SetList2 = set(list_2)

        a = SetList1.difference(SetList2)
        b = SetList2.difference(SetList1)

        list_a = list(a)
        list_b = list(b)

        for obj in list_a:
            add_list.append(obj)

        for obj in list_b:
            add_list.append(obj)

        save_list.append(add_list)

        print('data_structure: duplication_compare = ', save_list)

    return save_list


# 데이터 리스트 에 None 같은 것이 있다면 pop 합니다.
def removal_garbage(data_list):

    for obj_list in data_list:

        i = 0
        for obj in obj_list:

            if obj is None:
                _list: list = obj_list
                _list.pop(i)

            i = i + 1

    return data_list
