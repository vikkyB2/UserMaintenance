import psycopg2
import psycopg2.extras
import json
import traceback
import logging
from config import config
#from apps.Utils.logger import configLogger

#log = configLogger(logging.getLogger(__name__))

def excecuteFetchoneQuery(query):
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
        print(myresult)
    except Exception as e: 
        print(e)
    finally:
          if conn is not None:
            conn.close()
    return myresult

query = """select * from "TB_USER_DETAILS";"""
result = excecuteFetchoneQuery(query)
print(result["USER_ID"])