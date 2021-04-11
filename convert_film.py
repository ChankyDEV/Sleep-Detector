
import cv2


def cropAndScaleVideo(filmName, width, height):
    fourcc = cv2.VideoWriter_fourcc(*'FMP4')
    out = cv2.VideoWriter(filmName + '_cutted_scaled.mp4', fourcc, 20, (width, height))
    capture = cv2.VideoCapture(filmName + '.mp4')
    fps = capture.get(cv2.CAP_PROP_FPS)
    while True:
        ret, frame = capture.read()
        if ret:
            sky = frame[300:1300, 200:900]
            resized_frame = cv2.resize(sky, (width, height), fx=0, fy=0, interpolation=cv2.INTER_CUBIC)
            out.write(resized_frame)
            cv2.imshow('', resized_frame)
        if cv2.waitKey(int(1000/fps)) & 0xFF == ord('q'):
            break
    capture.release()

cropAndScaleVideo('cut_film_1', 400, 800)

