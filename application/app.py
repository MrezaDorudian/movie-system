import flask
import jwt
from .handlers import admin, users, guests  # noqa: E402

ADMIN_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhY2Nlc3NfbGV2ZWwiOiJhZG1pbiJ9.dtLqN1M1-xMMC98TSy70Z0sVn5z_ctq8j9oj6Z_4S3c'

app = flask.Flask(__name__)


def admin_auth_check():
    try:
        token = flask.request.headers['Authorization'].split(' ')[1]
        if token != ADMIN_TOKEN:
            return flask.make_response(flask.jsonify({'message': 'unauthorized'}), 401)
    except KeyError:
        return flask.make_response(flask.jsonify({'message': 'unauthorized'}), 401)


def user_auth_check():
    try:
        token = flask.request.headers['Authorization'].split(' ')[1]
        decoded_token = jwt.decode(token, '', algorithms=['HS256'])
        access_level = decoded_token['access_level']
        user_id = decoded_token['id']
    except KeyError:
        return flask.make_response(flask.jsonify({'message': 'unauthorized'}), 401)
    if access_level != 'user':
        return flask.make_response(flask.jsonify({'message': 'unauthorized'}), 401)
    return int(user_id)


def get_app():
    return app

@app.route('/admin/movie', methods=['POST'])
def add_movie():
    return admin.add_movie()


@app.route('/admin/movie/<id>', methods=['PUT', 'DELETE'])
def manage_movie(id):
    if flask.request.method == 'PUT':
        return admin.update_movie(id)
    elif flask.request.method == 'DELETE':
        return admin.delete_movie(id)


@app.route('/admin/comments/<id>', methods=['PUT', 'DELETE'])
def manage_comment(id):
    if flask.request.method == 'PUT':
        return admin.update_comment(id)
    elif flask.request.method == 'DELETE':
        return admin.delete_comment(id)


@app.route('/user/vote', methods=['POST'])
def vote_movie():
    return users.vote_movie()


@app.route('/user/comment', methods=['POST'])
def insert_comment():
    return users.insert_comment()


@app.route('/comments', methods=['GET'])
def get_comments():
    return guests.get_comments()


@app.route('/movies', methods=['GET'])
def get_movies():
    return guests.get_movies()


@app.route('/movie/<id>', methods=['GET'])
def get_movie_info(id):
    return guests.get_movie_info(id)
