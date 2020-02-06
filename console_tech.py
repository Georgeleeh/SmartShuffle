import pickle, sys, os, random
from Graph import Graph, Node

def main(graph):
    nodes = list(graph.nodes.values())
    random.shuffle(nodes)

    current = nodes[0]

    while True:
        random.shuffle(nodes)
        #for node in nodes:
        #    if current.self_to_other.get(node.track_id) is None and current != node:
        #        test = node
        #        break
        
        test = nodes[0] if nodes[0] != current else nodes[1]
        print(f'{current.track_name} - {current.track_artist}\nv\n{test.track_name} - {test.track_artist}')
        char = input('skip or play? (s/p)')


        if char.lower() == 's':
            current.skipped(test)
        elif char.lower() == 'p':
            current.listened(test)
        else:
            pass

        current = test






if __name__ == '__main__':
    FILENAME = 'mypickle(skips).pkl'

    try:
        pickle_file = open(FILENAME, 'rb')
    except (OSError, IOError) as e:
        pickle.dump(Graph(), open(FILENAME, "wb"))
        pickle_file = open(FILENAME, 'rb')

    graph = pickle.load(pickle_file)
    graph.pickle_file = FILENAME
    pickle_file.close()

    print(graph, '\n\n')
    print(f"The graph currently contains {graph.size} nodes.\nThat's {graph.size*graph.size-graph.size} possible connections, {graph.weighted_connections} of them are non-null. That's {int(graph.weighted_connections/(graph.size*graph.size-graph.size) * 100)}% coverage!")


    try:
        main(graph)
    except KeyboardInterrupt:
        print('Interrupted')
        print(f"The graph currently contains {graph.size} nodes.\nThat's {graph.size*graph.size-graph.size} possible connections, {graph.weighted_connections} of them are non-null. That's {int(graph.weighted_connections/(graph.size*graph.size-graph.size) * 100)}% coverage!")

        graph.save()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)