import sqlite3
import configs.config as config
import alpaca_trade_api as tradeAPI



connection = sqlite3.connect(config.DB_PATH)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

cursor.execute("SELECT symbol, company FROM stock")
rows = cursor.fetchall()
symbols = [row['symbol'] for row in rows]

api = tradeAPI.REST(config.API_KEY, config.API_SECRET, config.API_ENDPOINT)
assets = api.list_assets()

for asset in assets:
    try:
        if asset.status == 'active' and asset.tradable and asset.symbol not in symbols:
            cursor.execute("INSERT INTO stock (symbol, company) VALUES (?, ?)", (asset.symbol, asset.name))
            print (f"New asset: {asset.symbol} was inserted")
    except Exception as e:
        print(asset.name)
        print(e)
    
connection.commit()