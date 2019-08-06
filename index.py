from flask import Flask, send_from_directory, jsonify, request
#from flask_jwt import JWT, jwt_required, current_identity
from flask_jwt_extended import (
    JWTManager, jwt_required,
    create_access_token, create_refresh_token,
    get_jwt_identity
)
from models.user import User

##############################################
# INIT WEB APP
app = Flask(__name__)
# TODO: switch debug to False in production
app.debug = True
#app.config['SECRET_KEY'] = 'super-secret'
app.config['JWT_SECRET_KEY'] = 'super-secret'

#jwt = JWT(app, user.User.authenticate, user.User.identity)
jwt = JWTManager(app)


#################################################################################
# ROUTES
# See https://flask-jwt-extended.readthedocs.io/en/latest/basic_usage.html
# on using JWT
#################################################################################

# AUTH ##############################################################
@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    success = User.authenticate(username, password)
    if not success:
        return jsonify({"msg": "Bad username or password"}), 401

    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=username)
    refresh_token = create_refresh_token(identity=username)
    return jsonify(access_token=access_token, refresh_token=refresh_token), 200


@jwt.user_identity_loader
def identity(username):
    user = User.get(username)
    return user


@app.route('/refresh')
@jwt_required
def refresh():
    return

@app.route('/user')
@jwt_required
def user():
    current_identity = get_jwt_identity()
    return jsonify(current_identity)


@app.route("/")
def index():
    return send_from_directory('static/html', 'index.html')



if __name__ == '__main__':
    app.run()
