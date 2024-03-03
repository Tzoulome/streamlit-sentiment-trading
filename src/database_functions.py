import sqlalchemy
from sqlalchemy import create_engine
import pandas as pd
import streamlit as st


def _connect_db():
    '''
    Connects to a PostgreSQL database with the credentials specified in a .env file
    Parameters:
        None
    Returns:
        engine: The SQLite database connection object.
    '''
    st.secrets["db_username"]
    engine = create_engine(f"postgresql+psycopg2://{st.secrets["db_username"]}:{st.secrets["db_password"]}@{st.secrets["db_host"]}:{st.secrets["db_port"]}/{st.secrets["db_db"]}")
    
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