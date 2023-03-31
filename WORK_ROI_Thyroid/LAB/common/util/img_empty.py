"""
Created by SungMin Yoon on 2020-09-10..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""
import numpy as np
import cv2 as cv


def np_image(cv_width, cv_height):
    # 빈 이미지 생성
    size = (cv_width, cv_height, 1)
    return np.zeros(size, np.uint8)


def np_image3(cv_width, cv_height):
    # 빈 이미지 생성
    size = (cv_width, cv_height, 3)
    return np.zeros(size, np.uint8)


# 아무 것도 없는 image 만들고 add_image 와 merge.
def np_add(origin_size_width, origin_size_height, x_offset, y_offset, add_image):
    result_image = np.zeros((origin_size_height, origin_size_width), np.uint8)
    result_image[y_offset:y_offset + add_image.shape[0],
    x_offset:x_offset + add_image.shape[1]] = add_image
    return result_image


# 빈곳 체우기
def fill_blank(src):
    contour, _ = cv.findContours(src, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)
    for cnt in contour:
        cv.drawContours(src, [cnt], 0, 255, -1)

    return cv.bitwise_not(src)


def merge_image(back, front, x, y):

    # convert to rgba
    back = cv.cvtColor(back, cv.COLOR_RGB2BGR)
    front = cv.cvtColor(front, cv.COLOR_RGB2BGR)

    # crop images
    bh, bw = back.shape[:2]
    fh, fw = front.shape[:2]
    x1, x2 = max(x, 0), min(x + fw, bw)
    y1, y2 = max(y, 0), min(y + fh, bh)
    front_cropped = front[y1 - y:y2 - y, x1 - x:x2 - x]
    back_cropped = back[y1:y2, x1:x2]

    alpha_front = front_cropped[:, :, :3] / 255
    print(f'af: {alpha_front.shape}\nfront_cropped: {front_cropped.shape}\nback_cropped: {back_cropped.shape}')

    result = back.copy()
    result[y1:y2, x1:x2, :3] = alpha_front * front_cropped[:, :, :3] + (1 - alpha_front) * back_cropped[:, :, :3]

    # overlay
    # alpha_back = back_cropped[:, :] / 255
    # result[y1:y2, x1:x2] = (alpha_front + alpha_back) / (1 + alpha_front * alpha_back) * 255

    return result
