import cv2
import os

scale_width = 32
scale_height = 32

def scale(file):
    global scale_width, scale_height
    img = cv2.imread(file)
    img =  cv2.resize(img, (scale_width, scale_height), interpolation=cv2.INTER_CUBIC)
    cv2.imwrite(file, img)

def setScale(width, height):
    global scale_width, scale_height
    scale_width = width
    scale_height = height

def itrFile(dirPath):
    if os.path.exists(dirPath):
        print('start to process !')
        for parent, dirnames, filenames in os.walk(dirPath):
            for dirname in dirnames:
                print('dirname is %s' % dirname)
                for parent, dirnames, filenames in os.walk(dirPath+"/"+dirname):
                    for filename in filenames:
                        print('filename is %s' % filename)
                        scale(dirPath+'/'+dirname+'/'+filename)                
    else:
        print('not a valid full path !')
        return
