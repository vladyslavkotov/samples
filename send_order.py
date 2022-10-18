import threading, time, datetime

from ibapi.contract import Contract
from ibapi.order import *
from ibapi import order_condition
from classes import Order_Sender

'''
Another helper script. Navigating IB platform is insufferably complex and slow. Especially adding conditions to orders, you have to perform like different actions to add a condition to an order. So I wrote this script to send orders from a console. Supports stocks and stock options. Can be used with the scanner. Each clientID is the number of microseconds currently elapsed since the beginning of the current second, highly unlikely they will ever match.

Accepts string like

aapl b 100 mkt
aapl b 100 lmt 145.60
aapl.150.c.20221021 b 1 mkt 
aapl.150.c.20221021 b 1 mkt if spy > 380

'''


# =======================================================================================
now=datetime.datetime.today().replace(microsecond=0)
clientID=datetime.datetime.today().strftime(format='%f')
print(clientID)
app = Order_Sender()
app.connect('127.0.0.1', 7496, clientID)

time.sleep(2)
app.run()
time.sleep(1)

i=1
while True:
    try:
        s1=input(str('symbol b/s quantity order_type lmt_price trigger_price\n'))
        if s1=='quit':
            app.disconnect()
            break
        else:
            s1=s1.split(' ')

            if len(s1[0])>5: #option

                option=s1[0].split('.')#aapl.180.p.exp_date

                contract = Contract()
                contract.symbol = option[0].upper()
                contract.secType = "OPT"
                contract.exchange = "BOX"
                contract.currency = "USD"
                contract.lastTradeDateOrContractMonth = option[3]
                contract.strike = option[1]
                contract.right = option[2].upper()
                contract.multiplier = "100"

            else: #stock

                contract = Contract()
                contract.symbol = s1[0].upper()
                contract.secType = "STK"
                contract.exchange = "SMART"
                contract.currency = "USD"

            order = Order()
            if s1[1]=='b':
                order.action = "BUY"
            elif s1[1] == 's':
                order.action = "SELL"
            else:
                print('invalid input')

            order.totalQuantity = s1[2]

            if s1[3]=='mkt':
                order.orderType = "MKT"

            elif s1[3] == 'lmt':
                order.orderType = "LMT"
                order.lmtPrice=float(s1[4])

            elif s1[3] == 'mit':
                order.orderType = "MIT"
                order.auxPrice = float(s1[4])

            elif s1[3] == 'lit':
                order.orderType = "LIT"
                order.lmtPrice = float(s1[4])
                order.auxPrice = float(s1[5])

            elif s1[3] == 'stlmt':
                order.orderType = "STP LMT"
                order.lmtPrice = float(s1[4])
                order.auxPrice = float(s1[5])

            elif s1[3] == 'stmkt':
                order.orderType = "STP"
                order.auxPrice = float(s1[4])

            if s1[4]=='if':

                contract1 = Contract()
                contract1.symbol = s1[5]
                contract1.secType = "STK"
                contract1.exchange = "SMART"
                contract1.currency = "USD"

                app.reqContractDetails(i, contract1)

                w1 = 0
                while Order_Sender.conid ==0:
                    time.sleep(0.1)
                    w1+=1
                    if w1==50:
                        print('cant retrieve symbol for condition')
                        break

                c1=order_condition.Create(order_condition.OrderCondition.Price)

                c1.conId=Order_Sender.conid
                c1.exchange="SMART"
                if s1[6]=='>':
                    c1.isMore=True
                elif s1[6]=='<':
                    c1.isMore = False
                else:
                    print('invalid input')

                c1.triggerMethod=0
                c1.price=s1[7]
                c1.isConjunctionConnection=False

                order.conditions.append(c1)

            app.placeOrder(i, contract, order)
            print(order.conditions)
            i += 1
            Order_Sender.conid=0

    except IndexError:
        print('invalid input')
