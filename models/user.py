##############################################
# File: user.py

from utils.passwords import hash_password, verify_password


class User(object):
    def __init__(self, id, username, password, role="regular"):
        self.id = id
        self.username = username
        self.password = hash_password(password)
        self.role = role

    def __str__(self):
        return "User(id='%s')" % self.id

    def authenticate(username, password):
        user = username_table.get(username, None)
        if user and verify_password(user.password, password):
            return user

    def identity(payload):
        user_id = payload['identity']
        return userid_table.get(user_id, None)


##############################################
# todo: FOR DB
users = [
    User(1, 'user1', 'abcxyz'),
    User(2, 'user2', 'abcxyz'),
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}


