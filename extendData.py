import cv2
import os
import numpy as np
def extendData(dirPath):
    for parent, dirpaths, filenames in os.walk(dirPath):
        for filename in filenames:
            filePath = os.path.join(parent, filename)
            img = cv2.imread(filePath)
            cols, rows, channel = img.shape
            #cv2.imshow('origin', img)
            #平移
            move = np.float32([[1, 0, 1], [0, 1, -1]])
            dest = cv2.warpAffine(img, move, (cols, rows))
            cv2.imwrite(os.path.join(parent, 'c'+filename), dest)
            move = np.float32([[1, 0, 2], [0, 1, -2]])
            dest = cv2.warpAffine(img, move, (cols, rows))
            cv2.imwrite(os.path.join(parent, 'd'+filename), dest)
            #cv2.imshow('move', dest)
            #旋转
            rotation = cv2.getRotationMatrix2D((cols/2, rows/2), -3, 1)
            dest = cv2.warpAffine(img, rotation, (cols, rows))
            #cv2.imshow('rotation', dest)
            cv2.imwrite(os.path.join(parent, 'a'+filename), dest)
            rotation = cv2.getRotationMatrix2D((cols/2, rows/2), 3, 1)
            dest = cv2.warpAffine(img, rotation, (cols, rows))
            #cv2.imshow('rotation', dest)
            cv2.imwrite(os.path.join(parent, 'b'+filename), dest)
    print('job done')
