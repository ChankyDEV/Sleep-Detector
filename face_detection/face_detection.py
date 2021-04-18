import cv2 as cv2
from csv_reader import read_csv
from face_image_processing import getDistanceBetweenEarsAndEyes
from face_image_processing import getMaximumDistance
from face_image_processing import getFace


filmName = 'film_1'
xRightEye,yRightEye,_ = read_csv('data/'+filmName+'_points/LEye.csv')
xLeftEye,yLeftEye,_ = read_csv('data/'+filmName+'_points/REye.csv')
xNose,_,_ = read_csv('data/'+filmName+'_points/Nose.csv')
xRightEar,yRightEar,_ = read_csv('data/'+filmName+'_points/LEar.csv')
xLeftEar,yLeftEar,_ = read_csv('data/'+filmName+'_points/REar.csv')


positions = {
    'xRightEye':xRightEye,
    'yRightEye':yRightEye,
    'xLeftEye':xLeftEye,
    'yLeftEye':yLeftEye,
    'xNose':xNose,
    'xRightEar':xRightEar,
    'yRightEar':yRightEar,
    'xLeftEar':xLeftEar,
    'yLeftEar':yLeftEar,
}

capture = cv2.VideoCapture('data/'+filmName+'.mp4')
fps = capture.get(cv2.CAP_PROP_FPS)
framesCount = len(xRightEye)
maxEarToEar, maxEyeToEye = getDistanceBetweenEarsAndEyes(leftEar=xLeftEar,rightEar=xRightEar,leftEye=xLeftEye,rightEye=xRightEye)
earToUpperForhead = int(maxEarToEar/2)

frame = 0
while frame < framesCount:
    _, img = capture.read()

    face = getFace(img=img, frame=frame, border=10, earToUpperForhead=earToUpperForhead, maxDistanceBetweenEyes=maxEyeToEye,positions=positions)

    cv2.imshow('Video', img)
    frame+=1
    if cv2.waitKey(int(1000/fps)) & 0xFF == ord('q'):
        break

