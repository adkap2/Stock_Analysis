import pandas as pd
from main import *
import datetime
import yfinance as yf
from pandas_datareader import data as pdr
import sys
import matplotlib.pyplot as plt
import numpy as np
import config
import psycopg2
import psycopg2.extras
from sklearn import preprocessing
import matplotlib.dates as mdates
import os
from plotter import *
from scipy import stats


def get_stock(symbol, start, end):
    """ get_stock(symbol, start, end) -> Dataframe
    Takes a given stock symbol and a date range,
    then scrapes stock data from yahoo finance and returns as dataframe
    """
    yf.pdr_override()
    data = pdr.get_data_yahoo(symbol, start=start, end=end)
    df = pd.DataFrame(data)
    return df


def clean_data(data):
    """ clean_data(data) -> data
    drops unecessary columns from stock data
    """
    del data['Adj Close']
    del data['Volume']
    return data


def normalizer(df):
    """ normalizer(df) -> df
    normalizes data frame to values between 1 and -1
    """
    diff = df.max() - df.min()
    for i in range(len(df)):
        if df[i] > 0:
            df[i] = df[i]/diff
        else:
            df[i] = df[i]/diff
    return df


def organize_data(SQL_Query, symbol, start, end):
    """ organize_data(SQL_Query, symbol, start, end) -> dataframe
    takes in a sql query and a stock symbol to be analyzed.
    Then builds data frame from sql data base including stock price and number
    of times that stock is mentioned in posts for a given day.
    Then organizes the data into usable format by making gradient column
    and normalizing so that mentions can be directly compared to stock price.
    Finally makes specifc columnns for running statistical tests"""
    df = get_stock(symbol, start, end)
    df = clean_data(df)
    df1 = pd.DataFrame(SQL_Query, columns=['count', 'dt'])
    df1['Date'] = df1['dt']
    del df1['dt']
    df1 = df1.set_index('Date')
    result = pd.merge(df, df1, how='outer', left_index=True, right_index=True)
    result['Open-Close-Change'] = result['Close'] - result['Open']
    result['H-L-Change'] = result['High'] - result['Low']
    result['Change_Norm'] = result['Close'] - result['Open']
    result['Change_High_Low_Norm'] = result['High'] - result['Low']
    x = result[['count', 'Open', 'High']]  # returns a numpy array
    normalizer(result['Change_Norm'])
    normalizer(result['Change_High_Low_Norm'])
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    df = pd.DataFrame(x_scaled)
    df['Mentions_Norm'] = df[0]
    df['Open_Norm'] = df[1]
    df['High_Norm'] = df[2]
    df = df.drop([0, 1, 2], axis=1)
    result = result.reset_index()
    result = pd.merge(result, df, how=
        'outer', left_index=True, right_index=True)
    result['Mentions'] = result['count']
    result = result.drop(['count'], axis=1)
    result['Mentions-Diff'] = result['Mentions'].diff(periods=1)
    normalizer(result['Mentions-Diff'])
    result['Anova_Vals'] = (result['Mentions-Diff']*result['Change_Norm'])\
        .apply(lambda x: 1 if x > 0 else 0)
    return result


def main():
    """main() -> dataframes
    main function which calls all other functions from plot_stocks.
    Takes stock input and creates a connection to postgres db.
    handles error checking for invalid user input.
    returns the dataframe to overall program main file
    """
    symbol = input("What Stock would you like to see (Symbol): ")
    one_samples = {}
    dataframes = {}
    while symbol != 'q':
        connection = psycopg2.connect(host=config.DB_HOST, database=
            config.DB_NAME, user=config.DB_USER, password=config.DB_PASS)
        start_time = datetime.datetime(2021, 1, 1)
        end = datetime.date.today()
        queries = make_sql_queries()
        if symbol not in queries:
            print("Stock not in Database: Try Again")
        else:
            SQL_Query = pd.read_sql_query(queries[symbol], connection)
            result = organize_data(SQL_Query, symbol, start_time, end)
            plot_data(symbol, result)
            plot_changes(symbol, result)
            plot_high_low_changes(symbol, result)
            plot_full_values(symbol, result)
            plot_correlation_norm(symbol, result)
            dataframes[symbol] = result
        symbol = input("Grab another stock? Or press q to quit: ")
    return dataframes


def make_sql_queries():
    """ make_sql_queries() -> dic (Dictionary)
    dict of SQL queries to requested based on which stock
    is requested.
    Returns dictionary object"""
    dic = {}

    dic["GME"] = '''SELECT count(*), dt::date
    from mention
    where stock_id in (11033, 22109)
    AND dt::date BETWEEN '2021-01-1' AND '2021-02-25'
    group by dt::date
    order by dt ASC;'''

    dic["PLTR"] = '''SELECT count(*), dt::date
    from mention
    where stock_id in (21446, 10370)
    AND dt::date BETWEEN '2021-1-1' AND '2021-02-25'
    group by dt::date
    order by dt ASC;'''

    dic["AMC"] = '''SELECT count(*), dt::date
    from mention
    where stock_id in (9136, 20213)
    AND dt::date BETWEEN '2021-01-1' AND '2021-02-25'
    group by dt::date
    order by dt ASC;'''

    dic["SLV"] = '''SELECT count(*), dt::date
    from mention
    where stock_id in (10560, 21636)
    AND dt::date BETWEEN '2021-01-1' AND '2021-02-25'
    group by dt::date
    order by dt ASC;'''

    dic["NOK"] = '''SELECT count(*), dt::date
    from mention
    where stock_id in (10254, 21331)
    AND dt::date BETWEEN '2021-01-1' AND '2021-02-25'
    group by dt::date
    order by dt ASC;'''

    dic["TSLA"] = '''SELECT count(*), dt::date
    from mention
    where stock_id in (10766, 21842)
    AND dt::date BETWEEN '2021-01-1' AND '2021-02-25'
    group by dt::date
    order by dt ASC;'''

    dic["NIO"] = '''SELECT count(*), dt::date
    from mention
    where stock_id in (10224, 21301)
    AND dt::date BETWEEN '2021-01-1' AND '2021-02-25'
    group by dt::date
    order by dt ASC;'''

    dic["AAPL"] = '''SELECT count(*), dt::date
    from mention
    where stock_id in (22152)
    group by dt::date
    order by dt ASC;'''

    dic["ORCL"] = '''SELECT count(*), dt::date
    from mention
    where stock_id in (21388)
    AND dt::date BETWEEN '2021-01-1' AND '2021-02-25'
    group by dt::date
    order by dt ASC;'''

    dic["BABA"] = '''SELECT count(*), dt::date
    from mention
    where stock_id in (9826, 20903)
    group by dt::date
    order by dt ASC;'''

    dic["RKT"] = '''SELECT count(*), dt::date
    from mention
    where stock_id in (10476, 21552)
    group by dt::date
    order by dt ASC;'''

    dic["ZM"] = '''SELECT count(*), dt::date
    from mention
    where stock_id in (22144)
    group by dt::date
    order by dt ASC;'''

    return dic


if __name__ == "__main__":
    main()


# def get_stock_symbols(stock):
#     url="https://pkgstore.datahub.io/core/nasdaq-listings/nasdaq-listed_csv/data/7665719fb51081ba0bd834fde71ce822/nasdaq-listed_csv.csv"
#     s = requests.get(url).content
#     companies = pd.read_csv(io.StringIO(s.decode('utf-8')))
#     Symbols = companies['Symbol'].tolist()
