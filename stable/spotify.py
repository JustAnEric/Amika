import json,os,spotipy,webbrowser

def spotify_enabled():
    if not os.path.exists('./setup.cfog'): return False
    with open('./setup.cfog','r') as f:
        for i in f.readlines():
            content = i.strip("\n").split('=')
            if content[0] != "spotify_enabled":
                pass
            else:
                if content[1].split(' #')[0].lower() == "true":
                    return True
                else: return False
        f.close()
    return None

def manual_auth():
    clientID = '5c8e9bc5eff74aaaaf29e0b4b4be790e'
    clientSecret = '8ee6dff557394a268052635f9c9b1e08'
    redirect_uri = 'https://google.com/callback'
    oauth_object = spotipy.SpotifyOAuth(clientID, clientSecret, redirect_uri, scope="user-read-playback-state user-modify-playback-state user-read-currently-playing app-remote-control streaming user-read-email")
    token_dict = oauth_object.get_access_token()
    token = token_dict['access_token']
    spotifyObject = spotipy.Spotify(auth=token)
    user_name = spotifyObject.current_user()
    return True

if spotify_enabled():
    clientID = '5c8e9bc5eff74aaaaf29e0b4b4be790e'
    clientSecret = '8ee6dff557394a268052635f9c9b1e08'
    redirect_uri = 'https://google.com/callback'
    oauth_object = spotipy.SpotifyOAuth(clientID, clientSecret, redirect_uri, scope="user-read-playback-state user-modify-playback-state user-read-currently-playing app-remote-control streaming user-read-email")
    token_dict = oauth_object.get_access_token()
    token = token_dict['access_token']
    spotifyObject = spotipy.Spotify(auth=token)
    user_name = spotifyObject.current_user()
    
    # To print the JSON response from 
    # browser in a readable format.
    # optional can be removed
    #print(json.dumps(user_name, sort_keys=True, indent=4))
    
    #while True:
        #user_input = int(input("Enter Your Choice: "))
        #if user_input == 1:
            #search_song = input("Enter the song name: ")
            #results = spotifyObject.search(search_song, 1, 0, "track")
            #songs_dict = results['tracks']
            #song_items = songs_dict['items']
            #song = song_items[0]['external_urls']['spotify']
            #webbrowser.open(song)
            #print('Song has opened in your browser.')
        #elif user_input == 0:
            #print("Good Bye, Have a great day!")
            #break
        #else:
            #print("Please enter valid user-input.")

    class SpotifySearch:
        def init(self, term):
            self.result = spotifyObject.search(term, 1, 0, "track")
            self.song_items = self.result['tracks']['items']
            self.song = self.song_items[0]

        def play(self):
            spotifyObject.add_to_queue(self.song['external_urls']['spotify'])
            spotifyObject.next_track()

        def queue(self):
            spotifyObject.add_to_queue(self.song['external_urls']['spotify'])

        def get_last_song_requested(self):
            return self.song

    def next_tr():
        spotifyObject.next_track()
        
    def prev_tr():
        spotifyObject.previous_track()
        
    def pause():
        spotifyObject.pause_playback()

    def resume():
        spotifyObject.start_playback()
    
    def change_volume(volume_percent=100, device_id=None):
        try: spotifyObject.volume(volume_percent, device_id)
        except: pass