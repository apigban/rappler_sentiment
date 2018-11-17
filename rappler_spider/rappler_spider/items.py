# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class URLItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    text = scrapy.Field()
    fragment = scrapy.Field()
    status = scrapy.Field()
    source_domain = scrapy.Field()
    ismedia = scrapy.Field()
    scrape_date = scrapy.Field()
    nofollow = scrapy.Field()
    url_domain = scrapy.Field()
    pass
