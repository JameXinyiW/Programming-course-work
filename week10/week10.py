#Xinyi Wang Beihang SEM
import numpy as np
import pandas as pd
from wordcloud import WordCloud
from PIL import Image
from week2 import wordcut
from week6 import wk6
from celluloid import Camera
from sklearn import datasets
#from sklearn.manifold import TSNE
from openTSNE import TSNE
import librosa
import librosa.display
import glob
import tsneutil
import numpy
import matplotlib.pyplot as plt
import abc
import csv
import os
import imageio

class Plotter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def plot(self,*args,**kwargs):
        pass

class Point:
    '''
    在定义绘图类之前，先对数据点进行定义
    '''
    def __init__(self,x,y):
        l= []
        for i in range(len(x)):
            #这里加入了一个长度识别，因为散点图x,y长度应当是相等的
            if len(y)!=len(x):
                print("Unmatched data!")
                exit()
            l.append((x[i],y[i]))

        self.lis = l

class PointPlotter(Plotter):
    def __init__(self,data):
        self._data = data

    def plot(self):
        #实现散点图和坐标标注
        for x,y in self._data:
            plt.scatter(x,y)
            plt.text(x+0.1,y+0.1,(x,y),color='b')
        plt.show()

def data_read(filename):
    #用于读取数据，如果存在空缺值，使用到目前为止的平均值作为替代，返回一个数组
    with open(filename,newline='',encoding='UTF-8') as f:
        r = csv.reader(f)
        f_price=[]
        sum = 0
        count = 0
        for c in r:
            if c[1] != '':
                sum +=int(c[1])
                count+=1
                ave=int(sum/count)
            if c[1] == '':
                c[1] = ave
            f_price.append(int(c[1]))
    return f_price[0:243]

class ArrayPlotter(Plotter):
    '''
    这里的可视化只适用于n*2的数据
    '''
    def __init__(self,data):
        self._data = data

    def plot(self):
        x = self._data[0]
        y = self._data[1]
        for i in range(len(x)):
            plt.scatter(x[i],y[i])
        plt.show()

class TextPlotter(Plotter):
    '''
    文本数据可视化，这里用到了第二周里创建的wordcut函数，用于分词
    '''
    def __init__(self, data):
        self._data = data

    def plot(self):
        s = [] #停用词设置为空
        word_lis = wordcut.wordcut(self._data, s)
        words= '/'.join(word_lis)
        w = WordCloud(max_font_size=100,
                      background_color='white',
                      scale=3, font_path='C:/Windows/SIMLI.TTF')
        w.generate(words)  # 生成词云
        w.to_file('wordcloud.png')

class ImagePlotter(Plotter):
    '''
    图像型数据绘制，这里可以用第六周的图片处理类加以修饰
    '''
    def __init__(self,data):
        self._data = data

    def plot(self,row=3,column=4):
        for num in range(0,len(self._data),row*column):
            print(num)
            for each in range(1,row*column+1): #控制每张子图展示图片数量
                if num+each-1<len(self._data):
                    img = self._data[num+each-1]
                    img = Image.open(img)
                    img = img.resize((640,480))
                    #这里引用了wk6里的Edgex处理图片
                    im = wk6.Edgex(img)
                    im_processed = im.filter()

                    plt.subplot(row,column,each)
                    plt.axis('off')
                    plt.imshow(im_processed)#处理过后的图
                    #plt.imshow(img) #原图
            plt.show()
class GifPlotter(Plotter):
    '''
    图像型数据绘制，使用了celluloid中的Camera
    '''
    def __init__(self,data):
        self._data = data

    def plot(self):
        fig = plt.figure()
        camera = Camera(fig)
        for i in range(10):
            img = self._data[i]
            img = Image.open(img)
            img = img.resize((1000,1000))
            plt.imshow(img)
            camera.snap()
            plt.axis('off')#取消坐标轴，让gif看起来更好看
        animation = camera.animate()
        animation.save('pics.gif')

