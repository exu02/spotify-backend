from flask import Flask, request
from dotenv import find_dotenv, set_key, get_key
from flask_cors import CORS, cross_origin
import spotipy
import spotipy.util as util
from helpers import *

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content_Type"

@app.route('/')
def home():
    return 'API Server for Spotify Playlist Organizer'

@app.route('/api/setUser', methods=['POST'])
@cross_origin()
def setUserAndAuth():
    userJson = request.get_json()
    user = userJson['username']
    set_key(find_dotenv(), 'USERNAME', user)
    redirect_uri = "http://localhost:8080/"
    client_id = get_key(find_dotenv(), "CLIENT_ID")
    client_secret = get_key(find_dotenv(), "CLIENT_SECRET")
    token = util.prompt_for_user_token(username=user, scope="playlist-read-private user-top-read user-library-read", client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
    set_key(find_dotenv(), "CURR_USER_TOKEN", token)
    return {"Message": "Success"}

@app.route('/api/getPlaylists', methods=['GET'])
def getPlaylists():
    token = get_key(find_dotenv(), 'CURR_USER_TOKEN')
    sp = spotipy.Spotify(auth=token)
    playlists = sp.current_user_playlists()['items']
    return playlists

@app.route('/api/getTracksFromPlaylist', methods=['POST'])
@cross_origin()
def getTracksFromPlaylist():
    token = get_key(find_dotenv(), 'CURR_USER_TOKEN')
    sp = spotipy.Spotify(auth=token)
    playlist_id = request.get_json()['playlist_id']
    tracks = sp.playlist(playlist_id)['tracks']['items']
    return tracks

if __name__ == '__main__':
    app.run(debug=True)