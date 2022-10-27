import networkx as nx
import matplotlib.pyplot as plt

def plot_ego(G,mat,index):
    #输入网络图、邻居矩阵、需要绘制ego-network图的节点编号
    hub_ego = nx.ego_graph(G, index)
    # Draw graph
    pos = nx.spring_layout(hub_ego)
    nx.draw(hub_ego, pos, node_color='b', node_size=50, with_labels=True)
    # Draw ego as large and red
    nx.draw_networkx_nodes(hub_ego, pos, nodelist=[index], node_size=300, node_color='r', label=mat[index])
    plt.savefig('ego_graph.png')
    plt.show()

def plot_degree(G):
    degree=nx.degree_histogram(G)
    x = range(len(degree))  # 生成X轴序列，从1到最大度
    y = [z / float(sum(degree)) for z in degree]  # 将频次转化为频率
    plt.figure(figsize=(5.8, 5.2), dpi=150)
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.xlabel("Degree", size=14)  # Degree
    plt.ylabel("Frequency", size=14)  # Frequency
    plt.xticks(fontproperties='Times New Roman', size=13)
    plt.yticks(fontproperties='Times New Roman', size=13)
    plt.loglog(x, y, '.')
    plt.show()  # 显示图表