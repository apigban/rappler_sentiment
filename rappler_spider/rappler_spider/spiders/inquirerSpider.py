from __future__ import absolute_import
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import URLItem

from datetime import datetime


class InquirerSpider(CrawlSpider):
    name = 'inquirerSpider'
    allowed_domains = ['inquirer.com']
    start_urls = ['https://www.inquirer.net']

    rules = (Rule(LinkExtractor(), callback='parse_url', follow=False),)

    def parse_url(self, response):
        """
        Extracts all URLs from variable start_urls
        Populates item class with scrapy.link.Link object attrs
        yields item to pipelines.py per item
        :param response:
        """
        for link in LinkExtractor().extract_links(response):
            item = URLItem()
            item['url'] = link.url
            item['text'] = link.text
            item['fragment'] = link.fragment
            item['nofollow'] = link.nofollow
            item['source'] = link.url
            item['ismedia'] = 'no'
            item['status'] = 'unscraped'
            item['scrape_date'] = datetime.utcnow()
            yield item
