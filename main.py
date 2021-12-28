import connect as db
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get('/')
def index(request: Request):
    connection, cursor = db.getDbConnect()
    cursor.execute("SELECT * FROM stock ORDER BY symbol")

    rows = cursor.fetchall()
    return templates.TemplateResponse("index.html", {"request": request, "stocks": rows})

@app.get('/stock/{symbol}')
def stock_detail(request: Request, symbol):
    connection, cursor = db.getDbConnect()
    
    cursor.execute("SELECT * FROM stock WHERE symbol = ?", (symbol,))
    rows = cursor.fetchone()
    
    cursor.execute("SELECT * FROM stock_price WHERE stock_id = ?", (rows['id'],))
    prices = cursor.fetchall()
    
    return templates.TemplateResponse("stock.html", {"request": request, "prices": prices, "ticker": symbol})