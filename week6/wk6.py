from PIL import ImageFilter,Image
import os
import  matplotlib.pyplot as plt

class Filter:
    '''
    基类，包含两个数据属性，一个方法属性
    '''
    def __init__(self,image,p):
        Filter.image = image
        Filter.p = p
    def filter(self):
        pass

class Edgex(Filter):
    def __init__(self,image,p):
        Filter.__init__(self,image,p)

    def filter(self):
        self.im = self.image.filter(ImageFilter.CONTOUR)#or CONTOUR or EMBOSS
        return self.im

class Sharpen(Filter):
    def __init__(self,image,p):
        Filter.__init__(self,image,p)

    def filter(self):
        self.im = self.image.filter(ImageFilter.SHARPEN)
        return self.im

class Blur(Filter):
    def __init__(self,image,p):
        Filter.__init__(self,image,p)
        self.r = self.p[0]

    def filter(self):
        self.im = self.image.filter(ImageFilter.BoxBlur(self.r))
        return self.im

class Size(Filter):
    def __init__(self,image,p):
        Filter.__init__(self,image,p)
        self.size = self.p[0]

    def filter(self):
        self.im=self.image.resize(self.size)
        return self.im

class Imageshop:
    def __init__(self,type,pic_path):
        self.type = type #图片的类型 jpg,png
        self.pic_path= pic_path #图片路径
        self.im_save = [] #储存图片实例
        self.pic_save = []  #储存处理后的图片实例

    def load_images(self):
        #使用数据类型和文件路径
        for root,dirs,files in os.walk(self.pic_path):
            for file in files:
                if file.endswith(self.type):
                    self.im_save.append(Image.open(self.pic_path+'\\'+file))

    def __batch__ps(self,filter):
        #先检测是否是派生类
        self.p=[]
        if issubclass(filter,Filter):
            for im in self.im_save:
                s = filter(image=im,p=self.p)
                self.pic_save.append(s.filter())
            return self.pic_save
        else:
            print('类型错误')
        return

    def batch_ps(self,methods):
        'methods 为一个元组列表，每个元组分别表示操作的方式和参数'
        for m in methods:
            f = m[0]
            para = m[1]
            self.p = para
            self.pic_save = self.__batch__ps(f)
        return

    def display(self,col,row,size):
        #设置了行和列的数目以及画布的大小
        plt.figure(figsize=size)
        for i in range(0,len(self.pic_save)):
            plt.subplot(col,row,i+1)
            plt.imshow(self.pic_save[i])
            plt.axis('off')

        plt.show()

    def save(self,save_path,save_type):
        #参数为保存的路径和保存的文件类型
        i = 0
        for im in self.pic_save:
            im.save(save_path+str(i+1)+save_type)
            i+=1

class TestImageshop(Imageshop):
    def __init__(self,type,pic_path,methods,col,row,size,save_path,save_type):
        super().__init__(type=type,pic_path=pic_path)
        self.methods = methods
        self.col = col
        self.row = row
        self.size = size
        self.save_path = save_path
        self.save_type = save_type

    def tes(self):
        super().load_images()
        super().batch_ps(self.methods)
        super().display(self.col,self.row,self.size)
        super().save(self.save_path,self.save_type)

def main():
    '''im = Image.open('pic.jpg','r')
    p1=[1,2,3]
    F = Edgex(image=im,p=p1).filter()
    #F = Sharpen(image=im,p=p1).filter()
    #F = Size(image=im,p=p1).filter()
    #F = Blur(image=im,p=p1).filter()
    F.show()
    F.save('1.jpg')'''

    pic_path = 'D:\pycharm code\week6\pic2'
    type = '.jpg'
    methods=[(Edgex,[1,1,1])]
    col = 2
    row = 2
    size = (10,10)
    save_path = 'D:\pycharm code\week6\pic2_CONTOUR'
    save_type = '.png'
    t = TestImageshop(type,pic_path,methods,col,row,size,save_path,save_type)
    t.tes()

if __name__ == '__main__':
    main()