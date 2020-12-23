import unittest

from ImageDB.imagedb import ImageDB


class WidgetTestCase(unittest.TestCase):
    def setUp(self):
        self.image_db = ImageDB(db_id='test_account', user_id="test_db", password=None, query_cache=False)

    def test_default_widget_size(self):
        self.assertTrue(self.image_db.add_dataset('test'), 'incorrect default size')

    def test_widget_resize(self):
        self.assertTrue(self.image_db.add_image('test', 'image_test/19741_en_1.jpg'), 'wrong size after resize')