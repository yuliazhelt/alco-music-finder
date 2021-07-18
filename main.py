import json
import os
import requests
from flask import Flask, render_template, request, session, redirect, url_for
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from web_scrapping import df
from funcs import get_tracks, get_artists, langs_freq, styles_freq, suitable_cocktail_bases
from clients import SuitableCocktailFinder

app = Flask(__name__)
app.secret_key = os.urandom(24)
GIFS_FOLDER = os.path.join('static')
app.config['UPLOAD_FOLDER'] = GIFS_FOLDER

# данные зарегестрированного в My Dashboard Spotify приложения, которые я решила не скрывать
client_id = "ac1eeacc25cc43788c434d344fb521a2"
client_secret = "57bae2d4dad04d999217d916e6ff7d44"
redirect_uri = 'http://127.0.0.1:5000/redirectPage'
scope = 'user-library-read'

API_BASE = 'https://accounts.spotify.com'
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)


@app.route('/')
def start():
    session.clear()
    return render_template('start.html', user_image1=os.path.join(app.config['UPLOAD_FOLDER'], 'giphy1.gif'),
                           user_image2=os.path.join(app.config['UPLOAD_FOLDER'], 'giphy2.gif'))


def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=url_for('redirectPage', _external=True),
        scope=scope)


@app.route('/login')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


@app.route('/redirectPage')
def redirectPage():
    auth_token = request.args['code']
    code_payload = {
        'grant_type': "authorization_code",
        'code': str(auth_token),
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret,
    }
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload)
    response_data = json.loads(post_request.text)
    access_token = response_data['access_token']
    session['token'] = access_token
    return redirect('analyze')


@app.route('/analyze')
def analyze():
    return render_template('analyze.html', user_image1=os.path.join(app.config['UPLOAD_FOLDER'], 'giphy1.gif'),
                           user_image2=os.path.join(app.config['UPLOAD_FOLDER'], 'giphy2.gif'))


# количество песен каждого жанра (считается за счет количества песен артистов)
def genres_freq(artists):
    genres = {}
    for artist_id in artists:
        response = requests.get(f"https://api.spotify.com/v1/artists/{artist_id}",
                                headers={"Authorization": f"Bearer {session['token']}"})
        for genre in json.loads(response.text).get('genres'):
            if genre not in genres:
                genres[genre] = 0
            genres[genre] += artists[artist_id]
    return dict(sorted(genres.items(), key=lambda item: -item[1]))


@app.route('/getResults')
def get_results():
    collection = get_tracks(spotipy.Spotify(auth=session['token']))
    genres = genres_freq(get_artists(collection))
    langs_frequency = langs_freq(genres)
    styles_frequency = styles_freq(genres)
    suitable_cocktail_finder = SuitableCocktailFinder(df)
    # данные, нужные для выдачи результата в html
    form_data = {'name': [],
                 'url': [],
                 'img': []}
    for base in suitable_cocktail_bases(langs_frequency, styles_frequency):
        # получим список название-базы-ссылка-адрес изображения нужного коктейля:
        cocktail = df.loc[suitable_cocktail_finder(base)].values[0]
        form_data['name'].append(cocktail[0])
        form_data['url'].append(cocktail[2])
        form_data['img'].append('https://ru.inshaker.com' + cocktail[3])
    form_data_len = len(form_data['name'])
    return render_template('result.html', form_data=form_data, form_data_len=form_data_len)


if __name__ == '__main__':
    app.run()
