import streamlit as st
import pandas as pd
import sys

from src.database_functions import read_db
from src.objects import sql_queries_objects


st.write("Review the regex pattern extraction from the posts titles - \b[A-Z-?]{2,5}\b:")
tickers_review_df = read_db(sql_queries_objects.tickers_review)
tickers_review_df

st.write("Review popular tickers to identify the most common false positives (common accronyms or words):")
tickers_count_df = read_db(sql_queries_objects.tickers_count)
tickers_count_df