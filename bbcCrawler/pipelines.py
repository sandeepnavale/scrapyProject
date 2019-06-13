# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from   scrapy.conf import settings
import logging
import requests
import newspaper

class BbccrawlerPL(object):
    def process_item(self, item, spider):
        return item
class NewsTextPL(object):
    def process_item(self,item,spider):
        article = newspaper.Article(item['newsUrl'])
        article.download()
        article.parse()
        item['newsText'] = article.text
        item['author'] = article.authors[0]
        item['newsHeadline'] = article.title
        return item

class MongoPL(object):
    def __init__(self):
        connection = pymongo.MongoClient(
            # settings['MONGODB_URI']
            settings['MONGODB_SERVER']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if ((data == 'newsUrl' or data == 'newsHeadline' or data == 'newsText'
                 or data == 'author') and not data):
                valid = False
                raise DropItem('News Item dropped, missing ' + data)
        if valid:
            self.collection.insert(dict(item))
            logging.info('News Article inserted to MongoDB database!')
        return item

