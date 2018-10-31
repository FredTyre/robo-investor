import sqlite3
from datetime import datetime

stockDB = 'stockData.db'

dbConn = sqlite3.connect(stockDB)
dbCurs = dbConn.cursor()

investmentCreateSQL = 'CREATE TABLE investments '
investmentCreateSQL += '( "investment_id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL'
investmentCreateSQL += ', "investment_title" TEXT NOT NULL'
investmentCreateSQL += ', "investment_type_id" INTEGER'
investmentCreateSQL += ', "investment_abbreviation" TEXT NOT NULL'
investmentCreateSQL += ', "date_added" date_time NOT NULL'
investmentCreateSQL += ', "date_updated" date_time NOT NULL'
investmentCreateSQL += ')'
dbCurs.execute(investmentCreateSQL)
dbConn.commit()

investmentTypeCreateSQL = 'CREATE TABLE investment_types '
investmentTypeCreateSQL += '( "investment_type_id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL'
investmentTypeCreateSQL += ', "investment_type_title" TEXT NOT NULL'
investmentTypeCreateSQL += ', "date_added" date_time NOT NULL'
investmentTypeCreateSQL += ', "date_updated" date_time NOT NULL'
investmentTypeCreateSQL += ')'
dbCurs.execute(investmentTypeCreateSQL)
dbConn.commit()

now = datetime.now()
investmentTypeInsertSQL = "INSERT INTO investment_types (investment_type_title, date_added, date_updated) VALUES (?, ?, ?)"
dbCurs.execute(investmentTypeInsertSQL, ('Bonds', now, now))
dbCurs.execute(investmentTypeInsertSQL, ('CDs', now, now))
dbCurs.execute(investmentTypeInsertSQL, ('ETFs', now, now))
dbCurs.execute(investmentTypeInsertSQL, ('Forex', now, now))
dbCurs.execute(investmentTypeInsertSQL, ('Futures', now, now))
dbCurs.execute(investmentTypeInsertSQL, ('Mutual Funds', now, now))
dbCurs.execute(investmentTypeInsertSQL, ('Options', now, now))
dbCurs.execute(investmentTypeInsertSQL, ('Stocks', now, now))
dbConn.commit()

stockPricesCreateSQL = 'CREATE TABLE stock_prices '
stockPricesCreateSQL += '( "investment_id" INTEGER NOT NULL'
stockPricesCreateSQL += ', "day_of_price" date NOT NULL'
stockPricesCreateSQL += ', "open_price" REAL'
stockPricesCreateSQL += ', "high_price" REAL'
stockPricesCreateSQL += ', "low_price" REAL'
stockPricesCreateSQL += ', "close_price" REAL'
stockPricesCreateSQL += ', "adjusted_close_price" REAL'
stockPricesCreateSQL += ', "volume" INTEGER'
stockPricesCreateSQL += ', PRIMARY KEY(`investment_id`,`day_of_price`)'
stockPricesCreateSQL += ')'
dbCurs.execute(stockPricesCreateSQL)
dbConn.commit()

dbConn.close()
