import cv2
import mediapipe as mp
import time
import math
import numpy as np
import HandTrackingModule as htm
import os
import win32api, win32con

folderPath = "Header"
files = os.listdir(folderPath)
overlay = []
for imgPath in files:
    img = cv2.imread(f'{folderPath}/{imgPath}')
    overlay.append(img)


header = overlay[0]
color = (0,242,255)
wCam, hCam = 1280, 720
pTime = 0
cTime = 0
cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
detector = htm.handDetector()
xp = 0
yp = 0
brush = 3
bg = cv2.imread('canvas.jpg')
canvas = np.ones((720,1280,3),np.uint8)
while True:
    success, img = cap.read()
    img = cv2.flip(img,1)
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)    
    if len(lmList)!=0:   
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        
        fingers = detector.fingersUp()
        
        if fingers[1] and fingers[2] :
            if y1<144:
                if  240<x1<375:
                    header = overlay[0]
                    color = (0,242,255)
                    brush = 3
                elif  410<x1<550:
                    header = overlay[1]
                    color = (0,0,255)
                    brush = 3
                elif  575<x1<710:
                    header = overlay[2]
                    color = (39,127,255)
                    brush = 10
                elif  765<x1<895:
                    header = overlay[3]
                    color = (0,128,0)
                    brush = 10
                elif  1045<x1<1210:
                    header = overlay[4]
                    color = (0,0,0)
                    brush = 20

            xp = 0
            yp = 0

            cv2.rectangle(img,(x1,y1-15),(x2,y2+15),color,cv2.FILLED)

        if fingers[1] and fingers[2] == False :
            cv2.circle(img,(x1,y1),20,(255,0,0),cv2.FILLED)
            if xp == 0 and yp == 0:
                xp,yp = x1 , y1
            cv2.line(img,(xp,yp),(x1,y1),color,brush)
            cv2.line(canvas,(xp,yp),(x1,y1),color,brush)
            cv2.line(bg,(xp,yp),(x1,y1),color,brush)
            xp,yp = x1 , y1
            
    
    grey = cv2.cvtColor(canvas,cv2.COLOR_BGR2GRAY)
    _, inverse = cv2.threshold(grey,50,255,cv2.THRESH_BINARY_INV)
    inverse = cv2.cvtColor(inverse,cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img,inverse)
    img = cv2.bitwise_or(img,canvas)

    img[0:144,0:1280] = header
    #img = cv2.addWeighted(img,0.5,canvas,0.5,0)
    cv2.imshow("Image", img)
    cv2.imshow("Image1", canvas)
    cv2.imshow("Image2", bg)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        cv2.destroyWindow('Image')
        break




