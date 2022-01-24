import sqlite3
from datetime import datetime


def create_tables():
    connection = sqlite3.connect('sqliteDB.db')
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY,
    name TEXT,
    description TEXT ,
    rating REAL 
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS votes (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    movie_id INTEGER,
    vote REAL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (movie_id) REFERENCES movies(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS comments (
    id INTEGER primary key,
    user_id INTEGER,
    movie_id INTEGER,
    comment TEXT,
    approved INTEGER DEFAULT 0,
    created_at TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (movie_id) REFERENCES movies(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    role INTEGER ,
    username TEXT,
    password TEXT
    );
    """)
    connection.commit()
    connection.close()


def movie_counts():
    connection = sqlite3.connect('sqliteDB.db')
    cursor = connection.cursor()
    cursor.execute("""
    SELECT COUNT(*) FROM movies;
    """)
    result = cursor.fetchone()
    connection.close()
    return result[0]


def add_movie(name, description):
    connection = sqlite3.connect('sqliteDB.db')
    cursor = connection.cursor()
    cursor.execute("""
    INSERT INTO movies (id, name, description, rating)
    VALUES (?, ?, ?, ?);
    """, (movie_counts(), name, description, 0))
    connection.commit()
    connection.close()


def update_movie(id, name, description):
    connection = sqlite3.connect('sqliteDB.db')
    cursor = connection.cursor()
    cursor.execute("""
    UPDATE movies
    SET name=?, description=?
    WHERE id=?;
    """, (name, description, id))
    connection.commit()
    connection.close()


def delete_movie(id):
    connection = sqlite3.connect('sqliteDB.db')
    cursor = connection.cursor()
    cursor.execute("""
    DELETE FROM movies
    WHERE id=?;
    """, (id,))
    connection.commit()
    connection.close()


def movie_exist_by_name(name):
    connection = sqlite3.connect('sqliteDB.db')
    cursor = connection.cursor()
    cursor.execute("""
    SELECT * FROM movies
    WHERE name=?;
    """, (name,))
    result = cursor.fetchone()
    connection.close()
    if result:
        return True
    else:
        return False


def movie_exist_by_id(id):
    connection = sqlite3.connect('sqliteDB.db')
    cursor = connection.cursor()
    cursor.execute("""
    SELECT * FROM movies
    WHERE id=?;
    """, (id,))
    result = cursor.fetchone()
    connection.close()
    if result:
        return True
    else:
        return False


def get_movie_by_id(id):
    connection = sqlite3.connect('sqliteDB.db')
    cursor = connection.cursor()
    cursor.execute("""
    SELECT * FROM movies
    WHERE id=?;
    """, (id,))
    result = cursor.fetchone()
    connection.close()
    return {
        'id': result[0],
        'name': result[1],
        'description': result[2],
        'rating': result[3]
    }


def approve_comment(id):
    connection = sqlite3.connect('sqliteDB.db')
    cursor = connection.cursor()
    cursor.execute("""
    UPDATE comments
    SET approved=1
    WHERE id=?;
    """, (id,))
    connection.commit()
    connection.close()


def disapprove_comment(id):
    connection = sqlite3.connect('sqliteDB.db')
    cursor = connection.cursor()
    cursor.execute("""
    UPDATE comments
    SET approved=0
    WHERE id=?;
    """, (id,))
    connection.commit()
    connection.close()


def delete_comment(id):
    connection = sqlite3.connect('sqliteDB.db')
    cursor = connection.cursor()
    cursor.execute("""
    DELETE FROM comments
    WHERE id=?;
    """, (id,))
    connection.commit()
    connection.close()


def comment_exist_by_id(id):
    connection = sqlite3.connect('sqliteDB.db')
    cursor = connection.cursor()
    cursor.execute("""
    SELECT * FROM comments
    WHERE id=?;
    """, (id,))
    result = cursor.fetchone()
    connection.close()
    if result:
        return True
    else:
        return False


def add_comment(id, user_id, movie_id, comment):
    connection = sqlite3.connect('sqliteDB.db')
    cursor = connection.cursor()
    cursor.execute("""
    INSERT INTO comments (id, user_id, movie_id, comment)
    VALUES (?, ?, ?, ?);
    """, (id, user_id, movie_id, comment))
    connection.commit()
    connection.close()


def vote_counts():
    connection = sqlite3.connect('sqliteDB.db')
    cursor = connection.cursor()
    cursor.execute("""
    SELECT COUNT(*) FROM votes;
    """)
    result = cursor.fetchone()
    connection.close()
    return result[0]


def vote_movie(user_id, movie_id, vote):
    connection = sqlite3.connect('sqliteDB.db')
    cursor = connection.cursor()
    cursor.execute("""
    INSERT INTO votes (id, user_id, movie_id, vote)
    VALUES (?, ?, ?, ?);
    """, (vote_counts(), user_id, movie_id, vote))
    connection.commit()
    connection.close()


def user_exist(id):
    connection = sqlite3.connect('sqliteDB.db')
    cursor = connection.cursor()
    cursor.execute("""
    SELECT * FROM users
    WHERE id=?;
    """, (id,))
    result = cursor.fetchone()
    connection.close()
    if result:
        return True
    else:
        return False


def comment_counts():
    connection = sqlite3.connect('sqliteDB.db')
    cursor = connection.cursor()
    cursor.execute("""
    SELECT COUNT(*) FROM comments;
    """)
    result = cursor.fetchone()
    connection.close()
    return result[0]


def insert_comment(user_id, movie_id, comment):
    connection = sqlite3.connect('sqliteDB.db')
    cursor = connection.cursor()
    cursor.execute("""
    INSERT INTO comments (id, user_id, movie_id, comment, approved, created_at)
    VALUES (?, ?, ?, ?, ?, ?);
    """, (comment_counts(), user_id, movie_id, comment, 0, datetime.now()))
    connection.commit()
    connection.close()


def get_username_by_id(id):
    connection = sqlite3.connect('sqliteDB.db')
    cursor = connection.cursor()
    cursor.execute("""
    SELECT username FROM users
    WHERE id=?;
    """, (id,))
    result = cursor.fetchone()
    connection.close()
    return result[0]


def get_comments_by_movie_name(movie_name):
    connection = sqlite3.connect('sqliteDB.db')
    cursor = connection.cursor()
    cursor.execute("""
    SELECT * FROM comments
    WHERE movie_id IN (SELECT id FROM movies WHERE name=?);
    """, (movie_name,))
    result = cursor.fetchall()
    connection.close()
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
    connection = sqlite3.connect('sqliteDB.db')
    cursor = connection.cursor()
    cursor.execute("""
    SELECT * FROM movies;
    """)
    result = cursor.fetchall()
    connection.close()
    movies = []
    for row in result:
        movies.append({
            'id': row[0],
            'name': row[1],
            'description': row[2],
            'rating': row[3],

        })

    return {
        "movies": movies
    }


def get_movie_info(name):
    connection = sqlite3.connect('sqliteDB.db')
    cursor = connection.cursor()
    cursor.execute("""
    SELECT * FROM movies
    WHERE name=?;
    """, (name,))
    result = cursor.fetchone()
    connection.close()
    info = {}
    print(result)
    if result:
        return {
            'name': result[1],
            'description': result[2],
            'rating': result[3]
        }
    else:
        return False


create_tables()
