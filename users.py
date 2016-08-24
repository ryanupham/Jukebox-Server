from threading import Timer


class User:
    def __init__(self, name, uid, tokens=3):
        self.name, self.uid, self.tokens = name, uid, tokens
        Timer(60 * 10, self._add_token_timer).start()

    def _add_token_timer(self):
        self.tokens += 1
        Timer(60 * 10, self._add_token_timer).start()

    def to_JSON(self):
        return {"name": self.name, "uid": self.uid, "tokens": self.tokens}


class Users:
    def __init__(self):
        self._users = []

    def add_user(self, name, uid):
        user = User(name, uid)

        if user.uid not in [u.uid for u in self._users]:
            self._users.append(user)
            return "success"

        return "fail"

    def get(self, uid):
        for user in self._users:
            if user.uid == uid:
                return user

        return None

    def __len__(self):
        return len(self._users)


users = Users()
