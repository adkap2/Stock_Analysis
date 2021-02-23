import pandas as pd
import matplotlib.pyplot as plt
import praw
import numpy as np
import os
import sys
import datetime
from praw.models import MoreComments
from pandas_datareader import data as pdr
import yfinance as yf
from gme import *
from webscraper import *
from prawcore.exceptions import Forbidden
import itertools
from vaderSentiment.vaderSentiment.vaderSentiment import *
from mongo import *
from dotenv import load_dotenv
from sentiment_analysis import *
from psaw import PushshiftAPI
import csv


def get_input_data():
    sub = input("What Subreddit would you like to look at: ")
    stock = input("What Stock would you like to see: ")
    print(f"Lets take a look at {sub} and {stock} stock ")
    
    return sub, stock

def load_env_vars():
    env = {}
    load_dotenv()
    env['client_id'] = os.getenv('client_id')
    env['client_secret'] = os.getenv("client_secret")
    env['password'] = os.getenv("password")
    env['user_agent'] = os.getenv("user_agent")
    env['username'] = os.getenv("username")
    print(env)
    return env


def main():
    env = load_env_vars()
    #sub, stock = get_input_data()
    sub = "WallStreetBets"
    stock = "GME"
    start = datetime.datetime(2021,1,1)
    end = datetime.date.today()
    stock = get_stock(stock, start, end)
    stock = clean_data(stock)
    
    print(stock)
    reddit, subreddit = initiate(sub, env)
    db = make_mongo_ses()
    #posts = get_posts(reddit, subreddit, sub)
    #comments = get_comments(reddit, subreddit, sub, db, posts)
    # submissions = get_submissions_with_psaw(sub, start)
    # get_comments_with_psaw(sub, submissions)
    # print(db.wsb.count())

    make_sentiment_vals(db)

        

if __name__=="__main__":

    main()
