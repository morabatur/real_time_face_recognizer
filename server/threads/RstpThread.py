from threading import Thread

from server.model.FaceModel import FaceModel
from server.model.Camera import Camera
from server.model.SenderManager import SenderManager
from server.udp.UdpSender import UdpSender

import cv2
import numpy as np

from draft import face_recognition


class RstpThread(Thread):
    def __init__(self, camera: Camera, face_model: FaceModel, sender_manager: SenderManager):
        Thread.__init__(self)
        self.camera = camera
        self.face_model = face_model
        self.sender_manager = sender_manager

    def run(self):
        sender = UdpSender('localhost', 8089)

        video_capture = cv2.VideoCapture(self.camera.get_connect_url())

        known_face_names, known_face_encodings = self.face_model.load()

        while (True):
            ret, frame = video_capture.read()

            # videoStreamSocket.send_pyobj(frame)
            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_frame = frame[:, :, ::-1]

            # Find all the faces and face enqcodings in the frame of video
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            # Loop through each face in this frame of video
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                print('detected person: ' + name)

                if self.sender_manager.get_stream_ip() == self.camera.ip:
                    print('here')
                    # Draw a box around the face
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                    # Draw a label with a name below the face
                    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            if self.sender_manager.get_stream_ip() == self.camera.ip:
                print('here2')
                sender.send_data(frame)
                print('here3')


