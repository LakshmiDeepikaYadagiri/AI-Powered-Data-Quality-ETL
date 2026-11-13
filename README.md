
# AI-Powered Data Quality & ETL Pipeline

An end-to-end Python data engineering project that
automatically validates, cleans, and analyzes
transaction data using SQL and machine learning.

## Technologies Used

- Python
- Pandas and NumPy
- SQLite and SQL
- Scikit-learn (Isolation Forest)
- Streamlit
- Logging

## Key Features

1. Automated ETL pipeline
2. Missing-value detection
3. Duplicate record detection
4. Invalid price and quantity validation
5. Rejected-record reporting
6. SQLite database integration
7. SQL-based sales analytics
8. Machine learning anomaly detection
9. Interactive Streamlit dashboard
10. Automated execution and logging

## Project Workflow

Raw CSV Data
    |
    v
Data Validation and Cleaning
    |
    v
Clean and Rejected CSV Files
    |
    v
SQLite Database
    |
    v
SQL Analytics and AI Anomaly Detection
    |
    v
Streamlit Dashboard

## Dataset

The project uses 1,001 synthetic transaction
records, including intentionally introduced
data quality issues and unusual transactions.

## Sample Results

- Total input records: 1,001
- Expected clean records: 997
- Expected rejected records: 4
- AI model analyzed: 997 records
- Normal transactions: 877
- AI-flagged anomalies: 120

## How to Run

Install dependencies:

    pip install pandas numpy scikit-learn streamlit

Run the pipeline:

    python generate_data.py
    python run_pipeline.py

Launch the dashboard:

    streamlit run dashboard.py

## Future Improvements

- PostgreSQL integration
- Automated unit testing
- Cloud deployment
- Model evaluation using labeled data
- Pipeline scheduling

## Disclaimer

The dataset is synthetic. Anomaly detection
results indicate unusual patterns and do not
establish fraud or transaction errors.
