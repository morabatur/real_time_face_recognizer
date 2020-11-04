from client.ua.nules.api import ServerApi
from PyQt5 import QtCore
from PyQt5 import QtWidgets


class CameraButtonManager(object):
    def __init__(self, horizontalLayout, camera_scroll_area_widget_contents, main_self):
        self.main_self = main_self
        self.horizontalLayout = horizontalLayout
        self.camera_scroll_area_widget_contents = camera_scroll_area_widget_contents
        self.api = ServerApi('http://127.0.0.1:5000')


    def init_camera_buttons(self):

        res = self.api.get('/camera')

        for camera in res:
            self.addButton(camera)

        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)


    def delete_button(self, camera_id):
        widget = self.horizontalLayout.findChild(QtWidgets.QWidget, camera_id)
        api = ServerApi('http://127.0.0.1:5000')
        resp = api.rtsp_finish(camera_id)

        if resp.status_code == 200:
            widget.setParent(None)







    def addButton(self, camera):
        api = ServerApi('http://127.0.0.1:5000')

        _translate = QtCore.QCoreApplication.translate
        camera_widget = QtWidgets.QWidget(self.camera_scroll_area_widget_contents)
        camera_widget.setObjectName(str(camera.get('id')))

        horizontalLayout_3 = QtWidgets.QHBoxLayout(camera_widget)

        camera_button = QtWidgets.QPushButton(camera_widget)
        camera_button.setObjectName("camera_button" + camera.get('ip'))
        camera_button.setProperty('id', camera)
        camera_button.released.connect(self.button_released)

        camera_rtsp_buttom = QtWidgets.QPushButton(camera_widget)
        camera_rtsp_buttom.setObjectName("camera_rtsp_buttom" + camera.get('ip'))
        camera_rtsp_buttom.setProperty('id', camera)
        camera_rtsp_buttom.released.connect(self.rtsp_released)

        horizontalLayout_3.addWidget(camera_rtsp_buttom)
        horizontalLayout_3.addWidget(camera_button)

        self.horizontalLayout.addWidget(camera_widget)
        camera_button.setText(_translate("MainWindow", "View\n" + camera.get('ip')))
        resp = api.rtsp_item_status(camera.get('id'))
        stopped_status = resp.json().get('stopped')
        if stopped_status:
            camera_rtsp_buttom.setText(_translate("MainWindow", "Start stream"))
        else:
            camera_rtsp_buttom.setText(_translate("MainWindow", "Stop stream"))



    def rtsp_released(self):

        sending_button = self.main_self.sender()
        api = ServerApi('http://127.0.0.1:5000')

        if sending_button.text() == 'Start stream':
            resp = api.rtsp_start(sending_button.property('id').get('id'))
            print('start rtsp ', str(resp.status_code))
            if resp.status_code == 200 or resp.status_code == '200':
                sending_button.setText('Stop stream')
        else:
            resp = api.rtsp_finish(sending_button.property('id').get('id'))
            print('start rtsp ', str(resp.status_code))
            if resp.status_code == 200 or resp.status_code == '200':
                sending_button.setText('Start stream')

    def button_released(self):
        self.main_self.new_source_status = 'preinitialize'

        api = ServerApi('http://127.0.0.1:5000')
        sending_button = self.main_self.sender()
        res = api.get('/streaming/' + str(sending_button.property('id').get('id')))
        self.main_self.new_source_status = 'reinitialize'



