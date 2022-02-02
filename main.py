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
tick_period = 1 # <----- The tick interfal in seconds
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
    
    filename = "data.csv"
    # opening the file with w+ mode truncates the file
    f = open(filename, "w+")
    f.close()


    with open('data.csv', 'w', encoding='cp1251') as f:
        writer = csv.writer(f)

        writer.writerow(data)

        for row in data:
            writer.writerow(row)
            print(row)
            row += 1




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
        time.sleep(tick_period)



# Execute the main function
if __name__ == '__main__':
    main()



























# def calculations(asks, bids):
#     average_ask = int(sum(asks) / len(asks))
#     average_bid = int(sum(bids) / len(bids))
#     high_ask = max(asks)
#     high_bid = max(bids)
#     low_ask = min(asks)
#     low_bid = min(bids)
#     print(
#         '  -> Selling Price average: ', average_ask,'\n',
#         ' -> Buying Price average: ', average_bid,'\n',
#         ' -> Highest Selling Price: ', high_ask,'\n',
#         ' -> Highest Buying Price: ', high_bid,'\n',
#         ' -> Lowest Selling Price: ', low_ask,'\n',
#         ' -> Lowest Buying Price: ', low_bid
#     )


# def logger(pair, ask, bid, spread):
#     print_time = datetime.datetime.now().strftime('%H:%M:%S %Y-%m-%d')
#     print(
#         '\n',pair,' @ ',print_time , 
#         '\n--> Selling Price: ', ask, 
#         '\n--> Buying Price: ', bid, 
#         '\n--> Spread: ', spread
#     )


# def main():
#    
     
#     while exit == False:
#         try:            
#             ticker = connection.get_ticker(pair=currency_pair)
#             ask_price = round(float(ticker['ask']))
#             bid_price = round(float(ticker['bid']))
#             gap = ask_price - bid_price

#             asks.append(ask_price)
#             bids.append(bid_price)


#             #   ****************** Print Out The Arrays for bids and asks ****************
#             # print('Asks: ',asks,'\nBids: ',bids)


            
#             # Starts after data initialized
#             if len(asks) > data_flow:
#                 if initilized == False:
#                     print('Data Reached Cap | Now Initialized \n --> Bot Now Active')
#                     logger(currency_pair, ask_price, bid_price, gap)
#                     calculations(asks, bids)
#                     initilized = True
                
#                 asks.pop(0)
#                 bids.pop(0)
                
#                 if asks[-2] != ask_price or bids[-2] != bid_price:
#                     logger(currency_pair, ask_price, bid_price, gap)
#                     calculations(asks, bids)
                    
#             else:                
#                 print('Initializing... ', data_flow + 1 - len(asks))
            

            

#         except Exception as e:
#             print(e)   
#         time.sleep(period)
    
     


# if __name__ == '__main__':
#     main()

