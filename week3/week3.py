import re
import sys
import os
import jieba
import math
from sklearn import preprocessing
import numpy as np
import matplotlib.pyplot as plt
from week2 import wordcut
def dupliprocess(data):
    datalist=[[]for i in range(len(data))]
    i=0
    for con in data:
        if con not in datalist:
            datalist[i]=con
            i+=1
    return datalist

def getstopwords():
    stopwords = [line.strip() for line in open("D:\pycharm code\week2\stopwords_list.txt", encoding='UTF-8').readlines()]
    return stopwords

def textprocess(tex):
    l = re.compile( r'^[[].*?[]]')
    url = re.compile(
        r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))',
        re.IGNORECASE)
    tim = re.compile(r'(Fri).*')
    p = re.compile(u'['u'\U0001F300-\U0001F64F' u'\U0001F680-\U0001F6FF' u'\u2600-\u2B55 \U00010000-\U0010ffff]+')

    tex = re.sub(p, '', tex)
    # 将表情符合替换为空
    tex = re.sub(url, '', tex)
    tex = re.sub(r"http:", '', tex)
    tex = re.sub(r"我在这里:", '', tex)
    tex = re.sub(r"\\", '', tex)
    tex = re.sub(r"//", '', tex)
    tex = re.sub(r"(我在:)", "", tex)
    '''
    tex = re.sub(r"(\d+).0", "", tex)
    tex = re.sub(tim, "", tex)
        # 除去时间
    tex = re.sub(r"\s+", " ", tex)
        # 除去空格
    '''
    tex = re.sub(r"__", "", tex)
    # 除去一些无意义的数字，文字，符号

    # 除去网址
    tex= re.sub(l, '', tex)
    # 除去地址
    tex = re.sub(r"(回复)?(//)?\s*@\S*?\s*(:| |$)", " ", tex)
    # 除去正文中的@和回复/转发中的用户名
    tex = re.sub(r"\[\S+\]", "", tex)
    # 除去表情符号

    tex = re.sub(r"#\S+#", "", tex)
    # 除去话题内容

    tex = re.sub(u'[\U00010000-\U0010ffff]','',tex)
    return tex

def locationget(con):
    l = re.compile(r'^[[].*?[]]')
    loc = l.match(con).group(0)
    # 记录地址
    return loc


def readtxt(name):
    file_handle = open(name, encoding='UTF-8')
    content = file_handle.readlines()
    l_length = len(content)
    content = ''.join(content)  # 将列表类型转换为字符转类型
    content.strip('\n')  # strip函数可以将字符串
    content = content.split('\n')  # 将去掉\n之后的字符串再次转换为列表，分隔符为换行\n
    file_handle.close()
    return content

def plotime(emotion,time,emotionlist,timelist):
    week = ['Mon','Tus','Wed','Ths','Fri','Sat','Sun']
    week_dict = {}
    week_dict = week_dict.fromkeys(week,0)

    month = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    month_dict = {}
    month_dict = month_dict.fromkeys(month,0)

    hour = ['{:0>2d}'.format(i) for i in range(24)]
    hour_dict = {}
    hour_dict = hour_dict.fromkeys(hour,0)
    emotionlist=tuple(emotionlist)
    timelist=tuple(timelist)
    #print(emotionlist)

    if time == 'hour':
        hour_value = [0 for i in range(24)]
        for i in range(24):
            for emo in emotionlist:
                if timelist[emotionlist.index(emo)][3]==str(i):
                    hour_value[i]+=emo[emotion-1]
        plt.plot(hour, hour_value, 'o-', color='y', label='hour_{}'.format(emotion))
        plt.xlabel("hour")  # 横坐标名字
        plt.ylabel("degree")  # 纵坐标名字
        plt.legend(loc="best")  # 图例
        for a, b in zip(hour, hour_value):
            plt.text(a, b + 1, b, ha='center', va='bottom', fontsize=10)

    elif time == 'week':
        week_value = [0 for i in range(7)]
        for i in range(7):
            for emo in emotionlist:
                if timelist[emotionlist.index(emo)][0] == str(i):
                    week_value[i] += emo[emotion - 1]
        plt.plot(week,week_value,'o-',color='r',label='week_{}'.format(emotion))
        plt.xlabel("week")#横坐标名字
        plt.ylabel("degree")#纵坐标名字
        plt.legend(loc = "best")#图例
        for a,b in zip(week,week_value):
            plt.text(a,b+1,b,ha = 'center',va = 'bottom',fontsize=10)
        #print(week_dict)

    elif time == 'month':
        month_value = [0 for i in range(12)]
        for i in range(12):
            for emo in emotionlist:
                if timelist[emotionlist.index(emo)][1] == str(i):
                    month_value[i] += emo[emotion - 1]
        plt.plot(month,month_value,'o-',color='b',label='month_{}'.format(emotion))
        plt.xlabel("month")#横坐标名字
        plt.ylabel("degree")#纵坐标名字
        plt.legend(loc = "best")#图例
        for a,b in zip(month,month_value):
            plt.text(a,b+1,b,ha = 'center',va = 'bottom',fontsize=10)
        #print(month_dict)
    
    else:
        print('enter error!')

    plt.savefig('{}_{}.png'.format(time,emotion),dpi=800)
    plt.show()

