# Created on 2020/7/21

# This module is for importing, transforming and visualizing market data.

import numpy as np
import pandas as pd
from datetime import datetime
from datetime import timedelta
import random as random
import matplotlib.pyplot as plt
import bs4 as bs
import pickle
import requests
import pandas_datareader as pdr
from IPython.display import display, clear_output



def scrape_sp500_tickers():
    """
    Function that scrapes the SP500 from Wikipedia, using Beautiful Soup package.
    """
    
    # Getting the raw data
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    
    # Saving tables
    tickers = []
    
    # Looping through
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker[:-1])
        
    with open("sp500tickers.pickle","wb") as f:
        pickle.dump(tickers,f)
        
    return tickers



def get_assets_from_yahoo(list_assets, feature, start_time, end_time):
    """
    Function which extracts values associated to a feature for a list of assets between 2 dates, using Yahoo Finance data.
    
    The choices for the feature provided by Yahoo Finance are: 'High', 'Low', 'Open', 'Close', 'Volume', 'Adj Close'.
    """
    
    # Check the feature is right
    available_features = ['High', 'Low', 'Open', 'Close', 'Volume', 'Adj Close']
    try:
        assert(feature in available_features)
    except AssertionError:
        raise(AssertionError("Feature must be one of the following: 'High', 'Low', 'Open', 'Close', 'Volume', 'Adj Close'."))
    
    # Sort list
    listassets = np.sort(list_assets)
    
    # Initialization
    assets_adj_close = pd.DataFrame(data=None, columns=listassets)
    N = len(listassets)
    counter = 1
    
    # loop
    for i in range(N):
        print(i)
        # Printing status of execution
        clear_output(wait=True)
        display("Running... " + str(int(counter/N*100)) + '%')
        counter += 1
        
        try:
            adj_close_tmp = pdr.get_data_yahoo(listassets[i], start=start_time, end=end_time)[feature]
            assets_adj_close[listassets[i]] = adj_close_tmp
        except:
            print(listassets[i], " could not be imported.")

    return assets_adj_close