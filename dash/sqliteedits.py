import sqlite3
import pandas as pd

# Replace "database.db" with the path to your database file
db_path = "2012corn.sqlite"

# Replace "table_name" with the name of the table you want to remove
table_name = "Water Balance ET"

# Connect to the database
connection = sqlite3.connect(db_path)

# Get a cursor object
cursor = connection.cursor()

# cursor.execute(f"DROP TABLE '{table_name}'")

df = pd.read_csv('waterbalance13.csv')

treatments_dict_12 = {
    1: ['B11', 'B23', 'A33', 'A42'],
    2: ['A15', 'A22', 'B32', 'B46'],
    3: ['A14', 'A24', 'B31', 'B45'],
    4: ['B15', 'B22', 'A31', 'A46'],
    5: ['B14', 'B25', 'A34', 'A44'],
    6: ['A16', 'A26', 'B34', 'B41'],
    7: ['A11', 'A25', 'B33', 'B44'],
    8: ['B12', 'B26', 'A32', 'A41'],
    9: ['B13', 'B21', 'A35', 'A43'],
    10: ['A12', 'A23', 'B35', 'B42'],
    11: ['B16', 'B24', 'A36', 'A45'],
    12: ['A13', 'A21', 'B36', 'B43']
}
treatments_dict_13 = {
    1: ['C12', 'C22', 'D31', 'D43'],
    2: ['D12', 'D22', 'C34', 'C41'],
    3: ['D13', 'D21', 'C36', 'C45'],
    4: ['C14', 'C23', 'D34', 'D46'],
    5: ['C11', 'C24', 'D33', 'D44'],
    6: ['D16', 'D25', 'C35', 'C42'],
    7: ['C13', 'C21', 'D36', 'D45'],
    8: ['D14', 'D26', 'C32', 'C43'],
    9: ['D15', 'D23', 'C31', 'C44'],
    10: ['C16', 'C25', 'D35', 'D42'],
    11: ['C15', 'C26', 'D32', 'D41'],
    12: ['C13', 'C21', 'D36', 'D45']
}

def g(df, plots_dict):
    df['Plot'] = df['Trt_code'].apply(lambda x: plots_dict.get(x))
    
    return df
g(df, treatments_dict_13)
df = df.explode('Plot')
print(df)
df.to_sql(table_name, connection, if_exists='append', index=False)

# Commit the changes
connection.commit()

# Close the connection
connection.close()
