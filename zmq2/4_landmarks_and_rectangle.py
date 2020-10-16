import cv2
import zmq
import dlib

context = zmq.Context()
src = context.socket(zmq.PULL)
src.connect("tcp://127.0.0.1:5559")

dst = context.socket(zmq.PUSH)
dst.connect("tcp://127.0.0.1:5560")

predictor = dlib.shape_predictor("../shape_predictor_68_face_landmarks.dat")
facer = dlib.face_recognition_model_v1('../dlib_face_recognition_resnet_model_v1.dat')

while True:
    msg = src.recv_pyobj()
    grayFrame = msg['frame']
    faces = msg['faces']
    for face in faces:
        # Получение координат вершин прямоугольника и его построение на изображении
        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2 = face.bottom()
        cv2.rectangle(grayFrame, (x1, y1), (x2, y2), (255, 0, 0), 1)
        # landmarks = predictor(grayFrame, face)
        # print(landmarks)
        # print('=====================================')
    dst.send_pyobj(grayFrame)