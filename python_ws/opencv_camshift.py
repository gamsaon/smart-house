
import cv2 as cv 
import numpy as np
mouse_is_pressing = False
start_x, start_y, end_x, end_y=-1,-1,-1,-1 
step = 0
track_window= None
# 마우스 콜백함수
def mouse_callback(event,x,y, flags, param): 
    global start_x, start_y, end_x, end_y
    global step, mouse_is_pressing, track_window
# 왼쪽 버튼 누를 시 현재 좌표를 사각형 그릴때 시작 좌표로 저장 if event == cv.EVENT_LBUTTONDOWN:
    if event == cv.EVENT_LBUTTONDOWN:
        step = 1
        mouse_is_pressing=True
        start_x=x
        start_y=y
    elif event == cv.EVENT_MOUSEMOVE:
        if mouse_is_pressing:
            end_x = x
            end_y = y
            step = 2
    elif event == cv.EVENT_LBUTTONUP:
        mouse_is_pressing = False
        end_x = x
        end_y = y
        step = 3

cap = cv.VideoCapture(0)
if cap. isOpened() == False:
    print("카메라를 열 수 없습니다.") 
    exit(1)
cv.namedWindow("Color") 
cv.setMouseCallback("Color", mouse_callback)
while True:
#윈도우를 생성하고 마우스 콜백함수를 설정 
    ret, img_color = cap.read()
    if ret == False:
        print("캡쳐 실패")
        break
    if step == 1: # 처음 클릭 시 원을 보여줌 
        cv.circle(img_color, (start_x, start_y), 10, (0, 255, 0), -1)
    elif step == 2: # 마우스 이동 중 사각형을 그려줌 
        cv.rectangle(img_color, (start_x, start_y), (end_x, end_y), (0, 255, 0), 3)
    elif step == 3: # 손을 뗀 경우 RO1영역을 얻게 됨 
        if start_x > end_x:
            start_x, end_x = end_x, start_x
            start_y, end_y = end_y, start_x
        # 초기 사각형의 위치
        track_window=(start_x, start_y, end_x-start_x, end_y-start_y)
        # HSV 색 공간으로 변환하고 ROI 영역을 지정
        img_hsv = cv.cvtColor(img_color, cv.COLOR_BGR2HSV) 
        img_ROI = img_hsv [start_y:end_y, start_x:end_x] 
        cv. imshow("ROI", img_ROI)
        
        #ROI의 히스토그램을 계산
        objectHistogram = cv.calcHist ([img_ROI], [0], None, [180],(0, 180))
        # 히스토그램을 0~255 사이 값을 갖도록 정규화함
        cv.normalize(objectHistogram, objectHistogram, alpha=0, beta=255, norm_type=cv.NORM_MINMAX)
        step  = step + 1
    elif step == 4:
        # HSV 색 공간으로 변환
        img_hsv = cv.cvtColor(img_color, cv.COLOR_BGR2HSV)
        #Histogram Backprojection ÷ ōt of img_hsvoll objectHistogram
        #히스토그램을 갖는 영역을 찾음
        bp = cv.calcBackProject ([img_hsv], [0], objectHistogram, [0,180], 1)
        #Camshift를 적용하여 새로운 오브젝트 위치를 얻음 
        rotatedRect, track_window= cv.CamShift (bp, track_window,( cv. TERM_CRITERIA_EPS | cv. TERM_CRITERIA_COUNT, 10, 1))
        print(rotatedRect[0])#중심 좌표 출력
        # 오브젝트 위치에 빨간색 타원을 그려줌
        cv.ellipse (img_color, rotatedRect, (0, 0, 255), 2)
        # 회전된 경계 사각형을 초록색으로 그려줌
        pts =cv.boxPoints (rotatedRect)
        pts= np. int0(pts)
        for i in range(4):
            cv.line(img_color, tuple(pts[i]), tuple(pts[(i + 1) % 4]),(0, 255, 0), 2)
    cv.imshow("Color", img_color)    
    
    if cv.waitKey(25) >= 0:
        break
