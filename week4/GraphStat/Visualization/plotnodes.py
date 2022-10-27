import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def plot_nodes_attr(G,attr):
    attribute = nx.get_node_attributes(G,attr).values()
    #print(attribute)
    #print(list(attribute))
    #print(G.nodes.data)
    plt.hist(list(attribute),bins = 50,log = True,)
    '''plt.bar(len(attribute),attribute)
    plt.savefig('bar.jpg')'''
    #plt.savefig('hist_life_time.jpg')
    plt.savefig('hist_life_time.svg',dpi=600,format='svg')
    plt.savefig('hist_life_time.eps', dpi=600)