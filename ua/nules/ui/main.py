import pickle
import sys
import time
import os

import zmq
import cv2
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap

from ua.nules.ui.GUI import Ui_MainWindow
from PyQt5 import QtWidgets

import face_recognition
import numpy as np

def grab_photos(image_dir: str):
    photos_names = []
    photos_encodings = []
    for root, dirs, files in os.walk(image_dir):
        for file in files:
            if file.endswith('png') or file.endswith('jpg'):
                name_for_photo = root.split("\\")[1]
                path = os.path.join(root, file)

                image = face_recognition.load_image_file(path)
                photos_encoding = face_recognition.face_encodings(image)[0]

                photos_encodings.append(photos_encoding)
                photos_names.append(name_for_photo)

    return photos_names, photos_encodings

trainer_images_dir = '../../../trainer_images'
face_names_pickle = '%s/known_face_names.pickle' % trainer_images_dir
face_encodings_pickle = '%s/known_face_encodings.pickle' % trainer_images_dir

if os.path.exists(face_names_pickle) & os.path.exists(face_encodings_pickle):
    with open(face_names_pickle, 'rb') as f:
        known_face_names = pickle.load(f)
        print('load known_face_names')
    with open(face_encodings_pickle, 'rb') as f:
        known_face_encodings = pickle.load(f)
        print('load known_face_encodings')
else:
    known_face_names, known_face_encodings = grab_photos('%s' % trainer_images_dir)
    with open(face_names_pickle, 'wb') as f:
        pickle.dump(known_face_names, f)
    with open(face_encodings_pickle, 'wb') as f:
        pickle.dump(known_face_encodings, f)


known_face_names, known_face_encodings = grab_photos('../../../trainer_images')

class Thread(QThread):
    context = zmq.Context()
    faceRecognitionSocket = context.socket(zmq.PULL)
    faceRecognitionSocket.connect("tcp://127.0.0.1:5564")

    changePixmap = pyqtSignal(QImage)

    def run(self):
        video_capture = cv2.VideoCapture(0)

        while True:
            start_time = time.time()
            ret, frame = video_capture.read()

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_frame = frame[:, :, ::-1]

            # Find all the faces and face enqcodings in the frame of video
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            # Loop through each face in this frame of video
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

                print('matches', matches)
                print('-----------------')

                name = "Unknown"

                # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)


            # ===============
            # frame = self.faceRecognitionSocket.recv_pyobj()
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
