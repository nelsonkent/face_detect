import cv2
import sys
import string
import  PIL.Image
import io
import requests
import os
import time
import numpy
count = 0

class ImageHander(object):
    def __init__(self, cascPath):
        self.faceCascade = cv2.CascadeClassifier(cascPath)
        
    def handerImage(self, url, dirPath, imgType):
        print(url)
        try:
            file = io.BytesIO(requests.get(url, timeout=10).content)
            image = PIL.Image.open(file)
            image = numpy.array(image)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        except Exception as e:
            return
        # Detect faces in the image
        faces = self.faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(30, 30),
            flags = cv2.CASCADE_SCALE_IMAGE
        )

        print("Found {0} faces!".format(len(faces)))
        global count 
        for (x, y, w, h) in faces:
            crop = image[y:y+h,x:x+w]
            count = count + 1
            name = time.strftime("%Y%m%d%H%M%S", time.localtime())
            newfile = os.path.join(dirPath,  name + str(count)+'.'+ imgType)
            print(newfile)
            cv2.imwrite(newfile, crop)

            if __name__ == '__main__':
                for (x, y, w, h) in faces:
                   cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.imshow("Faces found", image)
                cv2.waitKey(0)

if __name__ == '__main__':
    imageHander = ImageHander('haarcascade_frontalface_default.xml')
    imageHander.handerImage('http://img.ishuo.cn/1609/1474689789.jpg', 'happy', 'jpg')
### Draw a rectangle around the faces
