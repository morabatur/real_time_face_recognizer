import sys
import threading
import time
import pickle
import socket
import struct

import cv2

from client.ua.nules.api import ServerApi
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, Qt
from PyQt5.QtGui import QImage, QPixmap

from client.ua.nules.ui.CameraList import CameraList
from client.ua.nules.ui.FacesList import FacesList
from client.ua.nules.ui.GUI import Ui_MainWindow
from client.ua.nules.ui.CameraDialog import CameraDialog
from PyQt5 import QtWidgets

from queue import Queue

main_queue = Queue()
main_widget_names = dict()




class Thread(QThread):

    changePixmap = pyqtSignal(QImage)
    _stop_event = threading.Event()
    # conn = None
    new_source_status = 'initialize'
    satus = False
    def stop(self):
        self._stop_event.set()

    def continue_thread(self):
        self._stop_event.clear()

    def is_stopped(self):
        return self._stop_event.is_set()

    def restart(self):
        self.satus = True
        if self.work() == '1':
            return '1'

    def work(self):
        pass



    def run(self):
        try:

            HOST = ''
            PORT = 8089

            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print('Socket created')

            self.s.bind((HOST, PORT))
            print('Socket bind complete')
            self.s.listen(10)
            print('Socket now listening')

            self.conn, addr = self.s.accept()

            data = b''
            payload_size = struct.calcsize("L")


            while True:
                start_time = time.time()
                print('Is alive at ' + str(start_time))
                if self.new_source_status == 'preinitialize':
                    print('preinitialize status')
                    continue
                elif self.new_source_status == 'reinitialize':
                    try:
                        self.conn.close()
                        self.s.close()
                    except BaseException as e:
                        print('fail in closing socket')
                        print(e)

                    print('reinitialize socket')
                    HOST = ''
                    PORT = 8089

                    self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    print('Socket re-created')

                    self.s.bind((HOST, PORT))
                    print('Socket re-bind complete')
                    self.s.listen(10)
                    print('Socket now re-listening')

                    self.conn, addr = self.s.accept()

                    data = b''
                    payload_size = struct.calcsize("L")

                    self.new_source_status = 'initialize'
                else:
                    pass
                try:
                    # Retrieve message size
                    while len(data) < payload_size:
                        # print('Retrieve message size')
                        data += self.conn.recv(4096)

                    packed_msg_size = data[:payload_size]
                    data = data[payload_size:]
                    msg_size = struct.unpack("L", packed_msg_size)[0]  ### CHANGED

                    # Retrieve all data based on message size
                    while len(data) < msg_size:
                        # print('Retrieve message size')
                        data += self.conn.recv(4096)

                    frame_data = data[:msg_size]
                    data = data[msg_size:]

                    # Extract frame
                    frame_data = pickle.loads(frame_data)
                    frame = frame_data[0] #frame
                    data_face_list = []
                    if not len(frame_data[1]) == 0:
                        for (name, top, right, bottom, left) in frame_data[1]:
                            face_only = frame[left:top, right:bottom]
                            data_face_list.append([name, face_only])

                            # Draw a box around the face
                            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                            # Draw a label with a name below the face
                            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                            font = cv2.FONT_HERSHEY_DUPLEX
                            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                    if not len(data_face_list) == 0:
                        main_queue.put(data_face_list)
                    h, w, ch = frame.shape
                    bytesPerLine = ch * w
                    convertToQtFormat = QImage(frame.data, w, h, bytesPerLine, QImage.Format_BGR888)
                    # p = convertToQtFormat.scaled(711, 631, Qt.KeepAspectRatio) unnecessary
                    self.changePixmap.emit(convertToQtFormat)
                    # print("--- %s seconds ---" % (time.time() - start_time))
                except BaseException as e:
                    print('Exceprion')
                    print(e)
            print('while end')
        except BaseException as e:
            print('exception')
            print(e)
        finally:
            print('FDFSDFSDFSDFSDF')

class CurrentProgram(QtWidgets.QMainWindow):
    def __init__(self):
        super(CurrentProgram, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_camera_buttons()
        self.th = Thread(self)
        self.th.changePixmap.connect(self.setImage)
        self.th.start()
        cameraDialog = CameraDialog()
        cameraList = CameraList()
        facesList = FacesList()
        self.ui.actionAdd.triggered.connect(lambda : cameraDialog.show() )
        self.ui.actionDelete.triggered.connect(lambda : cameraList.show() )
        self.ui.actionShow_faces.triggered.connect(lambda : facesList.show() )

        # self.timer = QtCore.QTimer()
        # self.timer.timeout.connect(self.delete_face)
        # self.timer.start(2000)


    @pyqtSlot(QImage)
    def setImage(self, image):
        self.ui.frame_label.setPixmap(QPixmap.fromImage(image))


    def init_camera_buttons(self):
        api = ServerApi('http://127.0.0.1:5000')
        res = api.get('/camera')

        for camera in res:
            self.addButton(camera)

        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.ui.horizontalLayout_2.addItem(spacerItem1)


    def addButton(self, camera):
        _translate = QtCore.QCoreApplication.translate
        camera_widget = QtWidgets.QWidget(self.ui.camera_scroll_area_widget_contents)

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

        self.ui.horizontalLayout_2.addWidget(camera_widget)
        camera_button.setText(_translate("MainWindow", "View\n" + camera.get('ip')))
        camera_rtsp_buttom.setText(_translate("MainWindow", "Start stream"))


    def rtsp_released(self):

        sending_button = self.sender()
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
        self.th.new_source_status = 'preinitialize'

        api = ServerApi('http://127.0.0.1:5000')
        sending_button = self.sender()
        res = api.get('/streaming/' + str(sending_button.property('id').get('id')))
        self.th.new_source_status = 'reinitialize'


    def add_new_face(self, person_name, frame):
        # print('added face')
        person_widget = QtWidgets.QWidget(self.ui.faces_scroll_area_widget_contents)
        person_widget.setObjectName(person_name)
        verticalLayout_2 = QtWidgets.QVBoxLayout(person_widget)
        name_lbl = QtWidgets.QLabel(person_widget)
        name_lbl.setText(person_name)
        verticalLayout_2.addWidget(name_lbl)
        self.ui.verticalLayout.addWidget(person_widget)

        # h, w, ch = frame.shape
        # bytesPerLine = ch * w
        # convertToQtFormat = QImage(frame.data, w, h, bytesPerLine, QImage.Format_BGR888)
        # p = convertToQtFormat.scaled(711, 631, Qt.KeepAspectRatio) unnecessary
        # self.changePixmap.emit(convertToQtFormat)
        # pixmap01 = QtGui.QPixmap.fromImage(convertToQtFormat)
        # pixmap_image = QtGui.QPixmap(pixmap01)
        #
        #
        # person_widget = QtWidgets.QWidget(self.ui.faces_scroll_area_widget_contents)
        # verticalLayout_2 = QtWidgets.QVBoxLayout(person_widget)
        # face_img = QtWidgets.QLabel(person_widget)
        # face_img.setMinimumSize(QtCore.QSize(151, 101))
        # face_img.setAlignment(QtCore.Qt.AlignCenter)
        # face_img.setPixmap(pixmap_image)
        # verticalLayout_2.addWidget(face_img)
        # name_lbl = QtWidgets.QLabel(person_widget)
        # name_lbl.setText(person_name)
        # verticalLayout_2.addWidget(name_lbl)
        # self.ui.verticalLayout.addWidget(person_widget)

        main_widget_names[person_name] = [time.time(), person_widget]



app = QtWidgets.QApplication([])
application = CurrentProgram()

application.show()

sys.exit(app.exec())
