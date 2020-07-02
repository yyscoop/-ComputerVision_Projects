""" VIRTUAL Paint """

import cv2
import numpy as np

webDisplay = cv2.VideoCapture(0)
webDisplay.set(3,640)   # Set width
webDisplay.set(4,500)   # Set Height
webDisplay.set(10,100)   # Set Brightness

""" Detect color using webColorPicker.py"""
paintColor = [0,169,138,6,255,255]      # Values: h_min, s_min, v_min, h_max, s_max, v_max // FOr RED pen

""" Create mask from detected color"""
def detect_color(img):
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    h_min, s_min, v_min, h_max, s_max, v_max = paintColor
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(imgHSV, lower, upper)
    cv2.imshow("Mask", mask)


while True:
    _, img = webDisplay.read()
    detect_color(img)
    cv2.imshow("Virtual Paint",img)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
