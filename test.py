import requests
import pandas as pd
import time
from datetime import date

trades_url = 'https://api.x.immutable.com/v1/trades?party_b_token_address=0xacb3c6a43d15b907e8433077b6d38ae40936fe2c&page_size=300&order_by=transaction_id&min_timestamp=2022-05-26T23%3A10%3A00Z&max_timestamp=2022-05-26T23%3A30%3A00Z'
cursor_req = requests.get(trades_url).json()

cursor = cursor_req['cursor']
print(cursor)






