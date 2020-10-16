import sys

# Tkinter selector
if sys.version_info[0] < 3:
    from Tkinter import *
    import Tkinter as tk
else:
    from tkinter import *
    import tkinter as tk
import numpy as np
import cv2
from PIL import Image, ImageTk
import dlib


def detect_faces_and_landmarks(data):
    # Конвертирование изображения в черно-белое
    grayFrame = cv2.cvtColor(data.frame, cv2.COLOR_BGR2GRAY)
    # Обнаружение лиц и построение прямоугольного контура
    # 1 - Перетворити кольоровий фрейм в сірий
    # 2 - Отримати список лиць із фрейму
    # 3 - Пройтись по лицях та визначити їх кординати
    # 4 - Визначити ключові точки обличчя
    # 5 - Намалювати прямокутники по визначених кординатах
    # 6 - Вивести все на екран
    faces = data.detector(grayFrame)
    # Обход списка всех лиц попавших на изображение
    for face in faces:
        # Выводим количество лиц на изображении
        # cv2.putText(data.frame, "{} face(s) found".format(len(faces)), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
        #             (255, 0, 0), 2)
        # Получение координат вершин прямоугольника и его построение на изображении
        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2 = face.bottom()
        cv2.rectangle(data.frame, (x1, y1), (x2, y2), (255, 0, 0), 1)
        # Получение координат контрольных точек и их построение на изображении
        landmarks = data.predictor(grayFrame, face)
        # face_descriptor = data.facer.compute_face_descriptor(data.frame, landmarks)
        print("Detection: Left: {} Top: {} Right: {} Bottom: {}".format(
             x1, x2, y1, y2))
        # print(face_descriptor)
        print('============================')
        # for n in range(0, 68):
        #     x = landmarks.part(n).x
        #     y = landmarks.part(n).y
        #     # print(x)
        #     # print(y)
        #     cv2.circle(data.frame, (x, y), 1, (255, 0, 0), 1)


def skip_and_scale_frames(data, skip, scale):
    for i in range(skip):  # skip frames
        data.camera.grab()
    grabbed, data.frame = data.camera.read()

    # scale_percent = scale  # percent of original size
    # data.width = int(data.frame.shape[1] * scale_percent / 100)
    # data.height = int(data.frame.shape[0] * scale_percent / 100)
    # dim = (data.width, data.height)
    # # resize image
    # data.frame = cv2.resize(data.frame, dim, interpolation=cv2.INTER_AREA)
    # # data.frame = cv2.cvtColor(data.frame, cv2.COLOR_BGR2GRAY)


def opencvToTk(frame):
    """Convert an opencv image to a tkinter image, to display in canvas."""
    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(rgb_image)
    tk_image = ImageTk.PhotoImage(image=pil_img)
    return tk_image


def drawCamera(canvas, data):
    data.tk_image = opencvToTk(data.frame)
    canvas.create_image(data.width / 2, data.height / 2, image=data.tk_image)


def redrawAll(canvas, data, root):
    # if data.camera_index == 0:
    #     data.camera_index = 1
    #     data.camera = cv2.VideoCapture(
    #         'rtsp://MyHomeRoman:Zibenaht300078789831a@192.168.1.44:554/stream1')
    # else:
    #     # data.camera_index = 0
    #     # data.camera = cv2.VideoCapture(0)

    _, data.frame = data.camera.read()
    # skip_and_scale_frames(data, 10, 50)

    detect_faces_and_landmarks(data)

    # Redrawing code
    canvas.delete(ALL)
    drawCamera(canvas, data)
    root.after(1, lambda: redrawAll(canvas, data, root))


# def new_camera1(data):
#     data.camera = cv2.VideoCapture(0)
#
#
# def new_camera2(data):
#     data.camera = cv2.VideoCapture(
#         'rtsp://MyHomeRoman:Zibenaht300078789831a@192.168.1.44:554/stream1')


# def keyPressed(event, data):
#     if event.keysym == "1":
#         new_camera1(data)
#     if event.keysym == "2":
#         new_camera2(data)
#     pass


class Struct(object): pass


def run(width, height):
    print("start")
    root = Tk()

    data = Struct()
    # Подключение детектора, настроенного на поиск человеческих лиц
    data.detector = dlib.get_frontal_face_detector()
    data.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
    data.facer = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')

    data.camera_index = 0
    data.camera = cv2.VideoCapture(0)
    # data.camera = cv2.VideoCapture('rtsp://MyHomeRoman:Zibenaht300078789831a@192.168.1.44:554/stream1')
    data.width = width
    data.height = height

    canvas = Canvas(root, width=width, height=height)
    canvas.pack(side=LEFT)

    redrawAll(canvas, data, root)
    # Переключение камеры через 10сек
    # root.after(10000, lambda: new_camera2(data))
    # root.bind("<Key>", lambda event: keyPressed(event, data))
    # Loop tkinter
    root.mainloop()
    # Once the loop is done, release the camera.
    print("Releasing camera!")
    data.camera.release()


if __name__ == "__main__":
    run(500, 500)