import connect

connection, cursor = connect.getDbConnect()
cursor.execute("DROP TABLE stock")
cursor.execute("DROP TABLE stock_price")


connection.commit()