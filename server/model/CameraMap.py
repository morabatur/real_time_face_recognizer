from server.model.Camera import Camera


class CameraMap(object):

    def __init__(self):
        self.camera_dict = dict()

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(CameraMap, cls).__new__(cls)
        return cls.instance

    def map(self) -> dict:
        return self.camera_dict

    def get(self, key: str) -> Camera:
        return self.camera_dict.get(key)

    def add(self, key: str, value: Camera):
        self.camera_dict[key] = value
