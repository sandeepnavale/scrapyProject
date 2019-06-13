# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from   scrapy.conf import settings
import logging
import requests
import html2text
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
        # item['author'] = ','.join(article.authors)
        item['author'] = article.authors[0]
        item['newsHeadline'] = article.summary
        article.is_media_news()
        return item

#
class TextPipeline(object):
    def process_item(self,item, spider):
        try:
            response = requests.get(item['newsUrl'])
            # doc = Document(response.text)
            # content = Document(doc.content()).summary()
            # h = html2text.HTML2Text()
            # h.ignore_links = True
            # articleText = h.handle(content)
            # articleText = articleText.replace('\r', ' ').replace('\n', ' ').strip()
            # item['newsText'] = articleText
        except Exception:
            raise DropItem("Failed to extract article text from: " + item['newsUrl'])
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

