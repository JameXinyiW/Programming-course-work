import pandas as pd
import numpy as np
import pickle

def init_node(edges_path,features_path):
    edge=pd.read_csv(edges_path)
    feature=pd.read_csv(features_path)
    edges=[tuple(e) for e in edge.values]
    node_feature=[tuple(f) for f in feature.values]
    #nod=dict(zip(tuple([i for i in range(len(node_feature))]),node_feature))

    keylis=['views','mature','life_time','created',
            'updated','numeric_id','dead','language','affiliate']
    nod={}
    for i in range(len(node_feature)):
        x=dict.fromkeys(keylis)
        for j in range(len(keylis)):
            x[keylis[j]]=node_feature[i][j]
        nod[i]=x
    #numeric_id_1\numeric_id_2
    #views\mature\lifetime\created\updated\numericid\deadaccount\language\affiliate
    return nod,edges
#返回一个字典，和用元组存储的边信息，一个元组表示有相连的两条边
def print_node(all_nodes,node_id):
    lis=all_nodes[node_id]
    print(lis)
    lis=list(lis.values())

    #print(lis)
    print('node id '+str(node_id)+':\nviews:{0}\nmature:{1}\nlifetime:{2}\ncreated:{3}\nupdated:{4}'
                  '\nnumeric id:{5}\ndead account:{6}\nlanguage:{7}\naffiliate:{8}'.
          format(lis[0],lis[1],lis[2],lis[3],lis[4],lis[5],lis[6],lis[7],lis[8]))
    return
#输入节点信息字典和节点编号，按一定格式输出节点信息

def save_n(n):
    with open('test.txt', 'wb') as f:
        pickle.dump(n, f)
    print('写入成功')

def load_n(filename):
    with open(filename, 'wb') as f:
        n=pickle.load(f)
    return n

