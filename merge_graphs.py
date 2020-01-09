from Graph import Graph, Node

import pickle


pickle_files = ['picklepop.pkl', 'picklerweird.pkl']

graphs = [pickle.load(open(filename, 'rb')) for filename in pickle_files]


merged_graph = graphs[0]
merged_graph.pickle_file = 'merged.pkl'

print('starter')
print(merged_graph)

for new_graph in graphs[1:]:
    print('mergin')
    print(new_graph)
    for node in new_graph.nodes.values():
        merged_graph.merge_node(node)

print('out')
print(merged_graph)

merged_graph.save_graph()