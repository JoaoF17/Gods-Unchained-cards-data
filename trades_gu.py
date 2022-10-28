import requests
import pandas as pd
import time
import pymysql
import sqlalchemy

def collect_trades(df):
    #collecting trade details from IMX for Gods Unchained cards
    trades_url = 'https://api.x.immutable.com/v1/trades?party_b_token_address=0xacb3c6a43d15b907e8433077b6d38ae40936fe2c&page_size=200&order_by=transaction_id&cursor=eyJ0cmFuc2FjdGlvbl9pZCI6ODE2Nzc4MDgsInN0YXR1cyI6InN1Y2Nlc3MiLCJwYXJ0eV9hX29yZGVyX2lkIjoyMDI4NzQ2MjcsInBhcnR5X2FfZXRoZXJfa2V5IjoiMHg1YTRkMTg1YzU5MGM1ODE1YTA3MGVkNjJjMjc4ZTY2NWQxMzdhMGQ5IiwicGFydHlfYV9zb2xkX3Rva2VuX3R5cGUiOiJFVEgiLCJwYXJ0eV9hX3NvbGRfdG9rZW5faWQiOiIiLCJwYXJ0eV9hX3NvbGRfdG9rZW5fYWRkcmVzcyI6IiIsInBhcnR5X2Ffc29sZF9xdWFudGl0eSI6IjExNTUwMDAwMDAwMDAwMCIsInBhcnR5X2Jfb3JkZXJfaWQiOjM1NDIyNzI4LCJwYXJ0eV9iX2V0aGVyX2tleSI6IjB4NTA0YjU5NWRlNzg3MzQ2YjQ2NzBmNTFiNmU5Mjc4M2YyYzU0YmU2NCIsInBhcnR5X2Jfc29sZF90b2tlbl90eXBlIjoiRVJDNzIxIiwicGFydHlfYl9zb2xkX3Rva2VuX2lkIjoiMTM5NjUyNzY0IiwicGFydHlfYl9zb2xkX3Rva2VuX2FkZHJlc3MiOiIweGFjYjNjNmE0M2QxNWI5MDdlODQzMzA3N2I2ZDM4YWU0MDkzNmZlMmMiLCJwYXJ0eV9iX3NvbGRfcXVhbnRpdHkiOiIxIiwiY3JlYXRlZF9hdCI6IjIwMjItMDUtMjZUMjM6MTM6NDguNjMwMDY0WiJ9&min_timestamp=2022-05-27T23%3A10%3A00Z&max_timestamp=2022-05-27T23%3A30%3A00Z'
    response = requests.get(trades_url).json()
    time.sleep(1)

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
            ignore_index=True)
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