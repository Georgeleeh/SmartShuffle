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
        print(self)
        print(str(self.distances))
        print(previous)
        print(str(previous.distances))
        print()
        dist = self.distances[previous.track_id]
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
        string = ''

        for ynode in self.nodes.values():
            string += str(ynode.track_id) + '\t' + ' '.join(str(ynode.distances[xnode.track_id]) for xnode in self.nodes.values()) + '\n'
        
        return string
    
    def print_edges(self):
        for node in self.nodes.values():
            print(str(node1) + '-'*100)
            for edge in node.distances.keys():
                print(edge)
    
    def health_check(self):

        for node1 in self.nodes.values():
            for node2 in self.nodes.values():
                if node1.distances[node2.track_id] != node2.distances[node1.track_id]:
                    print(f'distances between {node1} and {node2} are asymmetrical. Please check this.')

                if node2.track_id not in node1.distances:
                    print(f'node {node1} was missing distance to {node2}. Now fixed.')
                    node1.distances[node2.track_id] = 0

 
    def add_node(self, new_node):
        if new_node.track_id not in self.nodes:

            new_node.distances = {node.track_id:0 for node in self.nodes.values()}

            self.nodes[new_node.track_id] = new_node

            # add new node to distances of all existing nodes, with distance 0
            for node in self.nodes.values():
                node.distances[new_node.track_id] = 0

            print('new node added')
            self.health_check()
    
    def clear_graph(self):
        self.nodes = {}
        print('graph emptied')