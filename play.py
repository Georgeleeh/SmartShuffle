import spotipy
import configparser

import spotipy.oauth2 as oauth2
import spotipy.util as util

import pickle, sys, os, random
from Graph import Graph, Node

def main(graph): 
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

    shuffled = [node.track_info['uri'] for node in graph.nodes.values()]

    playlist = learn_mode(graph)

    sp.start_playback(uris=playlist)

# dumb shuffles all known songs
def shuffle_all(graph):
    shuff = [node.track_info['uri'] for node in graph.nodes.values()]
    random.shuffle(shuff)
    return shuff

def learn_mode(graph, n=10):
    playlist = []
    nodes = list(graph.nodes.values())
    random.shuffle(nodes)
    
    for i in range(n):
        for node in nodes:
            if len(playlist) == 0:
                playlist.append(node)
                break
            else:
                if node.self_to_other.get(playlist[-1].track_id) is None and node not in playlist:
                    playlist.append(node)
                    break

    playlist = [node.track_info['uri'] for node in playlist]
    return playlist








if __name__ == '__main__':

    pickle_file = open('mypickle(skips).pkl', 'rb')
    graph = pickle.load(pickle_file)
    pickle_file.close()

    try:
        main(graph)
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)