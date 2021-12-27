import sqlite3
import configs.config as config
import alpaca_trade_api as tradeAPI

api = tradeAPI.REST(config.API_KEY, config.API_SECRET, config.API_ENDPOINT)

# Get daily price data for AAPL over the last 5 trading days.
barset = api.get_barset('AAPL', 'day', limit=5)
aapl_bars = barset['AAPL']
print(aapl_bars)