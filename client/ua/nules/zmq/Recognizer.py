import cv2
import zmq
import pickle
from draft import face_recognition
import numpy as np
import os
import time
from datetime import datetime



def grab_photos(image_dir: str):
    print('start grab')
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
    print('end grub')
    return photos_names, photos_encodings


trainer_images_dir = '../../../../trainer_images'
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


context = zmq.Context()
videoStreamSocket = context.socket(zmq.PULL)
videoStreamSocket.connect("tcp://127.0.0.1:5560")

# faceRecognitionSocket = context.socket(zmq.PUSH)
# faceRecognitionSocket.bind("tcp://127.0.0.1:5564")

while True:
    start_time = time.time()

    frame = videoStreamSocket.recv_pyobj()
    # Grab a single frame of video
    # ret, frame = cv2.VideoCapture(0).read()
    # if ret:
    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    # rgb_frame = frame  # [:, :, ::-1]

    # Find all the faces and face enqcodings in the frame of video
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)
    # Loop through each face in this frame of video

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        # Or instead, use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        name = 'Unknown'
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        # cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        now = datetime.now()  # current date and time

        # cv2.putText(frame, str(now.strftime("%H:%M:%S")), (0 + 6, 0 - 6), font, 1.0, (255, 255, 255), 1)

        # faceRecognitionSocket.send_pyobj(frame)

    # cv2.imshow('video', frame)
    print("--- %s seconds ---" % (time.time() - start_time))
