import unittest

from ImageDB.imagedb import ImageDB


class WidgetTestCase(unittest.TestCase):
    def setUp(self):
        self.image_db = ImageDB(db_id='test_db', user_id="test_account", password="test", query_cache=False)

    def test_add_image(self):
        self.assertTrue(self.image_db.add_dataset('test'), 'fail to add the dataset')

    def test_add_test(self):
        self.assertTrue(self.image_db.add_dataset('test'), 'fail to add the dataset')
        self.assertTrue(self.image_db.add_image('test',
                                                'C:/Users/user/PycharmProjects/ImageDB/image_test/19741_en_1.jpg',
                                                True),
                        'fail to add the image')
