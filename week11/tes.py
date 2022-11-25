'''import json

with open('sohu_data.json','r',encoding='utf-8') as f:
    data = json.load(f)

print(dict(data[1])['content'])'''

import matplotlib.pyplot as plt
x=[1,2,3,4,5]
y=[4,5,6,7,8]

plt.plot(x,y)
for i in range(5):
    plt.text(x[i], y[i], (x[i],y[i]),fontsize=12, style="italic", weight="light", verticalalignment='center',
            horizontalalignment='right')

plt.show()
