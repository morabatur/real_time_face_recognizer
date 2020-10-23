import cv2
import zmq
import dlib
import time

cap = cv2.VideoCapture(0)
detector = dlib.get_frontal_face_detector()
context = zmq.Context()
videoStreamSocket = context.socket(zmq.PUSH)
videoStreamSocket.bind("tcp://127.0.0.1:5560")


def skip_frame(frame_number: int, cap: object):
    for i in range(frame_number):
        cap.grab()
        # Пропустить 10 кадров пример использования
        # skipFrames = 10
        # for i in range(skipFrames):
        #     cap.grab()


while True:
    start_time = time.time()
    ret, frame = cap.read()
    videoStreamSocket.send_pyobj(frame)
    print("--- %s seconds ---" % (time.time() - start_time))

