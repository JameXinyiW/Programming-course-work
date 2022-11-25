import time
import json
import matplotlib.pyplot as plt
from week2 import wordcut
from multiprocessing import Process,Manager

def get_data(filename):
    #data用来提取文档数据，汇总到列表中
    lis = []
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for txt in data:
        lis.append(dict(txt)['content'])
    return lis
    #所有文档汇总到列表中并返回

def Map(content,word_lis,stopwords):
    #Map函数进行分词并存储到列表
    for c in content:
        #这里使用了之前创建的分词函数，需要传入段落和停用词，返回分词列表
        text_lis = wordcut.wordcut(c,stopwords)
        for i in text_lis:
            word_lis.append(i)


def Reduce(lis):
    #Reduce函数将结果汇总到字典中
    dic = {}
    for k in lis:
        dic[k] = dic.get(k,0)+1
    dic_order=sorted(dic.items(),key=lambda x:x[1],reverse=True)
    #字典降序排序

    with open('results.txt','w',encoding='utf-8') as file:
        for k,v in dic_order:
            file.write(k+':'+str(v)+'\n')
            #将结果写入文件

if __name__=='__main__':
    stopwords = [line.strip() for line in open('stopwords_list.txt',encoding='UTF-8').readlines()]
    filename = 'sohu_data.json'
    d = get_data(filename)
    data_part = d[:10000]

    time_lis=[]
    process_lis = [1, 2, 4, 5, 8, 10, 20, 40, 100]
    datanum_lis = [int(10000 / x) for x in process_lis]
    #print(datanum_lis)
    p_lis=[]#存储Manager类的列表
    p1_lis=['p'+str(i) for i in range(9)]#储存Process的列表
    print(p1_lis)
    for j in range(9):
        start_time = time.perf_counter()
        plist = []
        print(p_lis)
        p_lis.append(Manager())
        list1 = p_lis[j].list([])
        for i in range(j):   #创建进程
            num=datanum_lis[i]
            print(num)
            p1 = Process(target=Map,args=(data_part[num*i:num*(i+1)],list1,stopwords))
            plist.append(p1)
        for p in plist:
            p.start()  #启动进程
        for p in plist:
            p.join()
        Reduce(list1)
        print('第%d次总运行时间：%.2f' % (j+1,(time.perf_counter() - start_time)))
        time_lis.append(round(time.perf_counter() - start_time, 2))
        print('第%d次运行完成时间：%s' % (j+1,(time.strftime('%Y-%m-%d %H:%M:%S'))))
    print(time_lis)

    plt.plot(process_lis,time_lis, lw=4, ls='-', c='b', alpha=0.1)
    for i in range(9):
        plt.text(process_lis[i]+2, time_lis[i]+1, (process_lis[i], time_lis[i]),
                 fontsize=12, style="italic", weight="light", verticalalignment='center',
                 horizontalalignment='right')
    plt.xlabel('number of process')
    plt.ylabel('time of process')
    plt.show()

