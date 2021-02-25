def get_submissions_with_psaw(sub, start):
    api = PushshiftAPI()
    submissions = list(api.search_submissions(q='Daily Discussion', a='AutoModerator', after=start,
                    subreddit=sub,
                    filter=['url', 'author', 'title', 'subreddit'],
                    limit=10000))
    for submission in submissions:
        words = submission.title.split()
        cashtags = list(set(filter(lambda word: word.lower().startswith('$'), words)))
        if len(cashtags) > 0:
            print(cashtags)
            print(submission.title)
    return submissions

def get_comments_with_psaw(sub, submissions):
    api = PushshiftAPI()
    comments = list(api.search_comments(q=submissions[3].title,
                subreddit=sub,
                limit=10))
    return comments
