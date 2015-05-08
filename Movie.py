import sqlite3
from settings import *


class Movie:

    def __init__(self, DB_NAME):
        self.conn = sqlite3.connect(DB_NAME)
        self.cursor = self.conn.cursor()

    def add_movie(self, name, rating):
        add_movie_query = """
            INSERT INTO Movies(name, rating)
            VALUES(?, ?)
            """
        self.cursor.execute(add_movie_query)
        self.conn.commit()

    def show_movies(self):
        get_movies_query = """
            SELECT * FROM Movies
            ORDER BY rating
        """
        return self.cursor.execute(get_movies_query)

    def get_movie_by_id(self, movie_id):
        select_movie_query = """
            SELECT name FROM Movies
            WHERE id = ?
            """
        self.cursor.execute(select_movie_query, (movie_id, ))
