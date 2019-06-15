# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BbccrawlerItem(scrapy.Item):
    headline = scrapy.Field()
    url = scrapy.Field()
    article = scrapy.Field()
    author = scrapy.Field()
    date = scrapy.Field()
