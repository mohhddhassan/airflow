import clickhouse_connect
import pandas as pd
from datetime import datetime
import os
import csv

def extract_and_save_metrics(execution_time: str):
    # Connect to ClickHouse
    client = clickhouse_connect.get_client(
        host='clickhouse-server',
        user='airflow',
        password='airflow_pass',
        database='system'
    )

    # Query system metrics
    result = client.query("SELECT now() AS timestamp, description AS metric_name, value FROM system.metrics")
    rows = result.result_rows

    # Prepare file path and headers
    dag_time = datetime.fromisoformat(execution_time)
    filename = f"metrics_{dag_time.strftime('%Y-%m-%d')}.csv"  # one file per day
    filepath = f"/opt/airflow/output/{filename}"
    file_exists = os.path.isfile(filepath)

    # Append each row to CSV
    with open(filepath, mode='a', newline='') as f:
        writer = csv.writer(f)

        # Write header only if file doesn't exist
        if not file_exists:
            writer.writerow(['timestamp', 'metric_name', 'value', 'dag_run_time'])

        for row in rows:
            writer.writerow([
                row[0],            # timestamp from ClickHouse
                row[1],            # metric_name
                row[2],            # value
                dag_time.strftime('%Y-%m-%d %H:%M:%S')  # DAG run time
            ])

    print(f"✅ Metrics appended to: {filepath}")
