
import csv_operations as reader
import cv2 as cv2
import numpy as np

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



