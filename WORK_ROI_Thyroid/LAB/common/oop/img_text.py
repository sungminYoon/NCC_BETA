"""
Created by SungMin Yoon on 2020-05-06..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""
import time
import numpy as np
from LAB.common.model.roi import Roi
from LAB.common.util import notice
from LAB.common.util import file_manager
from PIL import Image  # setting 에서 Pillow 설치


class ImgText:

    call_progress = None

    def __init__(self):
        pass

    def to_binary_one(self, day_folder, src_list):

        call = self.call_progress

        # src_list 형식은 개발자 임의 형태 입니다. -> list[int_obj(tuple (value, value))]
        for i in range(0, len(src_list)):
            int_obj = src_list[i]

            call(100, i)

            # list obj 를 가지고 옵니다.
            if src_list[i] == 0:
                pass
            else:
                src, index = int_obj

                # img 파일을 numpy 로 변환 합니다.
                img = np.array(src)

                # image 128 값 보다 색이 높은 곳을 1이라는 값으로 numpy -> binary 변환 합니다.
                binary = np.where(img > 128, 1, 0)

                print('ImgText: to_binary_loop -> ', index)
                index_str: str = f'{index}'

                # folder 를 생성 합니다.
                file_manager.make_folder(day_folder)
                time.sleep(0.1)  # 파일 저장할 시간을 주고

                # 파일을 저장 합니다.
                path = f'{day_folder}/{index_str}.text'

                # binary 를 reshape( , )2차원 (1, )1줄 ( , -1) 나머지 자동 맞춤 후 text 저장 합니다.
                np.savetxt(path, binary.reshape(1, -1), fmt="%s", header='')
                time.sleep(0.2)

                # text -> image 변환 합니다.
                self.to_image(path)
                time.sleep(0.3)

    def to_binary_group(self, day_folder, src_list):

        call = self.call_progress

        # src_list 형식은 개발자 임의 형태 입니다. -> list[int_obj(tuple (value, value))]
        for i in range(0, len(src_list)):
            int_obj = src_list[i]

            call(100, i)

            # list obj 를 가지고 옵니다.
            if src_list[i] == 0:
                pass
            else:
                src, index = int_obj

                # img 파일을 numpy 로 변환 합니다.
                img = np.array(src)

                # image 128 값 보다 색이 높은 곳을 1이라는 값으로 numpy -> binary 변환 합니다.
                binary = np.where(img > 128, 1, 0)

                print('ImgText: to_binary_loop -> ', index)
                index_str: str = f'{index}'
                index_list = index_str.split('_')
                folder_path = f'{day_folder}/{index_list[0]}'

                # folder 를 생성 합니다.
                file_manager.make_folder(folder_path)
                time.sleep(0.1)  # 파일 저장할 시간을 주고

                # 파일을 저장 합니다.
                file_name = f'{index_list[-1]}'
                path = f'{folder_path}/{file_name}.text'

                # binary 를 reshape( , )2차원 (1, )1줄 ( , -1) 나머지 자동 맞춤 후 text 저장 합니다.
                np.savetxt(path, binary.reshape(1, -1), fmt="%s", header='')
                time.sleep(0.2)

                # text -> image 변환 합니다.
                self.to_image(path)
                time.sleep(0.3)

    @ classmethod
    def to_binary(cls, folder, src, file_name, classification):

        # png 파일을 numpy 로 변환 합니다.
        img = np.array(src)

        # image 128 값 보다 색이 높은 곳을 1이라는 값으로 numpy -> binary 변환 합니다.
        binary = np.where(img > 128, 1, 0)

        # binary 를 reshape( , )2차원 (1, )1줄 ( , -1) 나머지 자동 맞춤 후 TEXT 저장합니다.
        file_name = f'{classification}_{file_name}'
        path = f'{folder}/{file_name}'

        np.savetxt(path, binary.reshape(1, -1), fmt="%s", header='')

        # 파일 저장할 시간을 주고
        time.sleep(0.5)

    def list_compare(self, export_list, user_select_list):

        call = self.call_progress

        # 감싸진 list 1개씩 꺼내 옵니다.
        for i in range(0, len(export_list)):
            obj_list = export_list[i]

            call(100, i)

            # 리스트 객체 읽기기
            for j in range(0, len(obj_list)):
                obj = obj_list[j]

                if obj is None:
                    pass

                else:
                    # 번호만 가져 오기
                    _number, _ = obj

                    a: int = int(_number)

                    # 유저가 선택한 리스트 가져 오기
                    user_select = user_select_list
                    for _object in user_select:

                        # 번호가 유저 체크 됬는지 판정
                        number, chk = _object
                        b: int = int(number)

                        # export 번호와 유저 번호가 일치 하면
                        if a == b:
                            if chk is False:

                                # export 리스트 0 처리
                                obj_list[j] = 0
                                print('mask_export:', j)
        return export_list

    def to_1_dimension(self, export_list):
        print('img_text: to_1_dimension')

        call = self.call_progress

        # 1차원 리스트 생성
        one_dimension_list = []

        # export list -> roi list 분리
        for i in range(0, len(export_list)):
            roi_list = export_list[i]

            call(100, i)

            # roi 리스트 에서 roi 분리
            for j in range(0, len(roi_list)):

                # list 에서 튜플 꺼내기
                tuple_obj = roi_list[j]

                # 들어 있는 값이 0 이면 패스
                if tuple_obj == 0 or tuple_obj is None:
                    pass
                else:
                    try:
                        # tuple roi 꺼내기
                        obj: Roi = tuple_obj[1]
                    except TypeError:
                        notice.message('Error', 'data 처리 하지 못 했 습니다. '
                                                '\n너무 작거나 큰 ROI 또는 Noise 가 포함 되면 해당 창이 표시 됩니다.'
                                                '\nRefresh 누른 후 Pre-processing "start ~ end 조절"등 의'
                                                '\n작업을 다시 설정해 주세요.')
                        return

                    # 인덱스 번호 만들기
                    str_number = f'{i}_{tuple_obj[0]}'
                    tuple_roi = (obj.image_mask, str_number)

                    # 1차원 리스트 저장
                    one_dimension_list.append(tuple_roi)

        # 1차원 리스트 반환
        return one_dimension_list

    @ classmethod
    def to_image(cls, file_name):

        print('ImgText: to_image ->', file_name)

        # TEXT -> IMAGE
        with open(file_name, mode='r') as file:
            fileContent = file.read().split(' ')
            value = []

            # STRING binary 를 INT binary 변환 합니다.
            i = 1
            count = len(fileContent)
            for obj in fileContent:

                if i >= count:
                    break

                # (512 * 512 = 262144)
                if i > 262144:
                    break

                try:
                    num = int(obj)
                    value.append(num)

                # 마지막 줄 바꿈 STRING 은 예외 처리 합니다.
                except ValueError:
                    value.append(0)
                    break
                i = i + 1

            # INT binary 를 image 변경 합니다.
            img = Image.new('1', (512, 512), "black")
            img.putdata(value)

            # 파일 이름만 가져 오기
            if file_name.count(".") == 1:  # . 이 한개 일떄
                V = file_name.split(".")
                print("file Name : " + V[0])

            # 파일을 저장 합니다.
            file_make = f'{V[0]}.jpg'
            img.save(file_make)
