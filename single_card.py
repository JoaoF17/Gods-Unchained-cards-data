import requests
import pandas as pd
import time

url_gu_collection = 'https://api.x.immutable.com/v1/assets'+'&collection=0xacb3c6a43d15b907e8433077b6d38ae40936fe2c&page_size=10000'
card_name = requests.get(url_gu_collection).json()

card_name




