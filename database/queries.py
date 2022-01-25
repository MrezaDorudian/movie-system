CREATE_MOVIE_TABLE = """
    CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY,
    name TEXT,
    description TEXT,
    rating REAL 
    );
"""

CREATE_VOTE_TABLE = """
    CREATE TABLE IF NOT EXISTS votes (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    movie_id INTEGER,
    vote REAL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (movie_id) REFERENCES movies(id)
    );
    """

CREATE_COMMENT_TABLE = """
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
    """

CREATE_USER_TABLE = """
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    role INTEGER ,
    username TEXT,
    password TEXT
    );
    """

GET_MOVIE_COUNTS = """
    SELECT COUNT(*) FROM movies;
    """

ADD_MOVIE = """
    INSERT INTO movies (id, name, description, rating)
    VALUES (?, ?, ?, ?);
    """

UPDATE_MOVIE = """
    UPDATE movies
    SET name=?, description=?
    WHERE id=?;
    """

DELETE_MOVIE = """
    DELETE FROM movies
    WHERE id=?;
    """

GET_MOVIE_BY_NAME = """
    SELECT * FROM movies
    WHERE name=?;
    """

GET_MOVIE_BY_ID = """
    SELECT * FROM movies
    WHERE id=?;
    """

UPDATE_COMMENT = """
    UPDATE comments
    SET approved=?
    WHERE id=?;
    """

DELETE_COMMENT = """
    DELETE FROM comments
    WHERE id=?;
    """

GET_COMMENT_BY_ID = """
    SELECT * FROM comments
    WHERE id=?;
    """

GET_VOTE_COUNTS = """
    SELECT COUNT(*) FROM votes;
    """

CHECK_USER_VOTED_FOR_A_MOVIE = """
    SELECT * FROM votes
    WHERE user_id=? AND movie_id=?;
    """

GET_ALL_VOTES = """
    SELECT * FROM votes
    WHERE movie_id=?;
    """

UPDATE_RATING = """
    UPDATE movies
    SET rating=?
    WHERE id=?;
    """

ADD_VOTE = """
    INSERT INTO votes (id, user_id, movie_id, vote)
    VALUES (?, ?, ?, ?);
    """

GET_COMMENT_COUNTS = """
    SELECT COUNT(*) FROM comments;
    """

ADD_COMMENT = """
    INSERT INTO comments (id, user_id, movie_id, comment, approved, created_at)
    VALUES (?, ?, ?, ?, ?, ?);
    """

GET_USERNAME_BY_ID = """
    SELECT username FROM users
    WHERE id=?;
    """

GET_COMMENTS_BY_MOVIE_NAME = """
    SELECT * FROM comments
    WHERE movie_id IN (SELECT id FROM movies WHERE name=?);
    """

GET_ALL_MOVIES = """
    SELECT * FROM movies;
    """