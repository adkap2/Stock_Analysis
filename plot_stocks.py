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

def get_stock(symbol, start, end):
    yf.pdr_override()
    data = pdr.get_data_yahoo(symbol, start=start, end=end)
    df = pd.DataFrame(data)
    return df

def clean_data(data):
    del data['Adj Close']
    del data['Volume']
    return data

def organize_data(SQL_Query, symbol, start, end):
    df = get_stock(symbol, start, end)
    df = clean_data(df)
    df1 = pd.DataFrame(SQL_Query, columns=['count', 'dt'])
    df1['Date'] = df1['dt']
    del df1['dt']
    df1 = df1.set_index('Date')
    result = pd.merge(df, df1, how = 'outer', left_index=True, right_index=True)
    result['Open-Close-Change'] = result['Close'] - result['Open']
    result['H-L-Change'] = result['High'] - result['Low']
    result['Change_Norm'] = result['Close'] - result['Open']
    result['Change_High_Low_Norm'] = result['High'] - result['Low']
    x = result[['count', 'Open', 'High']] #returns a numpy array
    x1 = result['Change_Norm']
    max = x1.max()
    min = x1.min()
    diff = max - min
    for i in range(len(x1)):
        if x1[i] > 0:
            x1[i] = x1[i]/diff
        else:
            x1[i] = (x1[i]/diff)
    x2 = result['Change_High_Low_Norm']
    max = x2.max()
    min = x2.min()
    diff = max - min
    for i in range(len(x2)):
        if x2[i] > 0:
            x2[i] = x2[i]/diff
        else:
            x2[i] = (x2[i]/diff)
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    df = pd.DataFrame(x_scaled)
    df['Mentions_Norm'] = df[0]
    df['Open_Norm'] = df[1]
    df['High_Norm'] = df[2]
    del df[0]
    del df[1]
    del df[2]
    result = result.reset_index()
    result = pd.merge(result, df, how = 'outer', left_index=True, right_index=True)
    result['Mentions'] = result['count']
    result['Mentions-Diff'] = result['Mentions'].diff(periods=1)
    result['Mentions-Diff-(-1,1)'] = result['Mentions-Diff'].apply(lambda x: 1 if x >= 0 else - 1)
    result['Change-HL-(-1,1)'] = result['Change_High_Low_Norm'].apply(lambda x: 1 if x >= 0 else - 1)
    result['Anova_Vals'] = (result['Mentions-Diff-(-1,1)'] + result['Change-HL-(-1,1)']).apply(lambda x: 0 if x == 0 else 1)
    del result['count']
    return result

def main():
    symbol = input("What Stock would you like to see (Symbol): ")
    dataframes = {}
    while symbol != 'q':
        connection = psycopg2.connect(host=config.DB_HOST, database=config.DB_NAME, user=config.DB_USER, password=config.DB_PASS)
        start_time = start = datetime.datetime(2021,1,1)
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
            dataframes[symbol] = result
        symbol = input("Grab another stock? Or press q to quit: ")
    return dataframes

def make_sql_queries():
    dic = {}

    dic["GME"] = '''SELECT count(*), dt::date
    from mention
    where stock_id in (11033, 22109)
    AND dt::date BETWEEN '2021-01-1' AND '2021-02-22'
    group by dt::date
    order by dt ASC;'''

    dic["PLTR"] = '''SELECT count(*), dt::date
    from mention
    where stock_id in (21446, 10370)
    AND dt::date BETWEEN '2021-1-1' AND '2021-02-22'
    group by dt::date
    order by dt ASC;'''

    dic["AMC"] = '''SELECT count(*), dt::date
    from mention
    where stock_id in (9136, 20213)
    AND dt::date BETWEEN '2021-01-1' AND '2021-02-22'
    group by dt::date
    order by dt ASC;'''

    dic["SLV"] = '''SELECT count(*), dt::date
    from mention
    where stock_id in (10560, 21636)
    AND dt::date BETWEEN '2021-01-1' AND '2021-02-22'
    group by dt::date
    order by dt ASC;'''

    dic["NOK"] = '''SELECT count(*), dt::date
    from mention
    where stock_id in (10254, 21331)
    AND dt::date BETWEEN '2021-01-1' AND '2021-02-22'
    group by dt::date
    order by dt ASC;'''

    dic["TSLA"] = '''SELECT count(*), dt::date
    from mention
    where stock_id in (10766, 21842)
    AND dt::date BETWEEN '2021-01-1' AND '2021-02-22'
    group by dt::date
    order by dt ASC;'''

    dic["NIO"] = '''SELECT count(*), dt::date
    from mention
    where stock_id in (10224, 21301)
    AND dt::date BETWEEN '2021-01-1' AND '2021-02-22'
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
    AND dt::date BETWEEN '2021-01-1' AND '2021-02-22'
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

if __name__=="__main__":
    main()

# def get_stock_symbols(stock):
#     url="https://pkgstore.datahub.io/core/nasdaq-listings/nasdaq-listed_csv/data/7665719fb51081ba0bd834fde71ce822/nasdaq-listed_csv.csv"
#     s = requests.get(url).content
#     companies = pd.read_csv(io.StringIO(s.decode('utf-8')))
#     Symbols = companies['Symbol'].tolist()
