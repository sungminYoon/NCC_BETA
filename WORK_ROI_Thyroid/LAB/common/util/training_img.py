"""
Created by SungMin Yoon on 2021-11-25..
Copyright (c) 2021 year NCC (National Cancer Center). All rights reserved.
"""
import os
import time
import cv2 as cv
import numpy as np
# import imageio

from LAB.common.oop import img_text


# from matplotlib import pyplot as plt


# 폴더의 jpg 파일 list 가지고 옵니다.
def file_jpg_list(_folder_path):
    file_list = os.listdir(_folder_path)
    jpg_list = [file for file in file_list if file.endswith(".jpg")]
    return jpg_list


# 정답 data 만듭니다.
def to_data_y(path):
    print('training_img: to_data_y')

    y = []          # 정답 데이터 저장 공간
    names = []      # 정답 데이터 이름 저장 공간
    numbers = []    # 정답 데이터 넘버 저장 공간

    # 경로, 폴더, 파일 리스트
    for r, d, f in os.walk(path):

        # 파일 text -> image 로 변환
        for file_name in f:
            if '.text' in file_name:
                text_path = os.path.join(r, file_name)
                img_text.to_image(text_path)

        # 이미지 파일을 저장할 시간을 줍니다.
        time.sleep(1)

        for img_name in f:
            if '.jpg' in img_name:

                # jpg 파일 경로를 가져 옵니다.
                image_path = os.path.join(r, img_name)

                # image -> data : read.
                with open(image_path, 'rb') as file_image:
                    data = file_image.read()

                # data -> numpy unit8 로 인코딩 합니다.
                encoded_img = np.fromstring(data, dtype=np.uint8)

                # 3차원 IMREAD_COLOR 인코딩 합니다.
                img = cv.imdecode(encoded_img, cv.IMREAD_GRAYSCALE)

                # '''image 복원 코드 세이브'''
                # img_array = np.array(img)
                # pil_image = Image.fromarray(img_array)
                # pil_image.show()

                # 이미지 저장
                y.append(img)

                # 파일 이름만 따로 저장 합니다.
                names.append(img_name)

                # 번호 들만 따로 저장
                last_name = img_name[img_name.rfind('_') + 1:]
                file_name = last_name.split(".")
                numbers.append(file_name[0])

    set_numbers = set(numbers)
    return y, set_numbers, names


# 훈련 data 만듭니다.
def to_data_x(path, choice_set):
    print('training_img: to_data_x')

    # 훈련용 데이터 저장 공간 생성
    x = []

    # 훈련용 data 있는 리스트
    file_list = file_jpg_list(path)

    for full_name in file_list:
        for y_str in choice_set:

            # 파일 name 이미지 "넘버(세자리)"만 get
            a = full_name[-7]
            b = full_name[-6]
            c = full_name[-5]
            number = f'{a}{b}{c}'
            x_num = int(number)
            y_num = int(y_str)

            # y 와 x 번호가 일치 하면 저장
            if y_num == x_num:
                print('training: ', y_num, ':', x_num)
                image_path = f'{path}{full_name}'

                # image -> data : read.
                with open(image_path, 'rb') as file_image:
                    data = file_image.read()

                # data numpy unit8 로 인코딩 합니다.
                encoded_img = np.fromstring(data, dtype=np.uint8)

                # 3차원 IMREAD_COLOR 인코딩 합니다.
                img = cv.imdecode(encoded_img, cv.IMREAD_GRAYSCALE)

                '''image 복원 코드 세이브'''
                # img_array = np.array(img)
                # pil_image = Image.fromarray(img_array)
                # pil_image.show()

                x.append(img)
    return x


# 테스트 data 만듭니다.
def to_data_x_all(path):
    print('training_img: to_data_x_all')

    # 테스트 데이터 저장 공간
    x = []

    # 테스트 data 있는 리스트
    file_list = file_jpg_list(path)

    for full_name in file_list:

        image_path = f'{path}{full_name}'

        # image -> data : read.
        with open(image_path, 'rb') as file_image:
            data = file_image.read()

        # data numpy unit8 로 인코딩 합니다.
        encoded_img = np.fromstring(data, dtype=np.uint8)

        # 3차원 IMREAD_COLOR 인코딩 합니다.
        img = cv.imdecode(encoded_img, cv.IMREAD_GRAYSCALE)

        '''image 복원 코드 세이브'''
        # img_array = np.array(img)
        # pil_image = Image.fromarray(img_array)
        # pil_image.show()

        x.append(img)

    return x
