# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.conf import settings
import logging
from newspaper import Article


class BbccrawlerPL(object):
    def process_item(self, item, spider):
        return item


class NewsTextPL(object):
    ''' Pipeline to process News Articles '''
    def process_item(self, item, spider):
        article = Article(item['url'])  # using Newspaper3k, instead of "Readability"
        article.download()
        article.parse()
        item['article'] = article.text
        if len(article.authors):
            item['author'] = article.authors[0]
        else:
            item['author'] = " "
        item['headline'] = article.title
        item['date'] = article.publish_date

        return item


class MongoPL(object):
    """ Mongo DB pipeline"""
    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if ((data == 'url' or data == 'headline' or data == 'article' or data == 'author')
                    and not data
            ):
                valid = False
                raise DropItem('News Item dropped, missing ' + data)
        if valid:
            self.collection.insert(dict(item))
            logging.info('News Article inserted to MongoDB')
        return item


class DropIfEmptyPipeline(object):
    def process_item(self, item, spider):
        if ((not item['headline']) or (not item['url'])
             or (not item['article']) or (not item['author'])):
            raise DropItem()
        else:
            return item
