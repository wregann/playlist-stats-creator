from typing import Final
from unittest import runner
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import json
import pandas as pd
import os.path

username = "wbregann"

# Options: Mild, Spicy
desired_playlist = "Mild"
desired_name = None

# Get uri and scope from settings json
with open("settings.json", 'r') as f:
    settings = json.load(f)
    runnerSettings = settings['runnerSettings']
    playlistSettings = settings['playlistSettings']

    # Get settings for playlist
    if desired_playlist not in playlistSettings["options"]:
        raise ValueError("Choose a valid playlist type")
    playlist_parameters = playlistSettings[desired_playlist]
    playlist_parameters = [i.split(",") for i in playlist_parameters]

    # Get settings for creator
    
    uri = runnerSettings['uri']
    scope = runnerSettings['scope']




# Get client and secret ID from text file
with open("ids.txt", 'r') as f:
    lines = f.readlines()
    cid = lines[0][:-1]
    secret = lines[1]

# Login to Spotify
#sp = sp.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=cid, client_secret=secret, redirect_uri=uri))
token = spotipy.util.prompt_for_user_token(username,scope,client_id=cid,client_secret=secret,redirect_uri=uri)
if token:
    sp = spotipy.Spotify(auth=token)


# Get User Info
user = sp.current_user()
user_id = user['id']
user_name = user['display_name']



# Get list of info to collect from JSON
features_to_collect = runnerSettings['collected_features']
info_to_collect = runnerSettings['collected_track_info']
track_frame = None
if not os.path.isfile("C:\\Users\\wrega\\Desktop\\SpotifyPlaylistCreator\\savedCSVs\\" + user_name + "LikedSongs.csv"):
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

    if runnerSettings['save_liked_songs'] == True:
        track_frame.to_csv("C:\\Users\\wrega\\Desktop\\SpotifyPlaylistCreator\\savedCSVs\\" + user_name + "LikedSongs.csv")
# Track frame already exists in folder, so just read it instead
else:
    track_frame = pd.read_csv("C:\\Users\\wrega\\Desktop\\SpotifyPlaylistCreator\\savedCSVs\\" + user_name + "LikedSongs.csv")

# Make Playlist
part_track_frames = []
for phrase in playlist_parameters:
    part_track_frame = track_frame.copy()
    for feature_setting in phrase:
        feature_to_check = playlistSettings["feature_letters"][feature_setting.strip()[0]]
        num_to_check = float(feature_setting.strip()[4:])

        if "<" in feature_setting:
            part_track_frame = part_track_frame[part_track_frame[feature_to_check] < num_to_check]
        else:
            part_track_frame = part_track_frame[part_track_frame[feature_to_check] > num_to_check]
    part_track_frames.append(part_track_frame)

new_playlist_frame = pd.concat(part_track_frames, axis=0).drop_duplicates()

if runnerSettings['save_new_playlist'] == True:
    new_playlist_frame.to_csv("C:\\Users\\wrega\\Desktop\\SpotifyPlaylistCreator\\savedCSVs\\" + user_name + desired_playlist + "Playlist.csv")

# Check if User wanted a specific name before creating auto generated one
if desired_name == None:
    name_to_create = user_name + "'s " + desired_playlist + ' Playlist Auto Generated'
else: name_to_create = desired_name

user_playlists = sp.user_playlists(user_id)['items']
# Check if playlist already exists and delete if it does
there = None
for playlist in user_playlists:
    if name_to_create == playlist['name']:
        there = playlist['id']
        break
if there != None:
    sp.user_playlist_unfollow(user_id, there)

new_playlist = sp.user_playlist_create(user_id, name_to_create, public=True, collaborative=False, description="Auto Generated Playlist using Will's program")
new_playlist_id = new_playlist['id']

tracks_to_add = new_playlist_frame['uri'].tolist()

for i in range(0, len(tracks_to_add), 99):
    j = i + 99
    if j > len(tracks_to_add):
        j = len(tracks_to_add)
    sp.user_playlist_add_tracks(user_id, new_playlist_id, tracks_to_add[i:j])
