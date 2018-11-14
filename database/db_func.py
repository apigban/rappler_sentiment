# !/usr/bin/env python3.7

from datetime import datetime as dt

from sqlalchemy.orm import sessionmaker
import log.log as log

from database.db_base import Base, engine, URLs, RapplerURLs

dbLogger = log.get_logger(__name__)

dateFormat = "%Y-%m-%d"

Base.metadata.create_all(engine, checkfirst=True)
DBSession = sessionmaker(bind=engine)
session = DBSession()


def recentRecords(TableName):
    """
    search db table for dynamic column, return max 1000
    'recentResult' is a list
    if no table is present from db, return an empty list
    ###SQL QUERY:
    SELECT composite FROM table
    ORDER BY id DESC
    """

    records = []

    dbRecords = session.query(TableName).order_by(TableName.id.desc()).limit(1000).all()
    #    dbRecords = session.query(f'{TableName}').order_by(f'{TableName}'.id.desc()).limit(1000).all()

    for item in dbRecords:
        records.append(item.links)
        print()
    return records


def db_rappler_commit(link):
    """
     search db table for dynamic column, return max 1000
     'recentResult' is a list
     if no table is present from db, return an empty list
     ###SQL QUERY:
     SELECT composite FROM table
     ORDER BY id DESC
     """
    newLink = RapplerLinks(link)

    recentDBRecords = recentRecords(RapplerLinks)

    if newLink.links in recentDBRecords:
        dbLogger.warn(
            f'DUPLICATE Link found. No Commit Done. LINK: {link}')
    else:
        dbLogger.info(
            f'NEW LINK: {link} Committing draw object to DB...')
        session.add(newLink)
        session.commit()
        dbLogger.info(f'Commit Done.')
        session.close()

    dbLogger.info(f'Session Closed')

    return link


def db_commit(table, content):
    """
         search db table for dynamic column, return max 1000
         'recentResult' is a list
         if no table is present from db, return an empty list
         ###SQL QUERY:
         SELECT composite FROM table
         ORDER BY id DESC
         """

    object_to_commit = table(content)

    session.add(object_to_commit)
    session.commit()
    dbLogger.info(f'Commit Done.')
    session.close()
    dbLogger.info(f'Session Closed')

    return link
