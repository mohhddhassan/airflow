import requests
import psycopg2
from datetime import datetime
import logging

def fetch_and_store_covid_data():
    try:
        # Step 1: Fetch COVID-19 data from the API
        url = "https://disease.sh/v3/covid-19/all"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        total_cases = data.get("cases")
        total_deaths = data.get("deaths")
        total_recovered = data.get("recovered")
        timestamp = datetime.utcnow()

        logging.info("Fetched data: %s", {
            "cases": total_cases,
            "deaths": total_deaths,
            "recovered": total_recovered,
            "timestamp": timestamp,
        })

        # Step 2: Connect to PostgreSQL
        conn = psycopg2.connect(
            host="postgres",
            database="airflow",
            user="airflow",
            password="airflow"
        )
        cursor = conn.cursor()

        # Step 3: Create the table if it doesn't exist
        create_table_query = """
        CREATE TABLE IF NOT EXISTS covid_stats (
            id SERIAL PRIMARY KEY,
            total_cases BIGINT,
            total_deaths BIGINT,
            total_recovered BIGINT,
            collected_at TIMESTAMP
        );
        """
        cursor.execute(create_table_query)

        # Step 4: Check the latest entry in the table
        cursor.execute("SELECT total_cases, total_deaths, total_recovered FROM covid_stats ORDER BY collected_at DESC LIMIT 1;")
        last_record = cursor.fetchone()

        # Step 5: Compare and insert only if data is new
        if last_record == (total_cases, total_deaths, total_recovered):
            logging.info("⏭️ No new data. Latest record matches current data. Skipping insert.")
        else:
            insert_query = """
            INSERT INTO covid_stats (total_cases, total_deaths, total_recovered, collected_at)
            VALUES (%s, %s, %s, %s);
            """
            cursor.execute(insert_query, (total_cases, total_deaths, total_recovered, timestamp))
            conn.commit()
            logging.info("✅ New data inserted into PostgreSQL.")

        # Cleanup
        cursor.close()
        conn.close()

    except Exception as e:
        logging.error("❌ Error occurred: %s", str(e))
        raise
