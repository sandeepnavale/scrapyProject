# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from   scrapy.conf import settings
import logging

class BbccrawlerPipeline(object):
    def process_item(self, item, spider):
        return item



class MongoDBPipeline(object):

    collection_name = 'tc_posts'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'tc_scraper')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item



#
#
# class MongoDBPipeline(object):
#     # def __init__(self):
#     #     connection = pymongo.MongoClient(
#     #         # settings['MONGODB_URI']
#     #         settings['MONGODB_SERVER'],
#     #         settings['MONGODB_PORT']
#     #     )
#     #     db = connection[settings['MONGODB_DB']]
#     #     self.collection = db[settings['MONGODB_COLLECTION']]
#     collection_name = 'scrapy_items'
#
#     def __init__(self, mongo_uri, mongo_db):
#         self.mongo_uri = mongo_uri
#         self.mongo_db = mongo_db
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         return cls(
#             mongo_uri=crawler.settings.get('MONGO_URI'),
#             mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
#         )
#
#     def open_spider(self, spider):
#         self.client = pymongo.MongoClient(self.mongo_uri)
#         self.db = self.client[self.mongo_db]
#
#     def close_spider(self, spider):
#         self.client.close()
#
#     def process_item(self, item, spider):
#         # print("SANDEEP NL " * 10)
#         # self.db[self.collection_name].insert_one(dict(item))
#         # return item
#
#         valid = True
#         for data in item:
#             if ((data == 'newsUrl' or data == 'newsHeadline' or data == 'newsText'
#                  or data == 'author') and not data):
#                 valid = False
#                 raise DropItem('News Item dropped, missing ' + data)
#         if valid:
#             self.collection.insert(dict(item))
#             logging.info('News Article inserted to MongoDB database!')
#         return item
#
#
#     #
#     # def process_item(self, item, spider):
#     #     print("HELLO MONGO")
#     #     valid = True
#     #     for data in item:
#     #         if ((data == 'newsUrl' or data == 'newsHeadline' or data == 'newsText'
#     #              or data == 'author') and not data):
#     #             valid = False
#     #             raise DropItem('News Item dropped, missing ' + data)
#     #     if valid:
#     #         self.collection.insert(dict(item))
#     #         logging.info('News Article inserted to MongoDB database!')
#     #     return item
