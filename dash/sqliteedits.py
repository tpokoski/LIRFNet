import sqlite3
import pandas as pd

# Replace "database.db" with the path to your database file
db_path = "2012corn.sqlite"

# Replace "table_name" with the name of the table you want to remove
table_name = "LAI by Plot"

# Connect to the database
connection = sqlite3.connect(db_path)

# Get a cursor object
cursor = connection.cursor()

# Drop the table
dropquery = f"DROP TABLE '{table_name}'"
cursor.execute(dropquery)

df = pd.read_csv('LAIfix.csv')
print(df)
df['LAI'] = pd.to_numeric(df['LAI'])
print(df.dtypes)

df.to_sql('LAI by Plot', connection, index=False)
# Commit the changes
connection.commit()

# Close the connection
connection.close()
