from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from dags.nasa_api.models import Base
from dags.nasa_api.etl import API
import database_connections as db
import logging


logging.basicConfig(filename='logs/etl.log', format='%(asctime)s %(message)s', level=logging.INFO)


def db_init():
    logging.INFO('Connecting to database')
    engine = db.postgres_connection()
    try:
        logging.info('Dropping the table')
        Base.metadata.drop_all(engine)
        logging.info('Creating the table')
        Base.metadata.create_all(engine)
    except Exception as e:
        print(e)


# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'caitlin.johnson',
    'depends_on_past': False,
    'start_date': days_ago(2),
    'retries': 2,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
        'nasa_to_postgres',  # this is the id
        default_args=default_args,
        description='A simple tutorial DAG',
        schedule_interval=timedelta(days=1),
    )

# Tasks are generated when instantiating operator objects
initialize_db = PythonOperator(task_id='initialize_db',
                               python_callable=db_init,
                               dag=dag)

execute_etl = PythonOperator(task_id='execute_etl',
                             python_callable=API.main,
                             dag=dag)

initialize_db >> execute_etl
