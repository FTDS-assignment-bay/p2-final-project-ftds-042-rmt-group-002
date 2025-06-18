from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import psycopg2
import os
from elasticsearch import Elasticsearch, helpers

PG_CONN = {
    "host": "localhost",
    "port": 5432,
    "dbname": "churn_db",
    "user": "postgres",
    "password": "your_password"
}

es = Elasticsearch("http://localhost:9200")

# Paths
RAW_PATH = "/tmp/churn_raw.csv"
CLEAN_PATH = "/tmp/churn_clean.csv"

def extract_from_postgres():
    conn = psycopg2.connect(**PG_CONN)
    query = "SELECT * FROM customer_usage_raw"
    df = pd.read_sql(query, conn)
    df.to_csv(RAW_PATH, index=False)
    conn.close()
    print("✅ Extracted data from PostgreSQL")

def clean_data():
    df = pd.read_csv(RAW_PATH)

    df.columns = df.columns.str.strip().str.lower().str.replace(r"\s+", "_", regex=True)

    df = df.drop_duplicates()

    df.to_csv(CLEAN_PATH, index=False)
    print("✅ Cleaned and saved to churn_clean.csv")

def load_to_elasticsearch():
    df = pd.read_csv(CLEAN_PATH)
    records = [
        {
            "_index": "churn_customers",
            "_source": row.to_dict()
        }
        for _, row in df.iterrows()
    ]
    helpers.bulk(es, records)
    print("✅ Loaded data to Elasticsearch")

default_args = {
    'start_date': datetime(2024, 1, 1),
    'catchup': False,
}

with DAG(
    dag_id="churn_etl_pipeline",
    schedule_interval="@daily",
    default_args=default_args,
    description="Extract from PostgreSQL, clean, and load to Elasticsearch",
    tags=["churn", "pipeline"]
) as dag:

    t1 = PythonOperator(
        task_id="extract_from_postgres",
        python_callable=extract_from_postgres
    )

    t2 = PythonOperator(
        task_id="clean_data",
        python_callable=clean_data
    )

    t3 = PythonOperator(
        task_id="load_to_elasticsearch",
        python_callable=load_to_elasticsearch
    )

    t1 >> t2 >> t3
