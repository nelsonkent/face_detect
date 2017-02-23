import queue
import urllib
import time
import requests
import re
from multiprocessing.dummy import Pool
import os
import sys
import threading
import thread
import face_detect

queue_lock = threading.Lock()
pend_queue = queue.Queue()
history_queue = queue.Queue()
imageHander = face_detect.ImageHander('haarcascade_frontalface_default.xml')

def historyUrls(history_url):
    while True:
        time.sleep(120) #两分钟更新一次
        print('后台存储baidu url历史记录！')
        with open('historyUrls.txt', 'w') as file:
            while not history_url.empty():
                file.write(history_url.get()+'\n')

def historyImgUrls():
    global history_queue
    while True:
        time.sleep(120)
        print('后台存储image url历史日志！')
        with open('historyImgUrls.txt', 'w') as file:
            while not history_queue.empty():
                file.write(history_queue.get()+'\n')
    


class Image(object):
    """图片类，保存图片信息"""

    def __init__(self, url, imgtype):
        super(Image, self).__init__()
        self.url = url
        self.type = imgtype
    
class BaiduSpider(object):
   # 解码网址用的映射表
    str_table = {
        '_z2C$q': ':',
        '_z&e3B': '.',
        'AzdH3F': '/'
    }

    char_table = {
        'w': 'a',
        'k': 'b',
        'v': 'c',
        '1': 'd',
        'j': 'e',
        'u': 'f',
        '2': 'g',
        'i': 'h',
        't': 'i',
        '3': 'j',
        'h': 'k',
        's': 'l',
        '4': 'm',
        'g': 'n',
        '5': 'o',
        'r': 'p',
        'q': 'q',
        '6': 'r',
        'f': 's',
        'p': 't',
        '7': 'u',
        'e': 'v',
        'o': 'w',
        '8': '1',
        'd': '2',
        'n': '3',
        '9': '4',
        'c': '5',
        'm': '6',
        '0': '7',
        'b': '8',
        'l': '9',
        'a': '0'
    }
    history_url = queue.Queue()
    session = requests.Session()
    re_objURL = re.compile(r'"objURL":"(.*?)".*?"type":"(.*?)"')

    def __init__(self, delay, word):
          print('init')
          self.delay = delay
          self.pool = Pool(4)
          self.word = word
          global history_queue
          if os.path.isfile('historyUrls.txt'):
              print('读取baidu url历史记录！')
              with open('historyUrls.txt', 'r') as file:
                  for url in file:
                      self.history_url.put(url)
          if os.path.isfile('historyImgUrls.txt'):
              print('读取imgUrl历史记录！')
              with open('historyImgUrls.txt', 'r') as file:
                  for url in file:
                      history_queue.put(url)

    def decode(self, url):
        for key, value in self.str_table.items():
             url = url.replace(key, value)
        trans = str.maketrans(self.char_table)
        return url.translate(trans)
        

    def buildUrls(self):
          if os.path.isfile('jsonUrls.txt'):
              print('jsonUrls.txt exits load data')
              urls = []
              with open('jsonUrls.txt', 'r') as file:
                      for line in file:
                          if 'str' in line:
                              break
                          urls.append(line)
              return urls 
          else:
              word = urllib.parse.quote(self.word)
              url = r"http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&fp=result&queryWord={word}&cl=2&lm=-1&ie=utf-8&oe=utf-8&st=-1&ic=0&word={word}&face=0&istype=2nc=1&pn={pn}&rn=30"
              time.sleep(self.delay)
              try:
                     html = self.session.get(url.format(word=word, pn=0), timeout = 15).content.decode('utf-8')
              except requests.exceptions.RequestException as e:
                     print("Exception in -> html = self.session.get(url.format(word=word, pn=0), timeout = 15).content.decode('utf-8')")
              results = re.findall(r'"displayNum":(\d+),', html)
              maxNum = int(results[0]) if results else 0
              urls = [url.format(word=word, pn=x)
                      for x in range(0, maxNum + 1, 30)]
              with open('jsonUrls.txt', 'w') as file:
                  for url in urls:
                      file.write(url + '\n')
              print('成功获取图片urls')
              return urls

    def getImgUrl(self, urls):
          global pend_queue
          time.sleep(self.delay)
          for index in range(len(urls)):
              url = urls[index]
              if url in (self.history_url.queue):
                  return
              else:
                  self.history_url.put(url)
                  try:
                      html = self.session.get(url, timeout = 15).content.decode('utf-8') 
                  except Exception as e :
                      print('error in getImgUrl')
                  datas = self.re_objURL.findall(html)
                  if len(datas) > 0:
                      imgs = [Image(self.decode(x[0]), x[1]) for x in datas]
                      pend_queue.put(imgs)

    #def handerImg()

def main():
    print('if you want to start for nothing clear all the txt file in this folder !')
    print('baiduSpider start!')
    searchWord = input('enter search word in baidu.com:')
    dirPath = input('enter save fileDir for face image:')
    if not os.path.exists(dirPath): #如果目录不存在就返回False
        os.mkdir(dirPath)
    print('search %s image in baidu.com save file to / %s' % (searchWord, dirPath))
    baiduSpider = BaiduSpider(2, searchWord)
    urls = baiduSpider.buildUrls()
    threads = []
    
    #后台baidu url日志
    historyThread= threading.Thread(target=historyUrls, args=(baiduSpider.history_url,))   
    historyThread.daemon = True
    #threads.append(historyThread)
    historyThread.start()
    
    #处理百度网址
    thread1 = threading.Thread(target=baiduSpider.getImgUrl, args = (urls,))
    threads.append(thread1)
    thread1.start()

    #线程合并
    for thread in threads:
        thread.join()
        
    #后台image url历史日志
    thread2 = threading.Thread(target=historyImgUrls)
    #threads.append(thread2)
    thread2.start()
    
    #获取图片后进行处理
    global pend_queue, history_queue
    while  not pend_queue.empty():
        imgs = pend_queue.get()
        for img in imgs:
            if img.url:
                if img.url not in history_queue.queue:
                    history_queue.put(img.url)
                    imageHander.handerImage(img.url, dirPath, img.type)


if __name__=='__main__':
    main()



##def on_click():
##    button['text'] = 'It is changed.'
##
##from tkinter import *
##root = Tk(className='aaa')
##button = Button(root)
##button['text'] = 'change it'
##button['command'] = on_click    #事件关联函数
##button.pack()
##root.mainloop()
