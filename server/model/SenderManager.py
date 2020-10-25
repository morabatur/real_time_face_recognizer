class SenderManager(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SenderManager, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.current_stream_ip = ''

    def set_stream_ip(self, ip):
        self.current_stream_ip = ip

    def get_stream_ip(self):
        return self.current_stream_ip
