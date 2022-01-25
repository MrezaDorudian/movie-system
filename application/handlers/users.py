import flask
from application import app
from database import sqliteDB


def vote_movie():
    request_data = flask.request.get_json()
    auth = app.user_auth_check()
    if type(auth) == int:
        user_id = auth
    else:
        return auth

    try:
        if sqliteDB.movie_exist_by_id(request_data['movie_id']):
            if not sqliteDB.check_user_voted_for_a_movie(user_id, request_data['movie_id']):
                sqliteDB.vote_movie(user_id, request_data['movie_id'], request_data['vote'])
                return flask.make_response(flask.jsonify({}), 204)
            else:
                return flask.make_response(flask.jsonify({'message': 'this user already voted for this movie'}), 400)
        else:
            return flask.make_response(flask.jsonify({'message': 'movie does not exist'}), 400)
    except KeyError:
        return flask.make_response(flask.jsonify({'message': 'missing data'}), 400)
    except TypeError:
        return flask.make_response(flask.jsonify({'message': 'invalid data'}), 400)
    except Exception as e:
        return flask.make_response(flask.jsonify({'message': str(e)}), 500)


def insert_comment():
    request_data = flask.request.get_json()
    auth = app.user_auth_check()
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