FROM apache/airflow:2.9.1-python3.10

USER airflow

# Install clickhouse-connect and any other dependencies you need
RUN pip install --no-cache-dir clickhouse-connect pandas

USER airflow
