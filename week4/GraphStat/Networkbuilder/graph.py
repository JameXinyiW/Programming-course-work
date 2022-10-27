import networkx as nx
import pickle

def graph_build(node,edges):
    size = len(node)
    mat = [()for i in range(size)]
    s = []
    j = 0
    x=edges[0][0]
    #print(x)
    for edge in edges:
        #print(edge[1])
        if edge[0] == x:
            #print(s)
            s.append(edge[1])
        else:
            mat[j] = set(s)
            j += 1
            x = edge[0]
            s = []
    '''print(mat[1])
    print(mat[16384])
    if 1 in mat[16383]:
        print('yes')'''
    #检验是否重复计算,结果是否
    #用集合存储与节点有链接的其他节点，如mat[0]表示与节点1相连接的其他所有节点的数字编号
    G=nx.Graph()
    G.add_nodes_from([i for i in range(len(mat))])
    nx.set_node_attributes(G,node)
    G.add_edges_from(edges)
    return mat,G

def save_g(G):
    with open('test.txt', 'wb') as f:
        pickle.dump(G, f)
    print('写入成功')

def load_g(filename):
    with open(filename, 'wb') as f:
        G=pickle.load(f)
    return G







