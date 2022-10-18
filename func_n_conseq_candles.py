import numpy as np, time, datetime, os
from func import *
from conditions import *


'''
A search function that looks for n or more consecutive green candles, which helps identify overextended moves.
'''

# np.set_printoptions(threshold=np. inf)
np.set_printoptions(formatter={'all': lambda x: str(x)})
t1 = time.perf_counter()

l1 = np.genfromtxt('storage/amd_1.csv')

l1=ar_separate_RTH_split(l1)
l1=ar_flatten(l1)
l1=ar_timeframe(l1,15)
l1=ar_split930(l1)

c1=search_green_intraday_gt_or_eq(l1, 3)
print('start')
for x in c1:
    print(x)
print(len(c1))

'''
sample outout

[[20220908.0, 1415.0], [20220908.0, 1430.0], [20220908.0, 1445.0], [20220908.0, 1500.0], [20220908.0, 1515.0]]
[[20220909.0, 1230.0], [20220909.0, 1245.0], [20220909.0, 1300.0], [20220909.0, 1315.0]]
[[20220909.0, 1445.0], [20220909.0, 1500.0], [20220909.0, 1515.0], [20220909.0, 1530.0]]
[[20220912.0, 1200.0], [20220912.0, 1215.0], [20220912.0, 1230.0], [20220912.0, 1245.0], [20220912.0, 1300.0]]
[[20220912.0, 1430.0], [20220912.0, 1445.0], [20220912.0, 1500.0]]
[[20220914.0, 1030.0], [20220914.0, 1045.0], [20220914.0, 1100.0]]
[[20220914.0, 1215.0], [20220914.0, 1230.0], [20220914.0, 1245.0]]
[[20220915.0, 1115.0], [20220915.0, 1130.0], [20220915.0, 1145.0]]
[[20220915.0, 1215.0], [20220915.0, 1230.0], [20220915.0, 1245.0], [20220915.0, 1300.0], [20220915.0, 1315.0]]
[[20220916.0, 1000.0], [20220916.0, 1015.0], [20220916.0, 1030.0]]
[[20220919.0, 930.0], [20220919.0, 945.0], [20220919.0, 1000.0]]
[[20220919.0, 1415.0], [20220919.0, 1430.0], [20220919.0, 1445.0], [20220919.0, 1500.0], [20220919.0, 1515.0], [20220919.0, 1530.0]]
[[20220920.0, 1445.0], [20220920.0, 1500.0], [20220920.0, 1515.0], [20220920.0, 1530.0]]
[[20220921.0, 945.0], [20220921.0, 1000.0], [20220921.0, 1015.0]]
[[20220921.0, 1315.0], [20220921.0, 1330.0], [20220921.0, 1345.0]]
[[20220923.0, 1500.0], [20220923.0, 1515.0], [20220923.0, 1530.0]]
[[20220927.0, 1345.0], [20220927.0, 1400.0], [20220927.0, 1415.0], [20220927.0, 1430.0]]
[[20220928.0, 1445.0], [20220928.0, 1500.0], [20220928.0, 1515.0], [20220928.0, 1530.0]]
[[20220930.0, 930.0], [20220930.0, 945.0], [20220930.0, 1000.0], [20220930.0, 1015.0], [20220930.0, 1030.0], [20220930.0, 1045.0], [20220930.0, 1100.0]]
[[20221003.0, 945.0], [20221003.0, 1000.0], [20221003.0, 1015.0]]
[[20221003.0, 1245.0], [20221003.0, 1300.0], [20221003.0, 1315.0], [20221003.0, 1330.0]]
[[20221003.0, 1400.0], [20221003.0, 1415.0], [20221003.0, 1430.0], [20221003.0, 1445.0], [20221003.0, 1500.0]]
[[20221005.0, 1030.0], [20221005.0, 1045.0], [20221005.0, 1100.0], [20221005.0, 1115.0], [20221005.0, 1130.0], [20221005.0, 1145.0], [20221005.0, 1200.0], [20221005.0, 1215.0]]
[[20221005.0, 1245.0], [20221005.0, 1300.0], [20221005.0, 1315.0], [20221005.0, 1330.0]]
[[20221005.0, 1400.0], [20221005.0, 1415.0], [20221005.0, 1430.0], [20221005.0, 1445.0], [20221005.0, 1500.0]]
[[20221010.0, 1300.0], [20221010.0, 1315.0], [20221010.0, 1330.0], [20221010.0, 1345.0]]
[[20221011.0, 1000.0], [20221011.0, 1015.0], [20221011.0, 1030.0]]
[[20221011.0, 1100.0], [20221011.0, 1115.0], [20221011.0, 1130.0]]
[[20221012.0, 1045.0], [20221012.0, 1100.0], [20221012.0, 1115.0], [20221012.0, 1130.0], [20221012.0, 1145.0]]
[[20221012.0, 1230.0], [20221012.0, 1245.0], [20221012.0, 1300.0]]
[[20221012.0, 1345.0], [20221012.0, 1400.0], [20221012.0, 1415.0]]
[[20221013.0, 1030.0], [20221013.0, 1045.0], [20221013.0, 1100.0]]
[[20221013.0, 1230.0], [20221013.0, 1245.0], [20221013.0, 1300.0], [20221013.0, 1315.0]]
[[20221013.0, 1430.0], [20221013.0, 1445.0], [20221013.0, 1500.0]]

'''