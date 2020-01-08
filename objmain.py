from Graph import Graph, Node
import time

class Engine:
    def __init__(self, config_file='config.cfg', pickle_file='objpickle.pkl', graph=None):
        self.config = config = configparser.ConfigParser()
        self.config.read('config.cfg')

        if graph is None:
            graph = Graph()
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
        pb = self.spotify.current_playback()

        if pb is None:
            print('no playback found')
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

            # might need to refresh token here, trying without
            self.spotify.current_playback()

            if pb is not None:
                if pb['item']['id'] != current_node.track_id:

                    if listening_duration_millis < current_node.track_duration_millis / 2:
                        print('skipped early')
                    else:
                        if last_listened_node != None:
                            print('listened to a lot')
                            current_node.listened(last_listened_node)
                        self.graph.health_check()
                        last_listened_node = current_node

                    if pb['item']['id'] not in self.graph.nodes:
                        new_node = Node(pb['item'])
                        print(new_node)
                        self.graph.add_node(new_node)
                    else:
                        new_node = self.graph.nodes[pb['item']['id']]

                    current_node = new_node
                    listening_duration_millis = 0
                    
                time.sleep(DELAY_SECS)
                listening_duration_millis = pb['progress_ms']

    
    


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
