import spotipy as sp
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import json
import pandas as pd
import os.path
# Get client and secret ID from text file
with open("ids.txt", 'r') as f:
    lines = f.readlines()
cid = lines[0][:-1]
secret = lines[1]

# Get uri and scope from settings json
with open("settings.json", 'r') as f:
    settings = json.load(f)
    runnerSettingsDict = settings['runnerSettings']
    uri = runnerSettingsDict['uri']
    scope = runnerSettingsDict['scope']

# Login to Spotify
sp = sp.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=cid, client_secret=secret, redirect_uri=uri))


# Get User Info
user = sp.current_user()
user_id = user['id']
user_name = user['display_name']



# Get list of info to collect from JSON
features_to_collect = runnerSettingsDict['collected_features']
info_to_collecclrt = runnerSettingsDict['collected_track_info']
track_frame = None
if os.path.isfile("./savedCSVs/" + user_name + "LikedSongs.csv"):
    songs = []
    # Get user liked songs
    off = 0
    while off < 10000:
        print(off)
        results = sp.current_user_saved_tracks(offset=off, limit=50)
        for idx, item in enumerate(results['items']):
            cur_song = []
            # Track Info
            track = item['track']
            if len(info_to_collect) > 0:
                for info in info_to_collect:
                    if info == "artist_name":
                        cur_song.append(track['artists'][0]['name'])
                    else:
                        cur_song.append(track[info])

            # Track Features
            if len(features_to_collect) > 0:
                feats = sp.audio_features(track['uri'])[0]
                for feat in features_to_collect:
                    cur_song.append(feats[feat])
            
            # Add current song to songs list
            songs.append(cur_song)

            # Break if all songs seen or iterate more
            if len(results['items']) < 50:
                break
            else:
                off += 50

    # Convert songs 2D list to dataframe
    track_frame = pd.DataFrame(data = songs, columns= info_to_collect + features_to_collect)

    if runnerSettingsDict['save_liked_songs'] == True:
        track_frame.to_csv("./savedCSVs/" + user_name + "LikedSongs.csv")
else:
    track_frame = pd.read_csv("./savedCSVs/" + user_name + "LikedSongs.csv")

