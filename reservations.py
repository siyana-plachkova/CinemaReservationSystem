from settings import HALL_COLS, HALL_ROWS


class Reservations:

    def __init__(self, database):
        self.conn = database.connection
        self.cursor = self.conn.cursor()

    def add_reservation(self, username, projection_id, row, col):
        add_reserve_query = """
            INSERT INTO reservations(
                username, projection_id, row, col)
            VALUES(?, ?, ?, ?);
            """
        self.cursor.execute(
            add_reserve_query, (username, projection_id, row, col))
        self.conn.commit()

    def get_reservations(self, username):
        sql = """
            SELECT id, projection_id, row, col FROM reservations
            WHERE username = ?
        """

        self.cursor.execute(sql, (username, ))
        return self.cursor.fetchall()

    def delete_reservation(self, name, projection_id):
        sql = """
            DELETE FROM reservations WHERE username = ? AND projection_id = ?
        """

        self.cursor.execute(sql, (name, projection_id))
        self.conn.commit()

    def make_hall(self, projection_id):
        self.proj_halls = {}
        sql = """
            SELECT row, col FROM reservations WHERE projection_id = ?
        """
        self.cursor.execute(sql, (projection_id, ))
        all_reservations = self.cursor.fetchall()
        matrix = []
        for i in range(HALL_ROWS):
            array = []
            for j in range(HALL_COLS):
                if (i + 1, j + 1) in all_reservations:
                    array.append("X")
                else:
                    array.append(".")
            matrix.append(array)
        return matrix
