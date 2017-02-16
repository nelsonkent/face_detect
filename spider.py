import urllib
from urllib import request
from urllib import error
from http import cookiejar
from bs4 import BeautifulSoup
from multiprocessing.pool import ThreadPool
import queue
import os
import re ##类似pattern
import threading
import codecs
import time

dirPath = 'happy'
history_queue = queue.Queue()
pend_queue = queue.Queue()
condition = threading.Condition()

class Image(object):

    """图片类，保存图片信息"""

    def __init__(self, url, type):
        super(Image, self).__init__()
        self.url = url
        self.type = type

class Downloader(object):
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
    
    def __init__(self):
        self.re_objURL = re.compile(r'"objURL":"(.*?)".*?"type":"(.*?)"')
        self.delay = 10

    ##proxy
    def enableProxy(self, enable_proxy):
        proxy_handler = request.ProxyHandler({"http" : 'http://some-proxy.com:8080'})
        null_proxy_handler = request.ProxyHandler({})
        if enable_proxy:
            opener = request.build_opener(proxy_handler)
        else:
            opener = request.build_opener(null_proxy_handler)
        request.install_opener(opener)
        return opener

    def handerHtml(self, html):
        global pend_queue, condition
        soup = BeautifulSoup(html, 'html.parser')
        ##print(soup.prettify())
        ##imgTags = soup.find_all('li')
        imgTags = self.re_objURL.findall(html) 
        imgs = [Image(self.decode(x[0]), x[1]) for x in imgTags]
        for img in imgs:
            condition.acquire()
            pend_queue.put(img.url)
            condition.notifyAll()
            condition.release()
            

    def saveFile(self, html, fileName):
        file = codecs.open(fileName, 'w', 'utf-8')
        file.write(str(html))
        file.close()


    def main(self):
        url = 'https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1487129188662_R&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word=%E9%AB%98%E5%85%B4%E4%BA%BA%E8%84%B8'
        values = {'username' : 'cqc',  'password' : 'XXXX' }  
        headers = {  
            'Connection': 'Keep-Alive',  
            'Accept': 'text/html, application/xhtml+xml, */*',  
            'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',  
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'  
        }
        opener = self.enableProxy(False);

        ##header
        header = [] 
        for key, value in headers.items():  
            elem = (key, value)  
            header.append(elem)  
        opener.addheaders = header 

        ##req = request.Request(url, headers=headers)
        ##resp = request.urlopen(req, timeout=10)
        try:
            resp = opener.open(url)
        except error.HTTPError as e:
            print(e.code)
        page = resp.read().decode('utf-8')
        self.saveFile(page, 'temp.txt')
        self.handerHtml(page)

    def decode(self, url):
        """解码图片URL
        解码前：
        ippr_z2C$qAzdH3FAzdH3Ffl_z&e3Bftgwt42_z&e3BvgAzdH3F4omlaAzdH3Faa8W3ZyEpymRmx3Y1p7bb&mla
        解码后：
        http://s9.sinaimg.cn/mw690/001WjZyEty6R6xjYdtu88&690
        """
        # 先替换字符串
        for key, value in self.str_table.items():
            url = url.replace(key, value)
        # 再替换剩下的字符
        return url.translate(self.char_table)

def downImg(inputs):
        """下载图片"""
        global  dirPath , history_queue, pend_queue, condition
        while True:
            condition.acquire()
            if pend_queue.empty():
                print('pend_queue is empty')
                condition.wait()
                print("thread %s is wait for task " % threading.currentThread().name)
            imgUrl = pend_queue.get()
            print(imgUrl)
            history_queue.put(imgUrl)
            condition.release()
            if imgUrl.find('.jpg')>0:
                try:
                    stream = request.urlopen(imgUrl, timeout=10).read()
                except error.URLError as e:
                    print(e.reason)
                if stream :
                    fileName = imgUrl[imgUrl.rfind('/')+1:]
                    if dirPath:
                        filePath = os.path.join(dirPath, fileName)
                    else:
                        filePath = fileName
                    if os.path.isfile(filePath):
                        print ('File %s exist.' % filePath)
                        continue
                    print(filePath)
                    with open(filePath, 'wb') as fp:
                        fp.write(stream)
                        fp.close()
                pend_queue.task_done()
                print(imgUrl)
            else:
                print("url %s is not a img" % imgUrl)

if __name__ == '__main__':
    baiduDownloader = Downloader()
    baiduDownloader.main()
    pool = ThreadPool(processes=10)
    inputs=list(range(2))
    pool.map(downImg, inputs)


##cookie
##cookie=cookiejar.CookieJar()
##cookiehand=request.HTTPCookieProcessor(cookie)
##opener=request.build_opener(cookiehand)
