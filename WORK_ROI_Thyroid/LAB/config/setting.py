"""
Created by SungMin Yoon on 2021-03-09..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""

'''WINDOW'''
TITLE_WINDOW = 'NCC AUTO ROI'   # 응용프로그램 이름
WINDOW_SCREEN_WIDTH = 950       # 응용프로그램 창 가로 크기
WINDOW_SCREEN_HEIGHT = 800      # 응용프로그램 창 세로 크기

'''ORB VALUE'''
ORB_SCORE = 600     # score 낮을 수록 비슷함 600 왠만 한건 리스트 에서 빼지 말고 통과
ORB_COUNT = 10      # count 높을 수록 비슷함 10 왠만 한건 리스트 에서 빼지 말고 통과

'''COMMON'''
USER_CHOICE_COUNT = 9   # 사용자 UI TOOL Threshold 선택 가능한 개수

''' FILTER '''
FILTER = ('Erosion', 'Gaussian', 'Laplace', 'Convolution', 'Canny')

''' ALGORITHM '''
ALGORITHM = ('LEVEL_1', 'LEVEL_2', 'LEVEL_3')

'''TOOL'''
DEFAULT_LEVEL_WINDOW = 800  # 초기값
DEFAULT_LEVEL_MUSCLE = 0    # 초기값

'''AUTO'''
PARAM_LEVEL_MUSCLE = 650    # 근육 초기값

'''Menu'''
THRESHOLD = 20          # 초기값
PROPERTY_MAX = 200      # roi 찾기 최대 크기
PROPERTY_MIN = 10       # roi 찾기 최소 크기

'''ROI VALUE'''
DISTANCE_LEVEL_1 = 20       # 찾아낸 Level ROI 와 처리 진행 중인 ROI 거리 20 이하 '혈관, 갑상선'
DISTANCE_LEVEL_3 = 20       # 찾아낸 Level ROI 와 처리 진행 중인 ROI 거리 20 이하 '침샘'
RANDOM_LEVEL_3 = 100        # LEVEL_3 ALGORITHM 랜덤 생성 반복 횟수
LOOP_LEVEL_2 = 50           # roi 적용할 Threshold 최대 크기 값
LOOP_LEVEL_3 = 100          # roi 적용할 Threshold 최대 크기 값
MINIMUM_DIMENSIONS = 20     # 찾아낸 ROI 최소 거리
MAX_LEVEL_COUNT = 200       # ROI 찾기 위한 레벨 처리 개수 맥스 값
ROI_SIZE_MARGIN = 1         # 찾은 Threshold 크기 마진 값

'''COLOR'''
ROI_COLOR = [(13, 214, 242),
             (0, 128, 0),
             (0, 0, 250),
             (250, 128, 250),
             (128, 128, 250),
             (0, 250, 200),
             (0, 250, 0),
             (255, 0, 0),
             (30, 128, 128)]



