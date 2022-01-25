import sqlite3
from datetime import datetime
from queries import *

DB_NAME = 'sqliteDB.db'


def connect_db(query, args=None):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    if type(query) == str:
        cursor.execute(query, args)
    elif type(query) == list:
        for q in query:
            cursor.execute(q, args)
    connection.commit()
    connection.close()
    return cursor


def create_tables():
    connect_db([
        CREATE_MOVIE_TABLE,
        CREATE_VOTE_TABLE,
        CREATE_COMMENT_TABLE,
        CREATE_USER_TABLE
    ])


def movie_counts():
    return connect_db(GET_MOVIE_COUNTS).fetchone()[0]


def add_movie(name, description):
    connect_db(ADD_MOVIE, (movie_counts(), name, description, 0))


def update_movie(id, name, description):
    connect_db(UPDATE_MOVIE, (name, description, id))


def delete_movie(id):
    connect_db(DELETE_MOVIE, (id,))


def movie_exist_by_name(name):
    return True if connect_db(GET_MOVIE_BY_NAME, (name,)).fetchone() else False


def movie_exist_by_id(id):
    return True if connect_db(GET_MOVIE_BY_ID, (id,)).fetchone() else False


def get_movie_by_id(id):
    result = connect_db(GET_MOVIE_BY_ID, (id,)).fetchone()
    return {
        'id': result[0],
        'name': result[1],
        'description': result[2],
        'rating': result[3]
    }


def update_comment(id, is_approved):
    connect_db(UPDATE_COMMENT, (is_approved, id))


def delete_comment(id):
    connect_db(DELETE_COMMENT, (id,))


def comment_exist_by_id(id):
    return True if connect_db(GET_COMMENT_BY_ID, (id,)).fetchone() else False


def vote_counts():
    return connect_db(GET_VOTE_COUNTS).fetchone()[0]


def check_user_voted_for_a_movie(user_id, movie_id):
    return True if connect_db(CHECK_USER_VOTED_FOR_A_MOVIE, (user_id, movie_id)).fetchone() else False


def get_all_votes(movie_id):
    return connect_db(GET_ALL_VOTES, (movie_id,)).fetchall()


def update_rating(movie_id):
    all_votes = get_all_votes(movie_id)
    rating = [all_votes[i][-1] for i in range(len(all_votes))]
    average_rating = sum(rating) / len(rating)
    connect_db(UPDATE_RATING, (average_rating, movie_id,))


def vote_movie(user_id, movie_id, vote):
    connect_db(ADD_VOTE, (user_id, movie_id, vote))
    update_rating(movie_id)


def comment_counts():
    return connect_db(GET_COMMENT_COUNTS).fetchone()[0]


def insert_comment(user_id, movie_id, comment):
    connect_db(ADD_COMMENT, (comment_counts(), user_id, movie_id, comment, 0, datetime.now()))


def get_username_by_id(id):
    return connect_db(GET_USERNAME_BY_ID, (id,)).fetchone()[0]


def get_comments_by_movie_name(movie_name):
    result = connect_db(GET_COMMENTS_BY_MOVIE_NAME, (movie_name,)).fetchall()
    comments = {"comments": []}
    for item in result:
        comments["comments"].append({
            "id": item[0],
            "author": get_username_by_id(item[1]),
            "body": item[3],
        })
    return {
        "movie": movie_name,
        "comments": comments["comments"],
    }


def get_all_movies():
    result = connect_db(GET_ALL_MOVIES).fetchall()
    movies = []
    for row in result:
        movies.append({
            'id': row[0],
            'name': row[1],
            'description': row[2],
            'rating': row[3],
        })

    return {
        "movies": movies,
    }


create_tables()
