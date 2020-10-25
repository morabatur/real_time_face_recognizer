import json


class Camera(object):
    def __init__(self, ip: str, port: int, user: str, password: str, rtsp_path: str):
        self.ip = ip
        self.port = port
        self.user = user
        self.password = password
        self.rtsp_path = rtsp_path
        # self.connect_url ='rtsp://' + user + ':' + password + '@' + ip + rtsp_path
        # example ('rtsp://MyHomeRoman:PASSWORD@192.168.1.45:554/stream1')

    def get_connect_url(self):
        # TODO delete this IF (only for test server)
        if self.port == 0:
            return 0
        return 'rtsp://' + self.user + ':' + self.password + '@' + self.ip + self.rtsp_path
