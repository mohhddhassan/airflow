from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import clickhouse_connect

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def query_clickhouse():
    client = clickhouse_connect.get_client(
        host='clickhouse-server',  # this matches the docker service name
        port=8123,
        username='airflow',
        password='airflow_pass'
    )

    current_hour = datetime.now().hour
    table_name = 'system.metrics' if current_hour % 2 == 0 else 'system.metric_log'

    result = client.query(f"SELECT COUNT(*) FROM {table_name}")
    row_count = result.result_rows[0][0]

    print(f"[{datetime.now()}] Row count in `{table_name}`: {row_count}")

with DAG(
    dag_id='clickhouse_metrics_checker',
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval='@hourly',
    catchup=False,
    tags=['clickhouse'],
) as dag:

    check_metrics = PythonOperator(
        task_id='check_metrics_row_count',
        python_callable=query_clickhouse,
    )

    check_metrics
