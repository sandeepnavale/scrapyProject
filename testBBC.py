import pymongo
import unittest


class TestBBC_DB(unittest.TestCase):
    ''' Test DB for entries from Scrapy crawl. should be > 0 '''

    def __init__(self, *args, **kwargs):
        ''' Init for Test cases'''
        super(TestBBC_DB, self).__init__(*args, **kwargs)
        self.connection = pymongo.MongoClient("localhost")
        self.db = self.connection['bbc_db']
        self.collection = self.db['articles']

    def test_for_articles_entry(self):
        ''' testing for > 0 count for article collection'''
        db_len = self.collection.count()
        print("Testing Mongo DB for entries", db_len)
        self.assertGreater(db_len, 0)


if __name__ == '__main__':
    unittest.main()
