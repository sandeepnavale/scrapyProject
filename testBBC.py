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

    def test_for_collection_entry(self):
        ''' testing for > 0 count for article collection'''
        db_len = self.collection.count()
        print("Testing Mongo DB for entries", db_len)
        self.assertGreater(db_len, 0)

    def test_for_author_entries(self):
        count_authors_identified = self.collection.count_documents(
            {"author": {
                "$ne": " "
            }})
        print(f'Identified {count_authors_identified} authors')
        self.assertGreater(count_authors_identified, 0)

    def test_for_url_entries(self):
        count_urls = self.collection.count_documents({"url": {"$ne": " "}})
        print(f'Identified {count_urls} urls')
        self.assertGreater(count_urls, 0)

    def test_for_headline_entries(self):
        count_headline = self.collection.count_documents(
            {"headline": {
                "$ne": " "
            }})
        print(f'Identified {count_headline} headlines')
        self.assertGreater(count_headline, 0)

    def test_for_article_entries(self):
        count_article = self.collection.count_documents(
            {"article": {
                "$ne": " "
            }})
        print(f'Identified {count_article} articles ')
        self.assertGreater(count_article, 0)


if __name__ == '__main__':
    unittest.main()
