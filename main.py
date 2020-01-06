class Node:
    def __init__(self, track_info, distances=None):
        self.track_info = track_info

        if distances is None:
            distances = {}
        self.distances = distances
    
    @property
    def track_id(self):
        return self.track_info['id']
    
    @property
    def track_duration_millis(self):
        return self.track_info['duration_ms']
    
    def __str__(self):
        return self.track_info['name'] + ' - ' +  self.track_info['artists'][0]['name']
    
    def listened(self, previous):
        self.distances[previous.track_id] += 1
        previous.distances[self.track_id] += 1
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
            string += ynode.track_id + '\t' + ' '.join(str(ynode.distances[xnode.track_id]) for xnode in self.nodes.values()) + '\n'
        
        return string

    
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


import spotipy
import configparser

import spotipy.oauth2 as oauth2
import spotipy.util as util

import time
import pickle
import sys, os

def main(graph):
    # Setup
    config = configparser.ConfigParser()
    config.read('config.cfg')
    client_id = config.get('SPOTIFY', 'CLIENT_ID')
    client_secret = config.get('SPOTIFY', 'CLIENT_SECRET')
    username = config.get('SPOTIFY', 'USERNAME')
    scope = 'user-read-currently-playing user-read-playback-state'
    redirect_uri = 'http://localhost:8888/callback/'
    token = util.prompt_for_user_token(username, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope)


    # Main
    nodes = {}
    sp = spotipy.Spotify(auth=token)

    pb = sp.current_playback()

    if pb is None:
        print('no playback found')
        return

    current_node = Node(pb['item'])
    print(current_node)
    last_listened_node = current_node

    graph.add_node(current_node)

    print(graph)


    wait_secs = 5
    listening_duration_millis = 0
    while True:

        # get current track info
        pb = sp.current_playback()
        if pb is not None:
            if pb['item']['id'] != current_node.track_id:
                new_node = Node(pb['item'])
                print(new_node)
                graph.add_node(new_node)

                if listening_duration_millis < current_node.track_duration_millis / 2:
                    print('skipped early')
                else:
                    print('listened to a lot')
                    if last_listened_node != current_node:
                        current_node.listened(last_listened_node)
                        print(current_node.distances[last_listened_node.track_id])
                    else:
                        print('first song in the chain, not updating distance')

                    last_listened_node = current_node

                current_node = new_node
                listening_duration_millis = 0
                
            time.sleep(wait_secs)
            if pb['is_playing']:
                listening_duration_millis += wait_secs * 1000



if __name__ == '__main__':

    pickle_file = open('pickle.pkl', 'rb')
    graph = pickle.load(pickle_file)
    pickle_file.close()

    try:
        main(graph)
    except KeyboardInterrupt:
        print('Interrupted')
        afile = open('pickle.pkl', 'wb')
        pickle.dump(graph, afile)
        afile.close()
        print('saved pickle.pkl')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    