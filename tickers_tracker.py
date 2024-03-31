import streamlit as st
import pandas as pd
import sys
from datetime import datetime, timedelta

from src.database_functions import read_db
from src.objects import sql_queries_objects

days_interval = 7
st.write(r"Tickers that increased the most:")

all_recent_tickers_df = read_db(sql_queries_objects.all_recent_tickers)

# This also groups subreddits together:
tickers_changes_df = all_recent_tickers_df[['tickers', 'created_at', 'id']]
tickers_changes_df = tickers_changes_df[tickers_changes_df['tickers'].notnull()]
tickers_changes_df = tickers_changes_df.explode('tickers')

all_recent_tickers_previous_df = tickers_changes_df[tickers_changes_df['created_at'] < datetime.today() - timedelta(days=days_interval)]
all_recent_tickers_previous_df = all_recent_tickers_previous_df.groupby(['tickers'])['id'].nunique().reset_index(name='previous_count')

all_recent_tickers_latest_df = tickers_changes_df[tickers_changes_df['created_at'] >= datetime.today() - timedelta(days=days_interval)]
all_recent_tickers_latest_df = all_recent_tickers_latest_df.groupby(['tickers'])['id'].nunique().reset_index(name='recent_count')

tickers_changes_df = all_recent_tickers_latest_df.merge(all_recent_tickers_previous_df, how='left', on='tickers')
tickers_changes_df = tickers_changes_df.rename(columns={'tickers': 'ticker'})
tickers_changes_df['ticker_count_diff'] = tickers_changes_df['recent_count'] - tickers_changes_df['previous_count']
tickers_changes_df = tickers_changes_df.fillna(0)
tickers_changes_df['ticker_count_diff_perc'] = tickers_changes_df['recent_count'] / tickers_changes_df['previous_count']
tickers_changes_df = tickers_changes_df.sort_values('ticker_count_diff', ascending=False).reset_index(drop=True)

# Trying to compensate relative changes outliers:
# total_recent_count = tickers_changes_df['recent_count'].sum()
# tickers_changes_df['compensated_change'] = (tickers_changes_df['recent_count'] / total_recent_count) * tickers_changes_df['ticker_count_diff_perc']


tickers_changes_df




ticker = st.selectbox('Ticker:', tickers_changes_df['ticker'])

ticker_select = {'ticker_select': ticker}
ticker_selection_all_times_df = read_db(sql_queries_objects.ticker_selection_all_times, params=ticker_select)
ticker_selection_all_times_timeseries_df = ticker_selection_all_times_df[['tickers', 'created_at', 'id']]
ticker_selection_all_times_timeseries_df = ticker_selection_all_times_timeseries_df.explode('tickers')
ticker_selection_all_times_timeseries_df = ticker_selection_all_times_timeseries_df[ticker_selection_all_times_timeseries_df['tickers'] == ticker]
ticker_selection_all_times_timeseries_df = ticker_selection_all_times_df[['created_at', 'id']]


ticker_selection_all_times_timeseries_df['created_at'] = ticker_selection_all_times_timeseries_df['created_at'].dt.date
ticker_selection_all_times_timeseries_df = ticker_selection_all_times_timeseries_df.groupby(['created_at'])['id'].nunique().reset_index(name='posts')
ticker_selection_all_times_timeseries_df = ticker_selection_all_times_timeseries_df[ticker_selection_all_times_timeseries_df['created_at'] >= datetime.today().date() - timedelta(days=30) ]
st.line_chart(ticker_selection_all_times_timeseries_df, x='created_at', y='posts')


ticker_selection_all_times_feed_df = ticker_selection_all_times_df[['subreddit', 'created_at', 'title', 'content', 'tickers']]
ticker_selection_all_times_feed_df




# st.write(r"Review the regex pattern extraction from the posts titles - \b[A-Z-?]{2,5}\b:")
# tickers_review_df = read_db(sql_queries_objects.tickers_review)
# tickers_review_df

# st.write("Review popular tickers to identify the most common false positives (common accronyms or words):")
# tickers_count_df = read_db(sql_queries_objects.tickers_count)
# tickers_count_df