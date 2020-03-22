from sqlalchemy import create_engine
import yaml


with open("config.yaml", 'r') as f:
    try:
        config = yaml.load(Loader=yaml.FullLoader, stream=f)
    except yaml.YAMLError as exc:
        print(exc)


def postgres_connection():
    """
    Connection object for Postgres
    :return: SQLAlchemy connection
    """
    database_uri = config['databases']['postgres']['uri']
    configured_database_uri = database_uri.format(database='nasa')
    engine = create_engine(configured_database_uri)
    return engine


if __name__ == "__main__":
    postgres_connection()
