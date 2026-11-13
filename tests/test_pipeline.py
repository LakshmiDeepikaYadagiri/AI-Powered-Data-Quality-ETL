from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_DIR / "output"


def test_output_files_exist():
    expected_files = [
        "clean_orders.csv",
        "rejected_orders.csv",
        "data_quality_report.csv",
        "anomaly_results.csv",
    ]

    for filename in expected_files:
        assert (OUTPUT_DIR / filename).exists(), (
            f"Missing output file: {filename}"
        )
import pandas as pd


def test_clean_orders_are_valid():
    df = pd.read_csv(OUTPUT_DIR / "clean_orders.csv")

    assert not df.empty, "Clean orders file is empty"

    assert df["customer_name"].notna().all(), (
        "Some customer names are missing"
    )

    assert df["customer_name"].astype(str).str.strip().ne("").all(), (
        "Some customer names are blank"
    )

    assert (df["price"] > 0).all(), (
        "Some orders have invalid prices"
    )

    assert (df["quantity"] > 0).all(), (
        "Some orders have invalid quantities"
    )   
def test_rejected_orders():
    df = pd.read_csv(OUTPUT_DIR / "rejected_orders.csv")

    assert "rejection_reason" in df.columns, (
        "Rejection reason column is missing"
    )

    assert not df.empty, (
        "Expected rejected records in the test dataset"
    )

    assert df["rejection_reason"].notna().all(), (
        "Some rejected records have no reason"
    )


def test_anomaly_detection():
    df = pd.read_csv(OUTPUT_DIR / "anomaly_results.csv")

    assert not df.empty, (
        "Anomaly detection results are empty"
    )

    assert "anomaly_prediction" in df.columns
    assert "anomaly_status" in df.columns
    assert "anomaly_score" in df.columns

    assert df["anomaly_prediction"].isin([-1, 1]).all(), (
        "Invalid anomaly predictions found"
    )

    assert df["anomaly_score"].notna().all(), (
        "Some anomaly scores are missing"
    )         