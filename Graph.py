import pickle

class Node:
    def __init__(self, track_info, self_to_other=None, other_to_self=None):
        self.track_info = track_info

        if self_to_other is None:
            self_to_other = {}
        self.self_to_other = self_to_other
    
    def __str__(self):
        return self.track_info['name'] + ' - ' +  self.track_info['artists'][0]['name']
    
    def __eq__(self, other):
        return self.track_id == other.track_id
    
    def __ne__(self, other):
        return self.track_id != other.track_id
    
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
    
    def skipped(self, previous):
        if self != previous:
            dist = previous.self_to_other.get(self.track_id)
            if dist is None:
                previous.self_to_other[self.track_id] = 1
            else:
                previous.self_to_other[self.track_id] = dist + 1

class Graph:
    def __init__(self, nodes=None, pickle_file=None):
        if nodes is None:
            nodes = {}
        self.nodes = nodes

        if pickle_file is None:
            pickle_file = 'pickle_default_save.pkl'
        self.pickle_file = pickle_file
    
    def __repr__(self):
        return self.nodes
    
    def __str__(self):
        string = '\t\t' + ' '.join(node.track_name[:1] for node in self.nodes.values()) + '\n'

        for ynode in self.nodes.values():
            string += str(ynode.track_name[:7]) + '\t\t' + ' '.join(str(ynode.self_to_other.get(xnode.track_id)) if ynode.self_to_other.get(xnode.track_id) is not None else 'x' if ynode == xnode else '0' for xnode in self.nodes.values()) + '\n'
        
        return string
    
    @property
    def size(self):
        return len(self.nodes)
    @property
    def weighted_connections(self):
        return len([weight for nodes in self.nodes.values() for weight in nodes.self_to_other.values() if weight != 0])

    
    def save(self):
        afile = open(self.pickle_file, 'wb')
        pickle.dump(self, afile)
        afile.close()
        #print('saved graph as pickle file')
    
    def merge_node(self, new_node):
        if new_node.track_id not in self.nodes:

            # check if new node has connection to old nodes. Connect nodes if not.
            for node in self.nodes.values():
                if new_node.self_to_other.get(node.track_id) is None:
                    new_node.self_to_other[node.track_id] = 0
            
            # add the new node to the graph
            self.nodes[new_node.track_id] = new_node

            # check if old nodes have connection to new node. Connect nodes if not.
            for node in self.nodes.values():
                if node != new_node and node.self_to_other.get(new_node.track_id) is None:
                    node.self_to_other[new_node.track_id] = 0
            
            self.save_graph()
 
    def add_node(self, new_node):
        if new_node.track_id not in self.nodes:
            # add the new node to the graph
            self.nodes[new_node.track_id] = new_node

            self.save()
            print('new node added')
        else:
            print('node already present in graph')
    
    def clear_graph(self):
        self.nodes = {}
        print('graph emptied')