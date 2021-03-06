import socket
import pickle
import struct
import time


class UdpSender(object):
    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientsocket.connect((ip, port))

    # def __new__(cls):
    #     if not hasattr(cls, 'instance'):
    #         cls.instance = super(UdpSender, cls).__new__(cls)
    #     return cls.instance

    def send_data(self, info: object):
        # Serialize frame
        data = pickle.dumps(info)

        # Send message length first
        message_size = struct.pack("L", len(data))

        try:
            # Then send data
            self.clientsocket.sendall(message_size + data)
        except BaseException:
            print('EXCEPRION, try reconnect')
            time.sleep(3)
            self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                self.clientsocket.connect((self.ip, self.port))
            except BaseException as e:
                print(e)

