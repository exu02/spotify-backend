from flask import Flask, request
from dotenv import find_dotenv, set_key, get_key
import spotipy
import spotipy.util as util
from helpers import *

app = Flask(__name__)

@app.route('/')
def home():
    return 'API Server for Spotify Playlist Organizer'

@app.route('/api/setUser', methods=['POST'])
def setUserAndAuth():
    userJson = request.get_json()
    user = userJson['username']
    set_key(find_dotenv(), 'USERNAME', user)
    return auth

@app.route('/api/getPlaylists', methods=['GET'])
def getPlaylists():
    token = get_key(find_dotenv(), 'CURR_USER_TOKEN')
    sp = spotipy.Spotify(auth=token)
    playlists = sp.current_user_playlists()['items']
    return playlists

@app.route('/api/getTracksFromPlaylist', methods=['POST'])
def getTracksFromPlaylist():
    token = get_key(find_dotenv(), 'CURR_USER_TOKEN')
    sp = spotipy.Spotify(auth=token)
    playlist_id = request.get_json()['playlist_id']
    tracks = sp.playlist(playlist_id)['tracks']['items']
    return tracks

if __name__ == '__main__':
    app.run(debug=True)