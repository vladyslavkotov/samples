
same_date="20200901"

'''
Just a helper file to keep things that need to be imported more than once. DRY principle + less clutter in scripts.
'''

done={
'SPY':'20161230',
'QQQ':'20161230',
'AAPL':'20161230',
'MSFT':'20161230',
'ZM':'20190422',
'AMD':'20161230',
'TSLA':'20161230',
'INTC':'20161230',
'HD':'20161230',
'LOW':'20161230',
'WMT':'20161230',
}

maintain=[x for x in done]

download={

}

wait={

'MRNA':'20200225',

'X':'20161230',
'CLF':'20161230',
'PYPL':'20161230',

'NIO':'20180913',
'LI':'20200731',
'XPEV':'20200820',

'AMZN':'20161230',
'PLTR':'20201001',
'NVDA':'20161230',

'NVAX':'20200115',


'HOOD':'20210730',
'ASAN':'20201001',
'RBLX':'20210311',
'BA':'20161230',
'PG':'20161230',
'ROKU':'20170929',
'NFLX':'20171230',
'AMC':'20201109',
'GME':'20200831',
'AAL':'20200102',
'UAL':'20200102',
'APPS':'20200102',
'SNAP':'20170303',
'TWTR':'20161230',
'V':'20161230',
'MA':'20161230',
'OXY':'20200102',
'MRO':'20200102',
'NUE':'20200102',
'F':'20200102',
}

download_symbols=[x for x in download]
download_dates=[x for x in download.values()]

server_errors=[320,321,322,323,324]
connect_errors=[1100,2105,2103,2157,200,165]

# t1=[x for x in range(700,760)]
# t2=[x for x in range(800,860)]
# t3=[x for x in range(900,930)]
# t1.extend(t2)
# t1.extend(t3)

start_t1=700
t1=[]
for x in range(7,16):
    g=[m for m in range(start_t1, start_t1+60)]
    t1.extend(g)
    start_t1+=100

t5=[m for m in range(930,960,5)]
start_t5=1000
for x in range(10,16):
    g=[m for m in range(start_t5, start_t5+60,5)]
    t5.extend(g)
    start_t5+=100

# symbol = ['', 'QCOM', '', '', '', '', '', '', '', '', 'C', 'MU', '', '', '', '', '', 'STLD', 'UBER', 'FCX', 'XOM', '', '', 'V', '', 'MA', '', '', 'AMAT', 'LAC', 'ALB', 'GM', 'F', '', '', 'CHWY', 'MCD', 'TNDM', 'ABT', 'PFE', 'MRK', 'LLY', '', '', '', 'COST', 'PEP', 'KO', '', '', 'GOOGL', '', 'BILI', '', '', 'SPOT', '', '', 'ALK', '', 'LUV', '', 'LYFT', 'BLDR', 'LTHM', 'TECK','HCC', 'MP', 'DD', 'OLN', 'VVV', 'GPK', 'FAST', '', 'U', '', 'ADBE', '', 'ADSK', 'DOCU', '', 'HUT', 'TTD', 'NOW', 'CRM', 'BILL', 'ZEN', 'ORCL', 'ON', 'TSM', 'AMBA', 'ENPH', '', 'AVGO', 'FSLR', 'JKS', 'NPTN', 'MCHP', 'HPQ', 'DELL', 'JNPR']

in_question=['SPOT','META']

#real time scan
symbol = ['AMD', 'QCOM', 'NIO', 'LI', 'XPEV', 'AAPL', 'NVDA', 'SPY', 'QQQ', 'INTC', 'C', 'MU', 'MSFT', 'CLF', 'X', 'AA', 'NUE', 'STLD', 'UBER', 'FCX', 'XOM', 'SNAP', 'TWTR', 'V', 'PYPL', 'MA', 'TSLA', 'AMZN', 'AMAT', 'LAC', 'ALB', 'GM', 'F', 'HD', 'LOW', 'CHWY', 'MCD', 'TNDM', 'ABT', 'PFE', 'MRK', 'LLY', 'MRNA', 'NVAX', 'WMT', 'COST', 'PEP', 'KO', 'PG' ,'ROKU', 'BILI', 'RBLX', 'AMC', 'SPOT', 'UAL', 'AAL', 'ALK', 'SAVE', 'LUV', 'BA', 'LYFT', 'BLDR', 'LTHM', 'TECK']
