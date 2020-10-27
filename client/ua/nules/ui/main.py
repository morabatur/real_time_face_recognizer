import sys
import time
import pickle
import socket
import struct
import requests
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap

from client.ua.nules.ui.GUI import Ui_MainWindow
from PyQt5 import QtWidgets


class Thread(QThread):

    changePixmap = pyqtSignal(QImage)

    def run(self):
        HOST = ''
        PORT = 8089

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Socket created')

        s.bind((HOST, PORT))
        print('Socket bind complete')
        s.listen(10)
        print('Socket now listening')

        conn, addr = s.accept()

        data = b''
        payload_size = struct.calcsize("L")

        while True:
            start_time = time.time()

            try:
                # Retrieve message size
                while len(data) < payload_size:
                    data += conn.recv(4096)

                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack("L", packed_msg_size)[0]  ### CHANGED

                # Retrieve all data based on message size
                while len(data) < msg_size:
                    data += conn.recv(4096)

                frame_data = data[:msg_size]
                data = data[msg_size:]

                # Extract frame
                frame = pickle.loads(frame_data)

                h, w, ch = frame.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(frame.data, w, h, bytesPerLine, QImage.Format_BGR888)
                # p = convertToQtFormat.scaled(711, 631, Qt.KeepAspectRatio) unnecessary
                self.changePixmap.emit(convertToQtFormat)
                print("--- %s seconds ---" % (time.time() - start_time))
            except BaseException:
                print('Exceprion')

class CurrentProgram(QtWidgets.QMainWindow):
    def __init__(self):
        super(CurrentProgram, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.start()

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.ui.frame_label.setPixmap(QPixmap.fromImage(image))


app = QtWidgets.QApplication([])
application = CurrentProgram()

# Initialize server streaming
# server_url = 'http://127.0.0.1:5000'
# requests.get('%s/rtsp/start/0' % server_url) # run thread with video streaming from LOCAL camera
#
# response = requests.get('%s/streaming/local' % server_url) #start streaming in client from LOCAL camera

application.show()

sys.exit(app.exec())
