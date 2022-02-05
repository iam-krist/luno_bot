from locale import currency
from operator import index
import time
from luno_python.client import Client
import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv


# ****************************************************************************************

# *********************************Variables**********************************************

# ****************************************************************************************
# Variables for strategy
currency_pair = 'ETHZAR'
tick_ = 1 # <----- The tick interfal in seconds
data_field = 10 # <----- The amount of rows to track for each second# Luno API Key

# API Key & Secret
secret = 'ilkbZ6RQVQee11g_6KT7-jEOSN7pCbJoq09YWVSOmvw'
key = 'ebb7ge7q6u6dp'

# Looping variables
exit = False
initialized = False

# Create containers for price data
asks = []
bids = []
average_ask = []
average_bid = []
high_ask = []
low_ask = []
high_bid = []
low_bid = []

data_matrix = []
# ******************************************************************************************




def handler(tick_raw):
    # Sets current moment of time to var
    now = datetime.datetime.now().strftime('%H:%M:%S')

    # Add current values to containers
    asks.append(round(float(tick_raw['ask'])))
    bids.append(round(float(tick_raw['bid'])))
    average_ask.append(int(sum(asks) / len(asks)))
    average_bid.append(int(sum(bids) / len(bids)))
    high_ask.append(max(asks))
    low_ask.append(min(asks))
    high_bid.append(max(bids))
    low_bid.append(min(bids))

    data = {
        'asks':asks,
        'bids':bids,
        'average_ask':average_ask,
        'average_bid':average_bid,
        'high_ask':high_ask,
        'low_ask':low_ask,
        'high_bid':high_bid,
        'low_bid':low_bid,
    }
    
    matrix = pd.DataFrame(data)
    print(matrix['average_ask'])
    




# Main Function Declaration
def main():
    # Create a socket
    connection = Client(api_key_id=key, api_key_secret=secret)
    

    # Start the main loop
    while exit == False:

        # Initialize failback for exceptions
        try:
            # Get the tick data from API socket
            ticker = connection.get_ticker(pair=currency_pair)
            
            # Send the tick data to the handler
            handler(ticker)




        # Exeption Return
        except Exception as e:
            print(e)

        # Wait for the next tick period
        time.sleep(tick_)



# Execute the main function
if __name__ == '__main__':
    main()


