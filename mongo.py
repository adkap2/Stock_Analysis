from main import *
from pymongo import MongoClient
import pprint

def make_mongo_ses():
    """Creates mongo session with name 'wsb' for WallStreetBets
    Returns: the database"""
    # Connect to the hosted MongoDB instance
    client = MongoClient('localhost', 27017)
    db = client['wsb']
    # Create a collection called wsb
    return db
