
import sqlite3
import pandas as pd
from pathlib import Path

# Project folder
project_folder = Path(__file__).parent

# Input and database paths
csv_file = project_folder / "output" / "clean_orders.csv"
database_file = project_folder / "orders.db"

# Read clean records
data = pd.read_csv(csv_file)

# Connect to SQLite
connection = sqlite3.connect(database_file)

# Save records into SQL table
data.to_sql(
    "clean_orders",
    connection,
    if_exists="replace",
    index=False
)

# Check saved records
result = pd.read_sql_query(
    "SELECT * FROM clean_orders",
    connection
)

print("\nSQL DATABASE REPORT")
print("-----------------------")
print("Records stored:", len(result))
print("\nSaved Records:")
print(result)

connection.close()

print("\nDatabase created successfully!")
