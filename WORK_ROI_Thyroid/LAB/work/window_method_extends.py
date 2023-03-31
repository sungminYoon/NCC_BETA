"""
Created by SungMin Yoon on 2021-11-24..
Copyright (c) 2021 year NCC (National Cancer Center). All rights reserved.
"""
import math

from PySide6.QtCore import QRect
from PySide6.QtGui import QImage, QPixmap
from .window_method import WindowMethod

'''
    window_method 의 
    확장(extends) 클레스 입니다. 
    보여 지는 view_center, view_second 의 기능, 
    사용자 선택 이미지 인덱스 표시, 진행바 등 구현 되어 있 습니다.
'''


class WindowMethodExtends(WindowMethod):

    def __init__(self, parent=None):
        super(WindowMethodExtends, self).__init__(parent)
        print('WindowMethodExtends: init')

    # Show currently selected images
    def change_label(self, number):
        print('WindowMethodExtends: change_label')
        str_number = f'<font color="White">{number}</font>'
        self.label_current_image.setText(str_number)

    # mark - Call back method: view_center
    def view_label_update(self, mouse_list):

        # 화면의 우측 에 표시 되는 테이블 라벨을 update 합니다.
        self.table_label.create(mouse_list, self.active_image_index)
        self.scroll_label.setWidget(self.table_label.top_widget)

    # mark - Call back method: table_label
    def view_handling(self, user_select_image, mouse_position_list, window, muscle, path):

        # 사용자 선택, 입력 정보를 이용해 뷰를 동작 시킵 니다.
        print('WindowMethodExtends: view_handling')

        # UI TOOL 표시 설정
        self.tool.set_slider_window(window)
        self.tool.set_slider_muscle(muscle)

        # 화면에 적용 되는 값 입력
        self.view_center.level_window = window
        self.view_center.level_muscle = muscle

        # 영상 처리에 적용 되는 값 입력
        self.auto.level_window = window
        self.auto.level_muscle = muscle

        # 화면 갱신및 마우스 좌표 정보 전달
        user_int: int = int(user_select_image)
        self.re_setting(path, user_int - 1)
        self.view_center.mouse_to_threshold(mouse_position_list)

    # mark -  Call back method: Table_img
    def re_setting(self, path, index):
        print('WindowMethodExtends: re_setting', path)

        # Table_image 에서 사용자 선택한 path, index 입니다.
        self.active_path = path
        self.active_image_index = index
        self.tool.set_select_image(path)

        # 현재 사용자 선택된 이미지 인덱스 입니다.
        int_index: int = int(index)

        # 메뉴에 사용자 선택된 현재 이미지 넘버.
        current_image_text = f' Select image : {int_index + 1} '
        self.change_label(current_image_text)

        # 보여 지는 view 에 들어갈 이미지 준비.
        img = self.input_cv_list[int_index]

        if img is None:
            print('view_center: error')
            return

        h, w = img.shape[:2]
        q_image = QImage(img, w, h, QImage.Format_Grayscale8)
        pix_image = QPixmap.fromImage(q_image)

        # 보여 지는 view 에 image 를 넣어 주고
        self.view_center.q_graphic.setPixmap(pix_image)
        self.view_center.re_setting(img)
        self.view_center.repaint()

        self.view_second.cv_img = img
        self.view_second.q_graphic.setPixmap(pix_image)
        self.view_second.repaint()

    # mark -  Call back method: auto
    def progress_value(self, length, input_value):

        if input_value == 0:
            self.progress_bar.setFixedSize(0, 10)
            self.repaint()

        # 진행 값을 percent 변환 합니다.
        f_value = float((input_value / length) * 600)
        result = math.floor(f_value)

        # 진행
        self.progress_bar.setFixedSize(result, 10)
        self.repaint()

    # mark -  Call back method: tool
    def doit(self):
        print("WindowMethodExtends: doit")
        self.popup.setGeometry(QRect(100, 100, 400, 200))
        self.popup.show()

    # mark -  Call back method: view_second
    def zoom(self, name):
        print("WindowMethodExtends: zoom ->", name)

        # 현재 사용자 선택된 이미지 인덱스 입니다.
        index = self.active_image_index
        number: int = int(index)

        # 보여 지는 view 에 들어갈 이미지 준비.
        cv_gray = self.input_cv_list[number]
        h, w = cv_gray.shape[:2]
        q_image = QImage(cv_gray, w, h, QImage.Format_Grayscale8)
        pix_image = QPixmap.fromImage(q_image)

        if name == 'zoom':

            # 보여 지는 view 에 image 를 넣어 주고
            self.view_second.cv_img = cv_gray
            self.view_second.q_graphic.setPixmap(pix_image)

            self.view_center.hide()
            self.view_second.show()

        if name == 'normal':
            self.view_second.hide()
            self.view_center.show()

        if name == 'apply':
            self.view_second.resize_apply()
            self.view_center.hide()
            self.view_second.show()

    # mark -  Call back method: view_second
    def sync_mask(self, mask, user_threshold_choice):
        print("WindowMethodExtends: sync_mask ->", user_threshold_choice)
        self.view_center.set_mask(mask, user_threshold_choice)
        self.view_center.update_screen()

