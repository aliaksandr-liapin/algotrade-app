import connect

connection, cursor = connect.getDbConnect()
cursor.execute("DROP TABLE IF EXISTS stock")
cursor.execute("DROP TABLE IF EXISTS stock_price")
cursor.execute("DROP TABLE IF EXISTS strategy")
cursor.execute("DROP TABLE IF EXISTS stock_strategy")


connection.commit()