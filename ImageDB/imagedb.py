"""
imagedb is one of the core services of ImageDB, it is responsible for insert image metadata into
PostgresSQL and export image file path.

To avoid extensive I/O, imagedb in default return the filepath but not the actual image.
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

        # scan all the dataset and check if there are missing files
        # it runs after establishing the query_cache as it will update the cache if needed
        # this will be useful in the future when query_cache is stored permanently
        self.image_db_scan()

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

    def get_image(self, dataset_id, image_id=None, file_name=None, refresh=False) -> list:
        """
        get image based on id or filename from a dataset
        :param dataset_id: the name of the dataset
        :param image_id: the id of the image
        :param file_name: the filename of the image
        :param refresh: skip the cache if true
        :return: [(image_id, filepath, filename, chksum), ...]
        """

        # if the cache function is turned on, then first find from the cache
        if self.query_cache_flag and ((dataset_id, image_id, file_name) in self.query_cache) and (not refresh):
            return self.query_cache[(dataset_id, image_id, file_name)]

        #
        assert image_id or file_name, 'Image id or the file name should provide at least one'
        cur = self.connector.get_cursor()
        if image_id:
            cur.execute(f"SELECT * FROM {dataset_id} WHERE image_id = {image_id}")
        elif file_name:
            cur.execute(f'SELECT * FROM {dataset_id} WHERE filename = {file_name}')

        query_result = cur.fetchall()

        # if the cache function is turned on, store the result
        if self.query_cache_flag:
            self.query_cache[('get_image', dataset_id, image_id, file_name)] = query_result

        return query_result

    def get_images(self, dataset_id, refresh=False) -> list:
        """
        get all images from a dataset based on the name of dataset
        :param dataset_id: the name of the dataset
        :param refresh: skip the cache if true
        :return: [(image_id, filepath, filename, chksum), ...]
        """

        # if the cache function is turned on, then first find from the cache
        if self.query_cache_flag and (('get_images', dataset_id) in self.query_cache) and (not refresh):
            return self.query_cache[('get_images', dataset_id)]

        # get all the image form a dataset
        cur = self.connector.get_cursor()
        cur.execute(f"SELECT * FROM {dataset_id};")
        query_result = cur.fetchall()

        # if the cache function is turned on, store the result
        if self.query_cache_flag:
            self.query_cache[('get_images', dataset_id)] = query_result

        return query_result

    def image_db_scan(self,
                      dataset_id: str = None,
                      image_id: str = None, file_name: str = None,
                      checksum: bool = False, refresh_query: bool = False):
        """
        scan the database and validate the data
        :param dataset_id:
        :param image_id:
        :param file_name:
        :param checksum:
        :param refresh_query:
        :return:
        """

        return
