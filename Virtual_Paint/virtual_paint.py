""" VIRTUAL Paint """

import cv2
import numpy as np

webDisplay = cv2.VideoCapture(0)
webDisplay.set(3,640)   # Set width
webDisplay.set(4,500)   # Set Height
webDisplay.set(10,100)   # Set Brightness

""" Detect color using webColorPicker.py"""
paintColor = [0,231,107,179,255,255]      # Values: h_min, s_min, v_min, h_max, s_max, v_max // FOr RED pen

drawPoints = []   # Values [x,y]

""" Create mask from detected color"""
def detect_color(img):
    points = []
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    h_min, s_min, v_min, h_max, s_max, v_max = paintColor
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(imgHSV, lower, upper)
    # cv2.imshow(" Paint", mask)
    x,y = getContours(mask)
    points.append([x,y])
    # paintOnCanvas(x,y)
    # print(points)
    return points

def getContours(img):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area>500:
            # cv2.drawContours(imgOutput, cnt, -1, (255, 0, 0),3)
            parameter = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * parameter, True)
            x, y, w, h = cv2.boundingRect(approx)
            # cv2.rectangle(imgOutput, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # cv2.circle(imgOutput, (x,y),10,(0,0,255),cv2.FILLED)
    return x+w//2,y

def paintOnCanvas(points):
    for x,y in points:
        cv2.circle(imgOutput, (x,y),10,(0,0,255),cv2.FILLED)

while True:
    _, img = webDisplay.read()
    imgOutput = img.copy()
    getPoints = detect_color(img)
    for pt in getPoints:
        drawPoints.append(pt)
        print(pt)
        # print(drawPoints)
    paintOnCanvas(drawPoints)

    cv2.imshow("Virtual Paint",imgOutput)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
