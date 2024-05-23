from dotenv import find_dotenv, set_key, get_key
import spotipy
import spotipy.util as util

def auth():
    client_id = get_key(find_dotenv(), 'CLIENT_ID')
    client_secret = get_key(find_dotenv(), 'CLIENT_SECRET')
    username = get_key(find_dotenv(), 'USERNAME')
    redirect_uri = 'http://localhost:8080/'

    token = util.prompt_for_user_token(username=username, scope='playlist-read-private user-top-read user-library-read', client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
    
    return set_key(find_dotenv(), 'CURR_USER_TOKEN', token)