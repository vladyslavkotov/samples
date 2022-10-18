import numpy as np
from matplotlib import pyplot as plt, ticker as tkr
from conditions import *

#correct and test

def ar_duplicate_days_1min(ar):
    '''
    for split 3d arrays. checks for duplicates i.e. same candle got downloaded twice
    returns list with indexes of duplicate days.
    '''
    c1 = []
    c2 = []
    c3 = []

    for x in ar:
        c1.append(x[0, 5])

    for i, x in enumerate(c1):
        if x in c2:
            c3.append(i)
        else:
            c2.append(x)
    return c3

def ar_duplicate_days_daily(ar):
    '''
    for daily 2d arrays. checks for duplicates i.e. same candle got downloaded twice
    returns list with indexes of duplicate days.
    '''
    c2 = []
    c3 = []

    for i, x in enumerate(ar[:,5]):
        if x in c2:
            c3.append(i)
        else:
            c2.append(x)
    return c3

def ar_start_700(ar):
    '''
    for split 1min 3d arrays with pre market ONLY. checks if each day starts with 0700 candle.
    empty list-test passed successfully
    '''
    error=[]
    for x in ar:
        if x[0,7]!=700:
            error.append(x[0,5])
    return error

def ar_RTH_time(ar):
    '''takes 3d 1min arrays, checks if every day starts at 930 and ends at 1559'''
    c1=[]
    for x in ar:
        if x[0,7]!=930 and x[-1,7]!=1559:
            c1.append(x)
    return c1

def ar_short_days_1(ar):
    '''
    accepts 3d array, returns list of indexes of incomplete days
    '''
    c1=[]
    for i,x in enumerate(ar):
        if len(x)!=540:
            c1.append(i)
    return c1

def ar_timeframe(ar, n):
    '''
    takes 2d continuous array of 1min candles, returns 2d array of n min candles
    '''
    c1=[]
    c2=[]
    c3=[]
    c4=[]
    assert 390%n==0,['Timeframe must be a divisor of 390']
    for candle in ar:
        if len(c1)<n:
            c1.append(candle)
            if len(c1)==n:
                c2.append(c1)
                c1=[]

    c2=np.array(c2)

    for a in c2:
        c3.append(a[0,0]) #open
        c3.append(np.max(a[:,1])) #high
        c3.append(np.min(a[:,2])) #low
        c3.append(a[-1, 3])
        c3.append(np.sum(a[:,4]))
        c3.append(a[0,5])
        c3.append(a[0, 6])
        c3.append(a[0, 7])
        c4.append(c3)
        c3=[]

    return np.array(c4)

def ar_flatten(ar):
    '''
    accepts a not-really-3d array, rather a 1d array of 2d array, we got from 1st split and flattens it.
    returns 2d array
    '''
    c1=[]
    for x in ar:
        for y in x:
            c1.append(y)
    return c1

def ar_split_700(ar):
    '''
    takes 2d continuous array of intraday candles, returns 3d array split into days
    '''
    split=[]
    for i,x in enumerate(ar):
        if x[7]==700 and i>0:
            split.append(i)
    return np.array(np.split(ar, split))

def ar_split930(ar):
    '''
    takes 2d continuous array of intraday candles, returns 3d array split into days
    '''
    split=[]
    for i,x in enumerate(ar):
        if x[7]==930 and i>0:
            split.append(i)
    return np.array(np.split(ar, split))

def ar_separate_RTH_split(ar):
    '''
    takes 2d continuous array of intraday candles, returns 3d array split into days without pre market
    '''
    split=[]
    delete=[]
    for i,x in enumerate(ar):
        if x[7]<930:
            delete.append(i)
    ar=np.delete(ar,delete,0)

    for i,x in enumerate(ar):
        if x[7]==930 and i>0:
            split.append(i)
    return np.array(np.split(ar, split))

def ar_separate_PM_split(ar):
    '''
    takes 2d continuous array of intraday candles, returns 3d array split into days of only pre market 700 - 929
    '''
    split=[]
    delete=[]
    for i,x in enumerate(ar):
        if x[7]>=930:
            delete.append(i)
    ar=np.delete(ar,delete,0)

    for i,x in enumerate(ar):
        if x[7]==700 and i>0:
            split.append(i)
    return np.array(np.split(ar, split))

