import pickle
import socket
import struct


class UdpReciver(object):
    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Socket created')
        self.s.bind((self.ip, self.port))
        print('Socket bind complete')
        self.s.listen(10)
        print('Socket now listening')

        self.conn, self.addr = self.s.accept()

        self.data = b''  ### CHANGED
        self.payload_size = struct.calcsize("L")  ### CHANGED

    # Need to use in while loop
    def recive_data(self):

        # Retrieve message size
        while len(self.data) < self.payload_size:
            self.data += self.conn.recv(4096)

        packed_msg_size = self.data[:self.payload_size]
        self.data = self.data[self.payload_size:]
        msg_size = struct.unpack("L", packed_msg_size)[0]  ### CHANGED

        # Retrieve all data based on message size
        while len(self.datadata) < msg_size:
            self.data += self.conn.recv(4096)

        frame_data = self.data[:msg_size]
        self.data = self.data[msg_size:]

        # Extract frame
        frame = pickle.loads(frame_data)

        return frame
