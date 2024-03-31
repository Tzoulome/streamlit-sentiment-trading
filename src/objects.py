class sql_queries_objects:
    tickers_review = '''
    SELECT
        p.subreddit,
        p.created_at,
        p.title,
        pt.tickers
    
    FROM reddit.posts p
    LEFT JOIN reddit.posts_tickers pt
    ON p.id = pt.post_id

    WHERE pt.tickers IS NOT NULL

    ORDER BY created_at DESC;
    '''
    
    tickers_count = '''
    SELECT
        subreddit,
        ticker,
        COUNT (DISTINCT id) AS count
    FROM (
        SELECT
            p.id,
            p.subreddit,
            UNNEST(pt.tickers) AS ticker
        
        FROM reddit.posts p
        LEFT JOIN reddit.posts_tickers pt
        ON p.id = pt.post_id) p1
    GROUP BY subreddit, ticker
    ORDER BY count DESC;
    '''


    # Create 2 queries for all st uses: 1 which is all data up to 2 weeks ago (test size), and 1 parametrised per ticker which is all times.

    all_recent_tickers = '''
    SELECT
        p.id,
        p.subreddit,
        p.username,
        p.created_at,
        p.title,
        p.content,
        p.flair,
        p.url,
        p.is_stickied,
        pt.tickers

    FROM reddit.posts p
    LEFT JOIN reddit.posts_tickers pt
    ON p.id = pt.post_id

    WHERE p.created_at >= CURRENT_DATE - interval '14 days'
    
    ORDER BY p.created_at DESC;
    '''

    ticker_selection_all_times = '''
    SELECT
        p.id,
        p.subreddit,
        p.username,
        p.created_at,
        p.title,
        p.content,
        p.flair,
        p.url,
        p.is_stickied,
        pt.tickers

    FROM reddit.posts p
    LEFT JOIN reddit.posts_tickers pt
    ON p.id = pt.post_id

    WHERE %(ticker_select)s = ANY(pt.tickers)
    
    ORDER BY p.created_at DESC;
    '''