def match_date(ar1, ar2):
    '''
    accepts split array and daily array, returns list of dates where daily date and intraday date dont match
    '''
    c1 = []
    for m, n in zip(ar1[:, 0, 5], ar2[:, 5]):
        if m != n:
            c1.append((m, n))
    return c1

def check_1min(ar):
    '''returns tests for 1min array'''
    return f''' 3 dimensions--{ar.ndim == 3}\n no duplicates 1min--{len(ar_duplicate_days_1min(ar)) == 0}\n days equal length--{len(ar_short_days_1(ar)) == 0}\n every day starts at 0700--{len(ar_start_700(ar)) == 0}'''

def check_daily(ar):
    '''returns test for duplicates for 1min array'''
    return f'no duplicates daily--{len(ar_duplicate_days_daily(ar)) == 0}'

def check_all(ar1, ar2):
    '''prints test for if daily and 5min arrays match in size and items'''
    return f' len 1min == len daily--{len(ar1) == len(ar2)}\n corrected 1min dates == corrected daily dates--{len(match_date(ar1, ar2)) == 0}\n no duplicates d--{len(ar_duplicate_days_daily(ar2)) == 0}'

def check_start_930(ar):
    '''returns test for duplicates for 1min array'''
    return f'starts at 930, ends at 1559--{len(ar_RTH_time(ar)) == 0}'

def correct_1day(ar, template: list):
    '''
    normalizes pre market for 1min arrays. accepts 2d array and template list with times
    '''

    c2 = []

    for candle in ar[:]:
        if candle[7] < 700 or candle[7] > 1559:
            ar.remove(candle)

    mask = ar[0].copy() #apparently this equal sign works both ways. if we equal and do not copy, changes in mask go the array as well

    for t in template:
        match = [c for c in ar if c[7] == t]
        mask[7] = t
        mask[4] = 0
        if match:
            c2.append(match[0])
            mask = match[0].copy()
        else:
            new_mask=mask.copy()
            c2.append(new_mask)

    return np.array(c2, dtype=np.float_)


#add indicators and values

def add_split_vwap(ar):
    '''
    takes 3d array of split intraday candles, adds cumvlm and vwap, returns array
    later we can add a reset at start of day to plot it on continuous array
    '''
    container=[]
    for x in ar: #one day, 2d ar
        vwap = []
        cumvlm = []
        total_dollars=0
        total_vlm=0
        for y in x: #one 5min candle
            total_vlm+=y[4]
            total_dollars+=(y[1]+y[2])/2*y[4]
            weighted_avg=total_dollars/total_vlm
            cumvlm.append(total_vlm)
            vwap.append(weighted_avg)
        vwap = np.around(vwap, decimals=2)
        x=np.column_stack((x,cumvlm,vwap))
        container.append(x)
    return np.array(container)

def add_sma(ar, length:int, input:int):
    '''
    simple mov avg for 2d arrays. input=col index of input data - close, vlm, hl/2, anything
    '''
    sma = []
    for i, x in enumerate(ar):
        if i < length - 1:
            sma.append(0)
        elif i >= length - 1:
            sma.append(np.average(ar[i + 1 - length:i + 1, input]))
    sma = np.around(sma, decimals=2)
    return np.array(np.column_stack((ar, sma)))

def add_ema(ar, length:int, input:int):
    '''
    exponential mov avg for 2d arrays.. input=col index of input data - close, vlm, hl/2, anything
    '''
    ema = []
    for i, x in enumerate(ar):
        if i < length - 1:
            ema.append(0)
        elif i >= length - 1:
            ema.append(np.average(ar[i + 1 - length:i + 1, input], weights=(np.arange(1, length + 1))))
    ema = np.around(ema, decimals=2)
    return np.array(np.column_stack((ar, ema)))

def add_gap(ar):
    '''daily gap'''
    shifted = np.around(np.roll(ar[:, 3], 1), decimals=2)
    gap = np.around((((ar[:, 0] * 100) / shifted) - 100), decimals=2)
    gap[0] = 0  # reassign incorrect 1st gap
    return np.array(np.column_stack((ar, gap)))

