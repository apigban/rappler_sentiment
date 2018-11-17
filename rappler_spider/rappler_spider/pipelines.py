# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# from scrapy_spider.models import QuoteDB, db_connect, create_table

from sqlalchemy.orm import sessionmaker

from .models import URLs, db_connect, create_table

from .proxy import scrapeProxy

import re
from tldextract import tldextract


class RunProxyScraperPipeline(object):
    """
    Runs proxyScraper.py to generate a fresh batch of proxy IPs
    """

    def start_proxy_generation(self, spider):
        scrapeProxy.main()


class StripWhitespacePipeline(object):
    """
    Strips leading and trailing whitespace from item['text']
    """

    def process_item(self, item, spider):
        item['text'] = item['text'].strip()
        return item


class URLCleanerPipeline(object):
    """
    Clean up url by
        - always start with "http://" or "https://"
        - remove element jumping
        - remove last '/'
    """

    def process_item(self, item, spider):

        # Deal with "http(s)://"
        if item['url'][0:4] != 'http':
            item['url'] = 'http://' + item['url']

        # Remove "#", seek url string for "#"
        idx = item['url'].find('#')
        if idx != -1:
            item['url'] = item['url'][:idx]

        # Remove last "/"
        urlLength = len(item['url'])
        if item['url'][urlLength - 1] == '/':
            item['url'] = item['url'][:urlLength - 1]

        return item


class GetDomainPipeline(object):
    """
    Get the domain of a given url
    """

    def process_item(self, item, spider):
        extractDomain = tldextract.extract(item['url']).domain
        extractSuffix = tldextract.extract(item['url']).suffix

        # item['source_domain'] = f'{extractDomain}.{extractSuffix}'
        item['url_domain'] = f'{extractDomain}.{extractSuffix}'
        return item


class CheckMediaPipeline(object):
    """
    Checks if item['url'] has a media filetype
    """

    def process_item(self, item, spider):

        if re.match(r'^.*\.(jpg|jpeg|gif|png|css|js|ico|xml|rss|txt|html).*$', item['url'], re.M | re.I):
            item['ismedia'] = 'true'
            return item
        else:
            item['ismedia'] = 'false'
            return item


class DBCommitPipeline(object):

    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """
        Save URLs in the database.

        This method is called for every item pipeline component.
        """
        session = self.Session()

        record = URLs()

        record.url = item['url']
        record.text = item['text']
        record.fragment = item['fragment']
        record.nofollow = item['nofollow']
        record.source_domain = item['source_domain']
        record.url_domain = item['url_domain']
        record.ismedia = item['ismedia']
        record.status = item['status']
        record.scrape_date = item['scrape_date']

        try:
            session.add(record)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
