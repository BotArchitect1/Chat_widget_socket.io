
users = {}


def get_user(sid):
    if sid in users:
        return users[sid]
    else:
        return None


def add_user(sid, user):
    users[sid] = user


def remove_user(sid):
    if sid in users:
        del users[sid]
