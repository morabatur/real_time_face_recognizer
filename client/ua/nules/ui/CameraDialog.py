import requests

from client.ua.nules.ui.ButtonManager import CameraButtonManager
from server.model.Camera import CameraSchema, Camera
from client.ua.nules.ui.CameraGUI import Ui_Dialog


from PyQt5 import QtWidgets

class CameraDialog(QtWidgets.QDialog):
    def __init__(self, button_manager: CameraButtonManager):
        super(CameraDialog, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.button_manager = button_manager
        self.ui.buttonBox.accepted.connect(self.accept_data)
        self.ui.buttonBox.rejected.connect(self.reject_data)
        self.camera_schema = CameraSchema()

    def accept_data(self):
        ip = self.ui.ip_lineEdit.text()
        port = self.ui.port_lineEdit.text()
        user = self.ui.user_lineEdit.text()
        password = self.ui.password_lineEdit.text()
        rtsp_path = self.ui.rtsp_lineEdit.text()

        r = requests.post('http://127.0.0.1:5000/camera', json={'ip': ip,
                                                           'port': port,
                                                           'user': user,
                                                           'password': password,
                                                           'rtsp_path': rtsp_path})
        print('status:')
        print(r.status_code)
        new_camera = r.json()
        self.button_manager.addButton(new_camera)



        self.close()

    def reject_data(self):
        print('reject_data')
        self.close()
