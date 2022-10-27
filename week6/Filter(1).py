from PIL import ImageFilter,Image
import os
import matplotlib.pyplot as plt

class Filter:
    def __init__(self,image,p):
        self.image=image
        self.p=p
    def filter(self):
        pass
#边缘提取
class Edge(Filter):
    def __init__(self,image,p):
        Filter.__init__(self,image,p)

    def filter(self):
        self.image = self.image.filter(ImageFilter.CONTOUR)
        return self.image
#锐化
class Sharpen(Filter):
    def __init__(self,image,p):
        Filter.__init__(image,p)

    def filter(self):
        self.image=self.image.filter(ImageFilter.SHARPEN)
        return self.image

#模糊,模糊半径由参数输入
class Vague(Filter):
    def __init__(self,image,parameter):
        Filter.__init__(image,parameter)

    def filter(self):
        self.image=self.image.filter(ImageFilter.BoxBlur(self.parameter))
        return self.image

#大小调整，调整大小由参数按照元组输入
class Sizechange(Filter):
    def __init__(self,image,parameter):
        Filter.__init__(image,parameter)

    def filter(self):
        self.image=self.image.resize(self.parameter,Image.ANTIALIAS)
        return self.image

#批量处理图片
class Imageshop:
    def __init__(self,type,path):
        self.type = type #图片的类型 jpg,png
        self.path= path #图片路径
        self.image_save = [] #储存图片实例
        self.image2_save = []  #储存处理后的图片实例

    #加载文件或目录中的所有特定格式图片，使用数据类型和文件路径
    def load_images(self):
        for root,dirs,files in os.walk(self.path):
            for file in files:
                #只对指定数据类型进行处理
                if file.endswith(self.type):
                    self.image_save.append(Image.open(self.path+'\\'+file))
    
    #利用某个过滤器对所有图片进行处理
    def __batch__ps(self,filter_type):
        #先检测是否是派生类
        self.p=None
        if issubclass(filter_type,Filter):
            #处理后存储至列表，之后返回列表
            for image in self.image_save:
                output=filter_type(image,self.p)
                self.image2_save.append(output.filter())
            return self.image2_save
        else:
            print('没有对应的滤波器\n')

    #批量处理图片的对外公开方法
    def batch_ps(self,solution):
        #operation为一个元组列表，每个元组分别表示操作的方式和参数
        for i in solution:
            filter_type=i[0]
            p=i[1]
            self.p=p
            self.image2_save= self.__batch__ps(filter_type)

    #处理效果显示，设置了行列以及每张图片的大小，以及最多显示多少张
    def display(self,col,row,size):
        plt.figure(figsize=size)
        for i in range(0,len(self.image2_save)):
            plt.subplot(col,row,i+1)
            plt.imshow(self.image2_save[i])
            plt.axis('off')
        plt.show()

        # 对处理图片进行存储，参数为保存的路径和保存的文件类型
        def save(self, save_path, save_type):
            i = 0
            for image in self.image2_save:
                image.save(save_path + str(i + 1) + save_type)
                i += 1

# 进行测试，指定图片路径，指定要进行的操作
class TestImageshop(Imageshop):
    def __init__(self, type, path, solution, col, row, size, save_path, save_type):
        super().__init__(type=type, path=path)
        self.solution = solution
        self.col = col
        self.row = row
        self.size = size
        self.save_path = save_path
        self.save_type = save_type

    # 测试函数
    def tes(self):
        super().load_images()
        super().batch_ps(self.solution)
        super().display(self.col, self.row, self.size)
        super().save(self.save_path, self.save_type)
def main():
    pic_path = 'D:\pycharm code\week6\pic2'
    type = '.jpg'
    methods = [(Edge, [1, 1, 1])]
    col = 2
    row = 2
    size = (10, 10)
    save_path = 'D:\pycharm code\week6\pic2_CONTOUR'
    save_type = '.png'
    t = TestImageshop(type, pic_path, methods, col, row, size, save_path, save_type)
    t.tes()

if __name__ == '__main__':
    main()