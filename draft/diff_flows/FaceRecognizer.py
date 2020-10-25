import cv2
import zmq
import dlib
from time import time


cap = cv2.VideoCapture(0)
detector = dlib.get_frontal_face_detector()
context = zmq.Context()
dst = context.socket(zmq.PUSH)
dst.bind("tcp://127.0.0.1:5561")

nextSrc = context.socket(zmq.PULL)
nextSrc.connect("tcp://127.0.0.1:5564")

predictor = dlib.shape_predictor("../shape_predictor_68_face_landmarks.dat")
facer = dlib.face_recognition_model_v1('../dlib_face_recognition_resnet_model_v1.dat')

while True:
    data = nextSrc.recv_pyobj()
    grayFrame = data['grayFrame']
    faces = data['faces']
    for face in faces:
        print('face {}', face)
        landmarks = predictor(grayFrame, face)
        print(landmarks)
        dst.send_pyobj(dict(landmarks=landmarks, ts=time()))



