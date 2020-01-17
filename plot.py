import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pylab

import pickle
from Graph import Graph, Node

def open_graph(filename):
    try:
        pickle_file = open(filename, 'rb')
    except (OSError, IOError) as e:
        pickle.dump(Graph(), open(filename, "wb"))
        pickle_file = open(filename, 'rb')

    graph = pickle.load(pickle_file)

    return graph


def mine_to_template(my_graph, plot_graph):
    def id_to_name(track_id):
        return my_graph.nodes[track_id].track_name


    for node in my_graph.nodes.values():
        for edge in node.self_to_other.keys():
            G.add_edges_from([(id_to_name(node.track_id), id_to_name(edge))], weight=node.self_to_other[edge])


G = nx.DiGraph(directed=True)

FILENAME = 'mypickle(skips).pkl'

graph = open_graph(FILENAME)

mine_to_template(graph, G)


edge_labels=dict([((u,v,),d['weight']) for u,v,d in G.edges(data=True)])
node_labels = {node:node for node in G.nodes()}

pos=nx.circular_layout(G)


nx.draw_networkx_labels(G, pos, labels=node_labels)
nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels,labels=[node for node in G])
nx.draw(G,pos, node_size=500)
pylab.show()