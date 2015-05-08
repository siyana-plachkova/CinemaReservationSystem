import sqlite3
from settings import *


class Projections:

    def __init__(self, DB_NAME):
        self.conn = sqlite3.connect(DB_NAME)
        self.cursor = self.conn.cursor()

    def show_movie_projection(self, id_of_movie):
        show_proj_query = """
            SELECT * FROM Projections
            WHERE movie_id = ?
            """
        return self.cursor.execute(show_proj_query, (id_of_movie, ))

    def add_projection(self, movie_id, type, proj_date, proj_time):
        add_proj_query = """
            INSERT INTO Projections(
                movie_id, type, projection_date, projection_time)
            VALUES(?, ?, ?, ?);
            """
        self.cursor.execute(
            add_proj_query, (movie_id, type, proj_date, proj_time))
        self.conn.commit()
tablename
    def make_all_hals(self):
        '''
            this will create matrix
            for every projection
            we will use this matrix
            for keep track of available seats
            and for printing the hall
            NOT FINISHED YET
        '''
        self.proj_halls = {}
        all_projections = self.cursor.execute('''SELECT id FROM Projections''')
        for elem in all_projections:
            matrix = []
            for i in range(HALL_ROWS):
                array = []
                for j in range(HALL_COLS):
                    array.append(".")
                matrix.append(array)
            self.proj_halls[elem[0]] = matrix
