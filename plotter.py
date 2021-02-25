import pandas as pd
from main import *
import datetime
import numpy as np
import matplotlib.dates as mdates
import os


def plot_full_values(stock, data):
    """ plot_full_values(stock, data) -> None
    Takes in a stock and sataframe and plots number mentions vs stock price
    """
    data['Date'] = pd.to_datetime(data['Date']).dt.date
    x = np.arange(0,len(data))
    fig, ax = plt.subplots()
    ax.plot(x, data['Mentions'])
    ax.legend([f"{stock} Mentions"])
    plt.ylabel('Number of Mentions')
    plt.xlabel('Date')
    ax.set_xticklabels(data['Date'])
    plt.xticks(np.arange(0,len(x), 10), data['Date'][::10])
    plt.title(f"Mentions for {stock} \n between {data['Date'][0]} and {data['Date'][len(data)-1]}")
    fig.tight_layout()
    plt.show(block=False)
    plt.pause(2)
    plt.close()
    figname = f"figures/{stock}_Mentions"
    fig.savefig(figname)


def plot_data(stock, data):
    """ plot_data(stock, data) -> None
    Takes in a stock and sataframe and plots number mentions
    vs stock price Normalized
    """
    data['Date'] = pd.to_datetime(data['Date']).dt.date
    x = np.arange(0,len(data))
    fig, ax = plt.subplots()
    ax.plot(x,data['High_Norm'])
    ax.plot(x, data['Mentions_Norm'])
    ax.legend([F"{stock} Daily High Price", f"{stock} Mentions"])
    plt.ylabel('Normalized Value')
    plt.xlabel('Date')
    ax.set_xticklabels(data['Date'])
    plt.xticks(np.arange(0,len(x), 10), data['Date'][::10])
    plt.title(f"Mentions and Stock price for {stock} normalized\n between {data['Date'][0]} and {data['Date'][len(data)-1]}")
    fig.tight_layout()
    plt.show(block=False)
    plt.pause(2)
    plt.close()
    figname = f"figures/{stock}_Mentions_Price"
    fig.savefig(figname)

def plot_changes(stock, data):
    """ plot_changes(stock, data) -> None
    Takes in a stock and dataframe and plots changes (gradient)
    normalized vs stock price daily change (gradient) normalized
    """
    data['Date'] = pd.to_datetime(data['Date']).dt.date
    x = np.arange(0,len(data))
    fig, ax = plt.subplots()
    ax.plot(x,data['Change_Norm'])
    ax.plot(x, data['Mentions_Norm'])
    ax.legend([F"{stock} Daily Change", f"{stock} Mentions"])
    plt.ylabel('Normalized Value')
    plt.xlabel('Date')
    ax.set_xticklabels(data['Date'])
    plt.xticks(np.arange(0,len(x), 10), data['Date'][::10])
    plt.title(f"Mentions and Daily Stock Change for {stock} normalized\n between {data['Date'][0]} and {data['Date'][len(data)-1]}")
    fig.tight_layout()
    plt.show(block=False)
    plt.pause(2)
    plt.close()
    figname = f"figures/{stock}_Mentions_Changes"
    fig.savefig(figname)

def plot_high_low_changes(stock, data):
    """ plot_high_low_changes(stock, data) -> None
    Takes in a stock and dataframe and plots changes (gradient)
    normalized vs stock change (daily high, Low) (gradient) normalized
    """
    data['Date'] = pd.to_datetime(data['Date']).dt.date
    x = np.arange(0,len(data))
    fig, ax = plt.subplots()
    ax.plot(x,data['Change_High_Low_Norm'])
    ax.plot(x, data['Mentions_Norm'])
    ax.legend([F"{stock} Daily High, Low Change", f"{stock} Mentions"])
    plt.ylabel('Normalized Value')
    plt.xlabel('Date')
    ax.set_xticklabels(data['Date'])
    plt.xticks(np.arange(0,len(x), 10), data['Date'][::10])
    plt.title(f"Mentions and Daily High Low Stock Change for {stock} normalized\n between {data['Date'][0]} and {data['Date'][len(data)-1]}")
    fig.tight_layout()
    plt.show(block=False)
    plt.pause(2)
    plt.close()
    figname = f"figures/{stock}_High_Low_Changes_Mentions"
    fig.savefig(figname)
