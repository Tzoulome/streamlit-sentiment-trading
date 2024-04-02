import streamlit as st
import pandas as pd
import sys
from datetime import datetime, timedelta

# from src.database_functions import read_db
from src.objects import sql_queries_objects
from src.streamlit_elements import generate_top_performers_table, generate_ticker_mentions_line_chart


st.set_page_config(page_title='Reddit Sentiment Trading', page_icon=':robot_face:')
st.title(':robot_face: :red[Reddit] Sentiment Trading')

st.header('Top Performers Mentions', anchor=False, divider='red')

performers_filters_col_1, performers_filters_col_2, performers_filters_col_3 = st.columns(3)
performers_filters_col_1.write('Comparison Perdiod:')
interval = performers_filters_col_2.slider(label='Interval', min_value=1, max_value=30, value=7, label_visibility='collapsed')
interval_unit = performers_filters_col_3.selectbox(label='Interval Unit', options=['hours', 'days'], index=1, label_visibility='collapsed')

# TODO: parametrise query
# TODO: Show data aggregated or by subreddit
# TODO: Create Heatmap
top_performers_df = generate_top_performers_table(
    sql_query=sql_queries_objects.all_recent_tickers,
    interval=interval,
    interval_unit=interval_unit
)

interval_cols_name = f'{interval} {interval_unit}'
st.dataframe(top_performers_df,
    use_container_width=True,
    column_config={
        'tickers': st.column_config.TextColumn('Ticker'),
        'previous_count': st.column_config.NumberColumn(f'# previous {interval_cols_name}'),
        'recent_count': st.column_config.NumberColumn(f'# current {interval_cols_name}'),
        'ticker_count_diff': st.column_config.NumberColumn('# diff'),
        'ticker_count_diff_perc': st.column_config.NumberColumn('% diff', format="%.2f %%")
    })


st.header('Ticker Analysis', anchor=False, divider='red')
ticker_filters_col_1, ticker_filters_col_2, ticker_filters_col_3 = st.columns(3)
ticker_filters_col_1.write('Select a tciker:')
ticker = ticker_filters_col_2.selectbox('Ticker:', top_performers_df['tickers'], label_visibility='collapsed')

ticker_mentions_df = generate_ticker_mentions_line_chart(
    sql_query=sql_queries_objects.ticker_selection_all_times,
    ticker=ticker
)

st.line_chart(ticker_mentions_df, x='created_at', y='posts')


# ticker_selection_all_times_feed_df = ticker_mentions_df[['subreddit', 'created_at', 'title', 'content', 'tickers']]
# ticker_selection_all_times_feed_df




# st.write(r"Review the regex pattern extraction from the posts titles - \b[A-Z-?]{2,5}\b:")
# tickers_review_df = read_db(sql_queries_objects.tickers_review)
# tickers_review_df

# st.write("Review popular tickers to identify the most common false positives (common accronyms or words):")
# tickers_count_df = read_db(sql_queries_objects.tickers_count)
# tickers_count_df