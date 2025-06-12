from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

# Step 1: Define a simple Python function (task logic)
def print_hello():
    print("Hi,This is hussain")
# Step 2: Define the DAG
with DAG(
    dag_id="hello_world_dag",
    start_date=datetime(2024, 1, 1),    
    schedule_interval="*/5 * * * *",  # ⬅ Every 5 minutes
    catchup=False
) as dag:


    # Step 3: Define tasks using operators
    task1 = PythonOperator(
        task_id="say_hello",
        python_callable=print_hello,
    )
