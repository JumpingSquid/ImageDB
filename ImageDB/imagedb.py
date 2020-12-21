import psycopg2
import cv2
import os

from ImageDB.connector import Connector


class ImageDB:

    def __init__(self, db_id, user_id):
        self.connector = Connector(db_id=db_id, user_id=user_id)

    def add_imgtable(self, table_name):
        cur = self.connector.get_cursor()
        cur.execute(f"CREATE TABLE {table_name} (id serial PRIMARY KEY,"
                    f" filepath varchar , filename varchar, chksum varchar );")

    def add_image(self, filepath):
        # assert the file existence
        # TODO: checksum for image

        if ~self.connector.isconnect():
            self.connector.connect()

        assert os.path.isdir(filepath), "The file not exists"

        filename = filepath.split("/")[-1]
        table_name = self.connector.db_id
        cur = self.connector.get_cursor()
        cur.execute("INSERT INTO {table_name} (filepath, filename, chksum) VALUES ({filepath}, {filename}, None)")
