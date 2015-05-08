class Projections:

    def __init__(self, database):
        self.conn = database.connection
        self.cursor = self.conn.cursor()

    def get_movie_projections(self, id_of_movie, date=None):
        get_proj_query = """
            SELECT id, type, projection_date, projection_time FROM projections
            WHERE movie_id = ?
        """

        parameters = [id_of_movie]
        if date:
            get_proj_query += " AND projection_date=?"
            parameters.append(date)

        self.cursor.execute(get_proj_query, tuple(parameters))
        return self.cursor.fetchall()

    def get_projection(self, projection_id):
        get_proj_query = """
            SELECT id, type, projection_date, projection_time FROM projections
            WHERE id = ?
        """

        self.cursor.execute(get_proj_query, (projection_id, ))
        return self.cursor.fetchone()

    def add_projection(self, movie_id, type, proj_date, proj_time):
        add_proj_query = """
            INSERT INTO projections(
                movie_id, type, projection_date, projection_time)
            VALUES(?, ?, ?, ?);
            """
        self.cursor.execute(
            add_proj_query, (movie_id, type, proj_date, proj_time))
        self.conn.commit()
