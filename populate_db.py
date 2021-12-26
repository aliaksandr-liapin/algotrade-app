import sqlite3
import alpaca_trade_api as tradeAPI

API_ENDPOINT = 'https://paper-api.alpaca.markets'
API_KEY = 'PK1BCBYMF8QF6IYVUOCE'
API_SECRET = 'bHq0vgFiZhuWL9l0FT1iWAsPngt35YkV3GTXUkfY'

connection = sqlite3.connect('app.db')
cursor = connection.cursor()

api = tradeAPI.REST(API_KEY, API_SECRET, API_ENDPOINT)
assets = api.list_assets()

for asset in assets:
    try:
        if asset.status == 'active' and asset.tradable:
            cursor.execute("INSERT INTO stock (symbol, company) VALUES (?, ?)", (asset.symbol, asset.name))
    except Exception as e:
        print(asset.name)
        print(e)
connection.commit()