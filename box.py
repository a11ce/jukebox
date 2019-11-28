from flask import request
from flask import Flask
import spotipy
import spotipy.util
import time

SPOTIFY_USERNAME = "oxa11ce"
SPOTIFY_SCOPE = "playlist-read-private playlist-modify-private"
token = spotipy.util.prompt_for_user_token(SPOTIFY_USERNAME, SPOTIFY_SCOPE)
sp = spotipy.Spotify(token)

newPl = sp.user_playlist_create(SPOTIFY_USERNAME,
                                "jukebox at " + str(time.time()), "")['uri']

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        try:
            useReq(request.form)
        except Exception as e:
            return "Error!\n" + str(e)
        return "Ok thank you (go back to submit again)"
    else:
        with open('index.html') as f:
            return f.read()
    return "ERROR"


def useReq(rDat):
    print(rDat['songtitle'])
    qu = rDat['songtitle'] + " " + rDat['artist']
    results = sp.search(q=qu, type='track')
    try:
        songUri = results['tracks']['items'][0]['uri']
    except:
        raise Exception('No songs found. Check your spelling.')
    print(songUri)
    sp.user_playlist_add_tracks(SPOTIFY_USERNAME, newPl, [songUri])
