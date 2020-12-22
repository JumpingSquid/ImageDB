"""
imagedb is one of the core services of ImageDB, it is responsible for insert image metadata into
PostgresSQL and retrieve image data.
"""

import cv2
import os
import hashlib
import io

from PIL import Image
from ImageDB.connector import Connector


class ImageDB:

    def __init__(self, db_id, user_id):
        self.connector = Connector(db_id=db_id, user_id=user_id)

    def add_imgtable(self, table_name):
        cur = self.connector.get_cursor()
        cur.execute(f"CREATE TABLE {table_name} (id serial PRIMARY KEY,"
                    f" filepath varchar , filename varchar, chksum varchar );")

    def add_image(self, filepath, checksum=False):
        # assert the file existence
        # default to close the checksum mechanism to avoid long processed time

        if ~self.connector.isconnect():
            self.connector.connect()

        assert os.path.isdir(filepath), "The file not exists"

        filename = filepath.split("/")[-1]
        table_name = self.connector.db_id
        cur = self.connector.get_cursor()

        # create MD5 for image file
        img_checksum = None
        if checksum:
            img_checksum = self.image_hashmap(file_path=filepath)
        cur.execute(f"INSERT INTO {table_name} (filepath, filename, chksum)"
                    f" VALUES ({filepath}, {filename}, {img_checksum})")

    @staticmethod
    def image_hashmap(file_path):
        assert os.path.isfile(file_path)
        md5hash = hashlib.md5(Image.open(file_path).tobytes())
        return md5hash

    def get_image(self):
        cur = self.connector.get_cursor()
        cur.execute("")

    def get_images(self):
        cur = self.connector.get_cursor()
        cur.execute("")