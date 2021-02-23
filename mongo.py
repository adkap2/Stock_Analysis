import pyspark as ps
import pyspark as ps    # for the pyspark suite
from pyspark.sql.functions import col, array_contains
from main import *

from pymongo import MongoClient
import pprint


def make_spark_ses():
    spark = ps.sql.SparkSession.builder.getOrCreate()
    sc = spark.sparkContext

def make_mongo_ses():
    # Connect to the hosted MongoDB instance
    client = MongoClient('localhost', 27017)
    db = client['wsb']
    # Create a collection called wsb
    print(db.wsb.count())
    
    return db


def test_db(db):
    pprint.pprint(db.find_one())


