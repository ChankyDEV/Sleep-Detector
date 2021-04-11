from csv_reader import read_csv
import cv2
import dlib
import numpy as np


def getDistanceBetweenEarsAndEyes(leftEar,rightEar,leftEye,rightEye): 
    earToEar = 0
    maxEarToEar = 0;
    eyeToEye = 0
    maxEyeToEye = 0;
    for i in range(len(leftEar)):        
        maxEarToEar = getMaximumDistance(left=leftEar[i],right=rightEar[i],maxDistance=maxEarToEar)        
        maxEyeToEye = getMaximumDistance(left=leftEye[i],right=rightEye[i],maxDistance=maxEyeToEye)      
    return maxEarToEar, maxEyeToEye

def getMaximumDistance(left,right,maxDistance):
    if left != 0 and right != 0:
        lefToRight = right - left
        if maxDistance < lefToRight:
            maxDistance = lefToRight
    return maxDistance

def getFace(img,frame,border,earToUpperForhead,maxDistanceBetweenEyes,positions):

    rightEarPointX = int(positions['xRightEar'][frame])
    rightEarPointY = int(positions['yRightEar'][frame])
    leftEarPointX = int(positions['xLeftEar'][frame])
    leftEarPointY = int(positions['yLeftEar'][frame])
    leftEyePointX = int(positions['xLeftEye'][frame])
    leftEyePointY = int(positions['yLeftEye'][frame])
    rightEyePointX = int(positions['xRightEye'][frame])
    rightEyePointY = int(positions['yRightEye'][frame])
    nosePointX = int(positions['xNose'][frame])
  
    if earsVisibility(leftEarPosition=leftEarPointX,rightEarPosition=rightEarPointX) == "BOTH":
        face, x1, y1, x2, y2 = cropToFace(img=img, x1=leftEarPointX-border, y1=leftEarPointY-earToUpperForhead-border,
        x2=rightEarPointX+border, y2=rightEarPointY+earToUpperForhead+border)       
        cv2.rectangle(img, (int(x1), int(y1)), (int(x2),int(y2)), (0, 255, 0), 2)

    if earsVisibility(leftEarPosition=leftEarPointX,rightEarPosition=rightEarPointX) == "ONLY_RIGHT":
        noseToEar = rightEarPointX - nosePointX;
        addition = noseToEar - earToUpperForhead
        face, x1, y1, x2, y2 = cropToFace(img=img,x1=leftEyePointX-addition-border,y1=rightEarPointY-earToUpperForhead-border,
        x2=rightEarPointX+border, y2=rightEarPointY+earToUpperForhead+border)       
        cv2.rectangle(img, (int(x1), int(y1)), (int(x2),int(y2)), (0, 255, 0), 2)

    if earsVisibility(leftEarPosition=leftEarPointX,rightEarPosition=rightEarPointX) == "ONLY_LEFT":
        noseToEar = nosePointX - leftEarPointX;
        addition = noseToEar - earToUpperForhead
        actualEyeToEye = rightEyePointX - leftEyePointX  

        if actualEyeToEye < maxDistanceBetweenEyes / 4:
            face, x1, y1, x2, y2 = cropToFace(img=img,x1=leftEarPointX-border, y1=leftEarPointY-earToUpperForhead-border, 
            x2=nosePointX+addition+border, y2=leftEarPointY+earToUpperForhead+border)       
            cv2.rectangle(img, (int(x1), int(y1)), (int(x2),int(y2)), (0, 255, 0), 2)   
        else:  
            face, x1, y1, x2, y2 = cropToFace(img=img,x1=leftEarPointX-border,y1=leftEarPointY-earToUpperForhead-border,
            x2=rightEyePointX+addition+border, y2=leftEarPointY+earToUpperForhead+border)       
            cv2.rectangle(img, (int(x1), int(y1)), (int(x2),int(y2)), (0, 255, 0), 2)  
    return face

def earsVisibility(leftEarPosition,rightEarPosition):
    if leftEarPosition != 0 and rightEarPosition != 0:
        return "BOTH"
    elif leftEarPosition == 0:
        return "ONLY_RIGHT"
    return "ONLY_LEFT" 

def cropToFace(img,x1,y1,x2,y2):
    return img[y1:y2,x1:x2],x1,y1,x2,y2


