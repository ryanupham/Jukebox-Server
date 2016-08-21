import threading
import time

import spotify
from spotify.player import PlayerState

song = None
start_time = 0

# Assuming a spotify_appkey.key in the current dir
session = spotify.Session()

# Process events in the background
loop = spotify.EventLoop(session)
loop.start()

# Connect an audio sink
audio = spotify.AlsaSink(session)

# Events for coordination
logged_in = threading.Event()


def on_connection_state_updated(session):
    if session.connection.state is spotify.ConnectionState.LOGGED_IN:
        logged_in.set()


session.on(spotify.SessionEvent.CONNECTION_STATE_UPDATED, on_connection_state_updated)

session.relogin()

logged_in.wait()


def play_song(uri):
    global song, start_time
    song = session.get_track(uri).load()
    session.player.load(song)
    session.player.play()

    start_time = time.time()


def stop_playback():
    session.player.unload()


def get_player_state():
    return {"playing": (session.player.state is PlayerState.PLAYING),
            "name": song.name if song is not None else "",
            "artist": song.artists[0].name if song is not None else "",
            "album": song.album.name if song is not None else "",
            "album art": "http://o.scdn.co/image/" + song.album.cover_link().url[31:] if song is not None else "",
            "duration": song.duration / 1000 if song is not None else 0,
            "seek": time.time() - start_time}


def register_end_of_track_listener(listener):
    session.on(spotify.SessionEvent.END_OF_TRACK, listener)
