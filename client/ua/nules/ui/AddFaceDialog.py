import os
import shutil

from PyQt5.QtWidgets import QFileDialog

from client.ua.nules.ui.AddFaceDialogGui import Ui_Dialog

from PyQt5 import QtCore, QtGui, QtWidgets

class AddFaceDialog(QtWidgets.QDialog):
    def __init__(self):
        super(AddFaceDialog, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.loadButton.clicked.connect(self.loadPhoto)
        self.ui.saveButton.clicked.connect(self.savePhoto)
        self.selectedImagePath = ''
        self.personFolderName = ''
        self.ui.photoPathLineEdit.setDisabled(True)

    def reshow(self):
        self.show()

    def savePhoto(self):
        new_folder = self.ui.nameLineEdit.text()
        trainer_images_dir = 'C:/Users/rcher/PycharmProjects/diploma/trainer_images'
        create_folder = os.path.join(trainer_images_dir, new_folder)
        print(create_folder)
        os.mkdir(create_folder)
        file_name = os.path.basename(self.selectedImagePath)
        if os.path.exists(create_folder):
            shutil.copyfile(self.selectedImagePath, create_folder + '/' + file_name)
        else:
            print('cant create')

        self.close()


    def loadPhoto(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file',
                                            'c:\\', "Image files (*.jpg *jpeg *.png)")
        self.selectedImagePath = fname[0]
        self.ui.photoPathLineEdit.setText(self.selectedImagePath)

