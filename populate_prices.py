import connect

connection, cursor = connect.getDbConnect()
api = connect.getAlpacaAPIconnect()

symbols = []
stock_dict = {}
chunk_size = 200
symbols = cursor.execute("SELECT id, symbol FROM stock").fetchall()

for symbol in symbols:
    stock_dict[symbol['symbol']] = symbol['id']

list_of_symbols = [symbol['symbol'] for symbol in symbols] 

for i in range(0, len(list_of_symbols), chunk_size):
    symbol_chunk = list_of_symbols[i:i+chunk_size]
    
    # Get daily price data for AAPL over the last 5 trading days.
    barset = api.get_barset(symbol_chunk, 'day')

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
    print(f'{i}->{i+chunk_size}')
    
connection.commit()