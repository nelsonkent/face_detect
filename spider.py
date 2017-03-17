import os
import requests
import time
import face_detect
import threading
import queue
count = 0
imageHander = face_detect.ImageHander('E:\\face_detect\\haarcascade_frontalface_default.xml')
urlqueue = queue.Queue()
def handle():
       global urlqueue
       with open('jsonUrls.txt') as file:
              for imgUrl in file:
                     urlqueue.put(imgUrl)
                      
def getimg():
       global imageHander
       while urlqueue.empty:
              imgUrl = urlqueue.get()
              imageHander.handerImage(imgUrl, 'shy', 'png')
       print('end')
handle()
thread = threading.Thread(target=getimg)
thread.start()
thread = threading.Thread(target=getimg)
thread.start()
thread = threading.Thread(target=getimg)
thread.start()

