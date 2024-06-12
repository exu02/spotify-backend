from flask import Flask, request
from dotenv import find_dotenv, set_key, get_key
from flask_cors import CORS, cross_origin
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from helpers import *

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content_Type'
client_id = get_key(find_dotenv(), 'CLIENT_ID')
client_secret = get_key(find_dotenv(), 'CLIENT_SECRET')
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

scaler = StandardScaler()
feature_names = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']
audio_feats_std = pd.DataFrame()
track_df = pd.DataFrame()

@app.route('/')
def home():
    return 'API Server for Spotify Playlist Organizer'

@app.route('/api/setUser', methods=['POST'])
@cross_origin()
def setUserAndAuth():
    userJson = request.get_json()
    user = userJson['username']
    set_key(find_dotenv(), 'USERNAME', user)

    return {'spotify_username': user}

@app.route('/api/getPlaylists', methods=['GET'])
@cross_origin()
def getPlaylists():
    playlists = sp.user_playlists(user=get_key(find_dotenv(), 'USERNAME'))['items']
    return playlists

@app.route('/api/getTracksFromPlaylist', methods=['POST'])
@cross_origin()
def getTracksFromPlaylist():
    global track_df
    global audio_feats_std

    playlist_id = request.get_json()['playlist_id']
    tracks = sp.playlist_items(playlist_id, fields='items(track(id, name, artists(name, id), album(name, id, images)))')['items']
    tracks = [tr['track'] for tr in tracks]
    track_df = pd.DataFrame(tracks)
    audio_feats = pd.DataFrame(sp.audio_features(track_df['id']))[feature_names]
    audio_feats_std = pd.DataFrame(
        scaler.fit_transform(audio_feats), 
        columns=audio_feats.columns
    )
    audio_feats_std.index = track_df['id']
    audio_feats_std.index.name = 'track_id'
    track_df = track_df.merge(
        right=audio_feats_std,
        how='inner',
        left_on='id',
        right_index=True
    )
    track_df['distance'] = track_df.index.copy()
    return track_df.to_dict('records')

@app.route('/api/analyzePlaylist', methods=['POST'])
@cross_origin()
def analyzePlaylist():
    global track_df

    track_df = track_df.drop('distance', axis=1)
    selected_tracks = request.get_json()
    centroid = computeCentroid(
        selected_tracks=selected_tracks,
        audio_feats=audio_feats_std
    )
    dists = computeDistances(
        audio_feats=audio_feats_std,
        centroid=centroid
    )
    track_df = track_df.merge(
        dists,
        how='inner',
        left_on='id',
        right_on='track_id'
    )

    return track_df.to_dict('records')

if __name__ == '__main__':
    app.run(debug=True)