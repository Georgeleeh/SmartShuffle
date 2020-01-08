from Graph import Node
import time

class Engine:
    def __init__(self, config_file='config.cfg', pickle_file='objpickle.pkl', graph=None):
        self.config = config = configparser.ConfigParser()
        self.config.read('config.cfg')

        if graph is None:
            graph = {}
        self.graph = graph

        self.spotify = spotipy.Spotify(auth=self.token)


    @property
    def token(self):
        client_id = self.config.get('SPOTIFY', 'CLIENT_ID')
        client_secret = self.config.get('SPOTIFY', 'CLIENT_SECRET')
        username = self.config.get('SPOTIFY', 'USERNAME')
        scope = 'user-read-currently-playing user-read-playback-state user-modify-playback-state'
        redirect_uri = 'http://localhost:8888/callback/'
        return util.prompt_for_user_token(username, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope)

    def learn(self):
        def listen():

            playback = self.spotify.current_playback()

            if playback is None:
                print('no playback found')
                return
            
            current_node = Node(playback['item'])
            print(current_node)
            last_listened_node = current_node

            self.add_node(current_node)

            wait_secs = 1
            listening_duration_millis = 0
            while True:
                # is this necessary?
                try:
                    playback = self.spotify.current_playback()
                except spotipy.client.SpotifyException:
                    self.spotify = spotipy.Spotify(auth=self.token)
                    playback = sp.current_playback()
                
                if playback is not None:
                    # if you're listening to a new song since the last check
                    if playback['item']['id'] != current_node.track_id:

                        if listening_duration_millis < current_node.track_duration_millis / 2:
                            print('skipped early')
                        else:
                            # if this isn't the first song in the chain
                            if last_listened_node != current_node:
                                print('listened to a lot')
                                self.increment_distance(last_listened_node, current_node)

                                last_listened_node = current_node
                    
                        new_node = Node(playback['item'])
                        print(new_node)
                        self.add_node(new_node)

                        current_node = new_node

                listening_duration_millis = playback['progress_ms']

                time.sleep(wait_secs)
        
        try:
            listen()
        except KeyboardInterrupt:
            print('Interrupted')
        

    
    def add_node(self, new_node):
        if new_node.track_id not in self.graph.keys():
            # connect new node to all nodes in graph
            for node in self.graph.values():
                new_node.distances[node.track_id] = 0

            # add the new node to the graph
            self.graph[new_node.track_id] = new_node

            # connect every node in the graph to the new node
            for key in self.graph.keys():
                node = self.graph[key]
                node.distances[new_node.track_id] = 0
                self.graph[key] = node
            
            print('added node')
    
    def increment_distance(self, node1, node2):
        print(f'updating distances in nodes {node1} and {node2}')
        print(f'starting distances are {node1.distances.get(node2.track_id)} and {node2.distances.get(node1.track_id)}')
        dist = node1.distances.get(node2.track_id)
        self.graph[node1.track_id].distances[node2.track_id] = dist + 1
        self.graph[node2.track_id].distances[node1.track_id] = dist + 1
        self.print_graph()
    
    def print_graph(self):

        for ynode in self.graph.values():
            print(str(ynode.track_name[:5]), '\t\t', ' '.join(str(ynode.distances.get(xnode.track_id)) for xnode in self.graph.values()), '\t', ynode.track_id, '\n')

    
    


import spotipy
import spotipy.oauth2 as oauth2
import spotipy.util as util

import configparser


def main():
    engine = Engine()
    engine.learn()




if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
