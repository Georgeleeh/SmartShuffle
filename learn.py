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

    print(f"The graph currently contains {graph.size} nodes.\nThat's {graph.size*graph.size} connections, {graph.weighted_connections} of them are non-zero!")

    if pb is None or pb.get('item') is None:
        print('no song playback found')
        return

    if pb['item']['id'] not in graph.nodes:
        current_node = Node(pb['item'])
        graph.add_node(current_node)
    else:
        current_node = graph.nodes[pb['item']['id']]

    print(current_node)

    last_listened_node = None

    DELAY_SECS = 1
    listening_duration_millis = 0
    while True:

        # get current track info
        try:
            pb = sp.current_playback()
        except spotipy.client.SpotifyException:
            token = util.prompt_for_user_token(username, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope)
            sp = spotipy.Spotify(auth=token)
            pb = sp.current_playback()

        if pb is not None and pb.get('item') is not None:
            pb_song = pb['item']
            if pb_song['id'] != current_node.track_id:

                if listening_duration_millis < current_node.track_duration_millis / 2:
                    print('skipped early')
                else:
                    if last_listened_node is not None:
                        print('listened to a lot')
                        current_node.listened(last_listened_node)
                    graph.health_check()
                    last_listened_node = current_node

                if pb_song['id'] not in graph.nodes:
                    new_node = Node(pb_song)
                    graph.add_node(new_node)
                else:
                    new_node = graph.nodes[pb_song['id']]
                
                current_node = new_node
                print(current_node)
                listening_duration_millis = 0
            
            listening_duration_millis = pb['progress_ms']
        
        time.sleep(DELAY_SECS)



if __name__ == '__main__':
    FILENAME = 'mypickle(LinkedList).pkl'

    try:
        pickle_file = open(FILENAME, 'rb')
    except (OSError, IOError) as e:
        pickle.dump(Graph(), open(FILENAME, "wb"))
        pickle_file = open(FILENAME, 'rb')

    graph = pickle.load(pickle_file)
    graph.pickle_file = FILENAME
    pickle_file.close()

    try:
        main(graph)
    except KeyboardInterrupt:
        print('Interrupted')
        graph.save_graph()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    