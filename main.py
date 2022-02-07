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
tick_ = 0.777 # <----- The tick interfal in seconds (Use this to speed up time) | Default 1
data_field = 60 # <----- The amount of rows to track and also the divider | Default 60

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
    'diff': [],
    'high_price': [],
    'low_price': [],
    'sma_open_price': [],
    'sma_close_price': []
}
data_day = {
    "time": [],
    "open_price": [],
    'close_price': [],
    'diff': [],
    'high_price': [],
    'low_price': [],
    'sma_open_price': [],
    'sma_close_price': []
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
                    # Runs every minute
                    
                    # Parse Time
                    data_hour['time'].append(now)

                    # Parse Open And Closing Values Also SMA
                    data_hour['open_price'].append(data_minute['prices'][0])
                    data_hour['close_price'].append(data_minute['prices'][-1])
                    data_hour['sma_open_price'].append(sum(data_hour['open_price'])/len(data_hour['open_price']))
                    data_hour['sma_close_price'].append(sum(data_hour['close_price'])/len(data_hour['close_price']))
                    data_hour['diff'].append(data_hour['close_price'][-1] - data_hour['open_price'][-1])

                    # Parse High and Low
                    data_hour['high_price'].append(max(data_minute['prices']))
                    data_hour['low_price'].append(min(data_minute['prices']))
                    
                    # Runs after a hours data is colected
                    if len(data_hour['time']) > data_field:
                        # Pop the values to stay a 1 hour frame
                        data_hour['time'].pop(0)
                        data_hour['open_price'].pop(0)
                        data_hour['close_price'].pop(0)
                        data_hour['high_price'].pop(0)
                        data_hour['low_price'].pop(0)
                        data_hour['diff'].pop(0)
                        data_hour['sma_open_price'].pop(0)
                        data_hour['sma_close_price'].pop(0)     

                        
                    else:
                        print('\nStill Building data for hour frame..', duration, ' out of ', data_field*data_field)

                    # Create a data Frame for Hour
                    df_hour = pd.DataFrame(data_hour, columns = ['time', 'open_price', 'close_price', 'diff', 'sma_open_price', 'sma_close_price', 'high_price', 'low_price'])
                    
                    print('\nMinute Complete\n\n')
                    print(df_hour.tail(3).to_markdown())
                    

                    # Append to the Daily Graph every hour
                    if duration % (data_field*data_field) == 0:
                            
                            # Parse Time
                            data_day['time'].append(now)

                            # Parse Open And Closing Values Also SMA
                            data_day['open_price'].append(data_hour['open_price'][0])
                            data_day['close_price'].append(data_hour['open_price'][-1])
                            data_day['sma_open_price'].append(sum(data_hour['open_price'])/len(data_hour['open_price']))
                            data_day['sma_close_price'].append(sum(data_hour['close_price'])/len(data_hour['close_price']))
                            data_day['diff'].append(data_day['close_price'][-1] - data_day['open_price'][-1])

                            # Parse High and Low
                            data_day['high_price'].append(max(data_hour['high_price']))
                            data_day['low_price'].append(min(data_hour['low_price']))
                            print('\n\n*****************************************************************')
                            print('\nHour Complete\n\n')
                            df_day = pd.DataFrame(data_day, columns = ['time', 'open_price', 'close_price', 'diff', 'sma_open_price', 'sma_close_price', 'high_price', 'low_price'])
                            print(df_day.to_markdown())
                            print('\n\n*****************************************************************')

                            # Runs after a day's data is colected
                            if len(data_day['time']) > 24:
                                # Pop the values to stay below a 24 hour frame
                                data_day['time'].pop(0)
                                data_day['open_price'].pop(0)
                                data_day['close_price'].pop(0)
                                data_day['high_price'].pop(0)
                                data_day['low_price'].pop(0)
                                data_day['diff'].pop(0)
                                data_day['sma_open_price'].pop(0)
                                data_day['sma_close_price'].pop(0)     

                                
                            else:
                                print('\nStill Building data for Daily frame..', duration, ' out of ', data_field*data_field*24)

                    # Write to a csv file
                    # if int(len(data_hour['time'])) == data_field:
                    #     df_hour.to_csv('data.csv')
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