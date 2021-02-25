from main import *
import pandas as pd
from sentiment_analysis import *
from vaderSentiment.vaderSentiment.vaderSentiment import *
import pprint
import csv

def initiate(subreddit, env):
    """ initiate(subreddit, env) -> reddit (OBJ), subreddit (Obj)
    initiate initializes the praw reddit api based on client information
    supplied in the .env file locally. This is also initiallize the specific subreddit
    to look at (WallStreetBets)
    """
    reddit = praw.Reddit(client_id=env['client_id'],
                     client_secret=env['client_secret'],
                     password=env['password'],
                     user_agent=env['user_agent'],
                     username=env['username'])
    subreddit = reddit.subreddit(subreddit)
    return reddit, subreddit

def get_posts(reddit, subreddit, sub):
    """ get_posts(reddit, subreddit, sub) reddit (Obj), subreddit(Obj), sub(str)
    returns a dictionary of posts from subreddit based on flair category"""
    posts = {}
    for submission in reddit.subreddit(sub).search('flair:"Daily Discussion"',sort= 'new', limit=100):
        posts[submission.title] = submission.url
    return posts

def get_comments(reddit, subreddit, sub, db, posts):
    """ get_comments(reddit, subreddit, sub, db, posts) -> post_dic_comments (Dictionary)
    iterates through each post in posts, then builds a dictionary holding each post as key,
    value as list of comment objects containing body and comment score
    returns the dictionary object """
    wsb = db['wsb']
    post_dic_comments = {}
    count = 0
    for post in posts:
        count += 1
        print(f"Current post scraping is {post}")
        post_dic_comments[post] = []
        submission = reddit.submission(url=posts[post])
        submission.comments.replace_more(limit=150) #Switch to None for everything
        for comment in submission.comments.list():
            post_dic_comments[post].append((comment.body, comment.score))
        wsb.insert_one({'sub': sub, 'thread': post, 'comments': post_dic_comments[post]})
        print(f"Process is {(count/97)*100}% complete")
        print(f"Number of comments in {post} is {len(post_dic_comments[post])}")
        print(f"Process is {(count/97)*100}% complete")
    return post_dic_comments

def make_sentiment_vals(db):
    """ make_sentiment_vals(db) -> None
    builds the sentiment analysis data frame where it overlays sentiment values
    for a given date with stock prices for that date. creates csv file with sentiment and stock values
    for each stock and sentiment
    """
    df = pd.DataFrame(columns=['Positive', 'Negative', 'Neutral', 'GME', 'PLTR'])
    thread_weights_list = get_sent(db)
    instances = count_instances(db)
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

# def get_post_names():
#     daily_disc = list()
#     string = "What Are Your Moves Tomorrow, January "
#     for i in range(1,31):
#         string1 = string + str(i) + ", 2021"
#         daily_disc.append(string1)
#     return daily_disc
