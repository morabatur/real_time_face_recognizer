import requests

from client.ua.nules.api import ServerApi
from server.model.Camera import Camera, CameraSchema
from client.ua.nules.ui.CameraListGui import Ui_Dialog

from PyQt5 import QtCore, QtGui, QtWidgets

class CameraList(QtWidgets.QDialog):
    def __init__(self):
        super(CameraList, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.buttonBox.accepted.connect(self.accept_data)
        self.ui.buttonBox.rejected.connect(self.reject_data)
        self.camera_schema = CameraSchema()
        api = ServerApi('http://127.0.0.1:5000')
        res = api.get('/camera')

        for camera in res:
            item = QtWidgets.QListWidgetItem()
            item.setStatusTip(str(camera.get('id')))
            item.setText(str(camera.get('ip')) + ':' + str(camera.get('port')))
            self.ui.listWidget.addItem(item)



    def accept_data(self):
        print('index ',  self.ui.listWidget.currentIndex())
        print('currentRow ',  self.ui.listWidget.currentRow())
        print('currentItem ',  self.ui.listWidget.currentItem())
        print('currentItem ',  self.ui.listWidget.currentItem().statusTip())

        r = requests.get('http://127.0.0.1:5000/camera')
        print('status:')
        print(r.status_code)



    def reject_data(self):
        print('reject_data')
        self.close()
