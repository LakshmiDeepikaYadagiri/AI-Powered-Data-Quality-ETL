
import pandas as pd
from pathlib import Path

# Find our dataset
file_path = Path(__file__).parent / "data" / "sample_orders.csv"

# Read the CSV file
data = pd.read_csv(file_path)

# Display the dataset
print("ORIGINAL DATA:")
print(data)

# Check data quality
print("\nDATA QUALITY REPORT")
print("-----------------------")
print("Total Records:", len(data))
print("Missing Names:", data["customer_name"].isnull().sum())
print("Duplicate Records:", data.duplicated().sum())
print("Invalid Prices:", (data["price"] < 0).sum())
