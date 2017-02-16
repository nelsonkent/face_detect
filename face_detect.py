import cv2
import sys
import string

def handerImage(imagePath, cascPath):
    
    # Create the haar cascade
    faceCascade = cv2.CascadeClassifier(cascPath)

    # Read the image
    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags = cv2.CASCADE_SCALE_IMAGE
    )

    print("Found {0} faces!".format(len(faces)))
    count = 0
    for (x, y, w, h) in faces:
        crop = image[y:y+h,x:x+w]
        count = count + 1
        ##存储
        import time
        filePath = "C:\\Users\\nelson\\Desktop\\face_detect\\happy\\"
        now = time.time()
        fileName = str(now) 
        filePath = filePath + fileName + ".png"
        print(filePath)
        cv2.imwrite(filePath, crop)
        ##cv2.imshow('crop'+str(count+1), crop)
    print(count)   

    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.imshow("Faces found", image)
    cv2.waitKey(0)

handerImage('abba.png' ,'haarcascade_frontalface_default.xml')

### Draw a rectangle around the faces

