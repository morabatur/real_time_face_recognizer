import cv2
import zmq
import dlib

from time import time

detector = dlib.get_frontal_face_detector()

context = zmq.Context()
src = context.socket(zmq.PULL)
src.connect("tcp://127.0.0.1:5557")

dst = context.socket(zmq.PUSH)
dst.connect("tcp://127.0.0.1:5558")

count = 0
delay = 0.0

while True:
    msg = src.recv_pyobj()
    ts = msg['ts']
    frame = msg['frame']
    tnow = time()
    count += 1
    delay += tnow - ts

    if count % 150 == 0:
        print(delay/count)
        delay = 0.0
        count = 0

    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(grayFrame)

    dst.send_pyobj(dict(grayFrame=grayFrame, faces=faces))

