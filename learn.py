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
    scope = 'user-read-currently-playing user-read-playback-state'
    redirect_uri = 'http://localhost:8888/callback/'
    token = util.prompt_for_user_token(username, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope)


    # Main
    nodes = {}
    sp = spotipy.Spotify(auth=token)

    pb = sp.current_playback()

    print(graph)

    if pb is None:
        print('no playback found')
        return

    current_node = Node(pb['item'])
    print(current_node)
    last_listened_node = current_node

    graph.add_node(current_node)

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

                if listening_duration_millis < current_node.track_duration_millis / 4:
                    print('skipped early')
                else:
                    print('listened to a lot')
                    if last_listened_node != current_node:
                        current_node.listened(last_listened_node)
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
    graph.health_check()
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
    