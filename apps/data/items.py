import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import logging


def fetchItems():
    scope =  ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('apps/data/credentials.json',scope)
    client = gspread.authorize(creds)
    sheet = client.open('salesforce_items').sheet1
    #row=[sheet.row_count-1,"bulb"]
    logging.debug(sheet.row_count)
    #sheet.insert_row(row,sheet.row_count)
    legislators = sheet.get_all_records()
    df = pd.DataFrame(legislators)
    columns = list(df)
    values = df.values.tolist()
    resp = {
        "values":values,
        "columns":columns,
        "name": "TB_ITEMS",
        "pk": ["id"],
        "types": [
            'VARCHAR(45)',
            'VARCHAR(45)',
            'VARCHAR(45)',
            'VARCHAR(45)',
        ]
    }
    return resp