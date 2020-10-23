import sys
import time

import zmq
import cv2
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap

from ua.nules.ui.GUI import Ui_MainWindow
from PyQt5 import QtWidgets


class Thread(QThread):
    context = zmq.Context()
    faceRecognitionSocket = context.socket(zmq.PULL)
    faceRecognitionSocket.connect("tcp://127.0.0.1:5564")
    changePixmap = pyqtSignal(QImage)

    def run(self):
        while True:
            start_time = time.time()

            frame = self.faceRecognitionSocket.recv_pyobj()
            # if ret:
            # https://stackoverflow.com/a/55468544/6622587
            # rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # h, w, ch = rgbImage.shape
            h, w, ch = frame.shape
            bytesPerLine = ch * w
            # convertToQtFormat = QImage(frame.data, w, h, bytesPerLine, QImage.Format_RGB888)
            convertToQtFormat = QImage(frame.data, w, h, bytesPerLine, QImage.Format_BGR888)
            # p = convertToQtFormat.scaled(400, 400, Qt.KeepAspectRatio)
            self.changePixmap.emit(convertToQtFormat)
            print("--- %s seconds ---" % (time.time() - start_time))


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

application.show()

sys.exit(app.exec())
