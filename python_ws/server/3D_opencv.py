import cv2
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import random


def update_plot(x, y, z):
    xdata.append(x)  # x 좌표 추가
    ydata.append(y)
    zdata.append(z)  # y 좌표 추가
    ax.scatter(xdata, ydata, zdata, c='b', marker='o', s=15, cmap='Greens')
    ax.relim()  # 축 범위 재설정

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
xdata, ydata, zdata = [], [], []    

ax.set_xlim3d(0,1280)
ax.set_ylim3d(0,700)
ax.set_zlim3d(0,720)
h1, = ax.plot3D([],[],[])

# 비디오 캡쳐 객체 생성
cap = cv2.VideoCapture(0)

# 전경-배경 분리 알고리즘 객체 생성
fgbg = cv2.createBackgroundSubtractorMOG2()

last_detected_box = None  # 마지막으로 감지된 박스 좌표

while True:
    # 비디오 프레임 읽기
    ret, frame = cap.read()

    # 전경-배경 분리
    fgmask = fgbg.apply(frame)

    # 노이즈 제거
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

    # 컨투어 검출
    contours, hierarchy = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 컨투어로부터 특징 추출
    bounding_boxes = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = float(w) / h
        area = cv2.contourArea(cnt)
        if aspect_ratio > 1.5 and area > 5000:
            # 사람이 일어나 있는 경우
            bounding_boxes.append((x, y, w, h))
        elif aspect_ratio < 0.8 and area > 5000:
            # 사람이 누워 있는 경우
            bounding_boxes.append((x, y, w, h))

    # 가장 큰 구역 추정
    max_box_index = -1
    max_box_area = -1
    for i, box in enumerate(bounding_boxes):
        x, y, w, h = box
        area = w * h
        if area > max_box_area:
            max_box_index = i
            max_box_area = area

    if max_box_index >= 0:
        # 결과 출력
        x, y, w, h = bounding_boxes[max_box_index]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        last_detected_box = (x, y, w, h)  # 마지막으로 감지된 박스 좌표 저장

    
    if max_box_index >= 0:
        # 결과 출력
        x, y, w, h = bounding_boxes[max_box_index]
        center_x, center_y = x + w // 2, y + h // 2
        cv2.circle(frame, (center_x, center_y), 10, (0, 0, 255), -1)

    cv2.imshow('frame', frame)
    cv2.imshow('fgmask', fgmask)
    print(center_x, center_y)
    
    
    
    x_grap = 1280 - center_x
    y_grap = random.randint(0,700)
    z_grap = 720 - center_y
    update_plot(x_grap, y_grap, z_grap)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    plt.pause(0.01)
    plt.cla()
    xdata, ydata, zdata = [], [], [] 
    ax.set_xlim3d(0,1280)
    ax.set_ylim3d(0,700)
    ax.set_zlim3d(0,720)   
    plt.pause(0.01)



# 객체 해제
cap.release()
cv2.destroyAllWindows()
