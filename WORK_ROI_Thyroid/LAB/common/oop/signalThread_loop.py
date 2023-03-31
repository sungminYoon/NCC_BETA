"""
Created by SungMin Yoon on 2022-02-08..
Copyright (c) 2021 year NCC (National Cancer Center). All rights reserved.
"""
import time
from PySide6.QtCore import QThread, SIGNAL


# QThread 신호 처리
class SignalThreadLoop(QThread):
    """
        [반복] 쓰레드 실행 예제.

        사용하려는 클레스에 아래 코드를 넣어 준다.
        self.signal_thread.start()
        self.signal_thread.terminate()

        사용하려는 클레스에 아래 메소드를 만들어 준다.
        def proc(self, count):
    """

    def __init__(self, proc):
        super().__init__()
        self.proc = proc
        self.count = 0

    def run(self):
        print('Thread: run -> ', self.count)

        while True:
            # 호출 클래스 에서 넘겨 받은 함수를 수신 부로 지정 하고 값을 송신 한다.
            self.emit(SIGNAL(self.proc(self.count)))
            time.sleep(1)
