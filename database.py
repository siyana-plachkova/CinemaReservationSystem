import sqlite3
from settings import DB_NAME


class Database:

    def __init__(self):
        self._connection = sqlite3.connect(DB_NAME)

    @property
    def connection(self):
        return self._connection

    def close(self):
        self._connection.close()
