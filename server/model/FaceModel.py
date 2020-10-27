import os
from draft import face_recognition
import pickle


class FaceModel(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(FaceModel, cls).__new__(cls)
        return cls.instance

    def grab_photos(self, image_dir: str):
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

    def load(self):
        trainer_images_dir = 'C:/Users/rcher/PycharmProjects/diploma/trainer_images'
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
            known_face_names, known_face_encodings = self.grab_photos('%s' % trainer_images_dir)
            with open(face_names_pickle, 'wb') as f:
                pickle.dump(known_face_names, f)
            with open(face_encodings_pickle, 'wb') as f:
                pickle.dump(known_face_encodings, f)

        return known_face_names, known_face_encodings

    # TODO implement function
    def reload_model(self):
        test = []


