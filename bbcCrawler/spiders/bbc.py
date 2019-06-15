import os
import logging
import json
from scrapy.spiders import CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from ..items import BbcCrawlerItem


# using CrawlSpider instead of scrapy.Spider
class BbcSpider(CrawlSpider):
    name = 'bbc'
    # https://docs.scrapy.org/en/latest/topics/spiders.html
    rules = []

    def __init__(self):
        # configure rules here.
        self.rule_file = json.load(open('Rules.json'))
        self.allowed_domains = self.rule_file['allowed_domains']
        self.start_urls = self.rule_file['start_urls']

        self.update_rules()
        # Avoid duplicates URL, by caching the already visited URL's
        self.update_urls_visited()

        super(BbcSpider, self).__init__()

    def update_rules(self):
        """
        update Rule objects. Each Rule defines a certain behaviour for crawling the site.
        If multiple rules match the same link, the first one will be used, according to
        the order they’re defined in this attribute.
        """
        for r in self.rule_file["rules"]:
            allowed = ()
            denied = ()
            restrict_xpaths_r = ()
            if 'allow' in r.keys():
                allowed = [a for a in r['allow']]
            if 'deny' in r.keys():
                denied = [d for d in r['deny']]
            if 'restrict_xpaths' in r.keys():
                restrict_xpaths_r = [rx for rx in r['restrict_xpaths']]

            BbcSpider.rules.append(
                Rule(
                    LinkExtractor(
                        allow=allowed,
                        deny=denied,
                        restrict_xpaths=restrict_xpaths_r,
                    ),
                    # follow is a boolean which specifies if links should be followed from each
                    # response extracted with this rule.
                    # Setting this to false in config, as it takes time to crawl.
                    follow=r['follow'],

                    # callback is a callable or a string (in which case a method from the spider
                    # object with that name will be used) to be called for each link extracted
                    # with the specified link_extractor. This callback receives a response as its
                    # first argument and must return a list containing Item and/or Request
                    # objects (or any subclass of them).
                    callback=r['callback']))

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

    def parse_items(self, response):
        if str(response.url) not in self.visitedUrls:
            try:
                logging.info('Parsing URL: ' + str(response.url))
                news_item = BbcCrawlerItem()
                news_item['url'] = response.url
                date = response.xpath(
                    '//div[@class="date date--v2"]/text()').extract()
                if len(date):
                    news_item['date'] = date[0]

                self.urlFile.write(str(response.url) + '\n')
                yield news_item
            except Exception as e:
                print(e)
