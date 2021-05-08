import csv_reader as reader
import cv2 as cv2
import numpy as np
import matplotlib.pyplot as plt

def cropEye(image,border,positionX,positionY):
    x1=positionX-border
    x2=positionX+border
    y1=int(positionY-(border/2))
    y2=int(positionY+(border/2))
    return image[y1:y2,x1:x2]

def scaleImage(image,scale):
    width = int(image.shape[1] * scale)
    height = int(image.shape[0] * scale)
    dim = (width, height)
    resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    return resized


def isEyeOpen(eye):

    gray = cv2.cvtColor(eye, cv2.COLOR_BGR2GRAY)
    leftFiltered = cv2.GaussianBlur(gray,(5,5),cv2.BORDER_DEFAULT)
    thresh = cv2.threshold(leftFiltered, 25, 50, cv2.THRESH_BINARY)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    dilate = cv2.morphologyEx(thresh, cv2.MORPH_DILATE, kernel)

    diff = cv2.absdiff(dilate, thresh)
    edges = 255-diff;
    inv = 255-edges

    eyeEdges = np.array(inv)
    edgePoints = np.where(inv != 0)[0]
    if len(edgePoints) > 0:
        return True
    else:
        return False    


def oneSecondPasssed(frameNumber):
    if frameNumber % 60 == 0:
        return True
    else:
        return False    

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

