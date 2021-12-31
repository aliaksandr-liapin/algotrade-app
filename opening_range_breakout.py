import connect as db
import yfinance as yf
from datetime import date



connection, cursor = db.getDbConnect()
api = db.getAlpacaAPIconnect()


cursor.execute("SELECT id FROM strategy WHERE name = 'opening_range_breakout'")
strategy_id = cursor.fetchone()['id']

cursor.execute("""
               SELECT symbol, name FROM stock 
               JOIN stock_strategy ON stock_strategy.stock_id = stock.id 
               WHERE stock_strategy.strategy_id = (?)""", (strategy_id,))
stocks = cursor.fetchall()
symbols = [stock['symbol'] for stock in stocks]

current_date = date.today().isoformat()
start_minute_bar = f'{current_date} 09:30:00-04:00'
end_minute_bar = f'{current_date} 09:45:00-04:00'

# getting 1 minute stock data (source must be defined)
for symbol in symbols:
    # minute_bar = api.polygon.historic_agg_v2(symbol, 1, 'minute', _from=current_date, to=current_date).df
    
    stock = yf.Ticker(symbol)
    minute_bar = stock.history(interval='1m', start='2020-10-29', end='2020-10-30')
    
    print(symbol)
    print(minute_bar)
    opening_range_mask = (minute_bar.index >= start_minute_bar) & (minute_bar.index < end_minute_bar)
    opening_range_bars = minute_bar.loc(opening_range_mask)
    opening_range_low = opening_range_bars['low'].min()
    opening_range_high = opening_range_bars['high'].max()
    
    # used for the stop-loss or take profit
    opening_range = opening_range_high - opening_range_low
    
    # start to find the first bar that closes above high range or below the low range
    after_opening_range_mask = minute_bar.index >= end_minute_bar
    after_opening_range_bar = minute_bar.loc[after_opening_range_mask]
    
    
