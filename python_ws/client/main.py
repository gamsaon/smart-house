import cv2
import socket
import time

if __name__ == '__main__':
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #UDP Socket
    Host = '192.168.210.6' #server의 IP 주소
    Port = 9000 #통신할 대상의 Port 주소


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
                standing = 1
                bounding_boxes.append((x, y, w, h))
            elif aspect_ratio < 0.8 and area > 5000:
                # 사람이 누워 있는 경우
                standing = 0
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

        cv2.imshow('frame', frame)
        cv2.imshow('fgmask', fgmask)

        if max_box_index >= 0:
            # 결과 출력
            x, y, w, h = bounding_boxes[max_box_index]
            center_x, center_y = x + w // 2, y + h // 2
            cv2.circle(frame, (center_x, center_y), 10, (0, 0, 255), -1)

        cv2.imshow('frame', frame)
        cv2.imshow('fgmask', fgmask)
        print(center_x, center_y)
       
        object_0 = [center_x,center_y,standing]
        object_1 = [0,0,0]
        object_2 = [0,0,0]
        object_3 = [0,0,0]
        object_4 = [0,0,0]
        
        x_coords = [object_0[0], object_1[0], object_2[0],object_3[0],object_4[0]]
        y_coords = [object_0[1], object_1[1], object_2[1],object_3[1],object_4[1]]
        z_coords = [object_0[2],object_1[2],object_2[2],object_3[2],object_4[2]]

        # x, y, z 좌표값을 하나의 문자열로 결합하여 패킷으로 만듦
        packet = ",".join([f"{x},{y},{z}" for x, y, z in zip(x_coords, y_coords, z_coords)])
        
        print(packet)
        
        send_data = bytes(packet.encode())
        
        client_sock.sendto(send_data, (Host, Port))
        


        # q를 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 객체 해제
    cap.release()
    cv2.destroyAllWindows()
