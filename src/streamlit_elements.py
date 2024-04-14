from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import yfinance as yf

from src.database_functions import read_db


def generate_top_performers_table_data(
    sql_query:str,
    latest_period:tuple,
    previous_period:tuple
):
    '''
    '''
    min_date = min(previous_period)
    sal_params = {'min_date': min_date}

    tickers_df = read_db(sql_query, params=sal_params)
    # This also groups subreddits together:
    tickers_df = tickers_df.explode('tickers')

    previous_tickers_df = tickers_df[(tickers_df['created_at'].dt.date >= previous_period[0]) & (tickers_df['created_at'].dt.date < previous_period[1] + timedelta(days=1))]
    previous_tickers_df = previous_tickers_df.groupby(['tickers'])['id'].nunique().reset_index(name='previous_count')

    recent_tickers_df = tickers_df[(tickers_df['created_at'].dt.date >= latest_period[0]) & (tickers_df['created_at'].dt.date < latest_period[1] + timedelta(days=1))]
    recent_tickers_df = recent_tickers_df.groupby(['tickers'])['id'].nunique().reset_index(name='recent_count')

    top_performers_df = previous_tickers_df.merge(recent_tickers_df, how='right', on='tickers')
    top_performers_df['ticker_count_diff'] = top_performers_df['recent_count'] - top_performers_df['previous_count']
    top_performers_df = top_performers_df.fillna(0)
    top_performers_df['ticker_count_diff_perc'] = ((top_performers_df['recent_count'] / top_performers_df['previous_count'] - 1) * 100).round(1)
    top_performers_df['tickers'] = '$' + top_performers_df['tickers']
    top_performers_df = top_performers_df.sort_values('ticker_count_diff', ascending=False).reset_index(drop=True)

    return top_performers_df


def generate_selected_ticker_charts_data(
    ticker_mentions_df,
    ticker_hitorical_price_df,
    ticker:str,
    time_granularity:str
):
    '''
    '''
    if not ticker_mentions_df.empty:
        ticker_mentions_df = ticker_mentions_df.explode('tickers')
        ticker_mentions_df = ticker_mentions_df[ticker_mentions_df['tickers'] == ticker]
        if time_granularity == 'day':
            ticker_mentions_df['created_at'] = ticker_mentions_df['created_at'].dt.date
        elif time_granularity == 'hour':
            ticker_mentions_df['created_at'] = ticker_mentions_df['created_at'].dt.strftime('%Y-%m-%d %H:00:00')
    
    ticker_mentions_df = ticker_mentions_df.drop(columns='tickers')
    ticker_mentions_prices_chart_df = ticker_mentions_df.groupby(['created_at'])['id'].nunique().reset_index(name='posts')

    ticker_mentions_prices_chart_df = ticker_mentions_prices_chart_df.merge(ticker_hitorical_price_df, how='outer', left_on='created_at', right_on='Date')
    ticker_mentions_prices_chart_df['Date'] = ticker_mentions_prices_chart_df['Date'].fillna(ticker_mentions_prices_chart_df['created_at'])
    ticker_mentions_prices_chart_df = ticker_mentions_prices_chart_df.drop(columns=['created_at'])

    ticker_mentions_table_df = ticker_mentions_df[['created_at', 'subreddit', 'username', 'title', 'content']].copy()

    return ticker_mentions_prices_chart_df, ticker_mentions_table_df