import spotipy
import configparser

import spotipy.oauth2 as oauth2
import spotipy.util as util

import time
import pickle
import sys, os

from Graph import Graph, Node

def main(graph):
    # Setup
    config = configparser.ConfigParser()
    config.read('config.cfg')
    client_id = config.get('SPOTIFY', 'CLIENT_ID')
    client_secret = config.get('SPOTIFY', 'CLIENT_SECRET')
    username = config.get('SPOTIFY', 'USERNAME')
    scope = 'user-read-currently-playing user-read-playback-state user-modify-playback-state'
    redirect_uri = 'http://localhost:8888/callback/'
    token = util.prompt_for_user_token(username, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope)


    # Main
    nodes = {}
    sp = spotipy.Spotify(auth=token)

    pb = sp.current_playback()

    print(graph)

    print()
    #graph.print_edges()

    if pb is None:
        print('no playback found')
        return

    current_node = Node(pb['item'])
    print(current_node)
    last_listened_node = None

    graph.add_node(current_node)

    wait_secs = 1
    listening_duration_millis = 0
    while True:

        # get current track info
        try:
            pb = sp.current_playback()
        except spotipy.client.SpotifyException:
            token = util.prompt_for_user_token(username, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope)
            sp = spotipy.Spotify(auth=token)
            pb = sp.current_playback()

        if pb is not None:
            if pb['item']['id'] != current_node.track_id:

                if listening_duration_millis < current_node.track_duration_millis / 2:
                    print('skipped early')
                else:
                    if last_listened_node != None:
                        print('listened to a lot')
                        current_node.listened(last_listened_node)
                    graph.health_check()
                    last_listened_node = current_node

                if pb['item']['id'] not in graph.nodes:
                    new_node = Node(pb['item'])
                    print(new_node)
                    graph.add_node(new_node)
                else:
                    new_node = graph.nodes[pb['item']['id']]

                current_node = new_node
                listening_duration_millis = 0
                
            time.sleep(wait_secs)
            listening_duration_millis = pb['progress_ms']



if __name__ == '__main__':

    pickle_file = open('pickle.pkl', 'rb')
    graph = pickle.load(pickle_file)
    graph.health_check()
    user_input = input('Would you like to clear the graph? (Y/N)\n')
    if user_input.lower() == 'y':
        graph.clear_graph()
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
    