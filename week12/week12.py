from urllib import request
from bs4 import BeautifulSoup
import requests
import csv
import time
from queue import Queue
from threading import Thread

headers={

                "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",

                "cookie":
'_ns=NS1.2.1527376066.1641570966; _ntes_nnid=7a17336b9171afacc52cd2d4d6281e48,1642329090851; _ntes_nuid=7a17336b9171afacc52cd2d4d6281e48; JSESSIONID-WYYY=ZSl51kxbrvvWYl/MOBhanGP98Z9dpMREaTdfK\oiTEtd+a5762iYb3gvhy1bR2CeIBFMx6hZAtjf8K3maK/dDOsnCGuZJSlCfoYxq8b7eGgudyuKmzs6tE0qtDZ0TT3Bptp1bO/1dxJG7CoPcwYfnVNJBa8P9yPZllRZS+//+UBdSeBl:1669255195949; _iuqxldmzr_=32; NMTID=00OaZyVA7D9TgLhHUekm5RJJato4IgAAAGEp0FtMQ; WEVNSM=1.0.0; WNMCID=ujngmx.1669253396335.01.0; WM_NI=Hbp6hQHQLf16aNuApFs8E8xwkCqFgb9kLX9I3MCbxKcJd5hjecFG/O+fMfQ1u/O7zQCLn1ZDok45H6xSxWd0Z9xwMevSgUHkZjPvxvo0ki3SFOgwo6rQYSSLJ5iYOaC0TVY=; WM_NIKE=9ca17ae2e6ffcda170e2e6ee86f944a7bfbfb3c74bb5b88ab2d55e929f8a87d5698befbbbbd447ed88bd83d42af0fea7c3b92a8cbec0d7eb5b8c8f8487b43ea392bba2f34eb1e88bd9fb7da99dbfa7e66afbb584b9bc43f1938d83fb41a196acd6eb62a7bd8aa8ae45e9ba8387d43bb7f181d8f95b8194a2d2d950adb5fcd6cb3ebc8db8b8e73c9ae7b898d06fb68da9b6cb619ab6a097fb7eadf0a58ab2598691a998ee3eb28f97b4d2488aeba7bace6b81f09cb7dc37e2a3; WM_TID=xaEDVs55L4lARAVFVBeQcNl+MVJvD9aU'
}


def urlbulid(start):
    #创建网址
    url='https://music.163.com/discover/playlist/?order=hot&cat=%E8%AF%B4%E5%94%B1&limit=35&offset='\
        +str(start)
    return url

def getpage(url,timeout,headers):
    #获取网页内容
    response=requests.get(url,timeout = timeout,headers=headers)
    #response.encoding = response.apparent_encoding
    response.encoding = 'utf-8'
    if response.status_code==200:
        return response.content
    return None


def producer(q, url):
    #生产者，用于获取网页内容
    response = requests.get(url=url, headers=headers)
    response.encoding = 'utf-8'
    html = response.content
    q.put(html)

def consumer(q):
    #消费者，从网页内容中获取需要的信息
    row = ['title', 'nickname', 'read_time', 'img_src', 'id', 'herf', 'introduction', 'fav', 'share', 'comment']
    file = open('data.csv', 'w', encoding='utf-8')
    csv_writer = csv.writer(file)  # csv格式写入文件file
    csv_writer.writerow(row)
    time_start = time.perf_counter()
    #html = getpage(url, timeout=1, headers=headers)
    html = q.get()
    soup = BeautifulSoup(html, 'html.parser')
    # 'id': 'm-pl-container'  'class':'m-cvrlst f-cb'
    s = soup.find_all(attrs={'class': 'm-cvrlst f-cb'})
    for i, child in enumerate(s):
        childs = child.find_all(name='li')
        for j, c in enumerate(childs):
            x = c.find_all(name='p')
            ti = x[0].a.string
            ni = x[1].a.string
            times = c.find_all(name='div')
            for k, t in enumerate(times):
                y = t.find_all(name='span')
            co = y[1].string
            id = c.div.div.a.attrs['data-res-id']
            pat = 'D:\\pycharm code\\week12\\图片\\'
            img_src = c.select('img')[0]['src']  # 图片链接
            herf = c.div.a.attrs['href']
            next_page = 'https://music.163.com' + herf
            # 对每个歌单对应的网页进行获取
            html_next = getpage(next_page, timeout=1, headers=headers)
            soup2 = BeautifulSoup(html_next, 'html.parser')

            s_intro = soup2.find(attrs={'class': 'intr f-brk'})
            s_list = []
            if s_intro != None:
                for s_2 in s_intro:
                    if s_2.string != None:
                        s_list.append(s_2.string)

                intro = ''.join(s_list)
            # s_fav = soup2.find(attrs={'class':"u-btni u-btni-fav "})

            s_fav = soup2.find(attrs={'data-res-action': "fav"})
            fav = s_fav.i.string[1:-1]

            s_share = soup2.find(attrs={'data-res-action': "share"})
            for s_4 in s_share:
                share = s_4.string[1:-1]

            s_com = soup2.find(attrs={'id': "cnt_comment_count"})
            for s_5 in s_com:
                com = s_5.string
                if com == '评论':
                    com = 0 #这里如果没有评论，文字内容会是‘评论’，做一个检测，如果没评论的话，数量记为0

            csv_writer.writerow([ti, ni, co, img_src,
                                 id, next_page, intro, fav, share, com])
            # res = requests.get(img_src,headers=headers).content
            request.urlretrieve(img_src, pat + ni + '.jpg')
            print('%s 下载成功' % (ti))