def add_dollar_range(ar):
    '''
    dollar range
    '''
    dollar_range = np.around((ar[:, 1] - ar[:, 2]), decimals=2)
    return np.array(np.column_stack((ar, dollar_range)))

def add_percent_range(ar):
    '''
    % range, negative and positive
    '''
    percent_range = []
    for x in ar:
        if x[0] < x[3]:
            percent_range.append((x[1] * 100 / x[2]) - 100)
        elif x[0] > x[3]:
            percent_range.append((x[2] * 100 / x[1]) - 100)
        elif x[0] == x[3]:
            percent_range.append(0)
    percent_range = np.around(percent_range, decimals=2)
    return np.array(np.column_stack((ar, percent_range)))

def add_anchored_vwap(ar, date:int, time:int):
    '''
    anchored vwap for 2d continuous arrays
    we can calculate how much $ value traded above and below avwap later
    if applied to daily, time=0
    '''
    avg = []
    cumvlm = []
    total_dollars = 0
    total_vlm = 0
    start=0
    for i,x in enumerate(ar): #x is one candle
        if x[5]==date and x[7]==time and start==0:
            avg.append(0)
            cumvlm.append(0)
        elif x[5]==date and x[7]==time or i>start:
            start=i
            total_vlm+=x[4]
            total_dollars+=(x[1]+x[2])/2*x[4]
            weighted_avg=total_dollars/total_vlm
            cumvlm.append(total_vlm)
            avg.append(weighted_avg)
    avg = np.around(avg, decimals=2)
    return np.array(np.column_stack((ar,cumvlm,avg)))

def add_midpoint(ar):
    '''
    midpoint. accepts 2d array, returns array
    '''
    dollar_range = np.around(((ar[:, 1] + ar[:, 2])/2), decimals=2)
    return np.array(np.column_stack((ar, dollar_range)))


#plot

def plot_days(ar,date:int,days_before:int=0, days_after:int=0):
    '''
    chart for specific date plus days before or after
    '''
    pos = np.argwhere(ar[:, 0, 5] == date)[0, 0]
    ar1=ar_flatten(ar[pos-days_before:pos+days_after+1])
    ar1=np.array(ar1)

    body = []
    colors = []
    days_total=days_after+days_before+1

    for x in ar1[:, (0, 3)]:
        body.append([np.max(x), np.min(x)])
        if x[1] > x[0]:
            colors.append('green')
        else:
            colors.append('red')

    body = np.array(body)
    colors = np.array(colors)

    timeline=[]
    ticks=[]

    c1 = np.array(ar1[:, (5,7)], dtype=np.int_)
    for a,b in c1:
        timeline.append(f'{a}_{b}')
        ticks.append(b)

    fig, (ax1, ax2) = plt.subplots(nrows=2, figsize=(days_total*5, 6), sharex=True, gridspec_kw={'height_ratios': [3, 1]})

    ax1.bar(timeline, ar1[:, 1] - ar1[:, 2], 0.3, ar1[:, 2], color='black')  # shadow
    ax1.bar(timeline, body[:, 0] - body[:, 1], 0.6, body[:, 1], color=colors)  # body
    ax2.bar(timeline, ar1[:, 4], 0.4, color='blue')

    fig.tight_layout()
    fig.subplots_adjust(bottom=0.2,right=1,wspace=0, hspace=0)
    # ax2.set_xlabel(f'{date}')

    ax2.ticklabel_format(style='plain',axis='y')
    # ax2.yaxis.set_major_formatter('{x:,.0f}')
    ax2.yaxis.set_major_formatter(tkr.EngFormatter())
    ax1.yaxis.set_major_formatter(tkr.EngFormatter()) ###not seeing any changes so far

    ax1.grid(which='major', axis='both',linewidth=0.5)
    ax2.grid(which='major',axis='both',linewidth=0.5)


    plt.xticks(np.arange(0,(78*days_total)+2,6),rotation=45,horizontalalignment='right')

    plt.show()

