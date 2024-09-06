
from flask import Flask, jsonify, request, send_file, send_from_directory
from flask_cors import CORS
#from flask_jwt import JWT, jwt_required, current_identity
#from flask_jwt_extended import (JWTManager, create_access_token,
#                                create_refresh_token, get_jwt_identity,
#                                jwt_refresh_token_required, jwt_required)
# above import migrated to:
from flask_jwt_extended import (JWTManager, create_access_token,
                                create_refresh_token, get_jwt_identity,
                                jwt_required)

import config
from models.user import User
from queries import asset_queries, location_queries
from utils.file_access import FileGuardian, file_access_token_required
from utils.filters import checkbox_group_filter
from logger import log

##############################################
# INIT WEB APP
# import web_pdb; web_pdb.set_trace() # TODO: remove?
app = Flask(__name__)

# TODO: switch debug to False in production
app.debug = True

# TODO: better secret and read in from external file
app.config['JWT_SECRET_KEY'] = 'super-secret'

# TODO: read a config or environment so CORS is used only in development
#app.config['CORS_HEADERS'] = 'Content-Type'
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
    #import pdb; pdb.set_trace()
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
    fg = FileGuardian()
    file_access_token = fg.issue_file_access_token()
    return jsonify(access_token=access_token, refresh_token=refresh_token, file_access_token=file_access_token), 200


@jwt.user_identity_loader
def identity(username):
    """get user identity"""
    user = User.get(username)
    return user


@app.route('/refresh', methods=['POST'])
#@jwt_refresh_token_required -- migrated from this to:
@jwt_required(refresh=True)
def refresh():
    current_identity = get_jwt_identity()
    username = current_identity['username']

    try:
        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)
        fg = FileGuardian()
        file_access_token = fg.issue_file_access_token()
        return jsonify(
            access_token=access_token, 
            refresh_token=refresh_token,
            file_access_token=file_access_token), 200
    except:
        return jsonify({"error":"This user could not be found."})

@app.route('/user')
#@jwt_required -- migrated from this to:
@jwt_required()
def user():
    current_identity = get_jwt_identity()
    return jsonify(current_identity)

# TODO: This may not be neccessary if serving front end through a serparate server
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
#@jwt_required -- migrated from this to:
@jwt_required()
def list_assets(page=0):
    # get filters - TODO: may want to move this to asset_queries (??) by passing request.args
    cost__gt = request.args.get('cost__gt', None)
    cost__lt = request.args.get('cost__lt', None)
    desc__contains = request.args.get('desc__contains', None)

    past = request.args.get('past', None)
    present = request.args.get('present', None)
    future = request.args.get('future', None)
    # TODO: call to filters library function goes here
    is_current_filters = checkbox_group_filter([past, present, future], 'asset.is_current')
    log(is_current_filters)
    #if past == 'true' and present == 'true' and future == 'true':
    #    is_current__includes = None
    #    is_current__is_null = None
    #else:
    #    is_current__includes = []
    #    if past == 'true':
    #        is_current__includes.append(0)
    #    if present == 'true':
    #        is_current__includes.append(1)
    #    if is_current__includes == []:
    #        is_current__includes = None

    #is_current__is_null = 1 if future == 'true' else None
    #log(is_current__includes)
    #log(is_current__is_null)

    # get file access token - if None, image links provided in this response may return 404 forbidden
    file_access_token = request.args.get('file_access_token', None)

    try:
        location__eq = request.args.get('location_count.location__eq', None)
        filters = {
            'location_count.location__eq': int(location__eq) if location__eq else None,
            'asset.cost__gt': int(float(cost__gt)*config.get_precision_factor()) if cost__gt else None,
            'asset.cost__lt': int(float(cost__lt)*config.get_precision_factor()) if cost__lt else None,
            'asset.description__contains': str(desc__contains) if desc__contains else None,
        }
        filters.update(is_current_filters)
        log(filters)
    except:
        return jsonify(error='Bad Request: malformed query params'), 400

    filters_arr = [f"{k}={v}" for k, v in filters.items() if v is not None]
    filters_str = '?' + '&'.join(filters_arr) if len(filters_arr) > 0 else ''
    
    # execute query
    assets = asset_queries.get_assets(page, filters)
    
    # pagination links
    prev = '/assets/' + str(max(page, 0)) + filters_str
    next = '/assets/' + str(page + 1) + filters_str

    return jsonify(
        msg='testing',
        filters=filters,
        assets=assets,
        prev=prev,
        next=next
    )


@app.route("/img/<path:path>", endpoint='get_image')
@file_access_token_required
def get_image(path):
    try:
        # This could result in sending a file as an image when the file is not really an image; 
        # the server trusts that the requested file really is an image. 
        # TODO: have file root load from env rather than hard-coded text
        #return send_file(f"db/files/{path}", mimetype='image/jpg')
        BASE_PATH = config.get_asset_files_base_path()
        return send_from_directory(BASE_PATH, path, mimetype='image/jpg')
    except:
        # TODO: have file root load from env rather than hard-coded text
        return send_file("db/files/file_not_found.jpg", mimetype='image/jpg')


@app.route("/file/<path:path>", endpoint='get_file')
@file_access_token_required
def get_file(path):
    try:
        # This could result in sending a file as an image when the file is not really an image; 
        # the server trusts that the requested file really is an image. 
        # TODO: have file root load from env rather than hard-coded text
        # See the following URL:
        # https://flask.palletsprojects.com/en/2.3.x/patterns/fileuploads/
        #   This does include a guide for indicating a download base path, further down the webpage
        #return send_file(f"db/files/{path}")
        BASE_PATH = config.get_asset_files_base_path()
        return send_from_directory(BASE_PATH, path)
    except:
        # This could result in sending a file as an image when the file is not really an image;
        # TODO: have file root load from env rather than hard-coded text
        return send_file("db/files/file_not_found.jpg", mimetype='image/jpg')


# LOCATIONS ##############################################################
@app.route("/locations")
#@jwt_required -- migrated from this to:
@jwt_required()
def list_locations():
   
    # execute query
    locs = location_queries.Locations()
    #ids = locs.get_subtree_ids(root)
    #locations = locs.get_tree()
    locations = locs.get_list()

    # create location tree
    return jsonify(
        locations=locations,
    )




if __name__ == '__main__':
    app.run()

 
