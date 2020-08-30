import config

def get_spotify_song(username):
    """Return user`s current playing song on spotify"""
    import spotipy
    from spotipy.oauth2 import SpotifyOAuth

    scope = "user-read-playback-state"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, username=username))

    r = sp.current_user_playing_track()
    if r and r['is_playing']:
        artists = []
        for artist in r['item']['artists']:
            artists.append(artist['name'])
        name = r['item']['name']
        return({'artists': artists, 'name': name})
    else: 
        return(None)


def get_lyrics_vocadb(artist, name):
    """Return song lyrics from vocadb"""
    import requests
    import json

    params = {'query': artist}
    headers = {'content-type': 'text/json'}
    r = requests.get('https://vocadb.net/api/artists', params=params, headers=headers)
    r_json = json.loads(r.text)
    if r_json['items']:
        artist_id = r_json['items'][0]['id']
    else: 
        artist_id = None

    params = {'query': name, 'artistId': artist_id ,'fields': 'lyrics'}
    headers = {'content-type': 'text/json'}
    r = requests.get('https://vocadb.net/api/songs', params=params, headers=headers)
    r_json = json.loads(r.text)
    if r_json['items'] and r_json['items'][0]['lyrics']:
        return r_json['items'][0]['lyrics'][0]['value']
    else:
        return None


def get_lyrics_genius(artist, name):
    """Return song lyrics from genius"""
    import lyricsgenius
    genius = lyricsgenius.Genius(config.genius_token)
    genius.verbose = False
    song = genius.search_song(artist, name)
    if song:
        return song.lyrics
    else: 
        return None


if __name__ == '__main__':
    import time
    import os
    current_song = None
    while True:
        new_current_song = get_spotify_song(config.spotify_username)
        if (new_current_song != current_song) and new_current_song:
            current_song = new_current_song
            os.system('cls||clear')
            print('%s - %s\n' % (', '.join(current_song['artists']), current_song['name']))

            lyrics = get_lyrics_genius(current_song['artists'][0], current_song['name'])
            if lyrics is None:
                lyrics = get_lyrics_vocadb(current_song['artists'][0], current_song['name'])
            if lyrics is None:
                lyrics = get_lyrics_vocadb(current_song['artists'][0], current_song['name'].split()[0])
            if lyrics is None:
                lyrics = 'Lyrics not found..'

            print(lyrics)
        time.sleep(5)
