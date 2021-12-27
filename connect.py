import sqlite3, configs.config as config
import alpaca_trade_api as tradeAPI
from sqlite3.dbapi2 import Cursor, connect
    

def getDbConnect():
    connect = sqlite3.connect(config.DB_PATH)
    connect.row_factory = sqlite3.Row
    cursor = connect.cursor()
    
    return connect, cursor

def getAlpacaAPIconnect():
    api = tradeAPI.REST(config.API_KEY, config.API_SECRET, config.API_ENDPOINT)
    
    return api