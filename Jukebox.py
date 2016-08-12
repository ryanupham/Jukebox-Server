from flask import Flask
from flask_restful import Resource, Api

import data
import player
import searching
import users

app = Flask(__name__)
api = Api(app)


class UserInfo(Resource):
    def get(self, uid):
        user = users.users.get(uid)
        return user.to_JSON() if user is not None else {}


class UserAdd(Resource):
    def get(self, name, uid):
        return users.users.add_user(name, uid)


class QueueGet(Resource):
    def get(self):
        return player.queue.to_JSON()


class QueueAdd(Resource):
    def get(self, uid, name, artist, album, uri):
        user = users.users.get(uid)

        if user is None:
            return "fail"

        return player.queue.add_track(user, data.Track(name, artist, album, uri))


class QueueSkip(Resource):
    def get(self, uid):
        user = users.users.get(uid)

        if user is None:
            return "fail"

        return player.queue.skip(user)  # TODO: trigger actual song skip


class QueueVoteSkip(Resource):
    def get(self, uid, index):
        user = users.users.get(uid)

        if user is None:
            return "fail"

        return player.queue.vote_skip(user, index)  # TODO: trigger actual song skip if there are enough votes


class QueueRemove(Resource):
    def get(self, uid, index):
        user = users.users.get(uid)

        if user is None:
            return "fail"

        return player.queue.remove(user, index)


class SearchSong(Resource):
    def get(self, query):
        return searching.find_songs(query)

api.add_resource(UserInfo, '/user/info/<string:uid>/')
api.add_resource(UserAdd, '/user/add/<string:name>/<string:uid>/')

api.add_resource(QueueGet, '/queue/')
api.add_resource(QueueAdd, '/queue/add/<string:uid>/<string:name>/<string:artist>/<string:album>/<string:uri>/')
api.add_resource(QueueSkip, '/queue/skip/<string:uid>/')
api.add_resource(QueueVoteSkip, '/queue/vote_skip/<string:uid>/<int:index>/')
api.add_resource(QueueRemove, '/queue/remove/<string:uid>/<int:index>/')

api.add_resource(SearchSong, '/search/song/<string:query>/')


if __name__ == '__main__':
    app.run()
