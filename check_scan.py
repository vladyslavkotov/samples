from ibapi.contract import Contract
from classes import App_1
from symbol_list import symbol,same_date,t1
from func import *

import time, datetime
import numpy as np

# =======================================================================================
today=datetime.datetime.today()

today_f=today.strftime(format='%Y%m%d_%H%M%S')
clientID=today.strftime(format='%f')

app = App_1()
app.connect('127.0.0.1', 7496, clientID)

time.sleep(2)

log=f"logs/{today_f}_5_scan_check.txt"

g=0
while g < len(symbol):

    contract = Contract()
    contract.symbol = symbol[g].upper()
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"

    store = f"scan_storage/{contract.symbol.upper()}_5_control.csv"
    open(store, "x")

    app.run()

    app.reqHistoricalData(g, contract, "", "1 D", "5 mins", "TRADES", 1, 1, False, [])
    print(contract.symbol)

    v = 0
    ready=0
    while ready == 0:
        for x in App_1.a1:
            if x[7] ==1555:
                ready = 1
                break  # break is for for loop, not while loop
        time.sleep(0.1)
        print(v, end='\r')
        v += 1

    a1 = np.array(App_1.a1, dtype=np.float_)

    if len(App_1.a1) > 0:
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
    App_1.log = ""

    g+=1

app.disconnect()
