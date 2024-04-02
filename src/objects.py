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
    AND p.created_at >= CURRENT_DATE - interval %(interval)s%(interval_unit)s
    
    ORDER BY p.created_at DESC;
    '''

    ticker_selection_all_times = '''
    SELECT
        p.id,
        p.created_at,
        pt.tickers

    FROM reddit.posts p
    LEFT JOIN reddit.posts_tickers pt
    ON p.id = pt.post_id

    WHERE %(ticker)s = ANY(pt.tickers)
    
    ORDER BY p.created_at DESC;
    '''