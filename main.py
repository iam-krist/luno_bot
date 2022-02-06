from multiprocessing import connection
import time
import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv, json
from luno_python.client import Client as luno_client


# Variables for strategy
currency_pair = 'ETHUSDC'
tick_ = 0.2 # <----- The tick interfal in seconds
data_field = 60 # <----- The amount of rows to track and also the divider | This should be 60, unless debugging

# Looping Values
exit = False

# User Login Details
f = open('user.json', "r")
raw = f.read()
user = json.loads(raw)



# Data Containers
time_data_sec = []
data_minute = {
    "prices": [],
    'sma': []
}
data_hour = {
    "time": [],
    "open_price": [],
    'close_price': [],
    'high_price': [],
    'low_price': []
}

# Main Function Declaration
def main():
    # Create a socket
    connection = luno_client(api_key_id=user['key'], api_key_secret=user['secret'])
    
    # Duration of session
    duration = int(0)

    # Start the main loop
    while exit == False:

        # Initialize failback for exceptions
        try:
            # Get the tick data from API socket
            ticker = connection.get_ticker(pair=currency_pair)
            # Get the current time
            now = datetime.datetime.now().strftime('%H:%M:%S -> ')        

            # Build Data Sets
            time_data_sec.append(now)
            data_minute['prices'].append((float(ticker['ask'])+float(ticker['bid']))/2)
            data_minute['sma'].append(sum(data_minute['prices'])/len(data_minute['prices']))



            if int(len(time_data_sec)) > data_field:
                # Runs after first passed minute

                # Pop the List to keep values below data_field
                data_minute['prices'].pop(0)
                data_minute['sma'].pop(0)
                time_data_sec.pop(0)


                # Create a data Frame For Current Minutes
                # df_min = pd.DataFrame(data_minute, columns = ['prices', 'sma'], index = time_data_sec)
                
                

                if duration % data_field == 0:
                    # Runs if a minute has passed

                    # Prints The last two lines of minute timeframe
                    # print(df_min.tail(2))
                    
                    if len(data_hour['time']) > 60:
                        data_hour['time'].pop(0)
                        data_hour['open_price'].pop(0)
                        data_hour['close_price'].pop(0)
                        data_hour['high_price'].pop(0)
                        data_hour['low_price'].pop(0)
                    else:
                        print('Still Building data for hour frame..', duration, ' out of 3600')

                    data_hour['time'].append(now)
                    data_hour['open_price'].append(data_minute['prices'][0])
                    data_hour['close_price'].append(data_minute['prices'][-1])
                    data_hour['high_price'].append(max(data_minute['prices']))
                    data_hour['low_price'].append(min(data_minute['prices']))

                    # Create a data Frame for Hour
                    df_hour = pd.DataFrame(data_hour, columns = ['open_price', 'close_price', 'high_price', 'low_price'], index = data_hour['time'])
                    print(df_hour)

                    
                # else:
                #     # Still initializing Starting Data
                #  

            # else:
            #     # Still initializing Starting Data
            #     




        # Exeption Return
        except Exception as e:
            print(e)

        # Increase the Duration of session
        duration += 1

        # Wait for the next tick period
        time.sleep(tick_)

# Execute the main function
if __name__ == '__main__':
    main()