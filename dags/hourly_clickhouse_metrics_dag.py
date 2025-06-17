from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys

# Include the scripts folder in the Python path
sys.path.append('/opt/airflow/scripts')
from extract_clickhouse_metrics import extract_and_save_metrics


default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='hourly_clickhouse_metrics_dag',
    default_args=default_args,
    description='Extract metrics from ClickHouse and store in CSV hourly',
    schedule_interval='@hourly',
    start_date=datetime(2025, 6, 13),
    catchup=False,
    tags=['clickhouse', 'csv', 'hourly'],
) as dag:

    extract_task = PythonOperator(
        task_id='extract_clickhouse_metrics',
        python_callable=extract_and_save_metrics,
        op_kwargs={'execution_time': '{{ execution_date }}'},
    )

    extract_task