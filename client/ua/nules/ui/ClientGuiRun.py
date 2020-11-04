import os
import shutil
import sys
import threading
import time
import pickle
import socket
import struct

import cv2

from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog

from client.ua.nules.ui.AddFaceDialog import AddFaceDialog
from client.ua.nules.ui.ButtonManager import CameraButtonManager
from client.ua.nules.ui.CameraList import CameraList
from client.ua.nules.ui.FacesList import FacesList
from client.ua.nules.ui.GUI import Ui_MainWindow
from client.ua.nules.ui.CameraDialog import CameraDialog

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
            print('Critical exception')

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
        cameraDialog = CameraDialog(self.button_manager)
        cameraList = CameraList(self.button_manager)
        facesList = FacesList()
        faceDialog = AddFaceDialog()
        self.ui.actionAdd.triggered.connect(lambda : cameraDialog.show() )
        self.ui.actionDelete.triggered.connect(lambda : cameraList.reshow() )
        self.ui.actionShow_faces.triggered.connect(lambda : facesList.reshow() )
        self.ui.actionAdd_face.triggered.connect(lambda : faceDialog.reshow())

        # self.timer = QtCore.QTimer()
        # self.timer.timeout.connect(self.delete_face)
        # self.timer.start(2000)

    def test(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file',
                                            'c:\\', "Image files (*.jpg *jpeg *.png)")

        file_path = fname[0]
        new_folder = 'testfolder'
        trainer_images_dir = 'C:/Users/rcher/PycharmProjects/diploma/trainer_images'
        create_folder = os.path.join(trainer_images_dir, new_folder)
        print(create_folder)
        os.mkdir(create_folder)
        if os.path.exists(create_folder):
            shutil.copyfile(file_path, create_folder + '/file_copy.jpg')
        else:
            print('cant create')



    @pyqtSlot(QImage)
    def setImage(self, image):
        self.ui.frame_label.setPixmap(QPixmap.fromImage(image))


app = QtWidgets.QApplication([])
application = CurrentProgram()

application.show()

sys.exit(app.exec())
