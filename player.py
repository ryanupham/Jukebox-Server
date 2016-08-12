import threading

import spotify


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
session.player.seek()

logged_in.wait()


def play_song(uri):
    song = session.get_track(uri).load()
    session.player.load(song)
    session.player.play()


def register_end_of_track_listener(listener):
    session.on(spotify.SessionEvent.END_OF_TRACK, listener)