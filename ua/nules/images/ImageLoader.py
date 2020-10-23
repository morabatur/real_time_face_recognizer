import os

import face_recognition


class ImageLoader(object):
    def __init__(self):
        print('Start')

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


if __name__ == "__main__":
    c = ImageLoader()
    tt, aa = c.grab_photos('../../../trainer_images')