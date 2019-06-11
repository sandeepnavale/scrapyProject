from scrapy.spiders import CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
import os
import logging
import json
from ..items import BbccrawlerItem


class BbcSpider(CrawlSpider):
    name = 'bbc'
    rules = []

    def __init__(self):
        self.ruleFile = json.load(open('Rules.json'))
        self.allowed_domains = self.ruleFile['allowed_domains']
        self.start_urls = self.ruleFile['start_urls']
        self.update_rules()
        self.update_urls_visited()
        super(BbcSpider, self).__init__()

    def update_rules(self):
        for r in self.ruleFile["rules"]:
            allowed = ()
            denied = ()
            restrict_xpaths_r = ()
            if 'allow' in r.keys():
                allowed = [a for a in r['allow']]
            if 'deny' in r.keys():
                denied = [d for d in r['deny']]
            if 'restrict_xpaths' in r.keys():
                restrict_xpaths_r = [rx for rx in r['restrict_xpaths']]

            BbcSpider.rules.append(Rule(
                LinkExtractor(
                    allow=allowed,
                    deny=denied,
                    restrict_xpaths=restrict_xpaths_r,
                ),
                follow=r['follow'],
                callback=r['callback']
            ))

    def update_urls_visited(self):
        visitedUrlFile = 'Output/visited_urls.txt'
        try:
            fileUrls = open(visitedUrlFile, 'r')
        except IOError:
            self.visitedUrls = []
        else:
            self.visitedUrls = [url.strip() for url in fileUrls.readlines()]
            fileUrls.close()
        finally:
            if not os.path.exists('Output/'):
                os.makedirs('Output/')
            self.urlFile = open(visitedUrlFile, 'a')

    def parseItems(self, response):
        if str(response.url) not in self.visitedUrls:
            try:
                logging.info('Parsing URL: ' + str(response.url))
                newsItem = BbccrawlerItem()
                hxs = scrapy.Selector(response)
                newsItem['newsUrl'] = response.url
                title = hxs.xpath(self.ruleFile['paths']['title'][0]).extract()[0]
                if title:
                    newsItem['newsHeadline'] = title.encode('ascii', 'ignore')
                newsItem['author'] = self.getAuthor(hxs)
                self.urlFile.write(str(response.url) + '\n')
                yield newsItem
            except Exception:
                pass

    def getAuthor(self, hxs):
        author = hxs.xpath(self.ruleFile['paths']['author'][0]).extract()
        if not author:
            author = hxs.xpath(self.ruleFile['paths']['author'][1]).extract()
        if author:
            return author[0].encode('ascii', 'ignore')
        else:
            return ''
