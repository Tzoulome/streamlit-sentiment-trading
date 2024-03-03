import os
from dotenv import load_dotenv
import sqlalchemy
from sqlalchemy import create_engine
import pandas as pd


load_dotenv(override=True)


def _connect_db():
    '''
    Connects to a PostgreSQL database with the credentials specified in a .env file
    Parameters:
        None
    Returns:
        engine: The SQLite database connection object.
    '''
    
    engine = create_engine(f"postgresql+psycopg2://{os.getenv('PGSQL_USERNAME')}:{os.getenv('PGSQL_PASSWORD')}@{os.getenv('PGSQL_HOST')}:{os.getenv('PGSQL_PORT')}/{os.getenv('PGSQL_DB')}")
    
    return engine


def read_db(sql:str):
    '''
    Runs a SELECT SQL statement to retrieve data from the PostgreSQL database into a Pandas DataFrame.
    Dependent Functions:
        _connect_db
    Parameters:
        sql: A SELECT SQL statement.
    Returns:
        df: the SQL result into a Pandas DataFrame.
    '''

    engine = _connect_db()
    with engine.connect() as session:

        df = pd.read_sql(sql, session)

    return df