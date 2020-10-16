import cv2
import zmq

context = zmq.Context()
zmq_socket = context.socket(zmq.PULL)
zmq_socket.bind("tcp://127.0.0.1:5560")

while True:
    msg = zmq_socket.recv_pyobj()
    cv2.imshow('frame', msg['grayFrame'])
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break