import connect

connection, cursor = connect.getDbConnect()

cursor.execute("SELECT symbol, company FROM stock")
rows = cursor.fetchall()
symbols = [row['symbol'] for row in rows]

api = connect.getAlpacaAPIconnect()
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