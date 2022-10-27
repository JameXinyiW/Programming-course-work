import datetime
import random
from scipy import spatial
import jieba
import pandas
import math
import jieba.analyse
import numpy as np
import wordcloud
import progressbar
import time
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
import logging

time0=datetime.datetime.now()
#得到所有的特征词allwords
def wordget(danmu,stopwords,allwords):
    wordcutlist=wordcut(danmu,stopwords)
    for word in wordcutlist:
        if word in allwords.keys():
            allwords[word]+=1
        if word not in allwords.keys():
            allwords[word]=1
    return 0

#返回该条弹幕对应的分词结果wordcutlist
def wordcut(danmu,stopwords):
    pre_wordcutlist = jieba.lcut(danmu)
    wordcutlist = []
    for preword in pre_wordcutlist:
        if preword not in stopwords and preword!=' ':
            wordcutlist.append(preword)
    return wordcutlist

def EucliDist(a,b):
    return math.sqrt(sum([(a - b)**2 for (a,b) in zip(a,b)]))

filename='danmuku.csv'
encoding='UTF-8'
f=open(filename,encoding=encoding)
names=['content','second','sent']
data=pandas.read_csv(f,names=names, low_memory=False)
content=list(data['content'])
stopwords=[line.strip() for line in open('stopwords_list.txt',encoding=encoding).readlines()]
allwords={}

#for i in progressbar.progressbar(range(100)):
for danmu in content[1:10000]:
    wordget(danmu, stopwords, allwords)

time1=datetime.datetime.now()
print('\n已经得到所有特征词',time1.strftime('%H:%M:%S'))
print('用时',(time1-time0).seconds,'秒')
for word in list(allwords.keys()):
    if allwords[word]<5:
        del allwords[word]
        continue

#print(allwords)
#表示第几条弹幕
#for i in progressbar.progressbar(range(1)):
j=0
'''
#这个循环生成向量表示的矩阵，应该是2790000*7626大小
#matrix=[0]*len(content)
matrix=[0]*10000
for danmu in content[1:10000]:
    result=wordcut(danmu,stopwords)
    vect=[0]*len(allwords)
    i=0
    for word in allwords:
        if word in result:
            vect[i]=1
            i+=1
    matrix[j]=vect
    j+=1
'''
distance=[0]*100
#欧式距离的问题：如果两条弹幕都不含特征词，那么都是0向量，距离也就是0
#余弦相似度：如果都是0向量，会返回nan,比较好
k=0
'''
for i in range(100):
    #print(i)
    x=random.randint(0,10000)
    y=random.randint(0,10000)
    danmux=content[x]
    danmuy=content[y]
    vx=matrix[x]
    vy=matrix[y]
    #distance[k]=EucliDist(vx,vy)
    k+=1
    #欧式距离
    distance[i]=1 - spatial.distance.cosine(vx,vy)#余弦相似度
    #print(danmux)
    #print(wordcut(danmux, stopwords))
    #print(danmuy)
    #print(wordcut(danmuy,stopwords))
    print(distance[i])
    #print(k)

'''
'''
new_order = sorted(allwords.items(), key=lambda x: x[1],reverse=True)
new_dic = { k : v for k,v in new_order}
#print(new_dic)
words=new_dic.keys()
#print(words)

w = wordcloud.WordCloud( width=1000,font_path = "msyh.ttc",height=700)
w.generate('/'.join(words))
w.to_file("pywcloud.png")
'''

'''
#使用TF-IDF方法：
for i in range(100):
    text=content[i]
    keywords=jieba.analyse.extract_tags(text, topK=5, withWeight=False, allowPOS=())
    print('第'+str(i)+'条:\nTF-IDF：'+str(keywords)+'\n词频:'+str(wordcut(content[i],stopwords)))
'''
import codecs
'''
target = codecs.open("D:\pycharm code\week2\output.txt", 'w',encoding="utf8")
for i in range(len(content)):
    line_seq=" ".join(wordcut(content[i],stopwords))
    target.writelines(line_seq)
target.close()
'''
'''
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    # Word2Vec第一个参数代表要训练的语料
    # sg=1 表示使用Skip-Gram模型进行训练
    # size 表示特征向量的维度，默认为100。大的size需要更多的训练数据,但是效果会更好. 推荐值为几十到几百。
    # window 表示当前词与预测词在一个句子中的最大距离是多少
    # min_count 可以对字典做截断. 词频少于min_count次数的单词会被丢弃掉, 默认值为5
    # workers 表示训练的并行数
    #sample: 高频词汇的随机降采样的配置阈值，默认为1e-3，范围是(0,1e-5)


#首先打开需要训练的文本
shuju = open("D:\pycharm code\week2\output.txt", 'rb')
#通过Word2vec进行训练
model = Word2Vec(LineSentence(shuju), sg=1, window=10, min_count=1, workers=15,sample=1e-3)
#保存训练好的模型
model.save('D:\pycharm code\week2\Test.word2vec')

print('训练完成')


'''

#第二次直接加载
model=Word2Vec.load("Test.word2vec")
#查看所有词

#print(model.wv.index_to_key)
print(model.wv['蒜'])

time2=datetime.datetime.now()
print('成功',time2.strftime('%H:%M:%S'))
print('用时',(time2-time0).seconds,'秒')