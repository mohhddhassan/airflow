import clickhouse_connect
import pandas as pd
from datetime import datetime

def extract_and_save_metrics(execution_time: str):
    # Connect to ClickHouse
    client = clickhouse_connect.get_client(
        host='clickhouse',       # service name from docker-compose
        user='airflow',
        password='airflow_pass',
        database='system'
    )

    # Query to get metrics
    query = """
        SELECT 
            now() AS timestamp,
            description AS metric_name,
            value
        FROM system.metrics
    """

    # Execute the query
    data = client.execute(query)

    # Create DataFrame
    df = pd.DataFrame(data, columns=['timestamp', 'metric_name', 'value'])

    # Add DAG execution time
    dag_time = datetime.fromisoformat(execution_time)
    df['dag_run_time'] = dag_time.strftime('%Y-%m-%d %H:%M:%S')

    # Format file name
    filename = f"metrics_{dag_time.strftime('%Y-%m-%d_%H-%M-%S')}.csv"
    filepath = f"/opt/airflow/output/{filename}"

    # Save to CSV
    df.to_csv(filepath, index=False)
    print(f"✅ Metrics successfully saved to: {filepath}")
