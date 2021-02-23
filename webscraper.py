from main import *
import pprint

def initiate(subreddit, env):

    reddit = praw.Reddit(client_id=env['client_id'],
                     client_secret=env['client_secret'],
                     password=env['password'],
                     user_agent=env['user_agent'],
                     username=env['username'])
    subreddit = reddit.subreddit(subreddit)
    print(reddit.user.me())
    return reddit, subreddit

def get_post_names():
    
    daily_disc = list()
    
    string = "What Are Your Moves Tomorrow, January "
    for i in range(1,31):
        string1 = string + str(i) + ", 2021"
        daily_disc.append(string1)
    return daily_disc

def get_posts(reddit, subreddit, sub):
    posts = {}
    for submission in reddit.subreddit(sub).search('flair:"Daily Discussion"',sort= 'new', limit=100):
        posts[submission.title] = submission.url
    return posts


def get_comments(reddit, subreddit, sub, wsb, posts):
    post_dic_comments = {}
    for post in posts:
        post_dic_comments[post] = []
        submission = reddit.submission(url=posts[post])
        submission.comments.replace_more(limit=200) #Switch to None for everything
        for comment in submission.comments.list():
            post_dic_comments[post].append((comment.body, comment.score))

        wsb.insert_one({'sub': sub, 'thread': post, 'comments': post_dic_comments[post]})

    posts = wsb.find({'sub': sub})
    for post in posts:
        pprint.pprint(post)
    return post_dic_comments


