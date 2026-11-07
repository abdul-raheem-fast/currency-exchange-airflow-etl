# Currency Exchange ETL Pipeline

Airflow ETL pipeline that extracts daily currency exchange rates from the Frankfurter API, transforms them, and loads into MongoDB. Built with Astro CLI.

## Architecture

```
Frankfurter API → [Extract] → [Transform] → [Load] → MongoDB
```

## Prerequisites

- Docker Desktop
- Astro CLI (`winget install -e --id Astronomer.Astro`)

## Setup & Run

```bash
# Start the pipeline
astro dev start

# Airflow UI: http://localhost:8080  (admin / admin)
# Mongo Express: http://localhost:8081
```

The Astro Airflow connection named `mongo_default` connects to MongoDB on the
Docker network using the credentials in `.env`. Mongo Express uses the same
authenticated MongoDB URI and exposes the stored `currency_db.exchange_rates`
documents at port 8081.

## DAG: `currency_exchange_etl`

| Task      | Description                               |
|-----------|-------------------------------------------|
| extract   | Fetches EUR→USD,GBP,JPY rates from API   |
| transform | Reshapes into per-currency documents      |
| load      | Inserts documents into MongoDB            |

Data is passed between tasks using Airflow named XCom keys (`raw_rates`, `transformed_rates`).
The load task reads the configured `mongo_default` connection through
`MongoHook`; no database URI is hard-coded in the DAG.

## Transformed Document Schema

```json
{
  "base_currency": "EUR",
  "target_currency": "USD",
  "exchange_rate": 1.15,
  "rate_date": "2026-11-04",
  "source": "Frankfurter API",
  "retrieved_at": "2026-11-05T07:15:00"
}
```

## Project Structure

```
├── dags/
│   └── currency_exchange_etl.py    # ETL DAG
├── tests/
│   └── test_dag_integrity.py       # DAG validation tests
├── docker-compose.override.yml     # MongoDB + Mongo Express
├── Dockerfile                      # Astro Runtime image
├── requirements.txt                # Python dependencies
└── .env                            # MongoDB credentials
```
