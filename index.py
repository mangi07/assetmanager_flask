from flask import Flask, send_from_directory
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp


##############################################
# MODELS
class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

##############################################
# todo: FOR DB
users = [
    User(1, 'user1', 'abcxyz'),
    User(2, 'user2', 'abcxyz'),
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}


##############################################
# AUTH
def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)


##############################################
# INIT WEB APP
app = Flask(__name__)
# TODO: switch debug to False in production
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'

jwt = JWT(app, authenticate, identity)



##############################################
# ROUTES
# See https://pythonhosted.org/Flask-JWT/#quickstart
# on how to access protected routes.
@app.route('/protected')
@jwt_required()
def protected():
    return '%s' % current_identity


@app.route("/")
def index():
    return send_from_directory('client/html', 'index.html')


@app.route('/<path:path>')
def send_frontend_file(path):
    return send_from_directory('client/', path)



if __name__ == '__main__':
    app.run()