""" Document Scanner"""

import cv2
import numpy as np

window_width = 600
window_height = 350
webcam = cv2.VideoCapture(0)   # Selecting webcam
webcam.set(3,window_width)   # Adjust Width
webcam.set(4,window_height)   # Adjust Height
webcam.set(10,150)   # Adjust Brightness

def imagePreProcessing(img):
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray,(5,5),1)
    imgCanny = cv2.Canny(imgBlur,100,100)
    kernal = np.ones([5,5])
    imgDilate = cv2.dilate(imgCanny,kernal,iterations=1)
    imgErode = cv2.erode(imgDilate, kernal, iterations=1)
    return imgDilate

def getContours(img):
    biggest_box = np.array([])
    maxArea = 0
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area>5000:
            cv2.drawContours(imgCountour, cnt, -1, (255, 0, 0),3)
            parameter = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * parameter, True)  ## Find approximation of our corner points
            # print(len(approx))
            if len(approx) == 4 and area > maxArea:
                biggest_box = approx
                maxArea = area
    return biggest_box

while True:
    _,img = webcam.read()
    imgCountour = img.copy()
    imgThresh = imagePreProcessing(img)
    getContours(imgThresh)
    cv2.imshow("Document Scanner",imgCountour)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
