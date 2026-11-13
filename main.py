
import pandas as pd
from pathlib import Path

# Step 1: Set file paths
project_folder = Path(__file__).parent
input_file = project_folder / "data" / "large_orders.csv"
output_folder = project_folder / "output"
output_folder.mkdir(exist_ok=True)

# Step 2: Read the dataset
data = pd.read_csv(input_file)

# Step 3: Find problems
missing_names = data["customer_name"].isna()
invalid_prices = data["price"] <= 0
invalid_quantities = data["quantity"] <= 0
duplicates = data.duplicated(keep="first")

# Step 4: Record rejection reasons
data["rejection_reason"] = ""

data.loc[missing_names, "rejection_reason"] += "Missing customer name; "
data.loc[invalid_prices, "rejection_reason"] += "Invalid price; "
data.loc[invalid_quantities, "rejection_reason"] += "Invalid quantity; "
data.loc[duplicates, "rejection_reason"] += "Duplicate record; "

# Step 5: Separate valid and invalid records
rejected_data = data[data["rejection_reason"] != ""].copy()
clean_data = data[data["rejection_reason"] == ""].copy()

# Remove rejection reason from clean records
clean_data = clean_data.drop(columns=["rejection_reason"])

# Step 6: Save results
clean_data.to_csv(output_folder / "clean_orders.csv", index=False)
rejected_data.to_csv(output_folder / "rejected_orders.csv", index=False)

# Step 7: Create a summary report
report = {
    "total_records": len(data),
    "clean_records": len(clean_data),
    "rejected_records": len(rejected_data),
    "missing_names": int(missing_names.sum()),
    "invalid_prices": int(invalid_prices.sum()),
    "invalid_quantities": int(invalid_quantities.sum()),
    "duplicate_records": int(duplicates.sum())
}

pd.DataFrame([report]).to_csv(
    output_folder / "data_quality_report.csv",
    index=False
)

# Step 8: Display results
print("\nDATA QUALITY REPORT")
print("-----------------------")

for key, value in report.items():
    print(f"{key}: {value}")

print("\nData quality report generated successfully!")
