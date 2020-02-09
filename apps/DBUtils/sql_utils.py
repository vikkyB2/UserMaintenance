import mysql.connector
import psycopg2
import psycopg2.extras
import json
import traceback
from apps.DBUtils.config import config
import logging
#from apps.Utils.logger import configLogger

#log = configLogger(logging.getLogger(__name__))

def excecuteFetchoneQuery(query):
    logging.debug(query)
    myresult = ""
    try:
        # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        mydb = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        mydb.execute(query)
        myresult = mydb.fetchone()
        mydb.close()
        logging.debug(myresult)
    except Exception as e: 
        logging.debug(e)
    finally:
          if conn is not None:
            conn.close()
    return myresult


def excecuteFetchAllQuery(query):
    myresult = ""
    try:
        # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        mydb = conn.cursour(cursor_factory = psycopg2.extras.DictCursor)
        mydb.execute(query)
        myresult = mydb.fetchall()
        logging.debug(myresult)
        mydb.close()
    except Exception as e: 
        logging.debug(e)
    finally:
        if conn is not None:
            conn.close()
    return myresult

def excecuteInsertQuery(sql,val):

    inserted = False
    try:
         # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        mydb = conn.cursor()
        mydb.execute(sql,val)
        conn.commit()
        mydb.close()
        inserted = True
    except Exception as e: 
        logging.debug(e)
    finally:
        if conn is not None:
            conn.close()
    return inserted

def excecuteDeleteQuery(query):
    deleted = False
    try:
        # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        mydb = conn.cursor()
        mydb.execute(query)
        conn.commit()
        deleted = True
        mydb.close()
    except Exception as e: 
        logging.debug(e)
    finally:
        if conn is not None:
            conn.close()
    return deleted

def excecuteUpdateQuery(query):
    logging.debug(query)
    updated = False
    try:
        # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        mydb = conn.cursor()
        mydb.execute(query)
        conn.commit()
        updated = True
        mydb.close()
    except Exception as e: 
        logging.debug(e)
    finally:
        if conn is not None:
            conn.close()
    return updated