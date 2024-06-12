from dotenv import find_dotenv, set_key, get_key
import spotipy
import spotipy.util as util
import numpy as np
import pandas as pd
from sklearn.metrics import euclidean_distances

def auth():
    client_id = get_key(find_dotenv(), 'CLIENT_ID')
    client_secret = get_key(find_dotenv(), 'CLIENT_SECRET')
    username = get_key(find_dotenv(), 'USERNAME')
    redirect_uri = 'http://localhost:8080/'

    token = util.prompt_for_user_token(username=username, scope='playlist-read-private user-top-read user-library-read', client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
    
    return set_key(find_dotenv(), 'CURR_USER_TOKEN', token)

def computeCentroid(selected_tracks: list, audio_feats: pd.DataFrame):
    track_ids = pd.Index([tr['track']['id'] for tr in selected_tracks])
    selected_audio_feats = audio_feats.loc[track_ids]
    centroid = selected_audio_feats.drop(['track_id'],axis=1).mean(axis=0)

    return centroid

def computeDistances(audio_feats: pd.DataFrame, centroid: pd.DataFrame):
    dists = euclidean_distances(audio_feats, [centroid])
    distDf = pd.DataFrame(dists, columns=["distance"])
    distDf['track_id'] = audio_feats.index.copy()
    
    return distDf

