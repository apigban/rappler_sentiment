import scrapy
from scrapy.linkextractor import LinkExtractor
from database.db_func import dbCommit


class RapplerSpider(scrapy.Spider):
    name = 'rappler_spider'
    allowed_domains = ['www.rappler.com/']
    start_urls = ('https://www.rappler.com/',)

    def parse(self, response):
        extractor = LinkExtractor(allow_domains='rappler.com')
        links = extractor.extract_links(response)
        for link in links:
            dbCommit(link)
