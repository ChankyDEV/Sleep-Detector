import cv2
import urllib.request as urlreq
import os
import matplotlib.pyplot as plt
import dlib

def readVideo(filmname):
    capture = cv2.VideoCapture('data/'+filmname+'.mp4')
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("models/shape_predictor_68_face_landmarks.dat")
    fps = capture.get(cv2.CAP_PROP_FPS)
    while True:
        _, frame = capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        for face in faces:
            print(face)
            x1 = face.left()
            y1 = face.top()
            x2 = face.right()
            y2 = face.bottom()
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
          
        cv2.imshow('Video', frame)
        if cv2.waitKey(int(1000/fps)) & 0xFF == ord('q'):
            break
    return capture.release() and cv2.destroyWindow()



