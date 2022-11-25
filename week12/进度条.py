# encoding= 'utf-8'
# 添加了进度条
# 未添加多线程
import requests
from bs4 import BeautifulSoup
import os
from lxml import etree
import time
import threading  # add later
import sys
class Actress():
    def __init__(self, string, headers):
    	#网址是不能说的秘密。。。
        self.url = "https://xxxx.com/html/%s" % int(string)
        self.headers = headers
        self.string = string

    def video_source(self, headers, timeout):
        r = requests.get(self.url, headers=headers)
        if r.status_code == 200:
            print("连接成功，开始下载:")
        else:
            print("网络连接失败，请检查网站书写或者网络连接\n")

        html = etree.HTML(r.text)
        soup = BeautifulSoup(r.text, 'lxml')
        title = soup.select(
            'div.container.xq_js > div >div.col-lg-12.col-md-12.col-xs-12 > div.j_s > h3')
        #获取指定信息的一种方式
        # src = soup.select(
        #    'div.container.xq_js > div > div.col-lg-12.col-md-12.col-xs-12 > div.j_s > div.rm_bq > ul > li > a')
        #也可以使用xpath
        src = html.xpath('//div[@class="rm_bq"]/ul/li/a/@href')
        for title, src in zip(title, src):
            data = {
                'title': title.get_text().strip().split(' ')[0],
                'src': src.strip()
            }
            self.src = src.strip()
            print(self.src)
        if str(self.src).endswith('.mp4'):
            url = str(self.src)
            self.r = requests.get(url, headers=self.headers)
            if self.r.status_code == 200:
                print('headers is ', self.r.headers)
                print('Type: ',
                      self.r.headers['Content-Type'])
                self.Type = str(self.r.headers['Content-Type']).split('/')[1]
                #print('now type is:', self.Type)
                print('Size: ',
                      self.r.headers['Content-Length'], 'bytes')
                self.volume = int(self.r.headers['Content-Length'])
            else:
                print('bad link')

        else:
            print('existing...')

    def video_download(self, headers, timeout):
        r = requests.get(self.src, headers=headers)
        temp_size = 0
        if r.status_code == 200:
            print('link successfully.')
            string = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
            path = 'D:\\file\\%s\\' % string
            if os.path.exists(path):
                pass
            else:
                os.mkdir(path)
                print('directory has been made up.')
            name = time.strftime("%H_%M_%S", time.localtime())
            with open(path + name + '.' + self.Type, 'wb') as f:
                for chunk in self.r.iter_content(chunk_size=1024 * 1024 * 10):
                    if chunk:
                        temp_size += len(chunk)
                        f.write(chunk)
                        f.flush()
                        # 进度条
                        has_done = int(50 * temp_size / self.volume)
                    sys.stdout.write("\r[%s%s]%d%%" % (
                        '>' * has_done, '-' * (50 - has_done), 100 * temp_size / self.volume))
                print()
            print('video downloaded. Stored in ', path + name)
        else:
            print('wrong link.')
            print('new link needed.')
if __name__ == "__main__":
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    # input 5 numbers while number 0 is not started with and no more than 40000
    number='30000'
    action = Action(str(number), headers=headers)
    action.__init__(str(number), headers=headers)
    action.video_source(headers=headers, timeout=10)
    action.video_download(headers=headers, timeout=10)
