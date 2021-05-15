import csv_operations as reader
import cv2 as cv2
import numpy as np
import matplotlib.pyplot as plt





filmName = 'film_2'
xRightEye,yRightEye,_ = reader.read_csv('data/'+filmName+'_points/LEye.csv')
xLeftEye,yLeftEye,_ = reader.read_csv('data/'+filmName+'_points/REye.csv')

capture = cv2.VideoCapture('data/'+filmName+'.mp4')
fps = capture.get(cv2.CAP_PROP_FPS)

framesCount = len(xRightEye)
frame = 0

leftEye = []
rightEye = []
seconds = 0
framesWhileEyeIsOpen=0
showHist = True


while frame < framesCount:
    _, img = capture.read()

    leftEyePointX = int(xLeftEye[frame])
    leftEyePointY = int(yLeftEye[frame])
    rightEyePointX = int(xRightEye[frame])
    rightEyePointY = int(yRightEye[frame])

    leftEye = cropEye(image=img,border=20,positionX=leftEyePointX,positionY=leftEyePointY)
    rightEye = cropEye(image=img,border=20,positionX=rightEyePointX,positionY=rightEyePointY)

    leftEye = scaleImage(image=leftEye,scale=8)
    rightEye = scaleImage(image=rightEye,scale=8)

    if isEyeOpen(eye=leftEye):
        framesWhileEyeIsOpen+=1;

    if oneSecondPasssed(frameNumber=frame):
        if framesWhileEyeIsOpen > 0:
            print(("Eye open in second - {sec}s").format(sec = seconds))
            
        framesWhileEyeIsOpen=0
        seconds+=1

    cv2.imshow('leftEye', leftEye)
    cv2.moveWindow('leftEye',350,200)
    
    frame+=1
    if cv2.waitKey(int(1000/fps)) & 0xFF == ord('q'):
        break

