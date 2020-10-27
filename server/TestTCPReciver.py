import zmq

import numpy as np
import cv2

context = zmq.Context()
videoStreamSocket = context.socket(zmq.PULL)
videoStreamSocket.connect("tcp://127.0.0.1:5560")



while True:
    # Capture frame-by-frame
    frame = videoStreamSocket.recv_pyobj()
    rgb_frame = frame[:, :, ::-1]
    # Our operations on the frame come here

    # Display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()