import mysql.connector
from config import config
import psycopg2
import json
import traceback
from apps.DBUtils.config import dbDetails
import logging
#from apps.Utils.logger import configLogger

#log = configLogger(logging.getLogger(__name__))

def excecuteFetchoneQuery(query):
    myresult = ""
    try:
        #resultset = {"status": False , "resultObj":{}};
        logging.debug(query)
        logging.debug('dbDetails' + json.dumps(dbDetails))
        mydb = mysql.connector.connect(
                host= dbDetails['host'],
                user= dbDetails['user'],
                passwd= dbDetails['passwd'],
                database= dbDetails['database']
            )
        cursourInst = mydb.cursor(dictionary=True)
        cursourInst.execute(query)
        myresult = cursourInst.fetchone()
        logging.debug(myresult)
    except Exception as e: 
        logging.debug(e)
    finally:
        cursourInst.close()
        mydb.close()
    return myresult


def excecuteFetchAllQuery(query):
    myresult = ""
    try:
        #resultset = {"status": False , "resultObj":{}};
        logging.error(query)
        logging.debug('dbDetails' + json.dumps(dbDetails))
        mydb = mysql.connector.connect(
                host= dbDetails['host'],
                user= dbDetails['user'],
                passwd= dbDetails['passwd'],
                database= dbDetails['database']
            )
        cursourInst = mydb.cursor(dictionary=True)
        cursourInst.execute(query)
        myresult = cursourInst.fetchall()
        logging.debug(myresult)
    except Exception as e: 
        logging.debug(e)
    finally:
        cursourInst.close()
        mydb.close()
    return myresult

def excecuteInsertQuery(sql,val):

    inserted = False
    try:
        mydb = mysql.connector.connect(
                host= dbDetails['host'],
                user= dbDetails['user'],
                passwd= dbDetails['passwd'],
                database= dbDetails['database']
            )
        cursourInst = mydb.cursor()
        cursourInst.execute(sql,val)
        mydb.commit()
        inserted = True
    except Exception as e: 
        logging.debug(e)
    finally:
        cursourInst.close()
        mydb.close()
    return inserted

def excecuteDeleteQuery(query):
    deleted = False
    try:
        mydb = mysql.connector.connect(
                host= dbDetails['host'],
                user= dbDetails['user'],
                passwd= dbDetails['passwd'],
                database= dbDetails['database']
            )
        cursourInst = mydb.cursor(dictionary=True)
        cursourInst.execute(query)
        deleted = True
    except Exception as e: 
        logging.debug(e)
    finally:
        cursourInst.close()
        mydb.close()
    return deleted

def excecuteUpdateQuery(query):
    logging.debug(query)
    updated = False
    try:
        mydb = mysql.connector.connect(
                host= dbDetails['host'],
                user= dbDetails['user'],
                passwd= dbDetails['passwd'],
                database= dbDetails['database']
            )
        cursourInst = mydb.cursor(dictionary=True)
        cursourInst.execute(query)
        updated = True
        mydb.commit()
    except Exception as e: 
        logging.debug(e)
    finally:
        cursourInst.close()
        mydb.close()
    return updated