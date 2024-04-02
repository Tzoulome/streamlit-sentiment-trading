import pandas as pd
from datetime import datetime, timedelta
from src.database_functions import read_db


def generate_top_performers_table(
    sql_query:str,
    interval:int,
    interval_unit:str
):
    '''
    '''

    interval_sql_param = {'interval': str(interval * 2), 'interval_unit': interval_unit}
    # When the interval is in days, it also includes today for the most recent count.
    tickers_df = read_db(sql_query, params=interval_sql_param)
    # This also groups subreddits together:
    tickers_df = tickers_df.explode('tickers')

    previous_tickers_df = tickers_df[tickers_df['created_at'] < datetime.today() - pd.Timedelta(interval, interval_unit)]
    previous_tickers_df = previous_tickers_df.groupby(['tickers'])['id'].nunique().reset_index(name='previous_count')

    recent_tickers_df = tickers_df[tickers_df['created_at'] >= datetime.today() - pd.Timedelta(interval, interval_unit)]
    recent_tickers_df = recent_tickers_df.groupby(['tickers'])['id'].nunique().reset_index(name='recent_count')

    top_performers_df = previous_tickers_df.merge(recent_tickers_df, how='right', on='tickers')
    top_performers_df['ticker_count_diff'] = top_performers_df['recent_count'] - top_performers_df['previous_count']
    top_performers_df = top_performers_df.fillna(0)
    top_performers_df['ticker_count_diff_perc'] = ((top_performers_df['recent_count'] / top_performers_df['previous_count'] - 1) * 100).round(1)
    top_performers_df['tickers'] = '$' + top_performers_df['tickers']
    top_performers_df = top_performers_df.sort_values('ticker_count_diff', ascending=False).reset_index(drop=True)

    return top_performers_df


def generate_ticker_mentions_line_chart(
    sql_query:str,
    ticker:str
):
    '''
    '''
    ticker = ticker[1::]
    ticker_param = {'ticker': ticker}
    ticker_mentions_df = read_db(sql_query, params=ticker_param)

    ticker_mentions_df = ticker_mentions_df.explode('tickers')
    ticker_mentions_df = ticker_mentions_df[ticker_mentions_df['tickers'] == ticker]
    ticker_mentions_df = ticker_mentions_df.drop(columns='tickers')
    ticker_mentions_df['created_at'] = ticker_mentions_df['created_at'].dt.date
    ticker_mentions_df = ticker_mentions_df.groupby(['created_at'])['id'].nunique().reset_index(name='posts')
    ticker_mentions_df = ticker_mentions_df[ticker_mentions_df['created_at'] >= datetime(2024, 3, 1).date()]

    return ticker_mentions_df