def plot_days_save(ar,date:int,days_before:int=0, days_after:int=0,folder:str="results"):
    '''
    chart for specific date plus days before or after
    '''
    date = int(date)
    pos = np.argwhere(ar[:, 0, 5] == date)[0, 0]
    ar1=ar_flatten(ar[pos-days_before:pos+days_after+1])
    ar1=np.array(ar1)

    body = []
    colors = []
    days_total=days_after+days_before+1

    for x in ar1[:, (0, 3)]:
        body.append([np.max(x), np.min(x)])
        if x[1] > x[0]:
            colors.append('green')
        else:
            colors.append('red')

    body = np.array(body)
    colors = np.array(colors)

    timeline=[]
    ticks=[]

    c1 = np.array(ar1[:, (5,7)], dtype=np.int_)
    for a,b in c1:
        timeline.append(f'{a}_{b}')
        ticks.append(b)

    fig, (ax1, ax2) = plt.subplots(nrows=2, figsize=(days_total*5, 6), sharex=True, gridspec_kw={'height_ratios': [3, 1]})

    ax1.bar(timeline, ar1[:, 1] - ar1[:, 2], 0.3, ar1[:, 2], color='black')  # shadow
    ax1.bar(timeline, body[:, 0] - body[:, 1], 0.6, body[:, 1], color=colors)  # body
    ax2.bar(timeline, ar1[:, 4], 0.4, color='blue')

    fig.tight_layout()
    fig.subplots_adjust(bottom=0.2,right=1,wspace=0, hspace=0)
    # ax2.set_xlabel(f'{date}')

    ax2.ticklabel_format(style='plain',axis='y')
    # ax2.yaxis.set_major_formatter('{x:,.0f}')
    ax2.yaxis.set_major_formatter(tkr.EngFormatter())
    ax1.yaxis.set_major_formatter(tkr.EngFormatter()) ###not seeing any changes so far

    ax1.grid(which='major', axis='both',linewidth=0.5)
    ax2.grid(which='major',axis='both',linewidth=0.5)

    plt.xticks(np.arange(0,(78*days_total)+2,6),rotation=45,horizontalalignment='right')

    plt.savefig(f'{folder}/{int(date)}') #if we dont convert to int here, it cant handle ".0"
    plt.close(fig)


#search

def search_green_intraday(ar, n:int):
    '''
    accepts 3d array
    searches for n consecutive green candles regardless of date
    returns 2d container with 1 subcontainer for each sequence.
    if >n green candles, it finds 1st n candles and doesnt see subsequent sets
    e.g. 5 candles in a row, it returns 1 2 3, doesnt find 2 3 4 and 3 4 5
    '''
    c1 = []  # large container
    c2 = []  # small container

    count = 0
    date=0

    for day in ar:
        c2 = []
        count = 0
        date=day_date(day)
        for i, candle in enumerate(day):
            if candle_close(candle) > candle_open(candle):
                if len(c2) == 0:
                    c2.append([candle_date(candle),candle_time(candle)])
                    count = i
                elif len(c2) > 0 and len(c2) < n and candle_date(candle)==date:
                    if i == count + 1:
                        c2.append([candle_date(candle),candle_time(candle)])
                        count = i
                        if len(c2) == n:
                            c1.append(c2)
                            c2 = []
                            count = 0
            else:
                c2 = []
                count = 0

    return c1

#n and more conseq candles
def search_green_intraday_gt_or_eq(ar, n:int):
    '''
    accepts 3d array
    searches for n consecutive green candles regardless of date
    returns 2d container with 1 subcontainer for each sequence.
    if >n green candles, it finds 1st n candles and doesnt see subsequent sets
    e.g. 5 candles in a row, it returns 1 2 3, doesnt find 2 3 4 and 3 4 5
    '''
    c1 = []  # large container
    c2 = []  # small container

    count = 0
    date=0

    for day in ar:
        c2 = []
        count = 0
        date=day_date(day)
        for i, candle in enumerate(day):
            if candle_close(candle) > candle_open(candle) and candle_date(candle)==date:
                if len(c2) == 0:
                    c2.append([candle_date(candle),candle_time(candle)])
                    count = i
                elif len(c2) > 0:
                    if i == count + 1:
                        c2.append([candle_date(candle),candle_time(candle)])
                        count = i
            else:
                if len(c2)<n:
                    c2 = []
                    count = 0
                elif len(c2)>=n:
                    c1.append(c2)
                    c2 = []
                    count = 0

    return c1
