from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

import extract
import transform
import load


dag = DAG(
    "amazon_best_sellers_pipeline",
    schedule="@daily",
    start_date=datetime(2023, 6, 24),
)

extract_task = PythonOperator(
    task_id="extract", python_callable=extract.getBestSellersHtml, dag=dag
)

transform_task = PythonOperator(
    task_id="transform", python_callable=transform.transformSellerInfo, dag=dag
)

load_task = PythonOperator(
    task_id="load", python_callable=load.loadToCloudStorage, dag=dag
)

extract_task >> transform_task >> load_task
