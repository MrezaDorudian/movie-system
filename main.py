import sqlite3
from datetime import timedelta

import flask
import sqliteDB
import jwt

ADMIN_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhY2Nlc3NfbGV2ZWwiOiJhZG1pbiJ9.dtLqN1M1-xMMC98TSy70Z0sVn5z_ctq8j9oj6Z_4S3c'

app = flask.Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)


def admin_auth_check():
    try:
        token = flask.request.headers['Authorization'].split(' ')[1]
        if token != ADMIN_TOKEN:
            return flask.make_response(flask.jsonify({'message': 'unauthorized'}), 401)
    except KeyError:
        return flask.make_response(flask.jsonify({'message': 'unauthorized'}), 401)


# ==================================== admin handlers start ====================================
@app.route('/admin/movie', methods=['POST'])
def add_movie():
    data = flask.request.get_json()
    auth = admin_auth_check()
    if auth.status_code == 401:
        return auth
    try:
        if sqliteDB.movie_exist_by_name(data['name']):
            return flask.make_response(flask.jsonify({'message': 'movie already exist'}), 400)
        else:
            sqliteDB.add_movie(data['name'], data['description'])
        return flask.make_response({}, 204)
    except KeyError:
        return flask.make_response(flask.jsonify({'message': 'missing data'}), 400)
    except TypeError:
        return flask.make_response(flask.jsonify({'message': 'invalid data'}), 400)
    except Exception as e:
        return flask.make_response(flask.jsonify({'message': str(e)}), 500)


@app.route('/admin/movie/<id>', methods=['PUT'])
def update_movie(id):
    request_data = flask.request.get_json()
    auth = admin_auth_check()
    if auth.status_code == 401:
        return auth
    try:
        if sqliteDB.movie_exist_by_id(id):
            sqliteDB.update_movie(id, request_data['name'], request_data['description'])
            return flask.make_response(flask.jsonify({}), 204)
        else:
            return flask.make_response(flask.jsonify({'message': 'movie does not exist'}), 400)
    except KeyError:
        return flask.make_response(flask.jsonify({'message': 'missing data'}), 400)
    except TypeError:
        return flask.make_response(flask.jsonify({'message': 'invalid data'}), 400)
    except Exception as e:
        return flask.make_response(flask.jsonify({'message': str(e)}), 500)


@app.route('/admin/movie/<id>', methods=['DELETE'])
def delete_movie(id):
    auth = admin_auth_check()
    if auth.status_code == 401:
        return auth
    try:
        if sqliteDB.movie_exist_by_id(id):
            sqliteDB.delete_movie(id)
            return flask.make_response(flask.jsonify({}), 204)
        else:
            return flask.make_response(flask.jsonify({'message': 'movie does not exist'}), 400)
    except Exception as e:
        return flask.make_response(flask.jsonify({'message': str(e)}), 500)


@app.route('/admin/comments/<id>', methods=['PUT'])
def manage_comments(id):
    request_data = flask.request.get_json()
    auth = admin_auth_check()
    if auth.status_code == 401:
        return auth
    try:
        if request_data['approved']:
            sqliteDB.approve_comment(id)
            return flask.make_response(flask.jsonify({}), 204)
        else:
            sqliteDB.disapprove_comment(id)
            return flask.make_response(flask.jsonify({}), 204)
    except KeyError:
        return flask.make_response(flask.jsonify({'message': 'missing data'}), 400)
    except TypeError:
        return flask.make_response(flask.jsonify({'message': 'invalid data'}), 400)
    except Exception as e:
        return flask.make_response(flask.jsonify({'message': str(e)}), 500)


@app.route('/admin/comments/<id>', methods=['DELETE'])
def delete_comment(id):
    auth = admin_auth_check()
    if auth.status_code == 401:
        return auth
    try:
        if sqliteDB.comment_exist_by_id(id):
            sqliteDB.delete_comment(id)
            return flask.make_response(flask.jsonify({}), 204)
        else:
            return flask.make_response(flask.jsonify({'message': 'comment does not exist'}), 400)
    except Exception as e:
        return flask.make_response(flask.jsonify({'message': str(e)}), 500)


