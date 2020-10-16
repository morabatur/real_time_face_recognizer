import cv2
import zmq
import dlib

context = zmq.Context()
zmq_socket = context.socket(zmq.PULL)
zmq_socket.bind("tcp://127.0.0.1:5558")

dst = context.socket(zmq.PUSH)
dst.bind("tcp://127.0.0.1:5559")

detector = dlib.get_frontal_face_detector()

while True:
    frame = zmq_socket.recv_pyobj()
    faces = detector(frame)
    dst.send_pyobj(dict(frame=frame, faces=faces))
