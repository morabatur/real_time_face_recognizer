import socket
import pickle
import struct


class UdpSender(object):
    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientsocket.connect((ip, port))

    def send_data(self, info: object):
        # Serialize frame
        data = pickle.dumps(info)

        # Send message length first
        message_size = struct.pack("L", len(data))

        try:
            # Then send data
            self.clientsocket.sendall(message_size + data)
        except BaseException:
            print('EXCEPRION')
