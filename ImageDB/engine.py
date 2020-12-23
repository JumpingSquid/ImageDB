"""
ImageDB engine
"""

import threading
import time

from ImageDB.connector import Connector


class Engine(threading.Thread):
    def __init__(self, connector: Connector):
        threading.Thread.__init__(self)
        self.connector = connector
        self.update_counter = 0
        self.refresh_frequency = 30
        self.status = 0

    def run(self):
        self.status = 1
        while self.status == 1:
            self.image_db_scan()
            self.image_db_commit()
            time.sleep(self.refresh_frequency)

    def close(self):
        self.status = 0

    def image_db_scan(self):
        # scan all the dataset and check if there are missing files
        # it runs after establishing the query_cache as it will update the cache if needed
        # this will be useful in the future when query_cache is stored permanently
        self.update_counter += 1
        print('auto scan completed')
        return

    def image_db_commit(self):
        self.connector.db_commit()
        print('auto database commit completed')
        return


class ImgSys:
    def __init__(self, connector):
        self.connector = connector
        self.engine = Engine(connector)
        self.last_update_time = None

    def get_time(self):
        update_time = self.engine.update_counter
        print(update_time)
        self.last_update_time = update_time

    def start_engine(self):
        self.engine = Engine(self.connector)
        if self.last_update_time:
            self.engine.update_counter = self.last_update_time
        self.engine.start()

    def end_engine(self):
        self.engine.close()

