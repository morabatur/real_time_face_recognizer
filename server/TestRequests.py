import os

image_dir = 'C:/Users/rcher/PycharmProjects/diploma/trainer_images'
photos_names = []
for root, dirs, files in os.walk(image_dir):
    for file in files:
        if file.endswith('png') or file.endswith('jpg'):
            name_for_photo = root.split("\\")[1]
            path = os.path.join(root, file)
