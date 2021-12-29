import connect as db
from fastapi.responses import RedirectResponse
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from datetime import date

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get('/')
def index(request: Request):
    stock_filter = request.query_params.get('filter', False)
    connection, cursor = db.getDbConnect()
    

        
    if stock_filter == 'new_intraday_hights':
        pass
    elif stock_filter == 'new_closing_hights':
        cursor.execute("""
                select * from (
                    select symbol, name, stock_id, max(close), date
                    from stock_price join stock on stock.id = stock_price.stock_id
                    group by stock_id
                    order by symbol
                ) where date = ?
                """, (date.today().isoformat(),))
    elif stock_filter == 'new_intraday_lows':
        pass
    elif stock_filter == 'new_closing_lows':
        pass
    else:
        cursor.execute("SELECT * FROM stock ORDER BY symbol")     

    rows = cursor.fetchall()
    return templates.TemplateResponse("index.html", {"request": request, "stocks": rows})

@app.get('/stock/{symbol}')
def stock_detail(request: Request, symbol):
    connection, cursor = db.getDbConnect()
    cursor.execute("SELECT * FROM strategy")
    strategies = cursor.fetchall()
    
    cursor.execute("SELECT * FROM stock WHERE symbol = ?", (symbol,))
    rows = cursor.fetchone()
    
    cursor.execute("SELECT * FROM stock_price WHERE stock_id = ?", (rows['id'],))
    prices = cursor.fetchall()
    
    return templates.TemplateResponse("stock.html", {"request": request, "prices": prices, 
                                                     "ticker": symbol, "stock": rows, 
                                                     "strategies": strategies})
    
@app.post('/apply_strategy')
def apply_strategy(strategy_id:int=Form(...), stock_id:int=Form(...)):
    connection, cursor = db.getDbConnect()
    
    cursor.execute("""
        INSERT INTO stock_strategy (stock_id, strategy_id) VALUES (?, ?)
        """, (stock_id, strategy_id))
    connection.commit()
    return RedirectResponse(url=f'/strategy/{strategy_id}', status_code=303)

@app.get('/strategy/{strategy_id}')
def strategy(request: Request, strategy_id):
    connection, cursor = db.getDbConnect()
    
    cursor.execute("""
        SELECT id, name
        FROM strategy
        WHERE id = ?
        """, (strategy_id,))
    strategy = cursor.fetchone()
    
    cursor.execute("""
        SELECT symbol, name
        FROM stock JOIN stock_strategy on stock_strategy.stock_id = stock.id
        WHERE strategy_id = ?
        """, (strategy_id, ))
    stocks = cursor.fetchall()
    
    return templates.TemplateResponse("strategy.html", {"request": request,
                                                        "stocks": stocks,
                                                        "strategy": strategy})
    
    