from sqlalchemy import create_engine, Column, Table, ForeignKey, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Integer, SmallInteger, String, Date, DateTime, Float, Boolean, Text, LargeBinary)

from database.db_config import *

import datetime

DeclarativeBase = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(f'postgresql://{username}:{password}@{host}:{port}/{database}', echo=True)


def create_table(engine):
    DeclarativeBase.metadata.create_all(engine)


class URLs(DeclarativeBase):
    __tablename__ = 'urls'

    id = Column(Integer, Sequence('url_id_seq'), primary_key=True)
    url = Column('url', Text, unique=True)
    text = Column('text', Text, default='')
    source_domain = Column('source_domain', Text, default='')
    url_domain = Column('url_domain', Text, default='')
    ismedia = Column('ismedia', String(6), default='false')
    fragment = Column('fragment', Text, default='')  # no idea what fragment is
    nofollow = Column('nofollow', Text, default='')
    status = Column('status', String(10), default='unscraped')  # scraped, unscraped, unsuccessful
    scrape_date = Column('scrape_date', DateTime, default=datetime.datetime.utcnow)

    # def __init__(self, url, text, source, fragment, nofollow, status, scrape_date):
    #    self.url = url
    #    self.text = text
    #    self.source = source
    #    self.fragment = fragment
    #    self.nofollow = nofollow
    #    self.status = status
    #    self.scrape_date = scrape_date

    def __repr__(self):
        return f'<URL RECORD(url={self.url}, text={self.text}, status={self.status})>'
