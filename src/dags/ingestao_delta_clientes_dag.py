from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="ingestao_delta_clientes",
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["spark", "delta", "clientes"]
) as dag:

    executar_spark = BashOperator(
        task_id="executar_ingestao_delta",
        bash_command="docker exec spark /opt/spark/bin/spark-submit /opt/spark-apps/ingestao_delta_clientes.py"
    )

    executar_spark
