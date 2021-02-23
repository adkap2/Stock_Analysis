from main import *
import pandas as pd
from sentiment_analysis import *
from vaderSentiment.vaderSentiment.vaderSentiment import *
import pprint
import csv

def initiate(subreddit, env):

    reddit = praw.Reddit(client_id=env['client_id'],
                     client_secret=env['client_secret'],
                     password=env['password'],
                     user_agent=env['user_agent'],
                     username=env['username'])
    subreddit = reddit.subreddit(subreddit)
    print(reddit.user.me())
    return reddit, subreddit

# def get_post_names():
#     daily_disc = list()
#     string = "What Are Your Moves Tomorrow, January "
#     for i in range(1,31):
#         string1 = string + str(i) + ", 2021"
#         daily_disc.append(string1)
#     return daily_disc

def get_posts(reddit, subreddit, sub):
    posts = {}
    for submission in reddit.subreddit(sub).search('flair:"Daily Discussion"',sort= 'new', limit=100):
        posts[submission.title] = submission.url
    return posts


def get_comments(reddit, subreddit, sub, db, posts):
    wsb = db['wsb']
    post_dic_comments = {}
    count = 0
    for post in posts:
        count += 1
        if count > 45: #Daily Disc Jan 25
            print(f"Current post scraping is {post}")
            post_dic_comments[post] = []
            submission = reddit.submission(url=posts[post])
            submission.comments.replace_more(limit=150) #Switch to None for everything
            for comment in submission.comments.list():
                post_dic_comments[post].append((comment.body, comment.score))
            wsb.insert_one({'sub': sub, 'thread': post, 'comments': post_dic_comments[post]})
            print(f"Process is {(count/97)*100}% complete")
            print(f"Number of comments in {post} is {len(post_dic_comments[post])}")
        else:
            print(f"Process is {(count/97)*100}% complete")
        
    return post_dic_comments

def make_sentiment_vals(db):

    df = pd.DataFrame(columns=['Positive', 'Negative', 'Neutral', 'GME', 'PLTR'])

    thread_weights_list = get_sent(db)
    instances = count_instances(db)
    #print(thread_weights)
    for i in range(20):
        print(instances[i][0], instances[i][1])
    with open('sentiments.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Thread", "Positive", "Negative", "Neutral"])
        for threads in thread_weights_list:
            for key, value in threads.items():
                positive , negative = value['positive'], value['negative']
                neutral = value['neutral']
                writer.writerow([key, positive, negative, neutral])
    with open('stocks.cvs', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["GME", "PLTR"])
        for i in range(len(instances)):
            writer.writerow([instances[i][0], instances[i][1]])


# def get_submissions_with_psaw(sub, start):
#     api = PushshiftAPI()
#     submissions = list(api.search_submissions(q='Daily Discussion', a='AutoModerator', after=start,
#                     subreddit=sub,
#                     filter=['url', 'author', 'title', 'subreddit'],
#                     limit=10000))

#     for submission in submissions:
        

#         words = submission.title.split()
#         cashtags = list(set(filter(lambda word: word.lower().startswith('$'), words)))

#         if len(cashtags) > 0:
#             print(cashtags)
#             #print(submission.created_utc)
#             print(submission.title)
#             #print(submission.url)
#         #print(words)
#     return submissions

# def get_comments_with_psaw(sub, submissions):
#     api = PushshiftAPI()
#     #for submission in submissions:
#     comments = list(api.search_comments(q=submissions[3].title,
#                 subreddit=sub,
#                 limit=10))

#     print(len(comments))


