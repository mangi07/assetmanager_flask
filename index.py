from flask import Flask, send_from_directory, jsonify, request
#from flask_jwt import JWT, jwt_required, current_identity
from flask_jwt_extended import (
    JWTManager, jwt_required,
    create_access_token, create_refresh_token, jwt_refresh_token_required,
    get_jwt_identity
)
from models.user import User
from flask_cors import CORS
from queries import asset_queries

##############################################
# INIT WEB APP
app = Flask(__name__)

# TODO: switch debug to False in production
app.debug = True

# TODO: better secret and read in from external file
app.config['JWT_SECRET_KEY'] = 'super-secret'

# TODO: read a config or environment so CORS is used only in development
CORS(app)

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
        return jsonify({"error": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"error": "Missing username"}), 400
    if not password:
        return jsonify({"error": "Missing password"}), 400

    success = User.authenticate(username, password)
    if not success:
        return jsonify({"error": "Bad username or password"}), 401

    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=username)
    refresh_token = create_refresh_token(identity=username)
    return jsonify(access_token=access_token, refresh_token=refresh_token), 200


@jwt.user_identity_loader
def identity(username):
    user = User.get(username)
    return user


@app.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_identity = get_jwt_identity()
    username = current_identity['username']

    try:
        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)
        return jsonify(access_token=access_token, refresh_token=refresh_token), 200
    except:
        return jsonify({"error":"This user could not be found."})

@app.route('/user')
@jwt_required
def user():
    current_identity = get_jwt_identity()
    return jsonify(current_identity)

rel_path = 'static/client/dist'
@app.route("/")
def index():
    return send_from_directory(rel_path, 'index.html')
@app.route("/<path:path>")
def send_static_files(path):
    return send_from_directory(rel_path, path)


# ASSETS ##############################################################
@app.route("/assets/<int:page>")
@app.route("/assets")
@jwt_required 
def list_assets(page=0):
    # create location tree
    # get filters - TODO: may want to move this to asset_queries (??) by passing request.args
    cost_gt = request.args.get('cost_gt', None)
    cost_lt = request.args.get('cost_lt', None)
    filters = {
        'location': request.args.get('location', None),
        'cost_gt': float(cost_gt) if cost_gt else None,
        'cost_lt': float(cost_lt) if cost_lt else None,
    }
    
    # execute query
    assets = asset_queries.get_assets(page, filters)
    
    # pagination links
    prev = '/assets/' + str(max(page, 0))
    next = '/assets/' + str(page + 1)

    return jsonify(
        msg='testing',
        filters=filters,
        assets=assets,
        prev=prev,
        next=next
    )



if __name__ == '__main__':
    app.run()