def main():
    #多线程模式主函数
    start_time = time.perf_counter()
    #记录时间
    url_list = []
    tlist = []
    clist = []
    q = Queue()
    for n in range(1, 700, 35):
        url = urlbulid(n)
        url_list.append(url)

    for url in url_list:
        t = Thread(target=producer, args=(q, url,))
        tlist.append(t)
        t.start()
        t.join()

    for i in range(10):
        c = Thread(target=consumer, args=(q,))
        clist.append(c)

    for c in clist:
        c.start()
        q.put(None)

    print('time = %f' % (time.perf_counter() - start_time))

def single():
    #单线程模式
    row = ['title', 'nickname', 'read_time', 'img_src', 'id',
           'herf', 'introduction', 'fav', 'share', 'comment']
    file = open('data.csv', 'w', encoding='utf-8')
    csv_writer = csv.writer(file)  # csv格式写入文件file
    csv_writer.writerow(row)
    time_start = time.perf_counter()
    for num in range(10):
        url = urlbulid(num*35+35)
        html = getpage(url, timeout=2, headers=headers)
        #html = q.get()
        soup = BeautifulSoup(html, 'html.parser')
        # 'id': 'm-pl-container'  'class':'m-cvrlst f-cb'
        s = soup.find_all(attrs={'class': 'm-cvrlst f-cb'})
        for i, child in enumerate(s):
            childs = child.find_all(name='li')
            for j, c in enumerate(childs):
                x = c.find_all(name='p')
                ti = x[0].a.string
                ni = x[1].a.string
                times = c.find_all(name='div')
                for k, t in enumerate(times):
                    y = t.find_all(name='span')
                co = y[1].string
                id = c.div.div.a.attrs['data-res-id']
                pat = 'D:\\pycharm code\\week12\\图片\\'
                img_src = c.select('img')[0]['src']  # 图片链接
                herf = c.div.a.attrs['href']
                next_page = 'https://music.163.com' + herf
                # 对每个歌单对应的网页进行获取
                html_next = getpage(next_page, timeout=1, headers=headers)
                soup2 = BeautifulSoup(html_next, 'html.parser')
                s_intro = soup2.find(attrs={'class': 'intr f-brk'})
                s_list = []
                if s_intro != None:
                    for s_2 in s_intro:
                        if s_2.string != None:
                            s_list.append(s_2.string)

                intro = ''.join(s_list)
                # s_fav = soup2.find(attrs={'class':"u-btni u-btni-fav "})
                s_fav = soup2.find(attrs={'data-res-action': "fav"})
                fav = s_fav.i.string[1:-1]
                s_share = soup2.find(attrs={'data-res-action': "share"})
                for s_4 in s_share:
                    share = s_4.string[1:-1]
                s_com = soup2.find(attrs={'id': "cnt_comment_count"})
                for s_5 in s_com:
                    com = s_5.string
                    if com == '评论':
                        com = 0  # 这里如果没有评价，文字内容会是评论，做一个检测
                csv_writer.writerow([ti, ni, co, img_src, id, next_page,
                                     intro, fav, share, com])
                # res = requests.get(img_src,headers=headers).content
                request.urlretrieve(img_src, pat + ni + '.jpg')
                print('%s 下载成功' % (ti))

            print('已完成%d%%'%(10*num+10))


if __name__ == '__main__':
    start_time = time.perf_counter()
    single()
    #main()

    print('用时%.2f秒' % (time.perf_counter() - start_time))
    print('进程运行结束')