class ArrayPlotterTSNE(Plotter):
    '''
    PCA之前做过了，所以这里学习TSNE
    https://blog.csdn.net/wenqiwenqi123/article/details/122260663
    '''
    def __init__(self,data):
        self._data = data

    def plot(self):
        x = self._data
        iris = datasets.load_iris()
        y = iris["target"]
        #print(x)
        #print(y)
        #x, y = iris["data"], iris["target"]

        tsne = TSNE(
            perplexity=50,
            n_iter=500,
            metric="euclidean",
            # callbacks=ErrorLogger(),
            n_jobs=8,
            random_state=42,
        )
        embedding = tsne.fit(x)
        tsneutil.plot(embedding, y, colors=tsneutil.MOUSE_10X_COLORS)

class AudioPlotter(Plotter):   #音频型数据绘制
    def __init__(self,data):
        self._data = data

    def plot(self):
        x , sr = librosa.load(self._data)
        librosa.display.waveshow(x, sr=sr)
        plt.savefig('audio.png')
        plt.show()


def main():
    #数据点类型数据
    x=[1,2,3,4,5,6]
    y=[1.1,3,2,5,6,3]
    p0 = Point(x,y)
    p = PointPlotter(p0.lis)
    #PointPlotter.plot(p)

    #多维数组类型数据
    #这里正好使用之前收集的豆1和甲醇期货价格数据，顺便写了个读取文件函数
    array_unprocessed=[]
    f=['dou1.csv','jc.csv']

    for file in f:
        array_unprocessed.append(np.array(data_read(file)))
    array = array_unprocessed
    a = ArrayPlotter(array)
    #ArrayPlotter.plot(a)

    #文本型数据绘制词云图，随便从网上复制粘贴了一段话
    t ='程序设计语言是计算机能够理解和识别用户操作意图的一种交互体系' \
       '它按照特定规则组织计算机指令使计算机能够自动进行各种运算处理。花半开最美，情留白最浓，' \
       '懂得给生命留白，亦是一种生活的智慧。淡泊以明志，宁静以致远，懂得给心灵留白，方能在纷杂繁琐的世界，' \
       '淡看得失，宠辱不惊，去意无留；懂得给感情留白，方能持久生香，留有余地，相互欣赏，拥有默契；懂得给生活留白，' \
       '揽一份诗意，留一份淡定，多一份睿智，生命方能如诗如画。人心，远近相安，时光，浓淡相宜。有些风景要远观，' \
       '才能美好；有些人情要淡然，才会久远，人生平淡更持久，留白方能生远，莲养心中，随遇而安，' \
       '生命的最美不过是懂得的距离。'
    text = TextPlotter(t)
    #text.plot()

    #图片型数据绘制词云图，用的自己珍藏的猫猫图
    #os导入文件,glob搜索文件
    path = 'D:\\.1文件夹\\我的宠物\\jyt\\'
    photos = glob.glob(os.path.join(path + '*.jpg'))
    im = ImagePlotter(photos)
    #im.plot()
    #图片序列可视化，输出gif动态图，继续使用猫猫图
    im_gif = GifPlotter(photos)
    im_gif.plot()

    #TSNE 对高维数据进行可视化，这里使用4*243的数据，同样为期货价格
    f1 = ['douyou.csv', 'dou1.csv', 'jc.csv', 'yec.csv']
    array_unprocessed2=[]
    for file in f1:
        array_unprocessed2.append(data_read(file)[0:150])

    array2 = pd.DataFrame(array_unprocessed2)
    array2= pd.DataFrame(array2.values.T)

    #print(array2)

    a2 = ArrayPlotterTSNE(array2)
    #a2.plot()

    #librosa处理音频数据
    audio_path = '你干嘛哎哟.wav'
    au = AudioPlotter(audio_path)
    #au.plot()



if __name__ =="__main__":
    main()
