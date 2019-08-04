from flask import Flask, send_from_directory
from flask_jwt import JWT, jwt_required, current_identity
from models import user 
from flask import jsonify

##############################################
# INIT WEB APP
app = Flask(__name__)
# TODO: switch debug to False in production
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'

jwt = JWT(app, user.User.authenticate, user.User.identity)


##############################################
# ROUTES
# See https://pythonhosted.org/Flask-JWT/#quickstart
# on how to access protected routes.
@app.route('/user')
@jwt_required()
def user():
    return jsonify(
        id = current_identity.id,
        username = current_identity.username,
        role = current_identity.role
    )



@app.route("/")
def index():
    return send_from_directory('static/html', 'index.html')



if __name__ == '__main__':
    app.run()
