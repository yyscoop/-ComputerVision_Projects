import cv2
import numpy as np

webcam = cv2.VideoCapture(0)
webcam.set(3, 600)  #width
webcam.set(4, 450)  #height
webcam.set(10,150)  #brightness

def skip(arg):
    pass

cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars",640,240)
cv2.createTrackbar("HUE Min","TrackBars",0,179,skip)
cv2.createTrackbar("SAT Min","TrackBars",0,255,skip)
cv2.createTrackbar("VALUE Min","TrackBars",0,255,skip)
cv2.createTrackbar("HUE Max","TrackBars",179,179,skip)
cv2.createTrackbar("SAT Max","TrackBars",255,255,skip)
cv2.createTrackbar("VALUE Max","TrackBars",255,255,skip)

while True:
    _, img = webcam.read()
    imgHsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    h_min = cv2.getTrackbarPos("HUE Min","TrackBars")
    h_max = cv2.getTrackbarPos("HUE Max", "TrackBars")
    s_min = cv2.getTrackbarPos("SAT Min", "TrackBars")
    s_max = cv2.getTrackbarPos("SAT Max", "TrackBars")
    v_min = cv2.getTrackbarPos("VALUE Min", "TrackBars")
    v_max = cv2.getTrackbarPos("VALUE Max", "TrackBars")
    print(h_min,h_max,s_min,s_max,v_min,v_max)

    lower = np.array([h_min,s_min,v_min])
    upper = np.array([h_max,s_max,v_max])
    mask = cv2.inRange(imgHsv,lower,upper)
    result = cv2.bitwise_and(img,img, mask = mask)

    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    horizontalStack = np.hstack([img,mask,result])

    cv2.imshow('Color Picker', horizontalStack)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()