import pandas as pd
from GraphStat.Networkbuilder import node,graph,stat
import networkx as nx
import matplotlib.pyplot as plt
from GraphStat.Visualization import plotgraph,plotnodes

def main():
    nodes, edges =node.init_node("large_twitch_edges.csv", "large_twitch_features.csv")
    mat,G = graph.graph_build(nodes,edges)
    #print(nodes)
    #node.print_node(nodes,2)
    num_nodes, num_edges, ave_degree, per = stat.statist(mat, nodes, 2)

    '''print('number of edges:', num_edges, '\nnumber of nodes:', num_nodes, "\naverage degree:{:.2f}"
          .format(ave_degree))
    print("English connected percentage:{:.2f}%".format(per))'''
    plotgraph.plot_degree(G)
    plotnodes.plot_nodes_attr(G,'life_time')

if __name__ == '__main__':
    main()