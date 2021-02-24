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


def get_stock_symbols(stock):
    
    url="https://pkgstore.datahub.io/core/nasdaq-listings/nasdaq-listed_csv/data/7665719fb51081ba0bd834fde71ce822/nasdaq-listed_csv.csv"
    s = requests.get(url).content
    companies = pd.read_csv(io.StringIO(s.decode('utf-8')))
    Symbols = companies['Symbol'].tolist()
    
    pass

def get_stock(symbol, start, end):

    yf.pdr_override()
    data = pdr.get_data_yahoo(symbol, start=start, end=end)
    df = pd.DataFrame(data)

    return df

def clean_data(data):
    del data['Adj Close']
    del data['Volume']
   
    return data

def plot_data(data):

    fig, ax = plt.subplots()
    ax.plot(data['Open_Norm'])
    ax.plot(data['High_Norm'])
    ax.plot(data['Mentions_Norm'])
    fig.tight_layout()
    ax.legend(['GME Opening Price', 'GME High Price','GME Mentions'])
    plt.show()

def main():

    connection = psycopg2.connect(host=config.DB_HOST, database=config.DB_NAME, user=config.DB_USER, password=config.DB_PASS)
    start_time = start = datetime.datetime(2021,1,10)
    end = datetime.date.today()
    symbol = "GME"
    df = get_stock(symbol, start_time, end)
    df = clean_data(df)


    SQL_Query = pd.read_sql_query('''SELECT count(*), dt::date
    from mention
    where stock_id in (11033, 22109)
    group by dt::date
    order by dt ASC;''', connection)


    df1 = pd.DataFrame(SQL_Query, columns=['count', 'dt'])

    df1['Date'] = df1['dt']
    del df1['dt']
    df1 = df1.set_index('Date')

    result = pd.merge(df, df1, how = 'outer', left_index=True, right_index=True)

    x = result[['count', 'Open', 'High']] #returns a numpy array
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)

    df = pd.DataFrame(x_scaled)
    df['Mentions_Norm'] = df[0]
    df['Open_Norm'] = df[1]
    df['High_Norm'] = df[2]
    del df[0]
    del df[1]
    result = result.reset_index()
    result = pd.merge(result, df, how = 'outer', left_index=True, right_index=True)

    print(result)
    plot_data(result)


if __name__=="__main__":
    main()