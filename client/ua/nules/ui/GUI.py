# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'app.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1027, 862)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(743, 0, 20, 661))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.frame_label = QtWidgets.QLabel(self.centralwidget)
        self.frame_label.setGeometry(QtCore.QRect(14, 15, 711, 631))
        self.frame_label.setText("")
        self.frame_label.setObjectName("frame_label")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(10, 650, 1001, 20))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(440, 660, 55, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(850, 10, 55, 16))
        self.label_2.setObjectName("label_2")
        self.faces_scroll_area = QtWidgets.QScrollArea(self.centralwidget)
        self.faces_scroll_area.setGeometry(QtCore.QRect(760, 40, 241, 611))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.faces_scroll_area.sizePolicy().hasHeightForWidth())
        self.faces_scroll_area.setSizePolicy(sizePolicy)
        self.faces_scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.faces_scroll_area.setWidgetResizable(True)
        self.faces_scroll_area.setObjectName("faces_scroll_area")
        self.faces_scroll_area_widget_contents = QtWidgets.QWidget()
        self.faces_scroll_area_widget_contents.setGeometry(QtCore.QRect(0, 0, 218, 609))
        self.faces_scroll_area_widget_contents.setObjectName("faces_scroll_area_widget_contents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.faces_scroll_area_widget_contents)
        self.verticalLayout.setObjectName("verticalLayout")


        self.person_widget = QtWidgets.QWidget(self.faces_scroll_area_widget_contents)
        self.person_widget.setObjectName("person_widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.person_widget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.up_line = QtWidgets.QFrame(self.person_widget)
        self.up_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.up_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.up_line.setObjectName("up_line")
        self.verticalLayout_2.addWidget(self.up_line)
        self.face_img = QtWidgets.QLabel(self.person_widget)
        self.face_img.setMinimumSize(QtCore.QSize(151, 101))
        self.face_img.setAlignment(QtCore.Qt.AlignCenter)
        self.face_img.setObjectName("face_img")
        self.verticalLayout_2.addWidget(self.face_img)
        self.name_lbl = QtWidgets.QLabel(self.person_widget)
        self.name_lbl.setObjectName("name_lbl")
        self.verticalLayout_2.addWidget(self.name_lbl)
        self.down_line = QtWidgets.QFrame(self.person_widget)
        self.down_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.down_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.down_line.setObjectName("down_line")
        self.verticalLayout_2.addWidget(self.down_line)
        self.verticalLayout. addWidget(self.person_widget)


        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.faces_scroll_area.setWidget(self.faces_scroll_area_widget_contents)

        self.cameras_scroll_area = QtWidgets.QScrollArea(self.centralwidget)
        self.cameras_scroll_area.setGeometry(QtCore.QRect(30, 680, 971, 131))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cameras_scroll_area.sizePolicy().hasHeightForWidth())
        self.cameras_scroll_area.setSizePolicy(sizePolicy)
        self.cameras_scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.cameras_scroll_area.setWidgetResizable(True)
        self.cameras_scroll_area.setObjectName("cameras_scroll_area")
        self.camera_scroll_area_widget_contents = QtWidgets.QWidget()
        self.camera_scroll_area_widget_contents.setGeometry(QtCore.QRect(0, 0, 969, 108))
        self.camera_scroll_area_widget_contents.setObjectName("camera_scroll_area_widget_contents")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.camera_scroll_area_widget_contents)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")




        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.cameras_scroll_area.setWidget(self.camera_scroll_area_widget_contents)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1027, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menutest = QtWidgets.QMenu(self.menubar)
        self.menutest.setObjectName("menutest")
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        self.menuCamera = QtWidgets.QMenu(self.menuSettings)
        self.menuCamera.setObjectName("menuCamera")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionShow_faces = QtWidgets.QAction(MainWindow)
        self.actionShow_faces.setObjectName("actionShow_faces")
        self.actionAdd_face = QtWidgets.QAction(MainWindow)
        self.actionAdd_face.setObjectName("actionAdd_face")
        self.actionRemove_Face = QtWidgets.QAction(MainWindow)
        self.actionRemove_Face.setObjectName("actionRemove_Face")
        self.actionVideo = QtWidgets.QAction(MainWindow)
        self.actionVideo.setObjectName("actionVideo")
        self.actionReadme = QtWidgets.QAction(MainWindow)
        self.actionReadme.setObjectName("actionReadme")
        self.actionAuthor = QtWidgets.QAction(MainWindow)
        self.actionAuthor.setObjectName("actionAuthor")
        self.actionAdd = QtWidgets.QAction(MainWindow)
        self.actionAdd.setObjectName("actionAdd")
        self.actionDelete = QtWidgets.QAction(MainWindow)
        self.actionDelete.setObjectName("actionDelete")
        self.menuFile.addSeparator()
        self.menutest.addSeparator()
        self.menutest.addAction(self.actionShow_faces)
        self.menutest.addAction(self.actionAdd_face)
        self.menutest.addAction(self.actionRemove_Face)
        self.menuCamera.addAction(self.actionAdd)
        self.menuCamera.addAction(self.actionDelete)
        self.menuSettings.addAction(self.menuCamera.menuAction())
        self.menuSettings.addAction(self.actionVideo)
        self.menuHelp.addAction(self.actionReadme)
        self.menuHelp.addAction(self.actionAuthor)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menutest.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Cameras"))
        self.label_2.setText(_translate("MainWindow", "Faces"))
        self.face_img.setText(_translate("MainWindow", "Face image"))
        self.name_lbl.setText(_translate("MainWindow", "TextLabel"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menutest.setTitle(_translate("MainWindow", "Model"))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))
        self.menuCamera.setTitle(_translate("MainWindow", "Camera..."))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionShow_faces.setText(_translate("MainWindow", "Show faces"))
        self.actionAdd_face.setText(_translate("MainWindow", "Add face"))
        self.actionRemove_Face.setText(_translate("MainWindow", "Remove Face"))
        self.actionVideo.setText(_translate("MainWindow", "Video..."))
        self.actionReadme.setText(_translate("MainWindow", "Readme"))
        self.actionAuthor.setText(_translate("MainWindow", "Author"))
        self.actionAdd.setText(_translate("MainWindow", "Add"))
        self.actionDelete.setText(_translate("MainWindow", "Delete"))