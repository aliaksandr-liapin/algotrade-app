from re import S
import connect as db
import yfinance as yf
from datetime import date


connection, cursor = db.getDbConnect()
api = db.getAlpacaAPIconnect()

current_date = date.today().isoformat()
start_minute_bar = f'{current_date} 09:30:00-04:00'
end_minute_bar = f'{current_date} 09:45:00-04:00'

orders = api.list_orders(status='all', limit = 500, after=f'{current_date}T13:30:00Z')
existing_order_symbols = [order.symbol for order in orders]

cursor.execute("SELECT id FROM strategy WHERE name = 'opening_range_breakout'")
strategy_id = cursor.fetchone()['id']

cursor.execute("""
               SELECT symbol, name FROM stock 
               JOIN stock_strategy ON stock_strategy.stock_id = stock.id 
               WHERE stock_strategy.strategy_id = (?)""", (strategy_id,))
stocks = cursor.fetchall()
symbols = [stock['symbol'] for stock in stocks]

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
    
    after_opening_range_breakout = after_opening_range_bar[after_opening_range_bar['close'] > opening_range_high]
    
    if not after_opening_range_breakout.empty:
        if symbol not in existing_order_symbols:
            limit_price = after_opening_range_breakout.iloc[0]['close']
            print(limit_price)
            print(f'placing order for {symbol} at {limit_price}, closed_above {opening_range_high} at {after_opening_range_breakout.iloc[0]}')

            api.submit_order(
                symbol=symbol,
                side='buy',
                type='limit',
                qty='100',
                time_in_force='day',
                order_class='bracket',
                limit_price=limit_price,
                take_profit=dict(
                    limit_price=limit_price + opening_range,
                ),
                stop_loss=dict(
                    stop_price=limit_price - opening_range,

                )
            )
        else:
            print(f'Already an order for {symbol}, skipping')