import psycopg2
import time


class Connector:

    def __init__(self, db_id, user_id):
        self.db = None
        self.db_id = db_id
        self.user_id = user_id
        self.timer = None
        self.status = None
        self.status_map = {1: "connect", 0: "disconnect"}

    def connect(self, dbname=None, user=None):
        try:
            if dbname and user:
                self.db = psycopg2.connect(f'dbname={dbname} username={user}')
            else:
                self.db = psycopg2.connect(f'dbname={self.db_id} username={self.user_id}')
        except ValueError:
            print('Wrong database name or username')
        finally:
            # log the error
            pass

        self.timer = time.time()

    def isconnect(self):
        return self.status == 1

    def get_cursor(self) -> psycopg2._psycopg.cursor:
        return self.db.cursor()

    def db_commit(self):
        self.db.commit()

