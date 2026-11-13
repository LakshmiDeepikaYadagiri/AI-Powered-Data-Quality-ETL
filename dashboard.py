
import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path

# Page settings
st.set_page_config(
    page_title="AI Data Quality Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 AI-Powered Data Quality & ETL Dashboard")
st.write("Monitor data quality, cleaned records, and sales performance.")

# File paths
project_folder = Path(__file__).parent
report_file = project_folder / "output" / "data_quality_report.csv"
database_file = project_folder / "orders.db"

# Load data quality report
report = pd.read_csv(report_file).iloc[0]

# Connect to database
connection = sqlite3.connect(database_file)
orders = pd.read_sql_query(
    "SELECT * FROM clean_orders",
    connection
)
connection.close()

# Dashboard metrics
st.header("Data Quality Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Records", int(report["total_records"]))
col2.metric("Clean Records", int(report["clean_records"]))
col3.metric("Rejected Records", int(report["rejected_records"]))

quality_score = (
    report["clean_records"] / report["total_records"] * 100
    if report["total_records"] > 0 else 0
)

st.metric("Data Quality Score", f"{quality_score:.1f}%")
st.progress(quality_score / 100)

# Sales analysis
st.header("Sales Analysis")

orders["revenue"] = orders["quantity"] * orders["price"]

total_revenue = orders["revenue"].sum()
st.metric("Total Revenue", f"${total_revenue:,.2f}")

sales_by_product = (
    orders.groupby("product")["revenue"]
    .sum()
    .sort_values(ascending=False)
)

st.subheader("Revenue by Product")
st.bar_chart(sales_by_product)

# Clean records
st.header("Clean Orders")
st.dataframe(orders, use_container_width=True)

# Rejected records
st.header("Rejected Orders")
rejected = pd.read_csv(
    project_folder / "output" / "rejected_orders.csv"
)
st.dataframe(rejected, use_container_width=True)

st.success("ETL Dashboard loaded successfully!")

# AI Anomaly Detection Section
st.header("🤖 AI Anomaly Detection")

anomaly_file = project_folder / "output" / "anomaly_results.csv"

if anomaly_file.exists():
    anomaly_data = pd.read_csv(anomaly_file)

    total_anomalies = (
        anomaly_data["anomaly_status"] == "Anomaly"
    ).sum()

    normal_orders = (
        anomaly_data["anomaly_status"] == "Normal"
    ).sum()

    col1, col2 = st.columns(2)

    col1.metric("Normal Transactions", int(normal_orders))
    col2.metric("Anomalies Detected", int(total_anomalies))

    st.subheader("AI Prediction Results")

    st.dataframe(
        anomaly_data[[
            "order_id",
            "customer_name",
            "total_amount",
            "anomaly_status"
        ]],
        use_container_width=True
    )

    st.subheader("Anomaly Distribution")

    anomaly_counts = (
        anomaly_data["anomaly_status"]
        .value_counts()
    )

    st.bar_chart(anomaly_counts)

    st.info(
        "Isolation Forest identifies unusual transactions "
        "based on quantity, price, and transaction amount. "
        "Anomalies are not necessarily fraudulent."
    )

else:
    st.warning(
        "Anomaly results not found. "
        "Run anomaly_detection.py first."
    )

# Top 10 Most Unusual Transactions
st.header("🔍 Top 10 Most Unusual Transactions")

if anomaly_file.exists():
    anomaly_data = pd.read_csv(anomaly_file)

    if "anomaly_score" in anomaly_data.columns:
        top_anomalies = anomaly_data.nlargest(
            10, "anomaly_score"
        )

        st.dataframe(
            top_anomalies[[
                "order_id",
                "customer_name",
                "total_amount",
                "anomaly_score",
                "anomaly_status"
            ]],
            use_container_width=True
        )

        st.subheader("Top 10 Anomaly Scores")

        chart_data = top_anomalies.set_index(
            "order_id"
        )[["anomaly_score"]]

        st.bar_chart(chart_data)

        st.info(
            "Higher anomaly scores indicate more unusual "
            "transactions. These records may require review."
        )
    else:
        st.warning("Anomaly scores are not available.")
else:
    st.warning("Run anomaly_detection.py first.")
