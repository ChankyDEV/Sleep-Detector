import csv
import matplotlib.pyplot as plt
from scipy import ndimage
from .position_data_processing import filterByConfidence
from .position_data_processing import averagePerSecond
from .position_data_processing import differentiation
from csv_operations import read_csv
import math

def getSpeedInEachSecond(filmname,bodypart,threshold):
    x,y,conf = read_csv('data/'+filmname+'_points/'+bodypart+'.csv')
    filteredX, filteredY = filterByConfidence(x,y,conf,0.75)   
    avgX = averagePerSecond(filteredX)
    avgY = averagePerSecond(filteredY)
    diffX = differentiation(avgX)
    diffY = differentiation(avgY)

    speeds = []
    distances = []
    videoTime = len(avgX)

    for second in range(videoTime-1):
        signleDistance = math.hypot(diffX[second],diffY[second])
        distances.append(signleDistance)


    for second in range(videoTime-1):
        if distances[second]>threshold or distances[second]<-threshold:
            actualSpeed = (second,distances[second])
            speeds.append(actualSpeed)       
    return speeds        


def isAnyMoveDetected(second,speeds):
    bodypartsLength = len(speeds)
    for bodypart in range(len(speeds)):       
        for s in range(len(speeds[bodypart])):
            if speeds[bodypart][s][0] == second:
                return True,bodypart          
    return False,bodypartsLength

def decideBodypartName(bodypartIndex):
    if bodypartIndex==0:
        return 'leftAnkle'
    if bodypartIndex==1:
        return 'rightAnkle'                   
    if bodypartIndex==2:
        return 'leftWrist'
    if bodypartIndex==3:
        return 'rightWrist'
    if bodypartIndex==4:
        return 'None'                  