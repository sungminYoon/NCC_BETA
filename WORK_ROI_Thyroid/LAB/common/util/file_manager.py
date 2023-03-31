"""
Created by SungMin Yoon on 2020-03-04..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""
import os
import time
import errno
import datetime
import zipfile as compression

from datetime import datetime
from PySide6.QtWidgets import *

from LAB.common.util import notice
from LAB.config.path import path_local


def auto_open(path):
    QFileDialog.getOpenFileName(None, 'Open file', path)


def file_open():
    full_path = QFileDialog.getOpenFileName(None, 'Open file', '/')
    if full_path[0]:
        file_path = f'{full_path[0]}'
        return file_path

    else:
        notice.message('Warning', '파일 선택을 하지 않았습니다.')
        return 0


# 사용 자가 선택한 폴더 경로를 가져 옵니다.
def open_folder():
    # 사용 자가 선택한 파일 경로
    file_path = file_open()

    if file_path is 0:
        return

    # 사용 자가 선택한 경로
    last_name = file_path[file_path.rfind('/') + 1:]
    _, fileExtension = os.path.splitext(last_name)

    # 사용자 선택한 폴더 이름
    o_folder = file_path.replace(last_name, '', 1)

    # 폴더 경로 반환
    return o_folder


def get_name(file_name):
    # 파일 이름만 가져 오기
    if file_name.count(".") == 1:  # . 이 한개일떄
        V = file_name.split(".")
        print("file Name : " + V[0])
    return V[0]


# 경로 에서 폴더 경로만 추출
def folder_path(path):

    # / 문자열 구분
    V = path.split("/")

    # 파일명 지우기
    F = path.strip(V[-1])

    return F


# 경로 에서 폴더 이름만 추출
def folder_name(path):

    # / 문자열 구분
    V = path.split("/")

    # 문자 열을 뒤에서 부터 읽을때 비어 있지 않으면 값 리턴
    for i in range(1, len(V)):
        str_name = V[-i]
        if str_name != '':
            return str_name
        else:
            pass


# 폴더의 파일 list 가지고 옵니다.
def file_list(_folder_path):
    _list = os.listdir(_folder_path)
    return _list


# 폴더의 json 파일 list 가지고 옵니다.
def file_json_list(_folder_path):
    file_name_list = os.listdir(_folder_path)
    json_list = [file for file in file_name_list if file.endswith(".json")]
    return json_list


# 폴더의 png 파일 list 가지고 옵니다.
def find_png_list(_folder_path):
    file_name_list = os.listdir(_folder_path)
    file_list_png = [file for file in file_name_list if file.endswith(".png")]
    return file_list_png


# 폴더의 해당 학장자 파일 list 가지고 옵니다.
def file_extension_list(_folder_path, extension):
    file_name_list = os.listdir(_folder_path)
    file_list_png = [file for file in file_name_list if file.endswith(extension)]
    return file_list_png


# 폴더에 있는 dicom 읽어 리스트로 만듭니다.
def get_dicom_path(source_folder):
    f_list = os.listdir(source_folder)
    file_list_all = [file for file in f_list if file.endswith(".dcm")]
    return file_list_all


# 원본 이미지 zip
def image_compression(ori, mask, zipfile):
    with compression.ZipFile(zipfile, mode='w') as f:
        f.write(ori, compress_type=compression.ZIP_DEFLATED)

    # append 압축 파일에 또 다른 파일 추가 마스크 이미지 압축 하기
    with compression.ZipFile(zipfile, mode='a') as f:
        f.write(mask, compress_type=compression.ZIP_DEFLATED)
    print('file_manager: 이미지 압축 완료')


# 압축된 이미지 불러 오기
def load_zip(zip_path, save_path):
    print('file_manager: load_zip')
    full_name = zip_path[zip_path.rfind('/') + 1:]
    folder_name_zip = full_name.replace(".zip", "")

    # zip 파일 인지 확인
    filename, fileExtension = os.path.splitext(full_name)
    if fileExtension != '.zip':
        print('zip 파일이 아닙 니다.')
        return 0

    path = f'{save_path}{folder_name_zip}'

    zip_image = compression.ZipFile(zip_path)
    zip_image.extractall(path)

    # 하드에 이미지 저장할 시간을 좀 주고
    time.sleep(0.1)
    print('압축 풀기 완료')

    # 압축을 풀어 넣은 경로와 파일 이름을 리턴 합니다.
    simplify_path = f'{path}/'
    ori_name = f'ori_{filename}.png'
    mask_name = f'mask_{filename}.png'
    return simplify_path, ori_name, mask_name


# 저장할 폴더 만들기
def make_folder(folder_path_str):
    if not os.path.isdir(folder_path_str):
        os.makedirs(folder_path_str)


# 저장할 폴더 만들기
def make_folder_date(folder_path_str):
    _name = datetime.today().strftime("%Y%m%d%H%M%S")
    day_folder = f'{folder_path_str}{_name}'
    create_folder(day_folder)
    return day_folder


# 폴더 생성
def create_folder(path):
    try:
        if not (os.path.isdir(path)):
            os.makedirs(os.path.join(path))
            return path
        return path

    except OSError as e:
        if e.errno != errno.EEXIST:
            print("Error to create roi_folder directory!")
            raise


# 상대 경로
def relative_path(full_path, start_name):
    folder_list = full_path.split('/')
    string_path = []

    try:
        index = folder_list.index(start_name)

        i = 0
        for name in folder_list:
            if i > index:
                string_path.append('/')
                string_path.append(name)
            i = i + 1

        # list 문자를 -> 문자 열로 변환 합니다.
        string_path = ''.join(string_path)
        result_path = f'{start_name}{string_path}'
        print('file_manager: relative_path = ', result_path)
        return result_path

    except OSError as e:
        if e.errno != errno.EEXIST:
            print('ERROR: relative_path')
            raise


# 데이터 파일의 이름과 생성 정보를 읽습니다.
def read_data_file_name(extension):

    # 데이터 이름 저장 리스트 생성
    data_name_list = []
    time_list = []

    # 데이터 폴더 없으면 생성
    create_folder(path_local.DATA_SET)

    # 데이터 폴더의 데이터 파일 리스트 get
    data_file_list = file_extension_list(path_local.DATA_SET, extension)

    # 데이터 파일 list 이름만 가져 옵니다.
    for name in data_file_list:

        # 파일 이름 으로 경로를 만듭니다.
        path = f'{path_local.DATA_SET}{name}'

        # 파일 경로로 파일 생성 시간을 가져 옵니다.
        file_time = os.path.getmtime(path)

        # 파일 생성 시간을 문자 열로 변환 구분 합니다.
        d_time = datetime.fromtimestamp(file_time)
        str_time = f'{d_time}'
        str_time = str_time.split(' ')

        # 파일 생성 날짜를 리스트로 만듭니다.
        time_list.append(str_time[0])

    # data 없는 경우 예외 처리
    if len(data_file_list) < 1:
        print('Window_method_extends: data_file_save Error')
        data_name_list.append('None')
        time_list.append('None')
        return data_name_list, time_list

    # 데이터 파일 이름만 저장
    for data_name_file in data_file_list:
        data_name_last = get_name(data_name_file)
        data_name_list.append(data_name_last)

    return data_name_list, time_list