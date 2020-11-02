# import sys
# import threading
# import time
# import pickle
# import socket
# import struct
#
# import cv2
#
# from client.ua.nules.api import ServerApi
# from PyQt5 import QtCore
# from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
# from PyQt5.QtGui import QImage, QPixmap
#
# from test_ui import Ui_MainWindow
# from PyQt5 import QtWidgets
#
# from queue import Queue
#
# class CurrentProgramUI(QtWidgets.QMainWindow):
#     def on_timer(self):
#         print('HERE')
#         self.ui.label.setParent(None)
#
#         if self.ui.label.parent() is None:
#             print('non')
#             _translate = QtCore.QCoreApplication.translate
#
#             label = QtWidgets.QLabel(self.ui.centralwidget)
#             label.setGeometry(QtCore.QRect(330, 270, 55, 16))
#             label.setObjectName("label")
#
#             label.setText(_translate("MainWindow", "TextLabel"))
#             print('end')
#
#     def __init__(self):
#         super(CurrentProgramUI, self).__init__()
#         self.ui = Ui_MainWindow()
#         self.ui.setupUi(self)
#         # self.timer = QtCore.QTimer()
#         # self.timer.timeout.connect(self.on_timer)
#         # self.timer.start(1000)
#
#
#
#
#
#
#
#
#
#
#
# app = QtWidgets.QApplication([])
# application = CurrentProgramUI()
#
# application.show()
#
# sys.exit(app.exec())
import time

my_dict = {}
my_tim = time.time()
time.sleep(2)
my_dict['1'] = my_tim
my_dict['2'] = time.time()
my_dict['3'] = time.time()

# def has_low_price(key):
#     print('here')
#     return time.time() - my_dict[key] >= 2
#
# map(lambda k: my_dict.pop(k) filter(has_low_price, my_dict.keys())

now = time.time()
for k in list(my_dict):
    v = my_dict[k]
    if now - v >= 2:
        print('delete')
        my_dict.pop(k)



for k, v in my_dict.items():
    print(k)
    print(v)




