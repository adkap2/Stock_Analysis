def get_submissions_with_psaw(sub, start):
    # Calls pushshift api and then plugs in author and post type and date range. This will yield a list of
    # Submissions
    api = PushshiftAPI()
    submissions = list(api.search_submissions(q='Daily Discussion', a='AutoModerator', after=start,
                    subreddit=sub,
                    filter=['url', 'author', 'title', 'subreddit'],
                    limit=10000))
    # Iterates through submission list to extract ticker symbols from each mention
    # These come in the form of cashtages
    # These are the values used to count the popularity of a stock
    # Over time
    for submission in submissions:
        words = submission.title.split()
        cashtags = list(set(filter(lambda word: word.lower().startswith('$'), words)))
        if len(cashtags) > 0:
            print(cashtags)
            print(submission.title)
    return submissions

def get_comments_with_psaw(sub, submissions):
    # This is used to extract comments
    # However getting comments was not the best method 
    # For running statistical analysis.
    api = PushshiftAPI()
    comments = list(api.search_comments(q=submissions[3].title,
                subreddit=sub,
                limit=10))
    return comments
