# Astro project test for DAG validation
import pytest
from airflow.models import DagBag


def test_no_import_errors():
    dag_bag = DagBag(include_examples=False)
    assert len(dag_bag.import_errors) == 0, f"Import errors: {dag_bag.import_errors}"


def test_dag_loaded():
    dag_bag = DagBag(include_examples=False)
    assert "currency_exchange_etl" in dag_bag.dags
    dag = dag_bag.dags["currency_exchange_etl"]
    assert len(dag.tasks) == 3
    assert {task.task_id for task in dag.tasks} == {"extract", "transform", "load"}
    assert dag.task_dict["extract"].downstream_task_ids == {"transform"}
    assert dag.task_dict["transform"].downstream_task_ids == {"load"}
