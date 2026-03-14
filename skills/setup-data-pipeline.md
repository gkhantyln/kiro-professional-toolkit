---
name: setup-data-pipeline
description: Production data pipeline with dbt, Apache Airflow, Great Expectations data quality, and incremental loading strategies
---

# Setup Data Pipeline

Production-ready veri pipeline'ı kurar:
- Apache Airflow DAG orchestration
- dbt transformations + tests
- Great Expectations data quality
- Incremental loading (SCD Type 2)
- Data lineage tracking
- Alerting on failures

## Usage
```
#setup-data-pipeline <postgres|bigquery|snowflake>
```

## dags/etl_pipeline.py
```python
from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
import pandas as pd
import great_expectations as gx

default_args = {
    "owner": "data-team",
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure": True,
    "email": ["data-alerts@company.com"],
}

@dag(
    dag_id="etl_pipeline",
    default_args=default_args,
    schedule_interval="0 2 * * *",
    start_date=days_ago(1),
    catchup=False,
    tags=["etl", "production"],
)
def etl_pipeline():

    @task()
    def extract(execution_date=None) -> str:
        hook = PostgresHook(postgres_conn_id="source_db")
        df = hook.get_pandas_df(
            sql="""
                SELECT * FROM orders
                WHERE updated_at >= %(start)s AND updated_at < %(end)s
            """,
            parameters={"start": execution_date, "end": execution_date + timedelta(days=1)},
        )
        path = f"/tmp/orders_{execution_date.date()}.parquet"
        df.to_parquet(path, index=False)
        return path

    @task()
    def validate(path: str) -> str:
        context = gx.get_context()
        ds = context.sources.add_or_update_pandas("orders")
        asset = ds.add_dataframe_asset("orders_batch")
        batch = asset.build_batch_request(dataframe=pd.read_parquet(path))

        suite = context.get_expectation_suite("orders_suite")
        results = context.run_validation_operator(
            "action_list_operator",
            assets_to_validate=[batch],
            expectation_suite_name="orders_suite",
        )
        if not results["success"]:
            raise ValueError(f"Data quality check failed: {results}")
        return path

    @task()
    def transform(path: str) -> str:
        df = pd.read_parquet(path)
        df["total_with_tax"] = df["total"] * 1.18
        df["order_date"] = pd.to_datetime(df["created_at"]).dt.date
        df["is_high_value"] = df["total"] > 1000
        out = path.replace(".parquet", "_transformed.parquet")
        df.to_parquet(out, index=False)
        return out

    @task()
    def load(path: str):
        hook = PostgresHook(postgres_conn_id="warehouse_db")
        df = pd.read_parquet(path)
        hook.insert_rows(
            table="fact_orders",
            rows=df.values.tolist(),
            target_fields=df.columns.tolist(),
            replace=True,
            replace_index=["id"],
        )

    raw = extract()
    validated = validate(raw)
    transformed = transform(validated)
    load(transformed)

dag = etl_pipeline()
```

## models/orders.sql (dbt)
```sql
{{ config(
    materialized='incremental',
    unique_key='order_id',
    incremental_strategy='merge',
    on_schema_change='sync_all_columns',
    indexes=[
        {'columns': ['order_date'], 'type': 'btree'},
        {'columns': ['customer_id'], 'type': 'btree'},
    ]
) }}

WITH source AS (
    SELECT * FROM {{ source('raw', 'orders') }}
    {% if is_incremental() %}
    WHERE updated_at > (SELECT MAX(updated_at) FROM {{ this }})
    {% endif %}
),

transformed AS (
    SELECT
        id                                          AS order_id,
        customer_id,
        total                                       AS order_total,
        total * 1.18                                AS order_total_with_tax,
        DATE(created_at)                            AS order_date,
        total > 1000                                AS is_high_value,
        CURRENT_TIMESTAMP                           AS dbt_updated_at
    FROM source
)

SELECT * FROM transformed
```

## tests/orders.yml (dbt tests)
```yaml
version: 2
models:
  - name: orders
    columns:
      - name: order_id
        tests:
          - unique
          - not_null
      - name: customer_id
        tests:
          - not_null
          - relationships:
              to: ref('customers')
              field: id
      - name: order_total
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0
              max_value: 1000000
```
