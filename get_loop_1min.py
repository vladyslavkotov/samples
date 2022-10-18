from ibapi.contract import Contract
from classes import App_1
from symbol_list import download_symbols,t1
from func import *

import time, datetime
import numpy as np

'''
Using daily candles as a template, this downloads and normalizes 1 day of 1min candles per cycle.
All the search functions are written in numpy, hence we heavily depend on the arrays being symmetrical. Pre market data is anything but. It can start at 4 or at 7 or at 8 depending on how much vlm is traded on average. It can miss candles. Missed candles may or may not be masked.
correct_1day() function uses the imported template to normalize the raw data minute by minute. If this minute is present in the data, it copies it as the mask and skips it. If the minute is absent, it masks it.
'''

# =======================================================================================
today=datetime.datetime.today()

today_f=today.strftime(format='%Y%m%d_%H%M%S')
clientID=today.strftime(format='%f')

log=f"logs/{today_f}_1_get.txt"

app = App_1()
app.connect('127.0.0.1', 7496, clientID)

time.sleep(2)

g=0
while g < len(download_symbols):

    template = np.genfromtxt(f'purgatory/{download_symbols[g].lower()}_d.csv')

    contract = Contract()
    contract.symbol = download_symbols[g].upper()
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"

    store = f"purgatory/{contract.symbol.lower()}_1.csv"
    open(store, "x")

    i=0

    while i<len(template):

        app.run()

        start_date = datetime.datetime.strptime(str(template[i, 5]), '%Y%m%d.0')
        ready = 0

        # this here to make sure the whole thing doesnt get stuck on 1 day. There is a bug that doesnt let me download several days in a year, and I dont know why. But if you change the end time, it downloads fine

        date1=start_date.strftime(format=f'%Y%m%d 16:10:00')

        app.reqHistoricalData(g, contract, date1, "1 D", "1 min", "TRADES", 0, 1, False, [])
        print(contract.symbol,date1)

        #constant waiting time via time.sleep() is unreliable. The speed with which it downloads the data is highly variable. So we have to wait and constantly check if the day is downloaded fully, because we cant risk writing incomplete days.

        v=0
        while ready == 0:
            for x in App_1.a1:
                if x[7] > 1600:
                    ready = 1
                    break #break is for for loop, not while loop
            time.sleep(0.1)
            print(v,end='\r')
            v+=1
            if v==300:
                break

        if len(App_1.a1) > 0:
            a1 = correct_1day(App_1.a1, t1)
            # print(a1[0])
            with open(store, 'a') as o1:
                np.savetxt(o1, a1, fmt='%s')
            with open(log, 'a') as o2:
                o2.write(App_1.log_error)
                o2.write(f"\n{contract.symbol.lower()} {today_f}--TRUE\n\n")

        else:
            with open(log, 'a') as o2:
                o2.write(App_1.log_error)
                o2.write(f"\n{contract.symbol.lower()} {today_f}--FALSE--EMPTY\n\n")

        App_1.a1 = []
        App_1.log_error = ""
        i+=1

    g+=1

app.disconnect()
