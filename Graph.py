import pickle

class Node:
    def __init__(self, track_info, distances=None):
        self.track_info = track_info

        if distances is None:
            distances = {}
        self.distances = distances
    
    def __str__(self):
        return self.track_info['name'] + ' - ' +  self.track_info['artists'][0]['name']
    
    @property
    def track_id(self):
        return self.track_info['id']
    
    @property
    def track_name(self):
        return self.track_info['name']
    
    @property
    def track_artist(self):
        return self.track_info['artists'][0]['name']
    
    @property
    def track_duration_millis(self):
        return self.track_info['duration_ms']
    
    def listened(self, previous):
        dist = self.distances.get(previous.track_id)
        if dist is None: dist = 0
        self.distances[previous.track_id] = dist + 1
        previous.distances[self.track_id] = dist + 1

class Graph:
    def __init__(self, nodes=None):
        if nodes is None:
            nodes = {}
        self.nodes = nodes
    
    def __repr__(self):
        return self.nodes
    
    def __str__(self):
        string = '\t\t' + ' '.join(node.track_name[:1] for node in self.nodes.values()) + '\n'

        for ynode in self.nodes.values():
            string += str(ynode.track_name[:5]) + '\t\t' + ' '.join(str(ynode.distances[xnode.track_id]) for xnode in self.nodes.values()) + '\n'
        
        return string
    
    def print_edges(self):
        for node in self.nodes.values():
            print(str(node.track_name) + '-'*100)
            for key in node.distances.keys():
                print(key, node.distances[key])
    
    def health_check(self):
        flag = True

        for node1 in self.nodes.values():
            for node2 in self.nodes.values():

                if node1.distances[node2.track_id] != node2.distances[node1.track_id]:
                    print(f'WARNING: distances between {node1} and {node2} are asymmetrical.')
                    flag=False

                if node2.track_id not in node1.distances:
                    print(f'WARNING: node {node1} is missing distance to {node2}.')
                    flag=False
        
        if flag: self.save_graph()
    
    def save_graph(self, filename='pickle.pkl'):
        afile = open(filename, 'wb')
        pickle.dump(self, afile)
        afile.close()
        #print('saved graph as pickle file')

 
    def add_node(self, new_node):
        if new_node.track_id not in self.nodes:

            new_node.distances = {node.track_id:0 for node in self.nodes.values()}

            self.nodes[new_node.track_id] = new_node

            # add new node to distances of all existing nodes, with distance 0
            for node in self.nodes.values():
                node.distances[new_node.track_id] = 0

            self.health_check()
            print('new node added')
        else:
            print('node already present in graph')
    
    def clear_graph(self):
        self.nodes = {}
        print('graph emptied')