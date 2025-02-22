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
        if not user:
            return False
        return verify_password(user.password, password)

    def get(username):
        user = username_table.get(username, None)
        return {'username':user.username, 'role':user.role}


##############################################
# todo: FOR DB
users = [
    #User(1, 'a', 'a'),
    #User(2, 'b', 'b'),
    User(1, 'reg', '24am20.'),
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}


