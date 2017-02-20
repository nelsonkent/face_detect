import queue
import urllib
import time
import requests
import re
from multiprocessing.dummy import Pool
import os

class Image(object):
    """图片类，保存图片信息"""

    def __init__(self, url, type):
        super(Image, self).__init__()
        self.url = url
        self.type = type
    
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
    pend_queue = queue.Queue()
    history_queue = queue.Queue()
    history_url = queue.Queue()
    session = requests.Session()
    re_objURL = re.compile(r'"objURL":"(.*?)".*?"type":"(.*?)"')

    def __init__(self, delay, word):
          print('init')
          self.delay = delay
          self.pool = Pool(30)
          self.word = word

    def buildUrls(self):
          if os.path.isfile('jsonUrls.txt'):
              print('jsonUrls.txt exits load data ')
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
              return urls

    def getImgUrl(self, url):
          time.sleep(self.delay)
          self.history_url.put(url)
          try:
                 html = self.session.get(url, timeout = 15).content.decode('utf-8')
          except requests.exceptions.RequestException as e:
                 print(e.__cause__)
                 return
          print(html)
          datas = self.re_objURL.findall(html)
          imgs = [Image(self.decode(x[0], x[1]))for x in datas]
          print(imgs)
          
    def decode(self, url):
          for key, value in self.str_table.items():
                 url = url.replace(key, value)
          return url.translate(self.char_table)

    #def handerImg(self):

       

def main():
       print('baiduSpider start!')
       baiduSpider = BaiduSpider(10, '高兴')
       urls = baiduSpider.buildUrls()
       baiduSpider.pool.map(baiduSpider.getImgUrl, urls)

if __name__=='__main__':
       main()
