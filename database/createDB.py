#########################################################################################
# Author : Fred Tyre (aka One5hot76)                                                    #
# See main folder for LICENSE and README files related to this open source project      #
# Gentle reminder to use at your own risk! Absolutely no warranty is implied with       #
# this product as stated in Readme file in main folder.                                 #
#########################################################################################

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

stockPriceDiffsCreateSQL = 'CREATE TABLE stock_price_diffs '
stockPriceDiffsCreateSQL += '( "investment_id" INTEGER NOT NULL'
stockPriceDiffsCreateSQL += ', "day_of_price" date NOT NULL'
stockPriceDiffsCreateSQL += ', "open_price_diff" REAL'
stockPriceDiffsCreateSQL += ', "high_price_diff" REAL'
stockPriceDiffsCreateSQL += ', "low_price_diff" REAL'
stockPriceDiffsCreateSQL += ', "close_price_diff" REAL'
stockPriceDiffsCreateSQL += ', "adj_close_price_diff" REAL'
stockPriceDiffsCreateSQL += ', "volume_diff" INTEGER'
stockPriceDiffsCreateSQL += ', PRIMARY KEY(`investment_id`,`day_of_price`)'
stockPriceDiffsCreateSQL += ')'
dbCurs.execute(stockPriceDiffsCreateSQL)
dbConn.commit()

stockPriceDiffPercsCreateSQL = 'CREATE TABLE stock_price_diff_percs '
stockPriceDiffPercsCreateSQL += '( "investment_id" INTEGER NOT NULL'
stockPriceDiffPercsCreateSQL += ', "day_of_price" date NOT NULL'
stockPriceDiffPercsCreateSQL += ', "open_price_diff_perc" REAL'
stockPriceDiffPercsCreateSQL += ', "high_price_diff_perc" REAL'
stockPriceDiffPercsCreateSQL += ', "low_price_diff_perc" REAL'
stockPriceDiffPercsCreateSQL += ', "close_price_diff_perc" REAL'
stockPriceDiffPercsCreateSQL += ', "adj_close_price_diff_perc" REAL'
stockPriceDiffPercsCreateSQL += ', "volume_diff_perc" REAL'
stockPriceDiffPercsCreateSQL += ', PRIMARY KEY(`investment_id`,`day_of_price`)'
stockPriceDiffPercsCreateSQL += ')'
dbCurs.execute(stockPriceDiffPercsCreateSQL)
dbConn.commit()

stockPricesWeeklyCreateSQL = 'CREATE TABLE stock_prices_weekly '
stockPricesWeeklyCreateSQL += '( "investment_id" INTEGER NOT NULL'
stockPricesWeeklyCreateSQL += ', "start_day_of_week" date NOT NULL'
stockPricesWeeklyCreateSQL += ', "end_day_of_week" date NOT NULL'
stockPricesWeeklyCreateSQL += ', "open_price" REAL'
stockPricesWeeklyCreateSQL += ', "high_price" REAL'
stockPricesWeeklyCreateSQL += ', "low_price" REAL'
stockPricesWeeklyCreateSQL += ', "close_price" REAL'
stockPricesWeeklyCreateSQL += ', "volume" INTEGER'
stockPricesWeeklyCreateSQL += ', "num_trading_days" INTEGER'
stockPricesWeeklyCreateSQL += ', PRIMARY KEY(`investment_id`,`start_day_of_week`)'
stockPricesWeeklyCreateSQL += ')'
dbCurs.execute(stockPricesWeeklyCreateSQL)
dbConn.commit()

stockPricesMonthlyCreateSQL = 'CREATE TABLE stock_prices_monthly '
stockPricesMonthlyCreateSQL += '( "investment_id" INTEGER NOT NULL'
stockPricesMonthlyCreateSQL += ', "month" date NOT NULL'
stockPricesMonthlyCreateSQL += ', "open_price" REAL'
stockPricesMonthlyCreateSQL += ', "high_price" REAL'
stockPricesMonthlyCreateSQL += ', "low_price" REAL'
stockPricesMonthlyCreateSQL += ', "close_price" REAL'
stockPricesMonthlyCreateSQL += ', "volume" INTEGER'
stockPricesMonthlyCreateSQL += ', "num_trading_days" INTEGER'
stockPricesMonthlyCreateSQL += ', PRIMARY KEY(`investment_id`,`month`)'
stockPricesMonthlyCreateSQL += ')'
dbCurs.execute(stockPricesMonthlyCreateSQL)
dbConn.commit()

stockPricesYearlyCreateSQL = 'CREATE TABLE stock_prices_yearly '
stockPricesYearlyCreateSQL += '( "investment_id" INTEGER NOT NULL'
stockPricesYearlyCreateSQL += ', "year" INTEGER NOT NULL'
stockPricesYearlyCreateSQL += ', "open_price" REAL'
stockPricesYearlyCreateSQL += ', "high_price" REAL'
stockPricesYearlyCreateSQL += ', "low_price" REAL'
stockPricesYearlyCreateSQL += ', "close_price" REAL'
stockPricesYearlyCreateSQL += ', "volume" INTEGER'
stockPricesYearlyCreateSQL += ', "num_trading_days" INTEGER'
stockPricesYearlyCreateSQL += ', PRIMARY KEY(`investment_id`,`year`)'
stockPricesYearlyCreateSQL += ')'
dbCurs.execute(stockPricesYearlyCreateSQL)
dbConn.commit()

investmentSimCreateSQL = 'CREATE TABLE investment_simulations '
investmentSimCreateSQL += '( "investment_sim_id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL'
investmentSimCreateSQL += ', "investment_sim_title" TEXT NOT NULL'
investmentSimCreateSQL += ', "start_date" date NOT NULL'
investmentSimCreateSQL += ', "end_date" date NOT NULL'
investmentSimCreateSQL += ', "commission_fee" REAL'
investmentSimCreateSQL += ')'
dbCurs.execute(investmentSimCreateSQL)
dbConn.commit()

investSimStockTransacsCreateSQL = 'CREATE TABLE invest_sim_stock_transactions '
investSimStockTransacsCreateSQL += '( "investment_sim_id" INTEGER NOT NULL'
investSimStockTransacsCreateSQL += ', "investment_id" INTEGER NOT NULL'
investSimStockTransacsCreateSQL += ', "day_of_price" date NOT NULL'
investSimStockTransacsCreateSQL += ', "buy_or_sell" TEXT NOT NULL'
investSimStockTransacsCreateSQL += ', "num_shares" INTEGER'
investSimStockTransacsCreateSQL += ', "transaction_price" REAL'
investSimStockTransacsCreateSQL += ', "commission_fee" REAL'
investSimStockTransacsCreateSQL += ', PRIMARY KEY(`investment_id`,`day_of_price`, `buy_or_sell`)'
investSimStockTransacsCreateSQL += ')'
dbCurs.execute(investSimStockTransacsCreateSQL)
dbConn.commit()

dbConn.close()
