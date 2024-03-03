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