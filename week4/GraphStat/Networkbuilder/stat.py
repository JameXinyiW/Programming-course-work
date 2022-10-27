
#import graph

def statist(mat,node1,id):
    num_nodes=len(mat)
    num_edges=sum(len(x) for x in mat)
    ave_degree=num_edges/num_nodes
    node_connect=mat[id]
    lan=[]
    for n in node_connect:
        lan.append(node1[n]['language'])
    count=0
    for x in lan:
        if x == 'EN':
            count+=1
    per=100*count/len(lan)

    #返回关联者中，使用英语人数占比
    return num_nodes,num_edges,ave_degree,per

'''def main():
    node, edges = node.init_node("large_twitch_edges.csv", "large_twitch_features.csv")
    mat = graph.graph_build(node, edges)
    num_nodes, num_edges, ave_degree, per = statist(mat, node, 2)
    print('number of edges:', num_edges, '\nnumber of nodes:', num_nodes, "\naverage degree:{:.2f}"
          .format(ave_degree))
    print("English connected percentage:{:.2f}%".format(per))

if __name__ == '__main__':
    main()'''
