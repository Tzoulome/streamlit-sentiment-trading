class sql_queries_objects:

    all_recent_tickers = '''
    SELECT
        p.id,
        p.created_at,
        pt.tickers

    FROM reddit.posts p
    LEFT JOIN reddit.posts_tickers pt
    ON p.id = pt.post_id

    WHERE pt.tickers IS NOT NULL
    AND p.created_at >= %(min_date)s
    
    ORDER BY p.created_at DESC;
    '''

    ticker_selected_mentions = '''
    SELECT
        p.id,
        p.subreddit,
        p.username,
        p.created_at,
        p.title,
        p.content,
        pt.tickers
    
    FROM reddit.posts p
    LEFT JOIN reddit.posts_tickers pt
    ON p.id = pt.post_id

    WHERE %(ticker)s = ANY(pt.tickers)
    AND p.created_at >= %(start_date)s
    AND p.created_at < %(end_date)s
    
    ORDER BY p.created_at DESC;
    '''