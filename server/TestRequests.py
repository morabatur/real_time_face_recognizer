# import os
#
# image_dir = 'C:/Users/rcher/PycharmProjects/diploma/trainer_images'
# def readFile(filename):
#     filehandle = open(filename)
#     print filehandle.read()
#     filehandle.close()
#
#
#
# fileDir = os.path.dirname(os.path.realpath('__file__'))
# print fileDir
#
# #For accessing the file in the same folder
# filename = "same.txt"
# readFile(filename)
#
# #For accessing the file in a folder contained in the current folder
# filename = os.path.join(fileDir, 'Folder1.1/same.txt')
# readFile(filename)
#
# #For accessing the file in the parent folder of the current folder
# filename = os.path.join(fileDir, '../same.txt')
# readFile(filename)
#
# #For accessing the file inside a sibling folder.
# filename = os.path.join(fileDir, '../Folder2/same.txt')
# filename = os.path.abspath(os.path.realpath(filename))
# print filename
# readFile(filename)