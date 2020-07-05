import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import logging


def fetchItems():
    logging.debug("fetchh items")
    scope =  ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('apps/itemdata/credentials.json',scope)
    client = gspread.authorize(creds)
    logging.debug("time")
    sheet = client.open('salesforce_items').sheet1
    row=[sheet.row_count-1,"bulb"]
    logging.debug(sheet.row_count)
    #sheet.insert_row(row,sheet.row_count)
    legislators = sheet.get_all_records()

    #df = pd.DataFrame(legislators)
    return legislators
