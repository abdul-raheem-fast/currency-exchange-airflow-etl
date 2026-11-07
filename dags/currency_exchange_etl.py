from datetime import datetime, timezone

import requests
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.mongo.hooks.mongo import MongoHook


API_URL = "https://api.frankfurter.dev/v2/rates"
QUOTES = ["USD", "GBP", "JPY"]
BASE_CURRENCY = "EUR"
MONGO_CONN_ID = "mongo_default"


def extract_rates(**context):
    """Fetch exchange rates from Frankfurter API."""
    response = requests.get(
        API_URL,
        params={"base": BASE_CURRENCY, "quotes": ",".join(QUOTES)},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    if not isinstance(data, list):
        raise ValueError("Frankfurter API returned an unexpected response shape")
    context["ti"].xcom_push(key="raw_rates", value=data)
    print(f"Extracted {len(data)} rate records")
    return data


def transform_rates(**context):
    """Reshape raw API data into per-currency documents."""
    raw = context["ti"].xcom_pull(task_ids="extract", key="raw_rates")
    if not isinstance(raw, list):
        raise ValueError("Missing or invalid raw_rates XCom payload")

    retrieved_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
    transformed = []
    for record in raw:
        transformed.append(
            {
                "base_currency": record["base"],
                "target_currency": record["quote"],
                "exchange_rate": record["rate"],
                "rate_date": record["date"],
                "source": "Frankfurter API",
                "retrieved_at": retrieved_at,
            }
        )

    context["ti"].xcom_push(key="transformed_rates", value=transformed)
    print(f"Transformed {len(transformed)} records")
    return transformed


def load_to_mongodb(**context):
    """Insert transformed rate documents into MongoDB."""
    records = context["ti"].xcom_pull(task_ids="transform", key="transformed_rates")
    if not isinstance(records, list) or not records:
        raise ValueError("Missing or empty transformed_rates XCom payload")

    client = MongoHook(mongo_conn_id=MONGO_CONN_ID).get_conn()
    try:
        collection = client["currency_db"]["exchange_rates"]
        result = collection.insert_many(records)
        print(f"Inserted {len(result.inserted_ids)} documents into MongoDB")
    finally:
        client.close()


with DAG(
    dag_id="currency_exchange_etl",
    description="Daily ETL: Frankfurter API to MongoDB",
    start_date=datetime(2026, 11, 1),
    schedule="@daily",
    catchup=False,
    tags=["etl", "currency", "mongodb"],
) as dag:
    extract = PythonOperator(
        task_id="extract",
        python_callable=extract_rates,
    )

    transform = PythonOperator(
        task_id="transform",
        python_callable=transform_rates,
    )

    load = PythonOperator(
        task_id="load",
        python_callable=load_to_mongodb,
    )

    extract >> transform >> load
