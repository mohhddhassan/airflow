import csv
import psycopg2
from datetime import datetime

def load_historical_data():
    try:
        conn = psycopg2.connect(
            host="postgres",
            database="airflow",
            user="airflow",
            password="airflow"
        )
        cursor = conn.cursor()

        with open('/opt/airflow/scripts/historical_data.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                date = datetime.strptime(row['date'], '%Y-%m-%d')
                total_cases = int(row['total_cases'])
                total_deaths = int(row['total_deaths'])
                total_recovered = int(row['total_recovered'])

                # Insert into the covid_stats table (same structure)
                cursor.execute("""
                    INSERT INTO covid_stats (total_cases, total_deaths, total_recovered, collected_at)
                    VALUES (%s, %s, %s, %s)
                """, (total_cases, total_deaths, total_recovered, date))

        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Historical data loaded successfully.")

    except Exception as e:
        print("❌ Error loading historical data:", e)
        raise
