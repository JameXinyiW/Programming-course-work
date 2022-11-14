import numpy as np
import matplotlib.pyplot as plt

def random_walk(mu,x,sigma,n):
    i = 0
    while i<n:
        yield x   #暂停并保存当前信息，下一次执行时从当前位置继续运行
        w = np.random.normal(0,sigma,1) #构建随机游走随机量
        x = round(mu*x + w[0],3)  #下一次游走的起始点
        i+=1

n = 15
walk1 = list(random_walk(0.1,0,1,n))
walk2 = list(random_walk(0.2,1,2,n))
walk3 = list(random_walk(0.3,3,3,n))

plt.figure(figsize=(8,8))

plt.subplot(221).set_title('walk1~walk2')
plt.plot(walk1,walk2)
plt.grid(color='r', linestyle='--', linewidth=1,alpha=0.3)
plt.subplot(222).set_title('walk1~walk3')
plt.plot(walk1,walk3)
plt.grid(color='r', linestyle='--', linewidth=1,alpha=0.3)
plt.subplot(223).set_title('walk2~walk3')
plt.plot(walk2,walk3)
plt.grid(color='r', linestyle='--', linewidth=1,alpha=0.3)
plt.subplot(224).set_title('walk3~walk2')
plt.plot(walk3,walk2)
plt.grid(color='r', linestyle='--', linewidth=1,alpha=0.3)

plt.show()

for i in zip(walk1,walk2,walk3):
    print(i)
