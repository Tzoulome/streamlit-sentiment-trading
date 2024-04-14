import streamlit as st
import pandas as pd
import numpy as np
import sys
from datetime import datetime, timedelta
import altair as alt

from src.objects import sql_queries_objects
from src.database_functions import read_db
from src.streamlit_elements import generate_top_performers_table_data, generate_selected_ticker_charts_data
from src.yahoo_finance_functions import get_historical_ticker_price


st.set_page_config(page_title='Reddit Sentiment Trading', page_icon=':robot_face:')
st.title(':robot_face: :red[Reddit] Sentiment Trading')

# Parameters
min_date = datetime(2024, 3, 1).date()
today = datetime.today().date()


########################
## Top performers viz ##
########################

st.header('Top Performers Mentions', anchor=False, divider='red')
with st.form(key='performers_filters', border=False):
    performers_filters_col_1, performers_filters_col_2, performers_filters_col_3 = st.columns(3)
    previous_period = performers_filters_col_1.date_input(
        label='Previous comparison Period:',
        value=[today - pd.Timedelta(14, 'days'), today - pd.Timedelta(7, 'days')],
        min_value=min_date,
        max_value=today,
        format='DD/MM/YYYY'
    )
    latest_period = performers_filters_col_2.date_input(
        label='Latest comparison Period:',
        value=[today - pd.Timedelta(6, 'days'), today],
        min_value=min_date,
        max_value=today,
        format='DD/MM/YYYY'
    )
    performers_filters_col_3.text('')
    performers_filters_col_3.text('')
    performers_filters_submit_button = performers_filters_col_3.form_submit_button(label='Apply', use_container_width=True)

# TODO: parametrise query
# TODO: Show data aggregated or by subreddit
# TODO: Create Heatmap
top_performers_df = generate_top_performers_table_data(
    sql_query=sql_queries_objects.all_recent_tickers,
    latest_period=latest_period,
    previous_period=previous_period,
)

st.dataframe(
    top_performers_df,
    use_container_width=True,
    column_config={
        'tickers': st.column_config.TextColumn('Ticker'),
        'previous_count': st.column_config.NumberColumn(f'# Previous Period'),
        'recent_count': st.column_config.NumberColumn(f'# Current Period'),
        'ticker_count_diff': st.column_config.NumberColumn('# Diff'),
        'ticker_count_diff_perc': st.column_config.NumberColumn('% Diff', format="%.2f %%")
    })


#####################
## Ticker Analysis ##
#####################

st.header('Ticker Analysis', anchor=False, divider='red')
with st.form(key='analysis_filters', border=False):
    analysis_filters_col_1, analysis_filters_col_2, analysis_filters_col_3, analysis_filters_col_4 = st.columns(4)
    ticker = analysis_filters_col_1.selectbox('Ticker:', top_performers_df['tickers'])
    analysis_period = analysis_filters_col_2.date_input(
        label='Period:',
        value= [min_date, today],
        min_value=min_date,
        max_value=today,
        format='DD/MM/YYYY'
    )
    time_granularity = analysis_filters_col_3.selectbox('Granularity:', ['Days', 'Hours'])
    analysis_filters_col_4.text('')
    analysis_filters_col_4.text('')
    analysis_filters_submit_button = analysis_filters_col_4.form_submit_button(label='Apply', use_container_width=True)

ticker = ticker[1::]
time_granularity = time_granularity.lower()[:-1]
start_date = analysis_period[0]
# Change 'day' to time_granularity when the period will have time options.
end_date = analysis_period[1] + pd.Timedelta(1, 'day')
sql_params = {'ticker': ticker, 'start_date': start_date, 'end_date': end_date}

ticker_mentions_df = read_db(
    sql=sql_queries_objects.ticker_selected_mentions,
    params=sql_params
)

ticker_hitorical_price_df = get_historical_ticker_price(
    ticker=ticker,
    time_granularity=time_granularity,
    start_date=start_date,
    end_date=end_date
)

ticker_mentions_prices_chart_df, ticker_mentions_table_df = generate_selected_ticker_charts_data(
    ticker_mentions_df=ticker_mentions_df,
    ticker_hitorical_price_df=ticker_hitorical_price_df,
    ticker=ticker,
    time_granularity=time_granularity
)
mentions_chart = (
    alt.Chart(ticker_mentions_prices_chart_df)
    .mark_bar(point=True)
    .encode(x='Date', y='posts')
)

if not ticker_hitorical_price_df.empty:
    price_scale = alt.Scale(domain=[ticker_mentions_prices_chart_df['Low'].min(), ticker_mentions_prices_chart_df['High'].max()])
    ticker_price_chart = (
        alt.Chart(ticker_mentions_prices_chart_df)
        .mark_area(point=True, color='red')
        .encode(
            alt.X('Date'),
            alt.Y('High', scale=price_scale),
            alt.Y2('Low'), color=alt.value('red'))
    )
    ticker_chart = (
        alt.layer(mentions_chart, ticker_price_chart)
        .resolve_scale(y='independent')
    )
    st.altair_chart(ticker_chart, use_container_width=True)

else:
    st.write(f":red[No price history was returned from yfinance using this ticker.]")
    st.altair_chart(mentions_chart, use_container_width=True)


st.dataframe(ticker_mentions_table_df)