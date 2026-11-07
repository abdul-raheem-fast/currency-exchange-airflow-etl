# Currency Exchange Airflow ETL Report

## Objective

The `currency_exchange_etl` DAG retrieves daily EUR exchange rates from the
Frankfurter API, transforms each rate into the required document shape, and
loads the documents into MongoDB.

## Pipeline

1. **Extract** calls `https://api.frankfurter.dev/v2/rates` for USD, GBP, and
   JPY and publishes the response under the named XCom key `raw_rates`.
2. **Transform** converts each API record to the required schema and publishes
   the result under `transformed_rates`.
3. **Load** reads `transformed_rates` and inserts the documents into
   `currency_db.exchange_rates` using the Airflow `mongo_default` connection.

The task dependency is:

```text
extract >> transform >> load
```

## Transformed document

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

## Infrastructure

- MongoDB 7.0 runs as the `mongo` Docker service with persistent volume
  `mongo_data`.
- Mongo Express runs as the `mongo-express` Docker service on port 8081.
- Both services share the default Docker network.
- Docker image metadata is defined with `maintainer`, `description`, and
  `version` labels.

## Validation evidence

- `python -m py_compile dags/currency_exchange_etl.py` completed successfully.
- `docker compose -f docker-compose.override.yml config` completed
  successfully.
- `tests/test_dag_integrity.py` validates importability, the three required
  tasks, and their dependency order when run inside the Astro Airflow
  environment.

To capture runtime screenshots for submission:

```bash
astro dev start
astro dev run dags list
astro dev run dags test currency_exchange_etl 2026-11-07
```

The Airflow Graph view and Mongo Express `currency_db.exchange_rates`
collection provide the code-output screenshots requested by the assignment.
