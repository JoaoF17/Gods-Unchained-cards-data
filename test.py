import requests
import pandas as pd
import time
import pymysql
import sqlalchemy

def collect_trades(df):
    #collecting trade details from IMX for Gods Unchained cards:   
    maxtime = '2022-10-30T00:10:00Z'
    mintime = '2022-10-29T23:00:00Z'
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
        #get assets info:
        for asset in response['result']:
            #if asset['b']['token_address'] == '0xacb3c6a43d15b907e8433077b6d38ae40936fe2c':
            transaction_id = asset['transaction_id']
            asset_id = asset['b']['token_id']
            currency = asset['a']['token_type']
            sell_value = asset['a']['sold']
            if asset['b']['token_address'] == '0x07865c6e87b9f70255377e024ace6630c1eaa37f':
                sell_value = int(sell_value) / 10e6
            else:
                sell_value = int(sell_value) / 10e17
            timestamp = asset['timestamp']
            #timestamp = str(timestamp).split('T')[0] 
            
            #collecting card info
            card_name_info = requests.get('https://api.x.immutable.com/v1/assets/0xacb3c6a43d15b907e8433077b6d38ae40936fe2c/'+ asset_id).json()

            card_name = card_name_info['name']   

            #save data in pandas df
            df = pd.concat([df, pd.DataFrame.from_records([{
                'transaction_id':transaction_id, 'card_name':card_name,
                'asset_id':asset_id,'currency':currency, 
                'sell_value':sell_value, 'timestamp':timestamp}])], 
                axis=0)
            df.sort_values(by=['transaction_id'], inplace=True, ascending=False)

    return df

#build dataframe
df = pd.DataFrame(columns=['transaction_id','card_name','asset_id','currency','sell_value','timestamp'])

df = collect_trades(df)

df

engine = sqlalchemy.create_engine('mysql+pymysql://root:Joao852654@localhost:3306/gu_trades')

df.to_sql(
    name = 'trades',
    con = engine,
    index = False,
    if_exists = 'replace'
)