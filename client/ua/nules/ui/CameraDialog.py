import requests

from server.model.Camera import Camera, CameraSchema
from client.ua.nules.ui.CameraGUI import Ui_Dialog


from PyQt5 import QtCore, QtGui, QtWidgets

class CameraDialog(QtWidgets.QDialog):
    def __init__(self):
        super(CameraDialog, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.buttonBox.accepted.connect(self.accept_data)
        self.ui.buttonBox.rejected.connect(self.reject_data)
        self.camera_schema = CameraSchema()

    def accept_data(self):
        ip = self.ui.ip_lineEdit.text()
        port = self.ui.port_lineEdit.text()
        user = self.ui.user_lineEdit.text()
        password = self.ui.password_lineEdit.text()
        rtsp_path = self.ui.rtsp_lineEdit.text()

        # new_camera = Camera(ip, port, user, password, rtsp_path)
        # json_data = self.camera_schema.jsonify(new_camera)
        # print(json_data)

        r = requests.post('http://127.0.0.1:5000/camera', json={'ip': ip,
                                                           'port': port,
                                                           'user': user,
                                                           'password': password,
                                                           'rtsp_path': rtsp_path})
        print('status:')
        print(r.status_code)

        self.close()

    def reject_data(self):
        print('reject_data')
        self.close()
