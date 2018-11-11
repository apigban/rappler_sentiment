from sqlalchemy import create_engine, Column, Text, Integer
from sqlalchemy.ext.declarative import declarative_base
from database.db_config import *

Base = declarative_base()


class Links(Base):
    __tablename__ = 'links'

    id = Column('id', Integer, primary_key=True)
    links = Column('links', Text, unique=True)

    def __init__(self, links):
        self.links = links


engine = create_engine(f'postgresql://{username}:{password}@{host}:{port}/{database}', echo=True)
