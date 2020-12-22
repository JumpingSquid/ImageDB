"""
imagedb is one of the core services of ImageDB, it is responsible for insert image metadata into
PostgresSQL and retrieve image data.

To avoid extensive I/O, imagedb in default return the filepath but not the actual image (perhaps in a np.array form).
"""

import cv2
import os
import hashlib
import io

from PIL import Image
from ImageDB.connector import Connector


class ImageDB:

    def __init__(self, db_id: str, user_id: str, query_cache: bool):
        self.connector = Connector(db_id=db_id, user_id=user_id)

        if ~self.connector.isconnect():
            self.connector.connect()

        # query_cache function is to store the query result
        # in the future, this might need to implement by using Memcache
        # now it only stores in the memory and lose the information once restarted
        self.query_cache_flag = query_cache
        self.query_cache = {}

    def add_dataset(self, dataset_id):
        # dataset is a collection of image files
        cur = self.connector.get_cursor()

        # currently the schema of a dataset will store the information of
        # image file with id, filepath, filename, and chksum
        cur.execute(f"CREATE TABLE {dataset_id} (image_id serial PRIMARY KEY,"
                    f" filepath varchar , filename varchar, chksum varchar );")

    def add_image(self, filepath, checksum=False):
        # assert the file existence
        # default to close the checksum mechanism to avoid long processed time

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

    def get_image(self, dataset_id, image_id=None, file_name=None):

        # if the cache function is turned on, then first find from the cache
        if self.query_cache_flag and ((dataset_id, image_id, file_name) in self.query_cache):
            return self.query_cache[(dataset_id, image_id, file_name)]

        # get image based on id or filename from a dataset
        assert image_id or file_name, 'Image id or the file name should provide at least one'
        cur = self.connector.get_cursor()
        if image_id:
            cur.execute(f"SELECT * FROM {dataset_id} WHERE image_id = {image_id}")
        elif file_name:
            cur.execute(f'SELECT * FROM {dataset_id} WHERE filename = {file_name}')

        query_result = cur.fetchall()
        if self.query_cache_flag:
            self.query_cache[(dataset_id, image_id, file_name)] = query_result

        return query_result

    def get_images(self, dataset_id):
        # get all the image form a dataset
        cur = self.connector.get_cursor()
        cur.execute(f"SELECT * FROM {dataset_id};")
        return cur.fetchall()
