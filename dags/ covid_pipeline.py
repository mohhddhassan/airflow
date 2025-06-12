from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
import sys
import logging

# Add the scripts directory to the path so we can import the custom function
sys.path.append('/opt/airflow/scripts')
from fetch_and_store import fetch_and_store_covid_data  # Your main function

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
    dag_id='covid_data_pipeline',
    default_args=default_args,
    description='Fetch and store COVID-19 data into PostgreSQL daily',
    schedule_interval='@daily',
    start_date=days_ago(1),
    catchup=False,  # Only run from today onward
    tags=['covid', 'data-pipeline', 'postgres'],
) as dag:

    # Python task that fetches and inserts data
    fetch_and_store_task = PythonOperator(
        task_id='fetch_and_store_covid_data',
        python_callable=fetch_and_store_covid_data,
    )

    fetch_and_store_task
