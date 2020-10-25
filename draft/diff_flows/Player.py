import cv2
import zmq
from datetime import datetime

context = zmq.Context()
videoStreamSocket = context.socket(zmq.PULL)
videoStreamSocket.connect("tcp://127.0.0.1:5560")

faceRecognitionSocket = context.socket(zmq.PULL)
faceRecognitionSocket.connect("tcp://127.0.0.1:5561")

while True:
    singleVideoFrame = videoStreamSocket.recv_pyobj()
    cv2.imshow('frame', singleVideoFrame)
    recognitionData = faceRecognitionSocket.recv_pyobj()
    landmarks = recognitionData['landmarks']
    timestamp = recognitionData['ts']
    humanTime = datetime.fromtimestamp(timestamp)
    print('detected face on ' + str(humanTime) + ", landmarks:")
    print(landmarks)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
