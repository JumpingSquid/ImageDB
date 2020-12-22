"""
Connector is an interface to communicate between ImageDB core and PostgresSQL database.
The connector will handle any execution related to PostgresSQL but itself does not produce any
execution unless called by other modules (passive service).
"""

import psycopg2
import time


class Connector:

    def __init__(self, db_id, user_id, password):
        self.db = None
        self.db_id = db_id
        self.user_id = user_id
        self.password = password
        self.timer = None
        self.status = None
        self.status_map = {1: "connect", 0: "disconnect"}

    def connect(self, dbname=None, user=None, password=None):
        try:
            if dbname and user and password:
                self.db = psycopg2.connect(f'dbname={dbname} user={user} password={password}')
            elif dbname:
                self.db = psycopg2.connect(f'dbname={dbname}')
            else:
                self.db = psycopg2.connect(f'dbname={self.db_id} user={self.user_id} password={self.password}')
        except ValueError:
            print('Wrong database name or username')
        finally:
            # log the error
            pass

        self.status = 1
        self.timer = time.time()

    def isconnect(self):
        return self.status == 1

    def get_cursor(self) -> psycopg2._psycopg.cursor:
        return self.db.cursor()

    def db_commit(self):
        self.db.commit()

