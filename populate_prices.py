import connect

connection, cursor = connect.getDbConnect()
api = connect.getAlpacaAPIconnect()

symbols = []
stock_dict = {}
symbols = cursor.execute("SELECT id, symbol FROM stock").fetchall()

for symbol in symbols:
    stock_dict[symbol['symbol']] = symbol['id']

# Get daily price data for AAPL over the last 5 trading days.
barset = api.get_barset(['AAPL', 'MSFT'], 'day', limit=5)

chunk_size = 200


for symbol in barset:
    for bar in barset[symbol]:
        if symbol in stock_dict.keys():
            bar_id = stock_dict[symbol]
        else:
            print(f'No stock_id for {symbol} found!')
            continue
        
        cursor.execute(f'INSERT INTO stock_price (stock_id, date, open, high, low, close, volume) VALUES (?, ?, ?, ?, ?, ?, ?)', 
                       (int(bar_id), bar.t.date(), bar.o, bar.h, bar.l, bar.c, bar.v))
        print(f'{symbol}: inserted')
    
connection.commit()