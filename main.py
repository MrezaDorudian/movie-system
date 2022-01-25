from application.app import get_app
from database import sqliteDB
import os


def start_db():
    if not os.path.exists('database/database.db'):
        sqliteDB.create_tables()
        print('database created')


def start_app():
    get_app().run(host='0.0.0.0', port=8080)


if __name__ == '__main__':
    start_db()
    start_app()
