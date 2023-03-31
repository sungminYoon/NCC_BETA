"""
Created by SungMin Yoon on 2021-06-07..
Copyright (c) 2021 year NCC (National Cancer Center). All rights reserved.
"""
import sys
from PySide6.QtWidgets import QApplication
from LAB.work.window import Window
from LAB.work.window_method_extends import WindowMethodExtends  # 마무리

if __name__ == '__main__':

    app = QApplication(sys.argv)
    window: Window = WindowMethodExtends()
    sys.exit(app.exec())

'''Debug CODE'''
# set_title = f'fix'
# cv.imshow(set_title, img)
# cv.waitKey(0)
# cv.destroyAllWindows()

''' 코드 시간 측정 '''
# import time
# start = time.time()
# print("time :", time.time() - start)




