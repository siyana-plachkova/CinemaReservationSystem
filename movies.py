class Movies:

    def __init__(self, database):
        self.conn = database.connection
        self.cursor = self.conn.cursor()

    def add_movie(self, name, rating):
        add_movie_query = """
            INSERT INTO movies(name, rating)
            VALUES(?, ?)
            """
        self.cursor.execute(add_movie_query)
        self.conn.commit()

    def get_movies(self):
        get_movies_query = """
            SELECT * FROM movies
            ORDER BY rating DESC
        """
        return self.cursor.execute(get_movies_query)

    def get_movie_by_id(self, movie_id):
        select_movie_query = """
            SELECT name, rating FROM movies
            WHERE id = ?
            """
        self.cursor.execute(select_movie_query, (movie_id, ))

        return self.cursor.fetchone()
