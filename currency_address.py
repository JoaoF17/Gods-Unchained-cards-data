import requests
import pandas as pd
import time

maxtime = '2022-10-30T01:10:00Z'
mintime = '2022-10-30T00:50:00Z'
params = {
    'max_timestamp': maxtime,
    'min_timestamp': mintime,
    'order_by': 'transaction_id',    
    'party_b_token_address': '0xacb3c6a43d15b907e8433077b6d38ae40936fe2c'
}
trades_url = 'https://api.x.immutable.com/v1/trades'
response = requests.get(trades_url, params=params).json()

for asset in response['result']:
    transaction_id = asset['transaction_id']
    asset_id = asset['b']['token_id']
    currency = asset['a']['token_type']
    if currency == 'ETH':
        currency = 'ETH'
    elif currency == 'ERC20' and asset['a']['token_address'] == '0xccc8cb5229b0ac8069c51fd58367fd1e622afd97':
        currency = 'GODS'
    elif currency == 'ERC20' and asset['a']['token_address'] == '0xf57e7e7c23978c3caec3c3548e3d615c346e79ff':
        currency = 'IMX'
    elif currency == 'ERC20' and asset['a']['token_address'] == '0x07865c6e87b9f70255377e024ace6630c1eaa37f':
        currency = 'USDC'
    else:
        currency = 'Unfamiliar currency'
    sell_value = asset['a']['sold']
    if currency == 'USDC':
        sell_value = int(sell_value) / 10e6
    else:
        sell_value = int(sell_value) / 10e17
    timestamp = asset['timestamp']

    print('--------------')
    print(transaction_id)
    print(asset_id)
    print(currency)
    print(sell_value)
    #print(currency_address)