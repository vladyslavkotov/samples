import datetime,time,re

'''
Simple countdown timer. Nothing impressive, I know, but I did use during dark times when Google timer was down.
'''

s1=input('enter time \n')
s1=s1.split(' ')

total=0

for x in s1:
    digits = ""
    unit = ""
    multiplier = 0

    for y in x:
        if y.isnumeric():
            digits+=y
        elif y.isalpha():
            unit+=y

        if unit=='s' or unit=='sec' or unit=='second' or unit =='seconds':
            multiplier=1
        elif unit=='m' or unit=='min' or unit=='minute' or unit =='minutes':
            multiplier=60
        elif unit=='h' or unit=='hr' or unit =='hrs' or unit=='hour' or unit =='hours':
            multiplier=3600
        elif unit=='d' or unit=='day' or unit =='days':
            multiplier=3600*24

    total += int(digits) * multiplier
    print(digits, unit)

now = datetime.datetime.today().replace(microsecond=0)
next = now + datetime.timedelta(seconds=total)

while now != next:
    now = datetime.datetime.today().replace(microsecond=0)
    print(f'{next - now}', end="\r")
    time.sleep(0.1)