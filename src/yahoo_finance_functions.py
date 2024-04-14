from datetime import datetime, timedelta
import pandas as pd
import yfinance as yf

def get_historical_ticker_price(
    ticker:str,
    time_granularity:str,
    start_date:datetime.date,
    end_date:datetime.date
):
    '''

    Parameters:
        - tciker: the ticker symbol to return historical price on, without the leading $, can be lowercase or uppercase.
        - time_granularity: the time granularity the prices serie should be returned by, can be 'day' or 'hour'.
        - start_time: From which date (inclusive) the prices serie should be returned.
        - end_date: Until which date (inclusive) the prices serie should be returned.
    '''

    ticker_yf = yf.Ticker(ticker)

    ticker_history_df = ticker_yf.history(start=start_date, end=end_date, interval=f'1{time_granularity[:1]}')
    ticker_history_df = ticker_history_df.reset_index()
    if not ticker_history_df.empty:

        if time_granularity == 'day':
            ticker_history_df['Date'] = ticker_history_df['Date'].dt.date

        elif time_granularity == 'hour':
            ticker_history_df = ticker_history_df.rename(columns={'Datetime': 'Date'})

            ticker_history_df['Date'] = ticker_history_df['Date'].dt.tz_convert(None)
            # TODO: Consider that this also trims the time by 30 mins.
            ticker_history_df['Date'] = ticker_history_df['Date'].dt.strftime('%Y-%m-%d %H:00:00')

    ticker_hitorical_price_df = ticker_history_df[['Date', 'High', 'Low']].copy()

    return ticker_hitorical_price_df