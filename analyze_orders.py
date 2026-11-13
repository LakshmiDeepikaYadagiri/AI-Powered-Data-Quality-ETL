
import sqlite3
import pandas as pd
from pathlib import Path

# Connect to our database
database = Path(__file__).parent / "orders.db"
connection = sqlite3.connect(database)

# Query 1: Total orders
query1 = """
SELECT COUNT(*) AS total_orders
FROM clean_orders
"""

# Query 2: Total revenue
query2 = """
SELECT SUM(quantity * price) AS total_revenue
FROM clean_orders
"""

# Query 3: Revenue by product
query3 = """
SELECT
    product,
    SUM(quantity) AS units_sold,
    SUM(quantity * price) AS revenue
FROM clean_orders
GROUP BY product
ORDER BY revenue DESC
"""

print("\nTOTAL ORDERS")
print(pd.read_sql_query(query1, connection))

print("\nTOTAL REVENUE")
print(pd.read_sql_query(query2, connection))

print("\nREVENUE BY PRODUCT")
print(pd.read_sql_query(query3, connection))

connection.close()

print("\nSQL analysis completed successfully!")
