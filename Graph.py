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
        self.distances[previous.track_id] += 1
        previous.distances[self.track_id] = self.distances[previous.track_id]

        if self.distances[previous.track_id] != previous.distances[self.track_id]:
            print(f'asymettric distances detected between {self} and {previous}')


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
    
    def health_check(self):
        print('Running graph health check...')
        for node1 in self.nodes.values():
            for node2 in self.nodes.values():
                if node2.track_id not in node1.distances:
                    print(f'node {node1} was missing distance to {node2}. Now fixed.')
                    node1.distances[node2.track_id] = 0
 
    def add_node(self, new_node):
        if new_node.track_id in self.nodes:
            print('node already exists in graph')
        else:
            new_node.distances = {node.track_id:0 for node in self.nodes.values()}

            self.nodes[new_node.track_id] = new_node

            # add new node to distances of all existing nodes, with distance 0
            for node in self.nodes.values():
                node.distances[new_node.track_id] = 0

            print('new node added')
    
    def clear_graph(self):
        self.nodes = {}
        print('graph emptied')