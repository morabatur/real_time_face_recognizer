import cv2
import zmq
import dlib
from datetime import datetime
from time import time



cap = cv2.VideoCapture(0)
detector = dlib.get_frontal_face_detector()
context = zmq.Context()
videoStreamSocket = context.socket(zmq.PUSH)
videoStreamSocket.bind("tcp://127.0.0.1:5560")

faceRecognitionSocket = context.socket(zmq.PUSH)
faceRecognitionSocket.bind("tcp://127.0.0.1:5564")

while True:
    ret, frame = cap.read()
    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(grayFrame)
    for face in faces:
        print(face)
        # Получение координат вершин прямоугольника и его построение на изображении
        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2 = face.bottom()
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 1)
        cv2.putText(frame, "FACE", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    cv2.putText(frame, "{} face found".format(len(faces)), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    ts = datetime.fromtimestamp(time())
    cv2.putText(frame, str(ts), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    faceRecognitionSocket.send_pyobj(dict(grayFrame=grayFrame, faces=faces))
    videoStreamSocket.send_pyobj(frame)






