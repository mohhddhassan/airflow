import random
import string
from datetime import datetime, timedelta
from clickhouse_connect import get_client

# Connect to ClickHouse
client = get_client(host='localhost', username='airflow', password='airflow_pass')

table_name = 'n3.signal_network_monthly_new '   # Replace with your table name
num_rows = 1000                  # Number of random rows to insert

# Get table schema
schema = client.query(f"DESCRIBE TABLE {table_name}").result_rows

# Define how to generate random data based on type
def generate_random_value(dtype):
    if dtype.startswith('Date'):
        return (datetime.now() - timedelta(days=random.randint(0, 30))).date()
    elif dtype.startswith('String'):
        return ''.join(random.choices(string.ascii_lowercase, k=8))
    elif dtype.startswith('UInt8'):
        return random.randint(0, 255)
    elif dtype.startswith('Float64'):
        return round(random.uniform(0, 100), 2)
    else:
        return None  # or raise an error if type not supported

# Prepare data
rows = []
for _ in range(num_rows):
    row = [generate_random_value(dtype) for _, dtype, *_ in schema]
    rows.append(row)

# Insert into table
column_names = [col_name for col_name, *_ in schema]
client.insert(table_name, rows, column_names=column_names)

print(f"Inserted {num_rows} random rows into `{table_name}`.")
