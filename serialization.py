import pickle
import face_recognition
import numpy as np
import os
import time

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


if os.path.exists('trainer_images/known_face_names.pickle') \
        & os.path.exists('trainer_images/known_face_encodings.pickle'):
    with open('known_face_names.pickle', 'rb') as f:
        known_face_names = pickle.load(f)
    with open('known_face_encodings.pickle', 'rb') as f:
        known_face_encodings = pickle.load(f)
else:
    known_face_names, known_face_encodings = grab_photos('trainer_images')
    with open('known_face_names.pickle', 'wb') as f:
        pickle.dump(known_face_names, f)
    with open('known_face_encodings.pickle', 'wb') as f:
        pickle.dump(known_face_encodings, f)




