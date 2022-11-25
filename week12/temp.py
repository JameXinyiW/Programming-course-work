import time
import csv
import requests
from io import BytesIO
from PIL import Image
import requests as req
from queue import Queue
from threading import Thread
from bs4 import BeautifulSoup


# 使用生产者消费者模式，生产者产生的id链接传给消费者执行
def producer(q, url):
    headers = {

        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",

        "cookie":
            '_ns=NS1.2.1527376066.1641570966; _ntes_nnid=7a17336b9171afacc52cd2d4d6281e48,1642329090851; _ntes_nuid=7a17336b9171afacc52cd2d4d6281e48; JSESSIONID-WYYY=ZSl51kxbrvvWYl/MOBhanGP98Z9dpMREaTdfK\oiTEtd+a5762iYb3gvhy1bR2CeIBFMx6hZAtjf8K3maK/dDOsnCGuZJSlCfoYxq8b7eGgudyuKmzs6tE0qtDZ0TT3Bptp1bO/1dxJG7CoPcwYfnVNJBa8P9yPZllRZS+//+UBdSeBl:1669255195949; _iuqxldmzr_=32; NMTID=00OaZyVA7D9TgLhHUekm5RJJato4IgAAAGEp0FtMQ; WEVNSM=1.0.0; WNMCID=ujngmx.1669253396335.01.0; WM_NI=Hbp6hQHQLf16aNuApFs8E8xwkCqFgb9kLX9I3MCbxKcJd5hjecFG/O+fMfQ1u/O7zQCLn1ZDok45H6xSxWd0Z9xwMevSgUHkZjPvxvo0ki3SFOgwo6rQYSSLJ5iYOaC0TVY=; WM_NIKE=9ca17ae2e6ffcda170e2e6ee86f944a7bfbfb3c74bb5b88ab2d55e929f8a87d5698befbbbbd447ed88bd83d42af0fea7c3b92a8cbec0d7eb5b8c8f8487b43ea392bba2f34eb1e88bd9fb7da99dbfa7e66afbb584b9bc43f1938d83fb41a196acd6eb62a7bd8aa8ae45e9ba8387d43bb7f181d8f95b8194a2d2d950adb5fcd6cb3ebc8db8b8e73c9ae7b898d06fb68da9b6cb619ab6a097fb7eadf0a58ab2598691a998ee3eb28f97b4d2488aeba7bace6b81f09cb7dc37e2a3; WM_TID=xaEDVs55L4lARAVFVBeQcNl+MVJvD9aU'
    }

    response = requests.get(url=url, headers=headers)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    ids = soup.select('m-cvrlst f-cb')  # 获取包含歌单详情页网址的标签
    #print(ids)
    q.put(ids)
    # print(ids)


def consumer(q):
    row = ['id', 'title', 'nickname', 'img', 'description', 'count', 'number of song', 'number of adding list', 'share',
           'comment']
    file = open('data.csv', 'w', encoding='utf-8')
    csv_writer = csv.writer(file)  # csv格式写入文件file
    csv_writer.writerow(row)
    headers = {

        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",

        "cookie":
            '_ns=NS1.2.1527376066.1641570966; _ntes_nnid=7a17336b9171afacc52cd2d4d6281e48,1642329090851; _ntes_nuid=7a17336b9171afacc52cd2d4d6281e48; JSESSIONID-WYYY=ZSl51kxbrvvWYl/MOBhanGP98Z9dpMREaTdfK\oiTEtd+a5762iYb3gvhy1bR2CeIBFMx6hZAtjf8K3maK/dDOsnCGuZJSlCfoYxq8b7eGgudyuKmzs6tE0qtDZ0TT3Bptp1bO/1dxJG7CoPcwYfnVNJBa8P9yPZllRZS+//+UBdSeBl:1669255195949; _iuqxldmzr_=32; NMTID=00OaZyVA7D9TgLhHUekm5RJJato4IgAAAGEp0FtMQ; WEVNSM=1.0.0; WNMCID=ujngmx.1669253396335.01.0; WM_NI=Hbp6hQHQLf16aNuApFs8E8xwkCqFgb9kLX9I3MCbxKcJd5hjecFG/O+fMfQ1u/O7zQCLn1ZDok45H6xSxWd0Z9xwMevSgUHkZjPvxvo0ki3SFOgwo6rQYSSLJ5iYOaC0TVY=; WM_NIKE=9ca17ae2e6ffcda170e2e6ee86f944a7bfbfb3c74bb5b88ab2d55e929f8a87d5698befbbbbd447ed88bd83d42af0fea7c3b92a8cbec0d7eb5b8c8f8487b43ea392bba2f34eb1e88bd9fb7da99dbfa7e66afbb584b9bc43f1938d83fb41a196acd6eb62a7bd8aa8ae45e9ba8387d43bb7f181d8f95b8194a2d2d950adb5fcd6cb3ebc8db8b8e73c9ae7b898d06fb68da9b6cb619ab6a097fb7eadf0a58ab2598691a998ee3eb28f97b4d2488aeba7bace6b81f09cb7dc37e2a3; WM_TID=xaEDVs55L4lARAVFVBeQcNl+MVJvD9aU'
    }
    # 设置请求头
    ids = q.get()
    for i in ids:
        url = 'https://music.163.com/' + i['href']  # 生产者传递的id链接
        response = requests.get(url=url, headers=headers)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        idd = soup.select('.s-fc7')[0]['href'].split('=')[-1]
        img = soup.select('img')[0]['data-src']  # 图片链接
        res = req.get(img)
        image = Image.open(BytesIO(res.content))  # 图片处理
        try:
            image.save(str(time.time()) + '.jpg')
        except:
            image.save(str(time.time()) + '.png')
            # os.remove(os.getcwd()+f'\\{cnt}.jpg')

        title = soup.select('title')[0].get_text()  # 标题
        nickname = soup.select('.s-fc7')[0].get_text()  # 昵称
        # print(idd,title,nickname)

        description = soup.select('p')[1].get_text()  # 简介
        count = soup.select('strong')[0].get_text()  # 播放次数
        song_number = soup.select('span span')[0].get_text()  # 歌的数目
        add_lis = soup.select('a i')[1].get_text()  # 添加进列表次数
        share = soup.select('a i')[2].get_text()  # 分享次数
        comment = soup.select('a i')[4].get_text()  # 评论次数
        # print(description,count,song_number,add_lis,share,comment)

        csv_writer.writerow([idd, title, nickname, img, description, count, song_number, add_lis, share, comment])
    file.close()


def main():
    start_time = time.time()  # 记录时间
    url_list = []
    plist = []
    clist = []

    q = Queue()
    for n in range(0, 1300, 35):
        url = f'https://music.163.com/discover/playlist/?order=hot&cat=%E8%AF%B4%E5%94%B1&limit=35&offset={n}'
        url_list.append(url)

    for url in url_list:
        p = Thread(target=producer, args=(q, url,))
        plist.append(p)
    for p in plist:  # 启动线程
        p.start()
    for t in plist:
        p.join()
    for i in range(40):
        c = Thread(target=consumer, args=(q,))
        clist.append(c)
    for c in clist:  # 启动线程
        c.start()
    for c in clist:
        q.put(None)
    print('time = %f' % (time.time() - start_time))

if __name__ == '__main__':

    main()
