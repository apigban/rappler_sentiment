from sqlalchemy import create_engine, Column, Sequence, Text, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from database.db_config import *
import datetime

Base = declarative_base()


class URLs(Base):
    __tablename__ = 'urls'

    id = Column(Integer, Sequence('url_id_seq'), primary_key=True)
    url = Column('url', Integer, unique=True)
    text = Column('links', Text, default='')
    fragment = Column('fragment', Text, default='')  # no idea what fragment is
    status = Column('status', String(10), default='unscraped')  # scraped, unscraped, unsuccessful
    scrape_date = Column('scrape_date', DateTime, default=datetime.datetime.utcnow)

    def __init__(self, url, text, fragment, status, scrape_date):
        self.url = url
        self.text = text
        self.fragment = fragment
        self.status = status
        self.scrape_date = scrape_date

    def __repr__(self):
        return f'<URL RECORD(url={self.url}, text={self.text}, status={self.status})>'


class RapplerURLs(Base):
    __tablename__ = 'rapplerurls'

    id = Column('id', Integer, Sequence('rappler_url_sequence'), primary_key=True)
    rappler_url_id = Column(Integer, ForeignKey('urls.id'))
    rappler_url = relationship('url')
    html_as_string = Column('full_HTML', Text, default='')
    newsdesk = Column('newsdesk', String(15), default='')
    tags = Column('tags', Text, default='')
    label = Column('label', Text, default='')
    headline = Column('headline', String(250), default='')
    wordcount = Column('wordcount', Integer, default=0)
    pubDate = Column(DateTime, default=datetime.datetime.utcnow)
    upDate = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, rappler_url_id, rappler_url, scrape_date, html_as_string, newsdesk, tags, label, headline,
                 wordcount, pubDate, upDate):
        self.rappler_url_id = rappler_url_id
        self.rappler_url = rappler_url
        self.html_as_string = html_as_string
        self.newsdesk = newsdesk
        self.tags = tags
        self.label = label
        self.headline = headline
        self.wordcount = wordcount
        self.scrape_date = scrape_date
        self.pubDate = pubDate
        self.upDate = upDate

    def __repr__(self):
        return f'<RapplerLink(newsdesk={self.newsdesk}, words={self.wordcount}, status={self.status})>'


engine = create_engine(f'postgresql://{username}:{password}@{host}:{port}/{database}', echo=True)
