import numpy as np
from PIL import Image
from pathlib import Path
from PIL import ImageFile
from memory_profiler import profile
import time
ImageFile.LOAD_TRUNCATED_IMAGES = True

class FaceDataset:
    def __init__(self, path, start=0, step=1, max=1000):
        self.path = path
        self.start = start
        self.step = step
        self.max = max

    def load_images(self):
        p = Path(self.path)
        images = p.rglob('*.*')
        images = [x for x in images if str(x)[-4:] =='.jpg']
        self.image_list = images

    def transform(self, image):
        img = Image.open(image)
        img = np.array(img)
        self.img = img
        return img

    def __iter__(self):
        return self

    def __next__(self):
        if self.start <= self.max:
            x = FaceDataset.transform(self, self.image_list[self.start])
            self.start += self.step
            return x
        else:
            raise StopIteration('超出阈值:{}'.format(self.max))
@profile

def main():
    t1 = time.perf_counter()
    path = 'D:\.1文件夹\学习文件\大三上\现代程序设计技术\第九周 10.28\originalPics'
    d = FaceDataset(path)
    d.load_images()
    i=1
    for imgaes in d:
        print(imgaes)
        i+=1
        if i>10:
            break
    t2 = time.perf_counter()
    print('Time:%.2f seconds' % (t2-t1))

main()
