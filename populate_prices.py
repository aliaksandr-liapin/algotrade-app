import connect

connection, cursor = connect.getDbConnect()
api = connect.getAlpacaAPIconnect()

# Get daily price data for AAPL over the last 5 trading days.
barset = api.get_barset(['AAPL', 'MSFT'], 'day', limit=5)
for bars in barset:
    print(bars)
    
# connection.commit()