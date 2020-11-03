import threading
from threading import Thread

from server.model.FaceModel import FaceModel
from server.model.Camera import Camera
from server.model.SenderManager import SenderManager
from server.udp.UdpSender import UdpSender

import cv2
import numpy as np

from draft import face_recognition


class RstpThread(Thread):
    def __init__(self, camera: Camera, face_model: FaceModel, sender_manager: SenderManager, udp_sender: UdpSender):
        Thread.__init__(self)
        self.udp_stream = False
        self._stop_event = threading.Event()
        self.camera = camera
        self.face_model = face_model
        self.sender_manager = sender_manager
        self.udp_sender = udp_sender
        print('init camera ' + str(camera.get_connect_url()) + ' in thread ' + str(threading.current_thread().ident))

    def stop(self):
        self._stop_event.set()

    def continue_thread(self):
        self._stop_event.clear()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):

        video_capture = cv2.VideoCapture(self.camera.get_connect_url())

        known_face_names, known_face_encodings = self.face_model.load()
        print('loaded model in ' + str(self.name))
        while (True):
            ret, frame = video_capture.read()

            if frame is None:
                print('LOSS SIGNAL for + str(self.name)')
                video_capture = cv2.VideoCapture(self.camera.get_connect_url())
                continue

            if self.name == 'rtsp://MyHomeRoman:Zibenaht300078789831a@192.168.1.45/stream1':
                print('read frame in ' + str(self.name))
            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_frame = frame[:, :, ::-1]

            # Find all the faces and face enqcodings in the frame of video
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            face_coordinates = []
            # Loop through each face in this frame of video
            if not len(face_encodings) == 0:
                for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

                    # Or instead, use the known face with the smallest distance to the new face
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    name = 'undefined'
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]
                    if self.name == 'rtsp://MyHomeRoman:Zibenaht300078789831a@192.168.1.45/stream1':
                        print('detected person: ' + name + 'in thread ' + str(self.name))
                    face_coordinates.append((name, top, right, bottom, left))
            else:
                face_coordinates = []
            if self.udp_stream:
                data = [frame, face_coordinates]
                self.udp_sender.send_data(data)


