import flask
from application import app
from database import sqliteDB


def add_movie():
    data = flask.request.get_json()
    auth = app.admin_auth_check()
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


def update_movie(id):
    request_data = flask.request.get_json()
    auth = app.admin_auth_check()
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


def delete_movie(id):
    auth = app.admin_auth_check()
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


def update_comment(id):
    request_data = flask.request.get_json()
    auth = app.admin_auth_check()
    if auth.status_code == 401:
        return auth
    try:
        if request_data['approved']:
            sqliteDB.update_comment(id, 1)
            return flask.make_response(flask.jsonify({}), 204)
        else:
            sqliteDB.update_comment(id, 0)
            return flask.make_response(flask.jsonify({}), 204)
    except KeyError:
        return flask.make_response(flask.jsonify({'message': 'missing data'}), 400)
    except TypeError:
        return flask.make_response(flask.jsonify({'message': 'invalid data'}), 400)
    except Exception as e:
        return flask.make_response(flask.jsonify({'message': str(e)}), 500)


def delete_comment(id):
    auth = app.admin_auth_check()
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