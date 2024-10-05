from flask import Flask, render_template, Response, request
import cv2
import datetime, time
import os, sys
import numpy as np
from threading import Thread
import mediapipe as mp
import math
import HandTrackingModule as htm
import time

global capture,rec_frame, grey, switch, neg, face, rec, out 
capture=0
grey=0
neg=0
face=0
switch=1
rec=0

try:
    os.mkdir('./shots')
except OSError as error:
    pass

 
app = Flask(__name__, template_folder='./')


camera = cv2.VideoCapture(0)



def getCanvas():  
    folderPath = "Header"
    files = os.listdir(folderPath)
    overlay = []
    for framePath in files:
        frame = cv2.imread(f'{folderPath}/{framePath}')
        overlay.append(frame)
    header = overlay[0]
    color = (0,242,255)
    wCam, hCam = 1280, 720
    camera.set(3,wCam)
    camera.set(4,hCam)
    pTime = 0
    smoothing = 0
    brush = 3
    detector = htm.handDetector()
    xp = 0
    yp = 0
    canvas = np.zeros((720,1280,3),np.uint8)
    while True:
        success, frame = camera.read()
        frame = cv2.flip(frame,1)
        frame = detector.findHands(frame)
        lmList, bbox = detector.findPosition(frame)    
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


            if fingers[1] and fingers[2] == False :
                if xp == 0 and yp == 0:
                    xp,yp = x1 , y1
                cv2.line(frame,(xp,yp),(x1,y1),color,brush)
                cv2.line(canvas,(xp,yp),(x1,y1),color,brush)
                xp,yp = x1 , y1
        
        canvas[0:144,0:1280] = header

        try:
            ret, buffer = cv2.imencode('.jpg', canvas)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except Exception as e:
            pass

def getwebcam():  
    folderPath = "Header"
    files = os.listdir(folderPath)
    overlay = []
    for framePath in files:
        frame = cv2.imread(f'{folderPath}/{framePath}')
        overlay.append(frame)
    header = overlay[0]
    color = (0,242,255)
    wCam, hCam = 1280, 720
    camera.set(3,wCam)
    camera.set(4,hCam)
    pTime = 0
    smoothing = 0
    brush = 3
    detector = htm.handDetector()
    xp = 0
    yp = 0
    canvas = np.zeros((720,1280,3),np.uint8)
    while True:
        success, frame = camera.read()
        frame = cv2.flip(frame,1)
        frame = detector.findHands(frame)
        lmList, bbox = detector.findPosition(frame)    
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


            if fingers[1] and fingers[2] == False :
                if xp == 0 and yp == 0:
                    xp,yp = x1 , y1
                cv2.line(frame,(xp,yp),(x1,y1),color,brush)
                cv2.line(canvas,(xp,yp),(x1,y1),color,brush)
                xp,yp = x1 , y1
            
    
        grey = cv2.cvtColor(canvas,cv2.COLOR_BGR2GRAY)
        _, inverse = cv2.threshold(grey,50,255,cv2.THRESH_BINARY_INV)
        inverse = cv2.cvtColor(inverse,cv2.COLOR_GRAY2BGR)
        frame = cv2.bitwise_and(frame,inverse)
        frame = cv2.bitwise_or(frame,canvas)
                
        

        
        frame[0:144,0:1280] = header

        try:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except Exception as e:
            pass

def getimg():  
    folderPath = "Header"
    files = os.listdir(folderPath)
    overlay = []
    for framePath in files:
        frame = cv2.imread(f'{folderPath}/{framePath}')
        overlay.append(frame)
    header = overlay[0]
    color = (0,242,255)
    wCam, hCam = 1280, 720
    camera.set(3,wCam)
    camera.set(4,hCam)
    pTime = 0
    smoothing = 0
    brush = 3
    detector = htm.handDetector()
    xp = 0
    yp = 0
    bg = cv2.imread('canvas.jpg')
    canvas = np.zeros((720,1280,3),np.uint8)
    while True:
        success, frame = camera.read()
        frame = cv2.flip(frame,1)
        frame = detector.findHands(frame)
        lmList, bbox = detector.findPosition(frame)    
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


            if fingers[1] and fingers[2] == False :
                if xp == 0 and yp == 0:
                    xp,yp = x1 , y1
                cv2.line(frame,(xp,yp),(x1,y1),color,brush)
                cv2.line(canvas,(xp,yp),(x1,y1),color,brush)
                cv2.line(bg,(xp,yp),(x1,y1),color,brush)
                xp,yp = x1 , y1
            
        
        bg[0:144,0:1280] = header

        try:
            ret, buffer = cv2.imencode('.jpg', bg)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except Exception as e:
            pass


global choice
choice = 0
@app.route('/')
def index():
    return render_template('form.html')

    
@app.route('/video_feed')
def video_feed():
    if(choice=='1'):
        return Response(getwebcam(), mimetype='multipart/x-mixed-replace; boundary=frame')
    
    elif(choice=='2'):
        return Response(getCanvas(), mimetype='multipart/x-mixed-replace; boundary=frame')
    
    elif(choice=='3'):
        return Response(getimg(), mimetype='multipart/x-mixed-replace; boundary=frame')
    
@app.route('/add_region', methods=['POST'])
def add_region():
    global choice
    choice = request.form['file_path']
    return render_template('index.html')
    

if __name__ == '__main__':
    app.run()
    
camera.release()
cv2.destroyAllWindows()     