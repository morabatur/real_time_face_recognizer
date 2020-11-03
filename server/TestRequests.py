import sys
import threading
import time
import pickle
import socket
import struct

import cv2


try:



    HOST = ''
    PORT = 8089

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket created')

    s.bind((HOST, PORT))
    print('Socket bind complete')
    s.listen(10)
    print('Socket now listening')

    conn, addr = s.accept()

    data = b''
    payload_size = struct.calcsize("L")

    while True:
        start_time = time.time()
        print('Is alive')
        try:

            # Retrieve message size
            while len(data) < payload_size:
                data += conn.recv(4096)

            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("L", packed_msg_size)[0]  ### CHANGED

            # Retrieve all data based on message size
            while len(data) < msg_size:
                data += conn.recv(4096)

            frame_data = data[:msg_size]
            data = data[msg_size:]

            # Extract frame
            frame_data = pickle.loads(frame_data)
            frame = frame_data[0]  # frame
            cv2.imshow('f', frame)
        except BaseException:
            print('Exceprion')
    print('while end')
except BaseException:
    print('exception')