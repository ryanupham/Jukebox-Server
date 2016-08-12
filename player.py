class QueueTrack:
    def __init__(self, track, owner):
        self.track, self.owner, self.skip_votes = track, owner, []

    def to_JSON(self):
        return {"name": self.track.name, "artist": self.track.artist, "album": self.track.album, "uri": self.track.uri,
                "owner": self.owner.name, "skip_votes": len(self.skip_votes)}


class SongQueue:
    def __init__(self):
        self._queue = []

    def add_track(self, user, track, play_next=False):
        track = QueueTrack(track, user)

        if play_next:
            if user.tokens >= 2:
                self._queue.insert(1, track)
                user.tokens -= 2

                return "success"

            return "fail"
        else:
            if user.tokens >= 1:
                self._queue.append(track)
                user.tokens -= 1

                return "success"

            return "fail"

    def next(self):
        self._queue.pop(0)
        return self._queue[0] if len(self._queue) > 0 else None

    def skip(self, user):
        if len(self._queue) > 0 and user.tokens >= 1:
            self._queue.pop(0)
            user.tokens -= 1

            return "success"

        return "fail"

    def vote_skip(self, user, index):
        if index < len(self._queue):
            if user.uid not in self._queue[index].skip_votes:
                self._queue[index].skip_votes.append(user.uid)

                return "success"

        return "fail"

    def remove(self, user, index):
        if 0 < index < len(self._queue) and user.tokens >= 1:
            self._queue.pop(index)
            user.tokens -= 1

            return "success"

        return "fail"

    def to_JSON(self):
        return [s.to_JSON() for s in self._queue]

queue = SongQueue()
