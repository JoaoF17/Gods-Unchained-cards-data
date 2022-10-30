import requests
import pandas as pd
import time
import pymysql
import sqlalchemy
import dateutil.parser

#collecting trade details from IMX for Gods Unchained cards:   
maxtime = '2022-10-28T01:10:22Z'
mintime = '2022-10-28T00:10:22Z'
params = {
    #'cursor': cursor,
    'max_timestamp': maxtime,
    'min_timestamp': mintime,
    'order_by': 'transaction_id',    
    'party_b_token_address': '0xacb3c6a43d15b907e8433077b6d38ae40936fe2c'
}
trades_url = 'https://api.x.immutable.com/v1/trades'
response = requests.get(trades_url, params=params).json()
time.sleep(1)
#loop through different pages (cursors):
remaining = response['remaining']
result = response['result']
while remaining == 1:
    params = {
        'cursor': response['cursor'],
        'max_timestamp': maxtime,
        'min_timestamp': mintime,
    }
    trades_url = 'https://api.x.immutable.com/v1/trades?party_b_token_address=0xacb3c6a43d15b907e8433077b6d38ae40936fe2c'
    response = requests.get(trades_url, params=params).json()
    cursor = response['cursor']
    if len(response['result'])<1:
        break

    print('----')
    print(cursor)
    

