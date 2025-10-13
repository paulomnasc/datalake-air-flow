from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import boto3
import json
import os
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

# Configurações do MinIO
# 1. Instanciar o Hook, referenciando o ID de conexão que você configurou
s3_hook = S3Hook(aws_conn_id='minio_conn')

# 2. Obter o Boto3 client configurado pelo Hook
s3_client = s3_hook.get_conn() 

# 3. Usar o client (agora configurado com "http://minio:9000")
response = s3_client.list_objects_v2(Bucket=BUCKET, Prefix=RAW_PREFIX)

BUCKET = 'lab01'
RAW_PREFIX = 'processed/raw/'
TRUSTED_PREFIX = 'processed/trusted/'

def validar_e_mover():
    response = s3.list_objects_v2(Bucket=BUCKET, Prefix=RAW_PREFIX)
    arquivos = response.get('Contents', [])

    for obj in arquivos:
        key = obj['Key']
        if not key.endswith('.json'):
            continue

        # Baixar o arquivo temporariamente
        local_file = '/tmp/temp.json'
        s3.download_file(BUCKET, key, local_file)

        # Validar JSON
        try:
            with open(local_file, 'r') as f:
                json.load(f)
        except Exception:
            print(f"Arquivo inválido: {key}")
            continue

        # Gerar novo nome com timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        base_name = os.path.basename(key).replace('.json', '')
        new_key = f"{TRUSTED_PREFIX}{base_name}_{timestamp}.json"

        # Copiar para zona trusted
        s3.copy_object(Bucket=BUCKET, CopySource=f"{BUCKET}/{key}", Key=new_key)
        s3.delete_object(Bucket=BUCKET, Key=key)
        print(f"Movido para trusted: {new_key}")

default_args = {
    'start_date': datetime(2023, 1, 1),
    'catchup': False
}

with DAG(
    dag_id='validate_and_move_persons_to_trusted',
    schedule_interval='@daily',
    default_args=default_args,
    description='Valida arquivos da zona raw e move para trusted com versionamento',
) as dag:

    validar_e_mover_task = PythonOperator(
        task_id='validar_e_mover',
        python_callable=validar_e_mover
    )