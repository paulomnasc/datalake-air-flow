from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow import settings
from airflow.www.security import utils

def create_admin_user():
    session = settings.Session()
    user = utils.get_user_by_username('admin')
    if not user:
        utils.create_user(
            username='admin',
            firstname='Air',
            lastname='Flow',
            email='admin@example.com',
            role='Admin',
            password='admin',
            session=session
        )
        print("✅ Usuário admin criado com sucesso!")
    else:
        print("ℹ️ Usuário admin já existe.")

with DAG(
    dag_id='create_admin_user_dag',
    start_date=days_ago(1),
    schedule_interval=None,
    catchup=False,
    tags=['setup']
) as dag:

create_user_task = PythonOperator(
    task_id='create_admin_user',
    python_callable=create_admin_user
)