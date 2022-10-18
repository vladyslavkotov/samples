import numpy as np,time,datetime, os
from func import *
from symbol_list import symbol

np.set_printoptions(threshold=np. inf)
np.set_printoptions(formatter={'all': lambda x: str(x)})
t1=time.perf_counter()

today=datetime.datetime.today()
today_f=today.strftime(format='%Y%m%d_%H%M%S')

log=f"logs/{today_f}_compare_scan.txt"
open(log, "x")

i=0
while i < len(symbol):

    scan= f'scan_storage/{symbol[i].upper()}_5.csv'
    control=f'scan_storage/{symbol[i].upper()}_5_control.csv'

    arr1 = np.genfromtxt(scan).tolist()
    arr2 = np.genfromtxt(control).tolist()
    print(len(arr1)==len(arr2))

    for a, b in zip(arr1, arr2):
        if a != b:
            print(f'mismatch\n{symbol[i].lower()}\n{a}\n{b}\n------------------------------')
            with open(log, 'a') as o1:
                o1.write(f'{symbol[i].lower()}\n{a}\n{b}\n------------------------------\n')

    i+=1

t2=time.perf_counter()
print(t2-t1)