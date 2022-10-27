import os
from PIL import Image

pic_path='D:\pycharm code\week6\pic'
typ='.jpg'
i=[]
for root, dirs, files in os.walk(pic_path):
    print(root)
    print(dirs)
    print(files)
    for file in files:
        if file.endswith(typ):
           Image.open(pic_path+'\\'+file)
