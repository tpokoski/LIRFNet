import pandas as pd
import sqlite3

excel_file = r'data\2012Corn2DB.xlsx'
excel_data = pd.read_excel(excel_file, sheet_name=None)

conn = sqlite3.connect('data/2012corn.db')
cursor = conn.cursor()

for sheet_name, df in excel_data.items():
    df.to_sql(sheet_name, conn, if_exists='replace', index=False)

conn.close()