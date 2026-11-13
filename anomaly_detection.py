
import pandas as pd
from sklearn.ensemble import IsolationForest
from pathlib import Path

project_folder = Path(__file__).parent
input_file = project_folder / "output" / "clean_orders.csv"
output_file = project_folder / "output" / "anomaly_results.csv"

data = pd.read_csv(input_file)

data["total_amount"] = data["quantity"] * data["price"]

features = data[["quantity", "price", "total_amount"]]

model = IsolationForest(
    n_estimators=100,
    contamination=0.15,
    random_state=42
)

data["anomaly_prediction"] = model.fit_predict(features)
# Higher scores indicate more unusual transactions
data["anomaly_score"] = -model.score_samples(features)

data["anomaly_status"] = data["anomaly_prediction"].map({
    1: "Normal",
    -1: "Anomaly"
})

data.to_csv(output_file, index=False)

print("\nAI ANOMALY DETECTION REPORT")
print("-----------------------------")
print(data[[
    "order_id",
    "customer_name",
    "total_amount",
    "anomaly_status"
]].to_string(index=False))

print("\nTotal Records:", len(data))
print("Normal Records:", (data["anomaly_status"] == "Normal").sum())
print("Anomalies Detected:", (data["anomaly_status"] == "Anomaly").sum())

print("\nAI anomaly detection completed successfully!")
