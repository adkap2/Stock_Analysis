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
import plot_stocks
from webscraper import *
from prawcore.exceptions import Forbidden
import itertools
from vaderSentiment.vaderSentiment.vaderSentiment import *
from mongo import *
from dotenv import load_dotenv
from sentiment_analysis import *
from psaw import PushshiftAPI
import psaw_getter
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
    return env

def access_comments():
    env = load_env_vars()
    sub, stock = get_input_data()
    start = datetime.datetime(2020,12,16)
    end = datetime.date.today()
    stock = plot_stocks.get_stock(stock, start, end)
    stock = plot_stocks.clean_data(stock)
    reddit, subreddit = initiate(sub, env)
    db = make_mongo_ses()
    posts = get_posts(reddit, subreddit, sub)
    comments = get_comments(reddit, subreddit, sub, db, posts)
    submissions = psaw_getter.get_submissions_with_psaw(sub, start)
    psaw_getter.get_comments_with_psaw(sub, submissions)
    make_sentiment_vals(db)

def main():
    # access_comments()
    plot_stocks.main()

if __name__=="__main__":
    main()
