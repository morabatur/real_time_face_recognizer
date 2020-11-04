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

from client.ua.nules.ui.ButtonManager import CameraButtonManager
from client.ua.nules.ui.CameraList import CameraList
from client.ua.nules.ui.FacesList import FacesList
from client.ua.nules.ui.GUI import Ui_MainWindow
from client.ua.nules.ui.CameraDialog import CameraDialog
from PyQt5 import QtWidgets





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
                    if not len(frame_data[1]) == 0:
                        for (name, top, right, bottom, left) in frame_data[1]:

                            # Draw a box around the face
                            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                            # Draw a label with a name below the face
                            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                            font = cv2.FONT_HERSHEY_DUPLEX
                            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

                    h, w, ch = frame.shape
                    bytesPerLine = ch * w
                    convertToQtFormat = QImage(frame.data, w, h, bytesPerLine, QImage.Format_BGR888)
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
        self.button_manager = CameraButtonManager(self.ui.horizontalLayout_2, self.ui.camera_scroll_area_widget_contents, self)
        self.button_manager.init_camera_buttons()
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


app = QtWidgets.QApplication([])
application = CurrentProgram()

application.show()

sys.exit(app.exec())
