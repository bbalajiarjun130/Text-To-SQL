import sqlite3
import pandas as pd
import os

csv_folder = 'DataCSV'
db_file = 'NBA.db'

# Connect to the database
connection = sqlite3.connect(db_file)

for filename in os.listdir(csv_folder):
    if filename.endswith('.csv'):
        filepath = os.path.join(csv_folder, filename)

        table_name = os.path.splitext(filename)[0]  # Use the filename without extension as table name

        print(f"Processing file: {filename} into table: {table_name}")

        df = pd.read_csv(filepath)

        df.to_sql(table_name, connection, if_exists='replace', index=False)

cursor = connection.cursor()

# Create a table if it doesn't exist
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("\nTables created:")
for row in cursor.fetchall():
    print(row[0])

connection.close()