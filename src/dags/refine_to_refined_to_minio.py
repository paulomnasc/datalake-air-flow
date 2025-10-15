import pandas as pd
import io
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from datetime import datetime

# ====================================================================
# VARIÁVEIS DE CONFIGURAÇÃO
# ====================================================================
BUCKET = 'lab01'
TRUSTED_KEY = 'processed/trusted/customers.parquet'
REFINED_KEY = 'processed/refined/customers_refined.parquet'

# ====================================================================
# FUNÇÃO DE REFINAMENTO
# ====================================================================
def refinar_customers():
    s3_hook = S3Hook(aws_conn_id='minio_conn')
    s3_client = s3_hook.get_conn()

    # 🔹 1. Carregar dados da zona trusted
    obj = s3_client.get_object(Bucket=BUCKET, Key=TRUSTED_KEY)
    df = pd.read_parquet(io.BytesIO(obj['Body'].read()))

    # 🔹 2. Preenchimento de dados faltantes
    df['creditLimit'] = df['creditLimit'].fillna(0)
    df['state'] = df['state'].fillna('N/A')
    df['salesRepEmployeeNumber'] = df['salesRepEmployeeNumber'].fillna(0)

    # 🔹 3. Colunas derivadas
    df['nome_completo'] = df['contactFirstName'].str.strip() + ' ' + df['contactLastName'].str.strip()
    df['valor_cliente'] = df['creditLimit']

    # 🔹 4. Segmentação por faixa de crédito
    df['faixa_credito'] = pd.cut(
        df['valor_cliente'],
        bins=[-1, 50000, 100000, 150000, float('inf')],
        labels=['Baixo', 'Médio', 'Alto', 'Premium']
    )

    # 🔹 5. Enriquecimento com taxa de câmbio simulada
    taxas = {
        'USA': 5.0, 'France': 5.3, 'Germany': 5.4, 'UK': 6.2,
        'Japan': 0.035, 'Canada': 3.8, 'Australia': 3.2, 'Spain': 5.1
    }
    df['taxa_cambio'] = df['country'].str.strip().map(taxas)
    df['credito_brl'] = df['valor_cliente'] * df['taxa_cambio']

    # 🔹 6. Curadoria final
    df_refinada = df[
        ['customerNumber', 'nome_completo', 'country', 'state', 'valor_cliente',
         'faixa_credito', 'credito_brl']
    ]

    # 🔹 7. Exportar para zona refinada
    buffer = io.BytesIO()
    df_refinada.to_parquet(buffer, index=False)

    s3_client.put_object(
        Bucket=BUCKET,
        Key=REFINED_KEY,
        Body=buffer.getvalue()
    )

    print(f"✅ Dados refinados salvos em: {REFINED_KEY}")

# ====================================================================
# DEFINIÇÃO DA DAG
# ====================================================================
default_args = {
    'start_date': datetime(2023, 1, 1),
    'catchup': False
}

with DAG(
    dag_id='refinar_customers',
    schedule_interval='@daily',
    default_args=default_args,
    description='Refina dados da tabela customers da zona trusted',
) as dag:

    refinar_customers_task = PythonOperator(
        task_id='refinar_customers',
        python_callable=refinar_customers,
        dag=dag
    )