import flask
from database import sqliteDB


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


def get_movies():
    try:
        movies = sqliteDB.get_all_movies()
        return flask.make_response(flask.jsonify(movies), 200)
    except Exception as e:
        return flask.make_response(flask.jsonify({'message': str(e)}), 500)


def get_movie_info(id):
    try:
        if sqliteDB.movie_exist_by_id(id):
            movie = sqliteDB.get_movie_by_id(id)
            return flask.make_response(flask.jsonify(movie), 200)
        else:
            return flask.make_response(flask.jsonify({'message': 'movie does not exist'}), 400)
    except Exception as e:
        return flask.make_response(flask.jsonify({'message': str(e)}), 500)