def distribution(emotion,location,k,r):
    emo = {'sadness':0,'joy':0,'fear':0,'disgust':0,'anger':0}
    center = location[k]
    #print(center)
    for i in range(len(location)):
        if location[i]!=[]:
            if ((center[0]-location[i][0])**2 + (center[1]-location[i][1])**2) <= r**2:
                for t in range(5):
                    emo[list(emo.keys())[t]] +=emotion[i][t]
    plt.figure(figsize=(6,9)) #调节图形大小
    labels = ['sadness','joy','fear','disgust','anger'] #定义标签
    sizes = []
    for emo in emo.values():
        sizes.append(emo)
    if sum(sizes)==0:
        print('No message in the area!')
    colors = ['red','yellow','green','blue','pink'] #每块颜色定义
    explode = (0,0,0,0,0) #将某一块分割出来，值越大分割出的间隙越大
    plt.pie(sizes,explode=explode,labels=labels,colors=colors,
            autopct = '%3.2f%%', #数值保留固定小数位
            shadow = False, #无阴影设置
            startangle =90, #逆时针起始角度设置
            pctdistance = 0.6) #数值距圆心半径倍数距离
    #patches饼图的返回值，texts1饼图外label的文本，texts2饼图内部的文本
    # x，y轴刻度设置一致，保证饼图为圆形
    plt.axis('equal')
    plt.savefig('pie.png',dpi=800)
    plt.show()


def main():
    weibo="D:\.1文件夹\学习文件\大三上\现代程序设计技术\第三周9.16\weibo.txt\weibo.txt"
    content = readtxt(weibo)[1:]

    wk_dir='D:\.1文件夹\学习文件\大三上\现代程序设计技术\第三周9.16\Anger makes fake news viral online-data&code\data\emotion_lexicon'
    anger_dir=os.path.join(wk_dir,"anger.txt")
    disgust_dir=os.path.join(wk_dir,"disgust.txt")
    fear_dir=os.path.join(wk_dir,"fear.txt")
    joy_dir=os.path.join(wk_dir,"joy.txt")
    sadness_dir=os.path.join(wk_dir,"sadness.txt")
    anger=readtxt(anger_dir)
    disgust = readtxt(disgust_dir)
    fear = readtxt(fear_dir)
    joy = readtxt(joy_dir)
    sadness = readtxt(sadness_dir)

    jieba.load_userdict(anger_dir)
    jieba.load_userdict(disgust_dir)
    jieba.load_userdict(fear_dir)
    jieba.load_userdict(joy_dir)
    jieba.load_userdict(sadness_dir)

    stopwords=getstopwords()
    # 坐标放到loc中
    loc = [[] for i in range(1000)]
    # 清洗后的文本数据放到tex中
    tex = [[] for i in range(10001)]
    #时间存放
    timelist = [[[] for i in range(4)]for i in range(10001)]

    time=[[]for i in range(10001)]
    #分词结果
    wordlist = [[] for i in range(10001)]
    emotion = [[0,0,0,0,0] for i in range(10001)]
    #情绪向量，五维分别表示生气、恶心、害怕、高兴、悲伤
    singlemotion=[0]*10001
    i = 0
    for con in content[1:1000]:

        tex[i] = textprocess(con)
        loc[i] = locationget(con)
        loc[i] = re.sub(",",' ',loc[i])
        loc[i] = loc[i].split()
        loc[i][0] = float(''.join(loc[i][0][1:]))
        loc[i][1] = float(''.join(loc[i][1][:-1]))
        #print(loc[i])
        time[i]=tex[i][-26:-9]
        timelist[i][0] = time[i][1:4]
        timelist[i][1] = time[i][4:7]
        timelist[i][2] = time[i][7:9]
        timelist[i][3] = time[i][9:11]

        tim = re.compile(r'(Fri).*')
        tex[i] = re.sub(r"(\d+).0", "", tex[i])
        tex[i] = re.sub(tim, "", tex[i])
        # 除去时间
        tex[i] = re.sub(r"\s+", " ", tex[i])
        # 除去空格

        wordlist[i]=wordcut.wordcut(tex[i],stopwords)
        for word in wordlist[i]:
            if word in anger:
                emotion[i][0] += 1
            if word in disgust:
                emotion[i][1] += 1
            if word in fear:
                emotion[i][2] += 1
            if word in joy:
                emotion[i][3] += 1
            if word in sadness:
                emotion[i][4] += 1
        #归一化
        maxn=max(emotion[i])
        minn=min(emotion[i])
        sign=1
        if maxn!=0:
            for j in range(5):
                emotion[i][j]=(emotion[i][j]-minn)/maxn
                if emotion[i][j] == maxn:
                    singlemotion[i]=j+1
                    if sign==0:
                        singlemotion[i]=0
                    sign=0
        i+=1

    #plotime(1, 'hour', emotion, timelist)
    #distribution(emotion, loc, k=100, r=0.5)
    #12345分别表示生气、恶心、害怕、高兴、悲伤


if __name__ == '__main__':
    main()