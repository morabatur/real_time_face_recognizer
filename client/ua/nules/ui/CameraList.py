import requests

from client.ua.nules.api import ServerApi
from client.ua.nules.ui.ButtonManager import CameraButtonManager
from server.model.Camera import Camera, CameraSchema
from client.ua.nules.ui.CameraListGui import Ui_Dialog

from PyQt5 import QtCore, QtGui, QtWidgets


class CameraList(QtWidgets.QDialog):
    def __init__(self, button_manager: CameraButtonManager):
        super(CameraList, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.deleteButton.clicked.connect(self.delete_camera)
        self.camera_schema = CameraSchema()
        self.ui.listWidget.clicked.connect(self.click_item)
        self.ui.listWidget.clicked.connect(self.click_item)
        self.button_manager = button_manager
        self.current_camera_id = ''
        self.api = ServerApi('http://127.0.0.1:5000')
        self.load_cameras()

    def load_cameras(self):
        self.ui.listWidget.clear()
        res = self.api.get('/camera')
        for camera in res:
            item = QtWidgets.QListWidgetItem()
            item.setStatusTip(str(camera.get('id')))
            item.setText(str(camera.get('ip')) + ':' + str(camera.get('port')))
            self.ui.listWidget.addItem(item)

    def click_item(self):
        self.current_camera_id = self.ui.listWidget.currentItem().statusTip()
        self.current_camera_index = self.ui.listWidget.currentRow()

    def delete_camera(self):
        camera_id = self.current_camera_id
        self.button_manager.delete_button(str(camera_id))
        response = self.api.delete_camera(str(camera_id))
        self.ui.listWidget.takeItem(self.current_camera_index)
        print('delete camera id ', str(camera_id), '; response ', str(response.status_code))

    def reshow(self):
        self.load_cameras()
        self.show()
