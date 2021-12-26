import sqlite3
import alpaca_trade_api as tradeAPI

API_ENDPOINT = 'https://paper-api.alpaca.markets'
API_KEY = 'PK1BCBYMF8QF6IYVUOCE'
API_SECRET = 'bHq0vgFiZhuWL9l0FT1iWAsPngt35YkV3GTXUkfY'

connection = sqlite3.connect('app.db')
cursor = connection.cursor()
# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS stock (
#         id INTEGER PRIMARY KEY, 
#         symbol TEXT NOT NULL UNIQUE, 
#         company TEXT NOT NULL
#     )
# """)
# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS stock_price (
#         id INTEGER PRIMARY KEY, 
#         stock_id INTEGER,
#         date NOT NULL,
#         open NOT NULL, 
#         high NOT NULL, 
#         low NOT NULL, 
#         close NOT NULL, 
#         adjusted_close NOT NULL, 
#         volume NOT NULL,
#         FOREIGN KEY (stock_id) REFERENCES stock (id)
#     )
# """)

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