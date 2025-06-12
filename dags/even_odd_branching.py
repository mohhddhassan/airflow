from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from datetime import datetime
import pendulum

default_args = {
    'start_date': datetime(2024, 1, 1),  # safe past date
}

def decide_even_or_odd():
    hour = datetime.now(pendulum.timezone("Asia/Kolkata")).hour
    return 'even_task' if hour % 2 == 0 else 'odd_task'

def print_even():
    print("Even hour")

def print_odd():
    print("Odd hour")

with DAG(
    dag_id='even_odd_branching',
    schedule_interval='*/5 * * * *',  # every 5 mins
    default_args=default_args,
    catchup=False,
) as dag:

    branching = BranchPythonOperator(
        task_id='branching',
        python_callable=decide_even_or_odd
    )

    even = PythonOperator(
        task_id='even_task',
        python_callable=print_even
    )

    odd = PythonOperator(
        task_id='odd_task',
        python_callable=print_odd
    )

    branching >> [even, odd]
