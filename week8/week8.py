from functools import wraps
from tqdm import  tqdm
from memory_profiler import profile
from line_profiler import  LineProfiler
from pygame import mixer
import os
import pickle
import time
import sys

class Sound:
    def __init__(self):
        pass
    def __call__(self,func,*args, **kwargs):
        @wraps(func)
        def wrapper(*args,**kwargs):
            func(*args,**kwargs)
            print('程序运行结束，开始播放音乐')
            mixer.init()
            mixer.music.load("D:\pycharm code\week8\你干嘛哎哟.mp3")
            mixer.music.play()
            time.sleep(5)
            mixer.music.stop()
        return wrapper

#https://www.jianshu.com/p/5b7bb69d562c
#https://blog.csdn.net/lumping/article/details/102892624
def check_save_path(path):
    def decorate(func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            if os.path.exists(path) == False:
                print('不存在该文件夹')
                os.mkdir(path)
                print('已成功创建该文件夹')
            if os.path.exists(path) == True:
                print('已找到该文件夹')
            return func(*args,**kwargs)
        return wrapper
    return decorate

def save_print(func):
    logpath = os.path.join(os.path.dirname(__file__), 'log.txt')
    def wrapper(*args,**kwargs):
        sys.stdout = open('temp.txt','w')
        func(*args,**kwargs)
        sys.stdout.close()
        #这个部分之前的print不会输出
        with open('temp.txt','r') as temp:#临时保存打印的内容
            with open(logpath,'a+') as fp:#从temp中读取打印的内容并保存在log里
                fp.write('[{}][{}]:{}'.format(time.strftime('%Y-%m-%d %X'), func.__name__,temp.read()))
    return wrapper

class Kill:
    def __init__(self):
        pass
    #@profile()
    def timekiller(self):
        p = []
        q = []
        x = open('1.txt','w')
        for i in tqdm(range(10),ascii=True,desc='kill-time'):
            q.extend([1]*10*i)
            for j in range(1000):
                p.append(j+i)
                x.write(str(p))
                #time.sleep(0.1)
            x.write(str(q))
        x.close()
        return None



def main():
    path1 = "D:\\pycharm code\\week8\\save_txt"
    path2 = "D:\\pycharm code\\week8\\save_txt\\1.txt"
    ''' 
    @check_save_path(path1)
    def write_to_file(filename):
        x = [1, 2, 3, 4]
        f = open(filename,'w')
        f.writelines(str(x))
        print('成功写入文件')
        f.close()
    write_to_file(path2)
    '''

    '''
    @Sound()
    def func():
        print('我想听音乐，所以写了这个程序')
        print('小鸡子，漏出黑脚了吧')
    func()
    '''

    '''
    @save_print
    def get_log():
        print(' ')
        for i in range(1,10):
            print(f'print this message for {i} times')

    get_log()
    '''
    ''' 
    k = Kill()
    lp = LineProfiler()
    lp_w = lp(k.timekiller)
    lp_w()
    lp.print_stats()
    '''
if __name__ == "__main__":
    main()