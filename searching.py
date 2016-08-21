import spotipy

from data import Track

spotify = spotipy.Spotify()


def find_songs(query):
    return [Track(r["name"], r["artists"][0]["name"], r["album"]["name"], r["uri"])._asdict()
            for r in spotify.search(query, limit=50)["tracks"]["items"]]
