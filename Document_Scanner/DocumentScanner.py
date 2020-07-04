"""
Document Scanner
Algo :  Take input from webcom
        Preprocess Image and return as Threshold image
        Find the biggest contour
        Using corner points to get bird eye view

"""

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
            # cv2.drawContours(imgCountour, cnt, -1, (255, 0, 0),3)
            parameter = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * parameter, True)  ## Find approximation of our corner points
            # print(len(approx))
            if len(approx) == 4 and area > maxArea:
                biggest_box = approx
                maxArea = area
    cv2.drawContours(imgCountour, biggest_box, -1, (255, 0, 0),20)
    return biggest_box

def reorder(points):
    points = points.reshape((4,2))
    newPoints = np.zeros((4,1,2),np.int32)

    add = points.sum(1)
    newPoints[0] = points[np.argmin(add)]    ## setting point [0,0]
    newPoints[3] = points[np.argmax(add)]   ## setting point [width,height]

    diff = np.diff(points, axis=1)
    newPoints[1] = points[np.argmin(diff)]  ## setting point [width,0]
    newPoints[2] = points[np.argmax(diff)]  ## setting point [0,height]
    return newPoints


def wrap(img,biggestContourPoint):
    biggestContourPoint = reorder(biggestContourPoint)
    width = window_width
    height = window_height
    pts1 = np.float32(biggestContourPoint)
    pts2 = np.float32([[0,0],[width,0],[0,height],[width,height]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgOutput = cv2.warpPerspective(img, matrix, (width, height))
    return imgOutput

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

while True:
    _,img = webcam.read()
    img = cv2.resize(img, (500, 200))
    imgCountour = img.copy()
    imgThresh = imagePreProcessing(img)
    biggestContour = getContours(imgThresh)
    # print(biggestContour,biggestContour.shape)
    imgStagedArray = []
    if biggestContour.size != 0:
        imgWrapOutput = wrap(img, biggestContour)
        cv2.imshow("Document Scanner", imgWrapOutput)
        imgStagedArray = [[img,imgThresh],[imgCountour,imgWrapOutput]]
    else:
        imgStagedArray = [[img,imgThresh],[img,img]]

    stackedImg = stackImages(0.6, imgStagedArray)
    cv2.imshow("Workflow", stackedImg)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
