from eye_detection.eye_detection_processing import cropEye
from eye_detection.eye_detection_processing import isEyeOpen
from eye_detection.eye_detection_processing import oneSecondPasssed
from eye_detection.eye_detection_processing import scaleImage
import csv_reader as reader
import cv2 as cv2
import numpy as np
from move_detection.move_detection import getSpeedInEachSecond
from move_detection.speed import Speed
from move_detection.move_detection import isAnyMoveDetected



# Choose film name
filmName = 'film_1'

# Get data
eyeX,eyeY,_ = reader.read_csv('data/'+filmName+'_points/REye.csv')

# Set capture to sepcific video
capture = cv2.VideoCapture('data/'+filmName+'.mp4')
fps = capture.get(cv2.CAP_PROP_FPS)

# Get speed
filmname = 'film_2'
leftAnkleSpeeds = getSpeedInEachSecond(filmname=filmname,bodypart='LAnkle',threshold=15)  
rightAnkleSpeeds = getSpeedInEachSecond(filmname=filmname,bodypart='RAnkle',threshold=15)
leftWristSpeeds = getSpeedInEachSecond(filmname=filmname,bodypart='LWrist',threshold=15)
rightWristSpeeds = getSpeedInEachSecond(filmname=filmname,bodypart='RWrist',threshold=15)

# Initialize consts
framesCount = len(eyeX)
actualFrameNumber = 0
framesWhileEyeIsOpen = 0
actualSecond = 0

# Main processing
while actualFrameNumber < framesCount:
    _, img = capture.read()

    eyePosX = int(eyeX[actualFrameNumber])
    eyePosY = int(eyeY[actualFrameNumber])

    eye = cropEye(image=img,border=20,positionX=eyePosX,positionY=eyePosY)
    eye = scaleImage(image=eye,scale=8)

    if isEyeOpen(eye=eye):
        framesWhileEyeIsOpen+=1;

    if oneSecondPasssed(frameNumber=actualFrameNumber):
        print(("{sec}s").format(sec = actualSecond))
        if framesWhileEyeIsOpen > 0:
            print(("eyes opened").format(sec = actualSecond))

        if isAnyMoveDetected(second=actualSecond,speeds=[leftAnkleSpeeds,rightAnkleSpeeds,leftWristSpeeds,rightWristSpeeds]):
            print(("move detected").format(sec = actualSecond))                

        framesWhileEyeIsOpen=0
        actualSecond+=1

    cv2.namedWindow('finalImg', cv2.WINDOW_NORMAL)
    cv2.imshow("finalImg",img)

    actualFrameNumber+=1
    if cv2.waitKey(int(1000/fps)) & 0xFF == ord('q'):
        break




    