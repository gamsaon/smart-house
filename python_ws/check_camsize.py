import cv2

capture = cv2.VideoCapture(0)
wth = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
hit = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)

print(wth)
print(hit)

#client cam size (1280,720)
#server cam size (,)
