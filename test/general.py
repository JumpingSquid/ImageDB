from ImageDB.imagedb import ImageDB

imagedb = ImageDB(db_id='postgres', user_id="postgres", password="", query_cache=False)
imagedb.add_dataset('img_test')
imagedb.add_image(dataset_id='img_test', filepath='C:/Users/user/PycharmProjects/ImageDB/image_test/19741_en_1.jpg')
