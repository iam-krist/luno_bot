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
currency_pair = 'ETHUSDC'
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
price_aim = []
average_ask = []
average_bid = []
high_ask = []
low_ask = []
high_bid = []
low_bid = []
time_string = []
sma = []
sma_price_diff = []

# Test Variable of Momentum
momentum = []


# ******************************************************************************************




def handler(tick_raw):
    # Sets current moment of time to var
    now = datetime.datetime.now().strftime('%H:%M | %S')

    # Add current values to containers
    asks.append(round(float(tick_raw['ask'])))
    bids.append(round(float(tick_raw['bid'])))
    average_ask.append(int(sum(asks) / len(asks)))
    average_bid.append(int(sum(bids) / len(bids)))
    high_ask.append(max(asks))
    low_ask.append(min(asks))
    high_bid.append(max(bids))
    low_bid.append(min(bids))
    time_string.append(now)
    price_aim.append((float(tick_raw['ask'])+float(tick_raw['bid']))/2)
    sma.append(sum(price_aim) / len(price_aim))




    # Set live data into datafield, wel ..frame
    matrix = pd.DataFrame(
            [price_aim, sma, asks, bids, average_ask, average_bid, high_ask, low_ask, high_bid, low_bid],
            index=['price', 'sma', 'asks', 'bids', 'average_ask', 'average_bid', 'high_ask', 'low_ask', 'high_bid', 'low_bid'],
            columns=time_string
        )
        

    sma_last_tick = matrix.loc['sma'][-1] 
    price_last_tick = matrix.loc['price'][-1]
    
    
    if sma_last_tick > price_last_tick:
        # Run if Price is less than Average
        sma_price_diff = sma_last_tick - price_last_tick
        momentum.append(-sma_price_diff)
        print('\nAverage is above with: ', sma_price_diff)
    elif price_last_tick > sma_last_tick:
        # Run if Price is Above Average
        sma_price_diff = price_last_tick - sma_last_tick
        momentum.append(sma_price_diff)
        print('\nPrice is above with: ', sma_price_diff)
    
    print('The momentum is: ',sum(momentum)/len(momentum))


 
    
    # Plot data to graph
    # if len(time_string) > 60:
    #     ax = plt.gca()

    #     matrix.plot(kind='line',x='sma',y='time_string', color='blue',ax=ax)
    #     matrix.plot(kind='line',x='price',y='time_string', color='green', ax=ax)
        

    #     plt.show()

    




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

            # Get Markets Data
            # market_df = connection.markets()
            # print(market_df)
            
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