# ==================================== admin handlers end ====================================


def user_auth_check():
    try:
        token = flask.request.headers['Authorization'].split(' ')[1]
        decoded_token = jwt.decode(token, '', algorithms=['HS256'])
        access_level = decoded_token['access_level']
        user_id = decoded_token['user_id']
    except KeyError:
        return flask.make_response(flask.jsonify({'message': 'unauthorized'}), 401)
    if access_level != 'user':
        return flask.make_response(flask.jsonify({'message': 'unauthorized'}), 401)
    return int(user_id)

# ==================================== normal users handlers start ====================================
@app.route('/user/vote', methods=['POST'])
def vote_movie():
    request_data = flask.request.get_json()
    auth = user_auth_check()
    if type(auth) == int:
        user_id = auth
    else:
        return auth

    try:
        if sqliteDB.movie_exist_by_id(request_data['movie_id']):
            sqliteDB.vote_movie(user_id, request_data['movie_id'], request_data['vote'])  # bug here
            return flask.make_response(flask.jsonify({}), 204)
        else:
            return flask.make_response(flask.jsonify({'message': 'movie does not exist'}), 400)
    except KeyError:
        return flask.make_response(flask.jsonify({'message': 'missing data'}), 400)
    except TypeError:
        return flask.make_response(flask.jsonify({'message': 'invalid data'}), 400)
    except Exception as e:
        return flask.make_response(flask.jsonify({'message': str(e)}), 500)


@app.route('/user/comment', methods=['POST'])
def insert_comment():
    request_data = flask.request.get_json()
    auth = user_auth_check()
    if type(auth) == int:
        user_id = auth
    else:
        return auth
    try:
        if sqliteDB.movie_exist_by_id(request_data['movie_id']):
            sqliteDB.insert_comment(user_id, request_data['movie_id'], request_data['comment_body'])  # bug here
            return flask.make_response('', 200)
        else:
            return flask.make_response(flask.jsonify({'message': 'movie does not exist'}), 400)
    except KeyError:
        return flask.make_response(flask.jsonify({'message': 'missing data'}), 400)
    except TypeError:
        return flask.make_response(flask.jsonify({'message': 'invalid data'}), 400)
    except Exception as e:
        return flask.make_response(flask.jsonify({'message': str(e)}), 500)


# ==================================== normal users handlers end ====================================

# ==================================== guest users handlers start ====================================
@app.route('/comments', methods=['GET'])
def get_comments():
    query_parameters = flask.request.args
    movie_name = query_parameters.get('movie')
    try:
        if movie_name:
            if sqliteDB.movie_exist_by_name(movie_name):
                comments = sqliteDB.get_comments_by_movie_name(movie_name)
                return flask.make_response(flask.jsonify(comments), 200)
            else:
                return flask.make_response(flask.jsonify({'message': 'movie does not exist'}), 400)
        else:
            return flask.make_response(flask.jsonify({'message': 'missing data'}), 400)
    except Exception as e:
        return flask.make_response(flask.jsonify({'message': str(e)}), 500)


@app.route('/movies', methods=['GET'])
def get_all_movies():
    try:
        movies = sqliteDB.get_all_movies()
        return flask.make_response(flask.jsonify(movies), 200)
    except Exception as e:
        return flask.make_response(flask.jsonify({'message': str(e)}), 500)


@app.route('/movie/<id>', methods=['GET'])
def get_movie_info(id):
    try:
        if sqliteDB.movie_exist_by_id(id):
            movie = sqliteDB.get_movie_by_id(id)
            return flask.make_response(flask.jsonify(movie), 200)
        else:
            return flask.make_response(flask.jsonify({'message': 'movie does not exist'}), 400)
    except Exception as e:
        return flask.make_response(flask.jsonify({'message': str(e)}), 500)


# ==================================== guest users handlers end ====================================

app.run(debug=True, host='localhost', port=80)
