from main import *

from pymongo import MongoClient
import pprint



def make_mongo_ses():
    # Connect to the hosted MongoDB instance
    client = MongoClient('localhost', 27017)
    db = client['wsb']
    # Create a collection called wsb
    print(db.wsb.count())
    return db


def test_db(db):
    pprint.pprint(db.find_one())


