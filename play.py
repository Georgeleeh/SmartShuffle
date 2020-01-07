import spotipy
import configparser

import spotipy.oauth2 as oauth2
import spotipy.util as util

import pickle
import sys, os

from Graph import Graph, Node

def main(graph): 
    config = configparser.ConfigParser()
    config.read('config.cfg')
    client_id = config.get('SPOTIFY', 'CLIENT_ID')
    client_secret = config.get('SPOTIFY', 'CLIENT_SECRET')
    username = config.get('SPOTIFY', 'USERNAME')
    scope = 'user-read-currently-playing user-read-playback-state streaming'
    redirect_uri = 'http://localhost:8888/callback/'
    token = util.prompt_for_user_token(username, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope)


    # Main
    nodes = {}
    sp = spotipy.Spotify(auth=token)

    sp.start_playback(uris=['spotify:track:7lEptt4wbM0yJTvSG5EBof'])






if __name__ == '__main__':

    pickle_file = open('pickle.pkl', 'rb')
    graph = pickle.load(pickle_file)
    graph.health_check()
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