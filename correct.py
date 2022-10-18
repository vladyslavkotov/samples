import numpy as np,time,datetime
from os import remove
from shutil import copyfile
from func import *
from symbol_list import download_symbols

'''
Takes both daily and 1min arrays, removes duplicates and makes sure the days match. Uses tests from the func.py file - functions that start with check_
1. checks if each day is 540 candles long
2. checks if each day start with 700am
3. splits 2d array of 1min candles into 3d arrays of days of 1min candles and checks if dates match with daily candles
'''

# np.set_printoptions(threshold=np. inf)
# np.set_printoptions(formatter={'all': lambda x: str(x)})
t1=time.perf_counter()

today=datetime.datetime.today()
today_f=today.strftime(format='%Y%m%d_%H%M%S')

log=f"logs/{today_f}_correct.txt"
open(log, "x")

i=0
while i < len(download_symbols):

    min1= f'purgatory/{download_symbols[i].lower()}_1.csv'
    daily=f'purgatory/{download_symbols[i].lower()}_d.csv'

    l1 = np.genfromtxt(min1)
    l2 = np.genfromtxt(daily)

    l1 = ar_split_700(l1)

    l1 = np.delete(l1, ar_duplicate_days_1min(l1), 0)
    l2 = np.delete(l2, ar_duplicate_days_daily(l2), 0)

    print(ar_duplicate_days_1min(l1))
    print(ar_duplicate_days_daily(l2))

    content=f'{download_symbols[i].lower()}\n{check_1min(l1)}\n{check_all(l1, l2)}'

    with open(log, 'a') as o2:
        o2.write(f"{content}\n")

    flat = ar_flatten(l1)

    np.savetxt(f'storage/{download_symbols[i].lower()}_1.csv', flat, fmt='%s')
    np.savetxt(f'storage/{download_symbols[i].lower()}_d.csv', l2, fmt='%s')

    copyfile(min1,f'raw/{download_symbols[i].lower()}_1.csv')
    copyfile(daily, f'raw/{download_symbols[i].lower()}_d.csv')

    remove(min1)
    remove(daily)

    i+=1

t2=time.perf_counter()
print(t2-t1)