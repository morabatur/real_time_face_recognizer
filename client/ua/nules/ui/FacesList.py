import os

import cv2
import requests

from client.ua.nules.ui.FacesListGui import Ui_Dialog

from PyQt5 import QtCore, QtGui, QtWidgets


class FacesList(QtWidgets.QDialog):
    def __init__(self):
        super(FacesList, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.accept_data)

        image_dir = 'C:/Users/rcher/PycharmProjects/diploma/trainer_images'
        for root, dirs, files in os.walk(image_dir):
            for dir in dirs:
                item = QtWidgets.QListWidgetItem()
                item.setStatusTip(str(os.path.join(root, dir)))
                item.setText(dir)
                self.ui.listWidget.addItem(item)

    def accept_data(self):
        for root, dirs, files in os.walk(self.ui.listWidget.currentItem().statusTip()):
            for file in files:
                if file.endswith('png') or file.endswith('jpg'):
                    path = os.path.join(root, file)
                    name_for_photo = path.split("\\")[-1]
                    cv2.imshow(name_for_photo, cv2.imread(path))
