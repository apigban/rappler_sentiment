from __future__ import absolute_import
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import RapplerSpiderItem

from datetime import datetime


# from database.db_func import db_commit


class RapplerSpider(CrawlSpider):
    name = 'rapplerSpider'
    allowed_domains = ['apigban.com']
    start_urls = ['http://resume.apigban.com']

    rules = (Rule(LinkExtractor(), callback='parse_url', follow=False),)

    def parse_url(self, response):
        for link in LinkExtractor().extract_links(response):
            item = RapplerSpiderItem()
            item['url'] = link.url
            item['text'] = link.text
            item['fragment'] = link.fragment
            item['nofollow'] = link.nofollow
            item['source'] = link.url
            item['ismedia'] = 'no'
            item['status'] = 'unscraped'
            item['scrape_date'] = datetime.utcnow()
            print(item['url'])

            #            print(f'LINK: {item}')
            yield item
