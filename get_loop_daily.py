from ibapi.contract import Contract
from classes import App_d
from symbol_list import download_dates,download_symbols

import time, datetime
import numpy as np

'''
downloads 52 weeks of daily candles since the date specified in the dictionary we import for this particular stock.
'''

# =======================================================================================
today=datetime.datetime.today()

today_f=today.strftime(format='%Y%m%d_%H%M%S')
clientID=today.strftime(format='%f')

app = App_d()
app.connect('127.0.0.1', 7496, clientID)

time.sleep(2)

log=f"logs/{today_f}_d_get.txt"

weeks=52

g=0
while g < len(download_symbols):

    start_date = datetime.datetime.strptime(download_dates[g], '%Y%m%d')
    # start_date = datetime.datetime.strptime(same_date, '%Y%m%d_%H%M')

    start_date += datetime.timedelta(weeks=weeks)

    contract = Contract()
    contract.symbol = download_symbols[g].upper()
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"

    store = f"purgatory/{contract.symbol.lower()}_d.csv"
    open(store, "x")

    i=0
    while today+datetime.timedelta(weeks=weeks)>=start_date:

        app.run()

        date1=start_date.strftime(format='%Y%m%d 16:10:00')

        app.reqHistoricalData(g, contract, date1, f"{weeks} W", "1 day", "TRADES", 0, 1, False, [])
        print(contract.symbol,date1)
        time.sleep(5)

        if len(App_d.a1) > 0:
            a1 = np.array(App_d.a1, dtype=np.float_)

            with open(store, 'a') as o1:
                np.savetxt(o1, a1, fmt='%s')
            with open(log, 'a') as o2:
                o2.write(App_d.log_error)
                o2.write(f"\n{contract.symbol.lower()} {today_f}--TRUE\n\n")

        else:
            with open(log, 'a') as o2:
                o2.write(App_d.log_error)
                o2.write(f"\n{contract.symbol.lower()} {today_f}--FALSE--EMPTY\n\n")

        App_d.a1 = []
        App_d.log_error=""
        i+=1
        start_date += datetime.timedelta(weeks=weeks)

    g+=1

app.disconnect()
