
import pandas as pd
import numpy as np
from pathlib import Path

# Set random seed for repeatable results
rng = np.random.default_rng(42)

project_folder = Path(__file__).parent
data_folder = project_folder / "data"
data_folder.mkdir(exist_ok=True)

products = {
    "Laptop": 750,
    "Mouse": 25,
    "Keyboard": 45,
    "Monitor": 200,
    "Headphones": 80
}

records = []

# Generate 1000 synthetic transactions
for order_id in range(1001, 2001):
    product = rng.choice(list(products.keys()))
    price = products[product]

    records.append({
        "order_id": order_id,
        "customer_name": f"Customer_{order_id}",
        "product": product,
        "quantity": int(rng.integers(1, 6)),
        "price": price
    })

data = pd.DataFrame(records)

# Add known data quality errors
data.loc[10, "customer_name"] = None
data.loc[20, "price"] = -50
data.loc[30, "quantity"] = 0

# Add unusual but valid transactions
data.loc[40, "quantity"] = 100
data.loc[50, "price"] = 10000

# Add a duplicate record
data = pd.concat([data, data.iloc[[60]]], ignore_index=True)

output_file = data_folder / "large_orders.csv"
data.to_csv(output_file, index=False)

print("\nSYNTHETIC DATASET CREATED")
print("-------------------------")
print("Total records:", len(data))
print("Saved to:", output_file)
print("Missing customer names:", data["customer_name"].isna().sum())
print("Negative prices:", (data["price"] < 0).sum())
print("Zero quantities:", (data["quantity"] == 0).sum())
print("Duplicate rows:", data.duplicated().sum())
